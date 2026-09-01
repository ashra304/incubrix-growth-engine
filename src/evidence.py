from dataclasses import dataclass
from typing import Optional
import re

@dataclass
class EvidenceRecord:
    country_iso2: Optional[str]
    primary_language: Optional[str]

    commercial_signal: bool
    monetization_evidence_url: Optional[str]

    incubrix_need: bool
    need_evidence_url: Optional[str]

    business_contact_type: Optional[str]
    business_contact: Optional[str]
    contact_evidence_url: Optional[str]

    country_evidence_url: Optional[str]
    language_evidence_url: Optional[str]

    checked_date: str


def create_country_evidence(
    country_iso2: Optional[str],
    profile_url: str,
    checked_date: str,
) -> EvidenceRecord:
    """
    Create an evidence record using the country
    publicly associated with a YouTube channel.
    """

    country = (
        country_iso2.strip().upper()
        if country_iso2
        else None
    )

    return EvidenceRecord(
        country_iso2=country,
        primary_language=None,

        commercial_signal=False,
        monetization_evidence_url=None,

        incubrix_need=False,
        need_evidence_url=None,

        business_contact_type=None,
        business_contact=None,
        contact_evidence_url=None,

        country_evidence_url=profile_url,
        language_evidence_url=None,

        checked_date=checked_date,
    )

def create_language_evidence(
    primary_language: Optional[str],
    evidence_url: Optional[str],
    checked_date: str,
) -> EvidenceRecord:
    """
    Create an evidence record using publicly available
    language information.
    """

    language = (
        primary_language.strip().lower()
        if primary_language
        else None
    )

    return EvidenceRecord(
        country_iso2=None,
        primary_language=language,

        commercial_signal=False,
        monetization_evidence_url=None,

        incubrix_need=False,
        need_evidence_url=None,

        business_contact_type=None,
        business_contact=None,
        contact_evidence_url=None,

        country_evidence_url=None,
        language_evidence_url=evidence_url,

        checked_date=checked_date,
    )
def detect_language_from_videos(
    videos: list[dict],
) -> tuple[Optional[str], Optional[str]]:
    """
    Estimate whether recent YouTube content is mainly English.

    Titles are the primary language signal.
    Descriptions are used only as a secondary signal.

    Returns:
        (language, evidence_url)
    """

    if not videos:
        return None, None

    english_words = {
        "the", "and", "for", "with", "you", "your",
        "how", "what", "why", "this", "that", "from",
        "about", "creator", "youtube", "technology",
        "video", "channel", "update", "tutorial",
        "guide", "tips", "review", "learn", "learning",
        "business", "growth", "marketing", "content",
        "online", "new", "best", "make", "making",
        "today", "monetization", "affiliate",
    }

    total_title_latin = 0
    total_title_non_latin = 0
    total_title_english_words = 0

    best_evidence_url = None

    for video in videos:
        title = video.get("title", "")
        description = video.get("description", "")

        # -------------------------------------------------
        # 1. Analyze TITLE — primary signal
        # -------------------------------------------------

        title_latin = re.findall(
            r"[A-Za-z]",
            title,
        )

        title_non_latin = re.findall(
            r"[^\x00-\x7F\s\d\W]",
            title,
        )

        total_title_latin += len(title_latin)
        total_title_non_latin += len(title_non_latin)

        title_words = re.findall(
            r"[a-zA-Z]+",
            title.lower(),
        )

        english_matches = sum(
            1
            for word in title_words
            if word in english_words
        )

        total_title_english_words += english_matches

        if (
            english_matches >= 2
            and best_evidence_url is None
        ):
            best_evidence_url = video.get("url")

        # -------------------------------------------------
        # 2. Use description only as supporting evidence
        # -------------------------------------------------

        description_words = re.findall(
            r"[a-zA-Z]+",
            description.lower(),
        )

        description_english_matches = sum(
            1
            for word in description_words
            if word in english_words
        )

        if (
            description_english_matches >= 5
            and best_evidence_url is None
        ):
            best_evidence_url = video.get("url")

    # -----------------------------------------------------
    # 3. Calculate title language ratio
    # -----------------------------------------------------

    total_title_chars = (
        total_title_latin
        + total_title_non_latin
    )

    if total_title_chars == 0:
        return None, None

    latin_ratio = (
        total_title_latin / total_title_chars
    )

    # -----------------------------------------------------
    # 4. Conservative English decision
    # -----------------------------------------------------

    if (
        latin_ratio >= 0.90
        and total_title_english_words >= 5
    ):
        return "english", best_evidence_url

    return None, None

