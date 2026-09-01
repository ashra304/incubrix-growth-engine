from typing import Iterable

from src.lead_schema import Lead


def _normalize(value: str | None) -> str:
    if not value:
        return ""

    return value.strip().lower().rstrip("/")


def deduplicate_leads(leads: Iterable[Lead]) -> list[Lead]:
    """
    Remove duplicate creators using stable identity signals.

    Priority:
    1. stable_creator_id
    2. profile_url
    3. website_url
    4. lead_id

    The first occurrence is retained.
    """

    seen_stable_ids: set[str] = set()
    seen_profiles: set[str] = set()
    seen_websites: set[str] = set()
    seen_lead_ids: set[str] = set()

    unique_leads: list[Lead] = []

    for lead in leads:
        stable_id = _normalize(lead.stable_creator_id)
        profile = _normalize(lead.profile_url)
        website = _normalize(lead.website_url)
        lead_id = _normalize(lead.lead_id)

        is_duplicate = (
            (stable_id and stable_id in seen_stable_ids)
            or (profile and profile in seen_profiles)
            or (website and website in seen_websites)
            or (lead_id and lead_id in seen_lead_ids)
        )

        if is_duplicate:
            continue

        unique_leads.append(lead)

        if stable_id:
            seen_stable_ids.add(stable_id)

        if profile:
            seen_profiles.add(profile)

        if website:
            seen_websites.add(website)

        if lead_id:
            seen_lead_ids.add(lead_id)

    return unique_leads