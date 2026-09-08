from src.qualification_stats import (
    QualificationStats,
    print_qualification_stats,
)


def test_qualification_stats():

    stats = QualificationStats(
        total=10,
        qualified=2,
        rejected=8,
        rejection_counts={
            "Country is outside the approved market list": 5,
            "Commercial activity evidence is missing": 4,
        },
    )

    assert stats.total == 10
    assert stats.qualified == 2
    assert stats.rejected == 8

    assert (
        stats.rejection_counts[
            "Country is outside the approved market list"
        ]
        == 5
    )

    print_qualification_stats(stats)


print("Qualification stats test OK")