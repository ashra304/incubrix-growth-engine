from dataclasses import dataclass


APPROVED_COUNTRIES = {
    "US",
    "CA",
    "GB",
    "IE",
    "AU",
    "NZ",
    "SG",
}

APPROVED_SEGMENTS = {
    "podcaster",
    "video_podcaster",
    "youtuber",
    "video_first_creator",
    "expert_led_creator",
}


@dataclass
class QualificationResult:
    qualified: bool
    rejection_reasons: list[str]


def qualify_creator(
    creator_segment: str,
    country_iso2: str,
    primary_language: str,
    has_official_profile: bool,
    has_stable_creator_id: bool,
    active_30d: bool,
    long_form_60d: bool,
    commercial_signal: bool,
    incubrix_need: bool,
    contactable: bool,
    complete_fields: bool,
    unique_creator: bool,
    evidence_within_30d: bool,
) -> QualificationResult:

    reasons = []

    segment = creator_segment.strip().lower()
    country = country_iso2.strip().upper()
    language = primary_language.strip().lower()

    # 1. Creator segment
    if segment not in APPROVED_SEGMENTS:
        reasons.append("Not an approved creator segment")

    # 2. Country
    if country not in APPROVED_COUNTRIES:
        reasons.append("Country is outside the approved market list")

    # 3. English content
    if language != "english":
        reasons.append("Recent content is not mainly in English")

    # 4. Real and relevant
    if not has_official_profile:
        reasons.append("Official profile is missing")

    if not has_stable_creator_id:
        reasons.append("Stable creator ID is missing")

    # 5. Activity
    if not (active_30d or long_form_60d):
        reasons.append("Activity requirement not satisfied")

    # 6. Commercial signal
    if not commercial_signal:
        reasons.append("Commercial activity evidence is missing")

    # 7. IncuBrix need
    if not incubrix_need:
        reasons.append("IncuBrix need evidence is missing")

    # 8. Contactability
    if not contactable:
        reasons.append("Verified public business contact is missing")

    # 9. Completeness
    if not complete_fields:
        reasons.append("Required workbook fields are incomplete")

    # 10. Uniqueness
    if not unique_creator:
        reasons.append("Creator is a duplicate")

    # 11. Evidence freshness
    if not evidence_within_30d:
        reasons.append("Evidence was not checked within 30 days")

    return QualificationResult(
        qualified=len(reasons) == 0,
        rejection_reasons=reasons,
    )