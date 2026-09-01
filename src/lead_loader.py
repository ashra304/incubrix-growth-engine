import csv
from pathlib import Path

from .lead_schema import Lead


REQUIRED_COLUMNS = [
    "lead_id",
    "creator_name",
    "creator_segment",
    "country_iso2",
    "primary_language",
    "primary_platform",
    "profile_url",
    "stable_creator_id",
]


def load_leads(csv_path: str) -> list[Lead]:
    """
    Load creator leads from the authoritative CSV file.
    """

    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(f"Lead file not found: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError("CSV file has no header row.")

        missing_columns = [
            column
            for column in REQUIRED_COLUMNS
            if column not in reader.fieldnames
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

        leads = []

        for row_number, row in enumerate(reader, start=2):
            try:
                lead = Lead(
                    lead_id=row["lead_id"].strip(),
                    creator_name=row["creator_name"].strip(),
                    creator_segment=row["creator_segment"].strip(),
                    country_iso2=row["country_iso2"].strip(),
                    primary_language=row["primary_language"].strip(),
                    primary_platform=row["primary_platform"].strip(),
                    profile_url=row["profile_url"].strip(),
                    stable_creator_id=row["stable_creator_id"].strip(),

                    website_url=row.get("website_url") or None,

                    followers_or_subscribers=_to_int(
                        row.get("followers_or_subscribers")
                    ),

                    last_content_date=row.get("last_content_date") or None,
                    recent_content_url=row.get("recent_content_url") or None,

                    content_count_30d=_to_int(
                        row.get("content_count_30d")
                    ),

                    longform_count_60d=_to_int(
                        row.get("longform_count_60d")
                    ),

                    monetization_signal=(
                        row.get("monetization_signal") or None
                    ),

                    monetization_evidence_url=(
                        row.get("monetization_evidence_url") or None
                    ),

                    incubrix_need=row.get("incubrix_need") or None,

                    need_evidence_url=(
                        row.get("need_evidence_url") or None
                    ),

                    business_contact_type=(
                        row.get("business_contact_type") or None
                    ),

                    business_contact=(
                        row.get("business_contact") or None
                    ),

                    contact_evidence_url=(
                        row.get("contact_evidence_url") or None
                    ),

                    country_evidence_url=(
                        row.get("country_evidence_url") or None
                    ),

                    language_evidence_url=(
                        row.get("language_evidence_url") or None
                    ),

                    checked_date=row["checked_date"].strip(),
                )

                leads.append(lead)

            except (KeyError, ValueError, TypeError) as error:
                raise ValueError(
                    f"Invalid data on CSV row {row_number}: {error}"
                ) from error

    return leads


def _to_int(value: str | None) -> int | None:
    """
    Convert an optional CSV value to an integer.
    """
    if value is None or value.strip() == "":
        return None

    return int(value.strip())