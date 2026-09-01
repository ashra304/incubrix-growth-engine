from dataclasses import dataclass
from typing import Optional


@dataclass
class Lead:
    # Identity
    lead_id: str
    creator_name: str
    creator_segment: str
    country_iso2: str
    primary_language: str
    primary_platform: str

    # Profile
    profile_url: str
    stable_creator_id: str
    website_url: Optional[str]
    followers_or_subscribers: Optional[int]

    # Activity
    last_content_date: Optional[str]
    recent_content_url: Optional[str]
    content_count_30d: Optional[int]
    longform_count_60d: Optional[int]

    # Commercial signals
    monetization_signal: Optional[str]
    monetization_evidence_url: Optional[str]

    # IncuBrix need
    incubrix_need: Optional[str]
    need_evidence_url: Optional[str]

    # Business contact
    business_contact_type: Optional[str]
    business_contact: Optional[str]
    contact_evidence_url: Optional[str]

    # Verification
    country_evidence_url: Optional[str]
    language_evidence_url: Optional[str]
    checked_date: str

    # Engine output
    priority: Optional[str] = None
    personalization_hook: Optional[str] = None
    candidate_status: Optional[str] = None
    rejection_reason: Optional[str] = None
    duplicate_check: Optional[str] = None
    completeness_check: Optional[str] = None