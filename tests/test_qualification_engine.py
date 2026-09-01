from src.creator_discovery import DiscoveryCandidate
from src.evidence import EvidenceRecord
from src.qualification_engine import evaluate_candidate


def test_qualification_engine():

    candidate = DiscoveryCandidate(
        creator_name="Test Creator",
        creator_segment="youtuber",
        primary_platform="YouTube",
        profile_url="https://youtube.com/channel/test",
        stable_creator_id="UC_TEST_001",
        discovery_source="YouTube Data API",
        discovery_query="technology creators",
        discovered_at="2026-09-01T00:00:00+00:00",
    )

    evidence = EvidenceRecord(
        country_iso2="US",
        primary_language="English",
        commercial_signal=True,
        monetization_evidence_url="https://example.com/commercial",
        incubrix_need=True,
        need_evidence_url="https://example.com/need",
        business_contact_type="email",
        business_contact="business@example.com",
        contact_evidence_url="https://example.com/contact",
        country_evidence_url="https://example.com/country",
        language_evidence_url="https://example.com/language",
        checked_date="2026-09-01",
    )

    activity = {
        "content_count_30d": 10,
        "longform_count_60d": 3,
        "last_content_date": "2026-08-31T00:00:00+00:00",
        "recent_content_url": "https://youtube.com/watch?v=test",
    }

    result = evaluate_candidate(
        candidate=candidate,
        evidence=evidence,
        activity=activity,
    )

    assert result.qualified is True
    assert result.rejection_reasons == []


print("Qualification engine test OK")