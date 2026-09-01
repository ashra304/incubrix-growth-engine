from datetime import datetime, timezone


def is_evidence_within_30_days(
    checked_date: str,
) -> bool:
    """
    Return True when evidence was checked within
    the last 30 days.
    """

    if not checked_date:
        return False

    try:
        checked = datetime.fromisoformat(
            checked_date.replace("Z", "+00:00")
        )

        if checked.tzinfo is None:
            checked = checked.replace(
                tzinfo=timezone.utc
            )

        now = datetime.now(timezone.utc)

        age_days = (
            now - checked
        ).total_seconds() / 86400

        return 0 <= age_days <= 30

    except (ValueError, TypeError):
        return False