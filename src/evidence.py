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

    The function looks for explicit and implicit commercial
    language in titles and descriptions.
    """

    if not videos:
        return False, None

    # Explicit commercial signals - must be present
    explicit_phrases = {
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
        "#ad",
        "#sponsored",
    }

    # Implicit commercial signals - suggest commercial activity
    implicit_phrases = {
        "course",
        "masterclass",
        "coaching",
        "membership",
        "subscription",
        "paid membership",
        "premium",
        "product launch",
        "ecommerce",
        "e-commerce",
        "store",
        "business",
        "revenue",
        "income",
        "earn money",
        "monetize",
        "monetization",
        "selling",
        "sell",
        "offer",
        "service",
        "consulting",
        "freelance",
        "agency",
        "brand deal",
        "partnership",
        "collaboration",
        "link in bio",
        "use code",
        "discount",
    }

    for video in videos:
        title = video.get("title", "")
        description = video.get("description", "")

        text = f"{title} {description}".lower()

        # Check for explicit signals first
        for phrase in explicit_phrases:
            if phrase in text:
                return True, video.get("url")

    # If no explicit signals, check for implicit commercial activity
    implicit_count = 0
    evidence_url = None
    for video in videos:
        title = video.get("title", "")
        description = video.get("description", "")
        text = f"{title} {description}".lower()

        for phrase in implicit_phrases:
            if phrase in text:
                # Count multiple occurrences of the same phrase
                occurrences = text.count(phrase)
                implicit_count += occurrences
                if evidence_url is None:
                    evidence_url = video.get("url")
                # If we have multiple commercial signals, consider it a real signal
                if implicit_count >= 2:
                    return True, evidence_url

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

    Looks for explicit and implicit creator/business problems
    in recent public YouTube content.
    
    IncuBrix-relevant needs include:
    - Content creation and strategy
    - Content repurposing and editing
    - Video editing and captions
    - Publishing and distribution
    - Consistency and scheduling
    - Content backlog management
    - Team workflow and collaboration
    """

    if not videos:
        return False, None

    # Explicit IncuBrix need signals
    explicit_needs = {
        "content strategy",
        "content management",
        "content workflow",
        "creator workflow",
        "creator tools",
        "creator business",
        "content creation",
        "video editing",
        "editing",
        "captions",
        "transcription",
        "repurposing",
        "repurpose",
        "publishing",
        "scheduling",
        "consistency",
        "backlog",
        "team management",
        "collaboration",
        "workflow automation",
        "content calendar",
        "production workflow",
        "batch record",
        "batch content",
    }

    # Implicit signals - suggest need for IncuBrix services
    implicit_needs = {
        "audience growth",
        "channel growth",
        "grow my channel",
        "grow your channel",
        "growing",
        "scaling",
        "scale my",
        "scale your",
        "automation",
        "automate",
        "productivity",
        "efficient",
        "save time",
        "time management",
        "quality",
        "high quality",
        "professional",
        "monetization",
        "creator economy",
        "sponsorship management",
        "brand deals",
        "brand partnerships",
        "consistent upload",
        "regular upload",
        "frequently",
        "manage",
        "organize",
        "tools",
        "system",
        "process",
        "business growth",
        "business strategy",
    }

    # Check for explicit signals first
    evidence_url = None
    explicit_count = 0
    for video in videos:
        title = video.get("title", "")
        description = video.get("description", "")
        text = f"{title} {description}".lower()

        for phrase in explicit_needs:
            if phrase in text:
                explicit_count += 1
                if evidence_url is None:
                    evidence_url = video.get("url")
                # One explicit signal is enough
                if explicit_count >= 1:
                    return True, evidence_url

    # If no explicit signals, check for multiple implicit signals
    implicit_count = 0
    evidence_url = None
    for video in videos:
        title = video.get("title", "")
        description = video.get("description", "")
        text = f"{title} {description}".lower()

        for phrase in implicit_needs:
            if phrase in text:
                implicit_count += 1
                if evidence_url is None:
                    evidence_url = video.get("url")
                # Need at least 3 implicit signals to confirm
                if implicit_count >= 3:
                    return True, evidence_url

    return False, None

def extract_business_contact(
    description: Optional[str],
    profile_url: str,
) -> tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Extract an explicitly published business contact from
    a public YouTube channel description.

    Returns:
        (contact_type, contact, evidence_url)

    Searches for business emails, contact forms, booking pages,
    and other verified public contact routes. Guessed contacts
    are not allowed - only published, verifiable contacts.
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
        "inquiries",
        "inquiry",
        "reach out",
        "email",
        "message",
        "dm",
        "booking",
        "book",
        "consulting",
        "hire",
        "hire me",
    }

    # Email pattern
    email_pattern = (
        r"\b[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    )

    # URL patterns for contact forms, booking pages, etc.
    url_patterns = [
        r"(?:https?://)?(?:www\.)?[\w\-\.]+\.(com|org|net|co|io|app|dev|me)/?(?=[^\w\-\.]|\s|$)",  # Basic domain
    ]

    lines = description.splitlines()
    contact_lines = []

    for line in lines:
        line_lower = line.lower()

        # Check if line contains business-related keywords
        has_business_context = any(
            keyword in line_lower
            for keyword in business_keywords
        )

        if has_business_context:
            contact_lines.append((line, line_lower))

    # Try to extract email first (most reliable)
    for line, line_lower in contact_lines:
        email_match = re.search(email_pattern, line)

        if not email_match:
            continue

        email = email_match.group(0)

        # Normalize common accidental trailing letters
        domain_endings = (
            ".com", ".org", ".net", ".co", ".in", ".io",
            ".ai", ".uk", ".ca", ".au", ".sg",
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

        return ("business_email", email, profile_url)

    # Try to extract contact form or booking page URLs
    for line, line_lower in contact_lines:
        # Look for URL patterns
        if "http" in line_lower or ".com" in line_lower:
            # Extract URLs
            url_matches = re.findall(
                r"https?://[^\s\)]+|www\.[^\s\)]+",
                line
            )
            for url in url_matches:
                # Clean up trailing punctuation
                url = url.rstrip('.,;:)')
                
                # Detect type of contact method
                url_lower = url.lower()
                if any(x in url_lower for x in ["contact", "inquiry"]):
                    return ("contact_form", url, profile_url)
                elif any(x in url_lower for x in ["book", "calendly", "calendar", "appointment", "acuity"]):
                    return ("booking_page", url, profile_url)
                elif any(x in url_lower for x in ["linktr", "beacons"]):
                    return ("link_aggregator", url, profile_url)
                else:
                    # Generic website link with business context
                    return ("website", url, profile_url)

    # Look for generic URLs in business context lines
    for line, line_lower in contact_lines:
        # Simple domain extraction
        domain_matches = re.findall(
            r"(?:https?://)?(?:www\.)?[\w\-\.]+\.(com|org|net|co|io)",
            line,
            re.IGNORECASE
        )
        if domain_matches:
            for domain in domain_matches:
                if isinstance(domain, tuple):
                    domain = domain[0]
                # Construct full URL if needed
                if not domain.startswith("http"):
                    domain = "https://" + domain
                return ("website", domain, profile_url)

    return None, None, None