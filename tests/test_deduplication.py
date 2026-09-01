from src.deduplication import deduplicate_leads
from src.lead_schema import Lead


def make_lead(
    lead_id: str,
    stable_creator_id: str,
    profile_url: str,
) -> Lead:
    return Lead(
        lead_id=lead_id,
        creator_name="Test Creator",
        creator_segment="creator",
        country_iso2="IN",
        primary_language="English",
        primary_platform="YouTube",
        profile_url=profile_url,
        stable_creator_id=stable_creator_id,
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
        checked_date="2026-08-31",
        priority=None,
        personalization_hook=None,
        candidate_status=None,
        rejection_reason=None,
        duplicate_check=None,
        completeness_check=None,
    )


def test_duplicate_stable_creator_id():
    leads = [
        make_lead("1", "creator_001", "https://youtube.com/@creator1"),
        make_lead("2", "creator_001", "https://youtube.com/@creator1"),
    ]

    result = deduplicate_leads(leads)

    assert len(result) == 1


def test_duplicate_profile_url():
    leads = [
        make_lead("1", "creator_001", "https://youtube.com/@creator1"),
        make_lead("2", "creator_002", "https://youtube.com/@creator1/"),
    ]

    result = deduplicate_leads(leads)

    assert len(result) == 1


def test_unique_leads_are_preserved():
    leads = [
        make_lead("1", "creator_001", "https://youtube.com/@creator1"),
        make_lead("2", "creator_002", "https://youtube.com/@creator2"),
    ]

    result = deduplicate_leads(leads)

    assert len(result) == 2


print("Deduplication test OK")