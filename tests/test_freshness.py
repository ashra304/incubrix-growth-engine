from datetime import datetime, timedelta, timezone

from src.freshness import is_evidence_within_30_days


def test_recent_evidence():

    date = (
        datetime.now(timezone.utc)
        - timedelta(days=5)
    ).date().isoformat()

    assert is_evidence_within_30_days(date) is True


def test_old_evidence():

    date = (
        datetime.now(timezone.utc)
        - timedelta(days=31)
    ).date().isoformat()

    assert is_evidence_within_30_days(date) is False


def test_missing_date():

    assert is_evidence_within_30_days("") is False


def test_invalid_date():

    assert is_evidence_within_30_days(
        "not-a-date"
    ) is False


print("Freshness test OK")