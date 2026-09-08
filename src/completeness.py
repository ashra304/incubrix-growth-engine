from dataclasses import dataclass

from src.lead_schema import Lead


@dataclass
class CompletenessResult:
    complete: bool
    missing_fields: list[str]


REQUIRED_FIELDS = [
    "lead_id",
    "creator_name",
    "creator_segment",
    "country_iso2",
    "primary_language",
    "primary_platform",
    "profile_url",
    "stable_creator_id",
    "last_content_date",
    "recent_content_url",
    "content_count_30d",
    "longform_count_60d",
    "monetization_signal",
    "monetization_evidence_url",
    "incubrix_need",
    "need_evidence_url",
    "business_contact_type",
    "business_contact",
    "contact_evidence_url",
    "country_evidence_url",
    "language_evidence_url",
    "checked_date",
]


def check_completeness(lead: Lead) -> CompletenessResult:
    """
    Check whether all mandatory Lead fields contain data.

    Returns:
        CompletenessResult(
            complete=True/False,
            missing_fields=[...]
        )
    """

    missing_fields = []

    for field in REQUIRED_FIELDS:
        value = getattr(lead, field, None)

        if value is None or str(value).strip() == "":
            missing_fields.append(field)

    return CompletenessResult(
        complete=len(missing_fields) == 0,
        missing_fields=missing_fields,
    )