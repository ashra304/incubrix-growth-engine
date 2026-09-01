from src.lead_schema import Lead
from src.duplicate_check import check_duplicate


def create_lead(
    lead_id="TEST-001",
    stable_id="UC123",
    profile="https://youtube.com/test",
    website=None,
):
    return Lead(
        lead_id=lead_id,
        creator_name="Test Creator",
        creator_segment="youtuber",
        country_iso2="US",
        primary_language="english",
        primary_platform="YouTube",

        profile_url=profile,
        stable_creator_id=stable_id,
        website_url=website,
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


def test_unique_lead():

    existing = create_lead(
        lead_id="EXISTING-001",
        stable_id="UC999",
    )

    new_lead = create_lead(
        lead_id="NEW-001",
        stable_id="UC123",
    )

    result = check_duplicate(
        new_lead,
        [existing],
    )

    assert result.is_duplicate is False
    assert result.reason == "unique"


def test_duplicate_stable_id():

    existing = create_lead(
        lead_id="EXISTING-001",
        stable_id="UC123",
    )

    new_lead = create_lead(
        lead_id="NEW-001",
        stable_id="UC123",
    )

    result = check_duplicate(
        new_lead,
        [existing],
    )

    assert result.is_duplicate is True
    assert result.reason == "stable_creator_id"


def test_duplicate_profile():

    existing = create_lead(
        lead_id="EXISTING-001",
        stable_id="UC999",
        profile="https://youtube.com/test",
    )

    new_lead = create_lead(
        lead_id="NEW-001",
        stable_id="UC123",
        profile="https://youtube.com/test/",
    )

    result = check_duplicate(
        new_lead,
        [existing],
    )

    assert result.is_duplicate is True
    assert result.reason == "profile_url"


def test_duplicate_website():

    existing = create_lead(
        lead_id="EXISTING-001",
        stable_id="UC999",
        website="https://example.com",
    )

    new_lead = create_lead(
        lead_id="NEW-001",
        stable_id="UC123",
        website="https://example.com/",
    )

    result = check_duplicate(
        new_lead,
        [existing],
    )

    assert result.is_duplicate is True
    assert result.reason == "website_url"


print("Duplicate check test OK")