from dataclasses import dataclass
from datetime import datetime, timezone

from src.sources.youtube import (
    discover_youtube_channels,
    get_channel_activity,
    get_recent_video_metadata,
)

from src.evidence import (
    create_country_evidence,
    detect_language_from_videos,
    detect_commercial_signal,
    detect_incubrix_need,
    extract_business_contact,
)


@dataclass
class DiscoveryCandidate:
    """
    A creator discovered from a public source.

    This is NOT yet a qualified Lead.
    Qualification happens later.
    """

    creator_name: str
    creator_segment: str
    primary_platform: str
    profile_url: str
    stable_creator_id: str

    discovery_source: str
    discovery_query: str
    discovered_at: str


def create_candidate(
    creator_name: str,
    creator_segment: str,
    primary_platform: str,
    profile_url: str,
    stable_creator_id: str,
    discovery_source: str,
    discovery_query: str,
) -> DiscoveryCandidate:
    """
    Create a normalized discovery candidate.
    """

    return DiscoveryCandidate(
        creator_name=creator_name.strip(),
        creator_segment=creator_segment.strip(),
        primary_platform=primary_platform.strip(),
        profile_url=profile_url.strip(),
        stable_creator_id=stable_creator_id.strip(),
        discovery_source=discovery_source.strip(),
        discovery_query=discovery_query.strip(),
        discovered_at=datetime.now(timezone.utc).isoformat(),
    )


def discover_creators(
    query: str,
    max_results: int = 10,
) -> list[tuple[DiscoveryCandidate, dict, object]]:
    """
    Discover creators from YouTube and collect their
    verified activity and evidence.

    Qualification happens later.
    """

    source_records = discover_youtube_channels(
        query=query,
        max_results=max_results,
    )

    candidates = []

    for record in source_records:

        # ---------------------------------------------
        # 1. Create discovery candidate
        # ---------------------------------------------

        candidate = create_candidate(
            creator_name=record.creator_name,
            creator_segment=record.creator_segment,
            primary_platform=record.primary_platform,
            profile_url=record.profile_url,
            stable_creator_id=record.stable_creator_id,
            discovery_source=record.source_name,
            discovery_query=query,
        )

        # ---------------------------------------------
        # 2. Verify channel activity
        # ---------------------------------------------

        activity = get_channel_activity(
            record.stable_creator_id
        )

        # ---------------------------------------------
        # 3. Create country evidence
        # ---------------------------------------------

        evidence = create_country_evidence(
            country_iso2=record.country_iso2,
            profile_url=record.profile_url,
            checked_date=datetime.now(timezone.utc).date().isoformat(),
        )

        # ---------------------------------------------
        # 4. Retrieve recent video metadata
        # ---------------------------------------------

        videos = get_recent_video_metadata(
            channel_id=record.stable_creator_id,
            max_results=10,
        )

        # ---------------------------------------------
        # 5. Detect primary language
        # ---------------------------------------------

        language, language_url = detect_language_from_videos(
            videos
        )

        evidence.primary_language = language
        evidence.language_evidence_url = language_url

        # ---------------------------------------------
        # 6. Detect commercial signal
        # ---------------------------------------------

        commercial_signal, commercial_url = (
            detect_commercial_signal(videos)
        )

        evidence.commercial_signal = commercial_signal
        evidence.monetization_evidence_url = commercial_url

        # ---------------------------------------------
        # 7. Detect IncuBrix need
        # ---------------------------------------------

        incubrix_need, need_url = (
            detect_incubrix_need(videos)
        )

        evidence.incubrix_need = incubrix_need
        evidence.need_evidence_url = need_url

        # ---------------------------------------------
        # 8. Extract business contact
        # ---------------------------------------------

        contact_type, contact, contact_url = (
            extract_business_contact(
                description=record.description,
                profile_url=record.profile_url,
            )
        )

        evidence.business_contact_type = contact_type
        evidence.business_contact = contact
        evidence.contact_evidence_url = contact_url

        # ---------------------------------------------
        # 9. Store complete evidence
        # ---------------------------------------------

        candidates.append(
            (
                candidate,
                activity,
                evidence,
            )
        )

    return candidates