def detect_commercial_signal(
    videos: list[dict],
) -> tuple[bool, Optional[str]]:
    """
    Detect explicit commercial activity signals in recent
    public YouTube video metadata.

    Returns:
        (commercial_signal, evidence_url)

    The function only returns True when explicit commercial
    language is found in titles or descriptions.
    """

    if not videos:
        return False, None

    commercial_phrases = {
        "sponsored",
        "sponsor",
        "paid partnership",
        "brand collaboration",
        "brand collab",
        "affiliate",
        "affiliate link",
        "affiliate marketing",
        "discount code",
        "promo code",
        "promotion code",
        "use my code",
        "coupon code",
        "shop now",
        "buy now",
        "amazon affiliate",
    }

    for video in videos:
        title = video.get("title", "")
        description = video.get("description", "")

        text = f"{title} {description}".lower()

        for phrase in commercial_phrases:
            if phrase in text:
                return True, video.get("url")

    return False, None

def create_commercial_evidence(
    commercial_signal: bool,
    evidence_url: Optional[str],
    checked_date: str,
) -> EvidenceRecord:
    """
    Create an evidence record using publicly available
    commercial activity information.
    """

    return EvidenceRecord(
        country_iso2=None,
        primary_language=None,

        commercial_signal=commercial_signal,
        monetization_evidence_url=evidence_url,

        incubrix_need=False,
        need_evidence_url=None,

        business_contact_type=None,
        business_contact=None,
        contact_evidence_url=None,

        country_evidence_url=None,
        language_evidence_url=None,

        checked_date=checked_date,
    )

def detect_incubrix_need(
    videos: list[dict],
) -> tuple[bool, Optional[str]]:
    """
    Detect public signals that may indicate an IncuBrix-relevant need.

    Returns:
        (incubrix_need, evidence_url)

    The function looks for explicit creator/business problems
    in recent public YouTube content.
    """

    if not videos:
        return False, None

    need_phrases = {
        "content strategy",
        "content management",
        "content workflow",
        "creator workflow",
        "creator tools",
        "creator business",
        "audience growth",
        "channel growth",
        "grow my channel",
        "grow your channel",
        "scaling",
        "scale my",
        "scale your",
        "automation",
        "automate",
        "workflow",
        "productivity",
        "team management",
        "managing my team",
        "business growth",
        "monetization",
        "creator economy",
        "sponsorship management",
        "brand deals",
        "brand partnerships",
    }

    for video in videos:

        title = video.get("title", "")
        description = video.get("description", "")

        text = f"{title} {description}".lower()

        for phrase in need_phrases:

            if phrase in text:
                return True, video.get("url")

    return False, None

def extract_business_contact(
    description: Optional[str],
    profile_url: str,
) -> tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Extract an explicitly published business email from
    a public YouTube channel description.

    Returns:
        (contact_type, contact, evidence_url)

    The function only extracts an email address when it
    appears in the publicly available channel description.
    """

    if not description:
        return None, None, None

    business_keywords = {
        "business",
        "business inquiries",
        "business inquiry",
        "for business",
        "business contact",
        "contact",
        "collaboration",
        "collaborations",
        "sponsor",
        "sponsorship",
        "work with me",
        "work with us",
        "partnership",
        "partnerships",
    }

    # Email pattern.
    email_pattern = (
        r"\b[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    )

    lines = description.splitlines()

    for line in lines:

        line_lower = line.lower()

        # The email must appear in a business-related line.
        has_business_context = any(
            keyword in line_lower
            for keyword in business_keywords
        )

        if not has_business_context:
            continue

        email_match = re.search(
            email_pattern,
            line,
        )

        if not email_match:
            continue

        email = email_match.group(0)

        # ---------------------------------------------
        # Normalize common accidental trailing letters
        # after standard domain endings.
        # ---------------------------------------------

        domain_endings = (
            ".com",
            ".org",
            ".net",
            ".co",
            ".in",
            ".io",
            ".ai",
            ".uk",
            ".ca",
            ".au",
            ".sg",
        )

        email_lower = email.lower()

        best_end = None

        for ending in domain_endings:
            position = email_lower.find(ending)

            if position != -1:
                end_position = position + len(ending)

                if best_end is None or end_position > best_end:
                    best_end = end_position

        if best_end is not None:
            email = email[:best_end]

        return (
            "business_email",
            email,
            profile_url,
        )

    return None, None, None