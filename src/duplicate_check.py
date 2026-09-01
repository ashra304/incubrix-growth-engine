from dataclasses import dataclass
from typing import Iterable

from src.lead_schema import Lead


@dataclass
class DuplicateCheckResult:
    is_duplicate: bool
    reason: str


def _normalize(value: str | None) -> str:
    """
    Normalize a value before comparing it.
    """
    if not value:
        return ""

    return value.strip().lower().rstrip("/")


def check_duplicate(
    lead: Lead,
    existing_leads: Iterable[Lead],
) -> DuplicateCheckResult:
    """
    Check whether a Lead already exists.

    Identity priority:

    1. stable_creator_id
    2. profile_url
    3. website_url
    4. lead_id
    """

    lead_stable_id = _normalize(
        lead.stable_creator_id
    )

    lead_profile = _normalize(
        lead.profile_url
    )

    lead_website = _normalize(
        lead.website_url
    )

    lead_id = _normalize(
        lead.lead_id
    )

    for existing in existing_leads:

        # -------------------------------------------------
        # Stable creator ID
        # -------------------------------------------------

        existing_stable_id = _normalize(
            existing.stable_creator_id
        )

        if (
            lead_stable_id
            and existing_stable_id
            and lead_stable_id == existing_stable_id
        ):
            return DuplicateCheckResult(
                is_duplicate=True,
                reason="stable_creator_id",
            )

        # -------------------------------------------------
        # Profile URL
        # -------------------------------------------------

        existing_profile = _normalize(
            existing.profile_url
        )

        if (
            lead_profile
            and existing_profile
            and lead_profile == existing_profile
        ):
            return DuplicateCheckResult(
                is_duplicate=True,
                reason="profile_url",
            )

        # -------------------------------------------------
        # Website URL
        # -------------------------------------------------

        existing_website = _normalize(
            existing.website_url
        )

        if (
            lead_website
            and existing_website
            and lead_website == existing_website
        ):
            return DuplicateCheckResult(
                is_duplicate=True,
                reason="website_url",
            )

        # -------------------------------------------------
        # Lead ID
        # -------------------------------------------------

        existing_lead_id = _normalize(
            existing.lead_id
        )

        if (
            lead_id
            and existing_lead_id
            and lead_id == existing_lead_id
        ):
            return DuplicateCheckResult(
                is_duplicate=True,
                reason="lead_id",
            )

    return DuplicateCheckResult(
        is_duplicate=False,
        reason="unique",
    )