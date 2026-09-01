import csv
from dataclasses import fields
from pathlib import Path
from typing import Iterable

from src.lead_schema import Lead


def export_leads_to_csv(
    leads: Iterable[Lead],
    output_path: str,
) -> str:
    """
    Export Lead objects to a CSV file.

    The Lead dataclass is treated as the authoritative
    output schema.

    Returns:
        The path of the created CSV file.
    """

    path = Path(output_path)

    # Create parent directory if it does not exist.
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    lead_fields = [
        field.name
        for field in fields(Lead)
    ]

    with path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=lead_fields,
        )

        writer.writeheader()

        for lead in leads:

            writer.writerow(
                {
                    field: getattr(
                        lead,
                        field,
                    )
                    for field in lead_fields
                }
            )

    return str(path)