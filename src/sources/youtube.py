import re
from datetime import datetime, timezone

import requests

from config.settings import YOUTUBE_API_KEY
from src.source_schema import SourceRecord


YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_CHANNELS_URL = "https://www.googleapis.com/youtube/v3/channels"
YOUTUBE_PLAYLIST_ITEMS_URL = "https://www.googleapis.com/youtube/v3/playlistItems"
YOUTUBE_VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"


# Operational rule:
# YouTube Shorts can be short-form even when they are longer than 60 seconds.
# We therefore use 3 minutes as a conservative long-form threshold.
LONG_FORM_MIN_SECONDS = 180


def normalize_youtube_channel(
    channel_id: str,
    channel_title: str,
    channel_url: str,
    country_iso2: str | None = None,
    description: str | None = None,
) -> SourceRecord:
    """
    Convert publicly available YouTube channel information
    into our internal SourceRecord format.

    This function does not qualify the creator.
    """

    return SourceRecord(
        creator_name=channel_title.strip(),
        creator_segment="youtuber",
        country_iso2=country_iso2,
        primary_language=None,
        primary_platform="YouTube",
        profile_url=channel_url.strip(),
        stable_creator_id=channel_id.strip(),
        source_name="YouTube Data API",
        source_url=channel_url.strip(),
        discovered_at="",
        description=description,
    )


def discover_youtube_channels(
    query: str,
    max_results: int = 10,
) -> list[SourceRecord]:
    """
    Discover YouTube channels using the YouTube Data API v3.

    This function only discovers candidates.
    Qualification happens later.
    """

    params = {
        "part": "snippet",
        "q": query,
        "type": "channel",
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY,
    }

    response = requests.get(
        YOUTUBE_SEARCH_URL,
        params=params,
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()

    channel_ids = []

    for item in data.get("items", []):
        channel_id = item.get("id", {}).get("channelId")

        if channel_id:
            channel_ids.append(channel_id)

    if not channel_ids:
        return []

    # Get channel details, including country when publicly available.
    channel_params = {
        "part": "snippet",
        "id": ",".join(channel_ids),
        "key": YOUTUBE_API_KEY,
    }

    channel_response = requests.get(
        YOUTUBE_CHANNELS_URL,
        params=channel_params,
        timeout=30,
    )
    channel_response.raise_for_status()

    channel_data = channel_response.json()

    records = []

    for item in channel_data.get("items", []):
        channel_id = item["id"]
        snippet = item.get("snippet", {})

        channel_title = snippet.get("title", "")
        description = snippet.get("description", "")
        country_iso2 = snippet.get("country")

        channel_url = (
            f"https://www.youtube.com/channel/{channel_id}"
        )

        record = normalize_youtube_channel(
            channel_id=channel_id,
            channel_title=channel_title,
            channel_url=channel_url,
            country_iso2=country_iso2,
            description=description,
        )

        records.append(record)

    return records


def parse_iso8601_duration(duration: str) -> int:
    """
    Convert an ISO 8601 duration such as PT12M30S
    into total seconds.
    """

    match = re.fullmatch(
        r"PT"
        r"(?:(\d+)H)?"
        r"(?:(\d+)M)?"
        r"(?:(\d+)S)?",
        duration,
    )

    if not match:
        return 0

    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)

    return hours * 3600 + minutes * 60 + seconds


