from src.creator_discovery import create_candidate


def test_create_candidate():
    candidate = create_candidate(
        creator_name="Test Creator",
        creator_segment="YouTuber",
        primary_platform="YouTube",
        profile_url="https://example.com/test",
        stable_creator_id="test_creator_001",
        discovery_source="manual_test",
        discovery_query="test creator",
    )

    assert candidate.creator_name == "Test Creator"
    assert candidate.creator_segment == "YouTuber"
    assert candidate.primary_platform == "YouTube"
    assert candidate.stable_creator_id == "test_creator_001"


print("Discovery test OK")