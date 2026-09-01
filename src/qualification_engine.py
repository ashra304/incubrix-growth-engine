from src.creator_discovery import DiscoveryCandidate
from src.evidence import EvidenceRecord
from src.qualification import QualificationResult, qualify_creator


def evaluate_candidate(
    candidate: DiscoveryCandidate,
    evidence: EvidenceRecord,
    activity: dict,
) -> QualificationResult:
    """
    Evaluate a discovered creator using verified activity
    and evidence.

    This function does not modify the qualification rules.
    It only maps collected evidence into the existing
    qualification contract.
    """

    active_30d = activity.get("content_count_30d", 0) >= 8
    long_form_60d = activity.get("longform_count_60d", 0) >= 2

    complete_fields = all(
        [
            candidate.creator_name,
            candidate.creator_segment,
            candidate.primary_platform,
            candidate.profile_url,
            candidate.stable_creator_id,
            evidence.country_iso2,
            evidence.primary_language,
            evidence.checked_date,
        ]
    )

    unique_creator = bool(candidate.stable_creator_id)

    evidence_within_30d = bool(evidence.checked_date)

    contactable = bool(
        evidence.business_contact_type
        and evidence.business_contact
        and evidence.contact_evidence_url
    )

    return qualify_creator(
        creator_segment=candidate.creator_segment,
        country_iso2=evidence.country_iso2 or "",
        primary_language=evidence.primary_language or "",
        has_official_profile=bool(candidate.profile_url),
        has_stable_creator_id=bool(candidate.stable_creator_id),
        active_30d=active_30d,
        long_form_60d=long_form_60d,
        commercial_signal=evidence.commercial_signal,
        incubrix_need=evidence.incubrix_need,
        contactable=contactable,
        complete_fields=complete_fields,
        unique_creator=unique_creator,
        evidence_within_30d=evidence_within_30d,
    )