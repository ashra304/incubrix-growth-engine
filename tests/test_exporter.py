from pathlib import Path

from src.lead_schema import Lead
from src.exporter import export_leads_to_csv


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
        followers_or_subscribers=10000,

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

        priority="A",
        personalization_hook="Test Creator shows a relevant creator-business need.",
        candidate_status="qualified",
        rejection_reason=None,
        duplicate_check="unique",
        completeness_check="complete",
    )


def test_export_csv():

    output_path = "data/test_export.csv"

    lead = create_test_lead()

    result = export_leads_to_csv(
        [lead],
        output_path,
    )

    assert result == output_path

    path = Path(output_path)

    assert path.exists()

    content = path.read_text(
        encoding="utf-8-sig"
    )

    assert "lead_id" in content
    assert "creator_name" in content
    assert "Test Creator" in content
    assert "business@test.com" in content
    assert "qualified" in content


print("Exporter test OK")