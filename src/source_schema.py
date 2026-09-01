from dataclasses import dataclass
from typing import Optional


@dataclass
class SourceRecord:
    """
    Raw information collected from a legitimate public source.

    A SourceRecord is not automatically a qualified lead.
    It must pass the qualification and evidence checks first.
    """

    creator_name: str
    creator_segment: str
    country_iso2: Optional[str]
    primary_language: Optional[str]
    primary_platform: str

    profile_url: str
    stable_creator_id: Optional[str]

    source_name: str
    source_url: str
    discovered_at: str

    description: Optional[str]