def get_video_durations(
    video_ids: list[str],
) -> dict[str, int]:
    """
    Retrieve video durations from YouTube.

    Returns:
        {
            video_id: duration_in_seconds
        }
    """

    if not video_ids:
        return {}

    params = {
        "part": "contentDetails",
        "id": ",".join(video_ids),
        "key": YOUTUBE_API_KEY,
    }

    response = requests.get(
        YOUTUBE_VIDEOS_URL,
        params=params,
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()

    durations = {}

    for item in data.get("items", []):
        video_id = item.get("id")
        duration = item.get("contentDetails", {}).get("duration")

        if video_id and duration:
            durations[video_id] = parse_iso8601_duration(duration)

    return durations


def get_channel_activity(
    channel_id: str,
) -> dict:
    """
    Retrieve recent public YouTube activity for a channel.

    Returns:
        content_count_30d
        longform_count_60d
        last_content_date
        recent_content_url
    """

    # ---------------------------------------------------------
    # 1. Find the channel's uploads playlist
    # ---------------------------------------------------------

    channel_params = {
        "part": "contentDetails",
        "id": channel_id,
        "key": YOUTUBE_API_KEY,
    }

    channel_response = requests.get(
        YOUTUBE_CHANNELS_URL,
        params=channel_params,
        timeout=30,
    )
    channel_response.raise_for_status()

    channel_data = channel_response.json()

    items = channel_data.get("items", [])

    if not items:
        return {
            "channel_id": channel_id,
            "content_count_30d": 0,
            "longform_count_60d": 0,
            "last_content_date": None,
            "recent_content_url": None,
        }

    uploads_playlist_id = (
        items[0]
        .get("contentDetails", {})
        .get("relatedPlaylists", {})
        .get("uploads")
    )

    if not uploads_playlist_id:
        return {
            "channel_id": channel_id,
            "content_count_30d": 0,
            "longform_count_60d": 0,
            "last_content_date": None,
            "recent_content_url": None,
        }

    # ---------------------------------------------------------
    # 2. Retrieve recent uploads
    # ---------------------------------------------------------

    playlist_params = {
        "part": "snippet,contentDetails",
        "playlistId": uploads_playlist_id,
        "maxResults": 50,
        "key": YOUTUBE_API_KEY,
    }

    playlist_response = requests.get(
        YOUTUBE_PLAYLIST_ITEMS_URL,
        params=playlist_params,
        timeout=30,
    )
    playlist_response.raise_for_status()

    playlist_data = playlist_response.json()

    # ---------------------------------------------------------
    # 3. Normalize video records
    # ---------------------------------------------------------

    video_records = []

    for item in playlist_data.get("items", []):
        snippet = item.get("snippet", {})
        content_details = item.get("contentDetails", {})

        published_at = snippet.get("publishedAt")
        video_id = content_details.get("videoId")

        if not published_at or not video_id:
            continue

        published_date = datetime.fromisoformat(
            published_at.replace("Z", "+00:00")
        )

        video_url = (
            f"https://www.youtube.com/watch?v={video_id}"
        )

        video_records.append(
            {
                "video_id": video_id,
                "published_date": published_date,
                "video_url": video_url,
            }
        )

    # ---------------------------------------------------------
    # 4. Retrieve actual video durations
    # ---------------------------------------------------------

    video_ids = [
        video["video_id"]
        for video in video_records
    ]

    durations = get_video_durations(video_ids)

    # ---------------------------------------------------------
    # 5. Calculate activity
    # ---------------------------------------------------------

    now = datetime.now(timezone.utc)

    content_count_30d = 0
    longform_count_60d = 0

    last_content_date = None
    recent_content_url = None

    for video in video_records:
        published_date = video["published_date"]
        video_id = video["video_id"]
        video_url = video["video_url"]

        age_days = (
            now - published_date
        ).days

        # Most recent content
        if (
            last_content_date is None
            or published_date > last_content_date
        ):
            last_content_date = published_date
            recent_content_url = video_url

        # Content published within the last 30 days
        if age_days <= 30:
            content_count_30d += 1

        # Long-form content within the last 60 days
        if age_days <= 60:
            duration_seconds = durations.get(
                video_id,
                0,
            )

            if duration_seconds >= LONG_FORM_MIN_SECONDS:
                longform_count_60d += 1

    # ---------------------------------------------------------
    # 6. Return activity information
    # ---------------------------------------------------------

    return {
        "channel_id": channel_id,
        "content_count_30d": content_count_30d,
        "longform_count_60d": longform_count_60d,
        "last_content_date": (
            last_content_date.isoformat()
            if last_content_date
            else None
        ),
        "recent_content_url": recent_content_url,
    }

def get_recent_video_metadata(
    channel_id: str,
    max_results: int = 10,
) -> list[dict]:
    """
    Retrieve recent public video metadata for a YouTube channel.

    Returns video titles, descriptions, publication dates,
    and public URLs for later evidence analysis.
    """

    channel_params = {
        "part": "contentDetails",
        "id": channel_id,
        "key": YOUTUBE_API_KEY,
    }

    channel_response = requests.get(
        YOUTUBE_CHANNELS_URL,
        params=channel_params,
        timeout=30,
    )
    channel_response.raise_for_status()

    channel_data = channel_response.json()
    items = channel_data.get("items", [])

    if not items:
        return []

    uploads_playlist_id = (
        items[0]
        .get("contentDetails", {})
        .get("relatedPlaylists", {})
        .get("uploads")
    )

    if not uploads_playlist_id:
        return []

    playlist_params = {
        "part": "snippet,contentDetails",
        "playlistId": uploads_playlist_id,
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY,
    }

    playlist_response = requests.get(
        YOUTUBE_PLAYLIST_ITEMS_URL,
        params=playlist_params,
        timeout=30,
    )
    playlist_response.raise_for_status()

    playlist_data = playlist_response.json()

    videos = []

    for item in playlist_data.get("items", []):
        snippet = item.get("snippet", {})
        content_details = item.get("contentDetails", {})

        video_id = content_details.get("videoId")
        title = snippet.get("title", "")
        description = snippet.get("description", "")
        published_at = snippet.get("publishedAt")

        if not video_id:
            continue

        videos.append(
            {
                "video_id": video_id,
                "title": title,
                "description": description,
                "published_at": published_at,
                "url": f"https://www.youtube.com/watch?v={video_id}",
            }
        )

    return videos