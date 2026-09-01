from src.lead_schema import Lead
from src.completeness import check_completeness


def create_test_lead():
    return Lead(
        lead_id="TEST-001",
        creator_name="Test Creator",
        creator_segment="youtuber",
        country_iso2="US",
        primary_language="english",
        primary_platform="YouTube",

        profile_url="https://youtube.com/test",
        stable_creator_id="UC123",

        website_url=None,
        followers_or_subscribers=None,

        last_content_date=None,
        recent_content_url=None,
        content_count_30d=None,
        longform_count_60d=None,

        monetization_signal=None,
        monetization_evidence_url=None,

        incubrix_need=None,
        need_evidence_url=None,

        business_contact_type=None,
        business_contact=None,
        contact_evidence_url=None,

        country_evidence_url=None,
        language_evidence_url=None,
        checked_date="2026-09-01",

        priority=None,
        personalization_hook=None,
        candidate_status=None,
        rejection_reason=None,
        duplicate_check=None,
        completeness_check=None,
    )


def test_complete_lead():

    lead = create_test_lead()

    result = check_completeness(lead)

    assert result.complete is True
    assert result.missing_fields == []


def test_incomplete_lead():

    lead = create_test_lead()

    lead.primary_language = ""
    lead.country_iso2 = ""

    result = check_completeness(lead)

    assert result.complete is False
    assert "primary_language" in result.missing_fields
    assert "country_iso2" in result.missing_fields


print("Completeness test OK")