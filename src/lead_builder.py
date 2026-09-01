from datetime import datetime, timezone

from src.creator_discovery import DiscoveryCandidate
from src.lead_schema import Lead


def build_lead(
    candidate: DiscoveryCandidate,
    activity: dict,
    evidence,
    lead_id: str,
) -> Lead:
    """
    Convert a DiscoveryCandidate, activity information,
    and EvidenceRecord into a Lead.

    This function only constructs the Lead.
    Qualification and deduplication happen elsewhere.
    """

    return Lead(
        # ---------------------------------------------
        # Identity
        # ---------------------------------------------

        lead_id=lead_id,
        creator_name=candidate.creator_name,
        creator_segment=candidate.creator_segment,
        country_iso2=evidence.country_iso2 or "",
        primary_language=evidence.primary_language or "",
        primary_platform=candidate.primary_platform,

        # ---------------------------------------------
        # Profile
        # ---------------------------------------------

        profile_url=candidate.profile_url,
        stable_creator_id=candidate.stable_creator_id,
        website_url=None,
        followers_or_subscribers=None,

        # ---------------------------------------------
        # Activity
        # ---------------------------------------------

        last_content_date=activity.get("last_content_date"),
        recent_content_url=activity.get("recent_content_url"),
        content_count_30d=activity.get("content_count_30d"),
        longform_count_60d=activity.get("longform_count_60d"),

        # ---------------------------------------------
        # Commercial signals
        # ---------------------------------------------

        monetization_signal=(
            "true"
            if evidence.commercial_signal
            else "false"
        ),

        monetization_evidence_url=(
            evidence.monetization_evidence_url
        ),

        # ---------------------------------------------
        # IncuBrix need
        # ---------------------------------------------

        incubrix_need=(
            "true"
            if evidence.incubrix_need
            else "false"
        ),

        need_evidence_url=evidence.need_evidence_url,

        # ---------------------------------------------
        # Business contact
        # ---------------------------------------------

        business_contact_type=evidence.business_contact_type,
        business_contact=evidence.business_contact,
        contact_evidence_url=evidence.contact_evidence_url,

        # ---------------------------------------------
        # Verification
        # ---------------------------------------------

        country_evidence_url=evidence.country_evidence_url,
        language_evidence_url=evidence.language_evidence_url,
        checked_date=evidence.checked_date,

        # ---------------------------------------------
        # Engine output
        # ---------------------------------------------

        priority=None,
        personalization_hook=None,
        candidate_status=None,
        rejection_reason=None,
        duplicate_check=None,
        completeness_check=None,
    )