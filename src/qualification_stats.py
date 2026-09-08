from collections import Counter
from dataclasses import dataclass

from src.qualification import qualify_creator


@dataclass
class QualificationStats:
    total: int
    qualified: int
    rejected: int
    rejection_counts: dict[str, int]


def analyze_qualification(
    discovered,
) -> QualificationStats:
    """
    Analyze qualification results without changing
    the qualification rules.

    `discovered` must contain tuples of:

        (candidate, activity, evidence)
    """

    total = 0
    qualified = 0
    rejected = 0

    rejection_counts = Counter()

    for candidate, activity, evidence in discovered:

        total += 1

        active_30d = (
            (activity.get("content_count_30d") or 0) >= 8
        )

        long_form_60d = (
            (activity.get("longform_count_60d") or 0) >= 2
        )

        contactable = bool(
            evidence.business_contact
        )

        complete_fields = all(
            [
                bool(candidate.creator_name),
                bool(candidate.creator_segment),
                bool(candidate.primary_platform),
                bool(candidate.profile_url),
                bool(candidate.stable_creator_id),
                bool(evidence.country_iso2),
                bool(evidence.primary_language),
            ]
        )

        result = qualify_creator(
            creator_segment=candidate.creator_segment,
            country_iso2=evidence.country_iso2 or "",
            primary_language=evidence.primary_language or "",
            has_official_profile=bool(candidate.profile_url),
            has_stable_creator_id=bool(
                candidate.stable_creator_id
            ),
            active_30d=active_30d,
            long_form_60d=long_form_60d,
            commercial_signal=evidence.commercial_signal,
            incubrix_need=evidence.incubrix_need,
            contactable=contactable,
            complete_fields=complete_fields,
            unique_creator=True,
            evidence_within_30d=bool(
                evidence.checked_date
            ),
        )

        if result.qualified:

            qualified += 1

        else:

            rejected += 1

            for reason in result.rejection_reasons:
                rejection_counts[reason] += 1

    return QualificationStats(
        total=total,
        qualified=qualified,
        rejected=rejected,
        rejection_counts=dict(
            rejection_counts
        ),
    )


def print_qualification_stats(
    stats: QualificationStats,
):
    """
    Print a readable qualification analysis.
    """

    print()
    print("=" * 55)
    print("QUALIFICATION ANALYSIS")
    print("=" * 55)

    print(
        f"Total discovered: {stats.total}"
    )

    print(
        f"Qualified:         {stats.qualified}"
    )

    print(
        f"Rejected:          {stats.rejected}"
    )

    print()
    print("REJECTION REASONS")
    print("-" * 55)

    if not stats.rejection_counts:

        print("No rejection reasons.")

    else:

        sorted_reasons = sorted(
            stats.rejection_counts.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        for reason, count in sorted_reasons:

            print(
                f"{count:>3}  {reason}"
            )

    print("=" * 55)