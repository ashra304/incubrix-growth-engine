from src.sources.youtube import normalize_youtube_channel


def test_normalize_youtube_channel():

    record = normalize_youtube_channel(
        channel_id="UC_TEST_001",
        channel_title="Test Creator",
        channel_url="https://www.youtube.com/channel/UC_TEST_001",
        country_iso2="US",
        description="Test creator channel",
    )

    assert record.creator_name == "Test Creator"
    assert record.primary_platform == "YouTube"
    assert record.stable_creator_id == "UC_TEST_001"
    assert record.country_iso2 == "US"


print("YouTube source test OK")