from src.lead_schema import Lead
from src.qualification import qualify_creator
from src.priority import calculate_priority
from src.personalization import generate_personalization_hook
from src.completeness import check_completeness
from src.duplicate_check import check_duplicate
from src.deduplication import deduplicate_leads


def create_valid_lead():
    return Lead(
        lead_id="E2E-001",
        creator_name="Test Creator",
        creator_segment="youtuber",
        country_iso2="US",
        primary_language="english",
        primary_platform="YouTube",

        profile_url="https://youtube.com/test",
        stable_creator_id="UC-E2E-001",

        website_url=None,
        followers_or_subscribers=50000,

        last_content_date="2026-08-30T10:00:00+00:00",
        recent_content_url="https://youtube.com/watch?v=test",
        content_count_30d=5,
        longform_count_60d=3,

        monetization_signal="true",
        monetization_evidence_url="https://youtube.com/watch?v=test",

        incubrix_need="true",
        need_evidence_url="https://youtube.com/watch?v=test",

        business_contact_type="business_email",
        business_contact="business@test.com",
        contact_evidence_url="https://youtube.com/test",

        country_evidence_url="https://youtube.com/test",
        language_evidence_url="https://youtube.com/watch?v=test",
        checked_date="2026-09-01",

        priority=None,
        personalization_hook=None,
        candidate_status=None,
        rejection_reason=None,
        duplicate_check=None,
        completeness_check=None,
    )


def test_end_to_end():

    lead = create_valid_lead()

    # ---------------------------------------------------------
    # 1. QUALIFICATION
    # ---------------------------------------------------------

    qualification = qualify_creator(
        creator_segment=lead.creator_segment,
        country_iso2=lead.country_iso2,
        primary_language=lead.primary_language,
        has_official_profile=True,
        has_stable_creator_id=True,
        active_30d=True,
        long_form_60d=True,
        commercial_signal=True,
        incubrix_need=True,
        contactable=True,
        complete_fields=True,
        unique_creator=True,
        evidence_within_30d=True,
    )

    assert qualification.qualified is True

    lead.candidate_status = "qualified"

    # ---------------------------------------------------------
    # 2. PRIORITY
    # ---------------------------------------------------------

    priority_result = calculate_priority(
        qualified=True,
        commercial_signal=True,
        incubrix_need=True,
        contactable=True,
        active_30d=True,
        long_form_60d=True,
    )

    lead.priority = priority_result.priority

    assert lead.priority is not None
    assert lead.priority != "REJECTED"

    # ---------------------------------------------------------
    # 3. PERSONALIZATION
    # ---------------------------------------------------------

    lead.personalization_hook = (
        generate_personalization_hook(
            creator_name=lead.creator_name,
            creator_segment=lead.creator_segment,
            commercial_signal=True,
            incubrix_need=True,
            active_30d=True,
            long_form_60d=True,
        )
    )

    assert lead.personalization_hook is not None
    assert "Test Creator" in lead.personalization_hook

    # ---------------------------------------------------------
    # 4. COMPLETENESS
    # ---------------------------------------------------------

    completeness_result = check_completeness(
        lead
    )

    assert completeness_result.complete is True

    lead.completeness_check = "complete"

    # ---------------------------------------------------------
    # 5. DUPLICATE CHECK
    # ---------------------------------------------------------

    duplicate_result = check_duplicate(
        lead,
        [],
    )

    assert duplicate_result.is_duplicate is False

    lead.duplicate_check = "unique"

    # ---------------------------------------------------------
    # 6. DEDUPLICATION
    # ---------------------------------------------------------

    final_leads = deduplicate_leads(
        [lead]
    )

    assert len(final_leads) == 1
    assert final_leads[0].lead_id == "E2E-001"


print("End-to-end test OK")