from src.creator_discovery import discover_creators
from src.lead_builder import build_lead


# ---------------------------------------------------------
# Discover a real creator
# ---------------------------------------------------------

results = discover_creators(
    "technology creators",
    1,
)

assert len(results) == 1


candidate, activity, evidence = results[0]


# ---------------------------------------------------------
# Build Lead
# ---------------------------------------------------------

lead = build_lead(
    candidate=candidate,
    activity=activity,
    evidence=evidence,
    lead_id="TEST-001",
)


# ---------------------------------------------------------
# Verify identity
# ---------------------------------------------------------

assert lead.lead_id == "TEST-001"
assert lead.creator_name == candidate.creator_name
assert lead.creator_segment == candidate.creator_segment
assert lead.primary_platform == "YouTube"


# ---------------------------------------------------------
# Verify profile
# ---------------------------------------------------------

assert lead.profile_url == candidate.profile_url
assert lead.stable_creator_id == candidate.stable_creator_id


# ---------------------------------------------------------
# Verify activity
# ---------------------------------------------------------

assert (
    lead.content_count_30d
    == activity["content_count_30d"]
)

assert (
    lead.longform_count_60d
    == activity["longform_count_60d"]
)


# ---------------------------------------------------------
# Verify evidence
# ---------------------------------------------------------

assert lead.country_iso2 == (
    evidence.country_iso2 or ""
)

assert lead.primary_language == (
    evidence.primary_language or ""
)

assert lead.monetization_evidence_url == (
    evidence.monetization_evidence_url
)

assert lead.need_evidence_url == (
    evidence.need_evidence_url
)

assert lead.business_contact == (
    evidence.business_contact
)


print("Lead builder test OK")