from src.source_schema import SourceRecord


def test_source_record():

    record = SourceRecord(
        creator_name="Test Creator",
        creator_segment="youtuber",
        country_iso2="US",
        primary_language="English",
        primary_platform="YouTube",
        profile_url="https://example.com/creator",
        stable_creator_id="creator_001",
        source_name="manual_public_research",
        source_url="https://example.com/source",
        discovered_at="2026-09-01T00:00:00+00:00",
    )

    assert record.creator_name == "Test Creator"
    assert record.primary_platform == "YouTube"
    assert record.country_iso2 == "US"
    assert record.stable_creator_id == "creator_001"


print("Source schema test OK")