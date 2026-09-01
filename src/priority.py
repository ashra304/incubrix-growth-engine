from dataclasses import dataclass


@dataclass
class PriorityResult:
    priority: str
    score: int


def calculate_priority(
    qualified: bool,
    commercial_signal: bool,
    incubrix_need: bool,
    contactable: bool,
    active_30d: bool,
    long_form_60d: bool,
) -> PriorityResult:
    """
    Calculate an explainable priority level for a creator.

    Priority is assigned only after qualification.

    Scoring:
        Commercial signal  : 25 points
        IncuBrix need       : 25 points
        Business contact   : 20 points
        Recent activity     : 15 points
        Long-form activity  : 15 points

    Maximum score: 100
    """

    # A rejected creator cannot become a priority lead.
    if not qualified:
        return PriorityResult(
            priority="REJECTED",
            score=0,
        )

    score = 0

    if commercial_signal:
        score += 25

    if incubrix_need:
        score += 25

    if contactable:
        score += 20

    if active_30d:
        score += 15

    if long_form_60d:
        score += 15

    if score >= 80:
        priority = "A"
    elif score >= 60:
        priority = "B"
    else:
        priority = "C"

    return PriorityResult(
        priority=priority,
        score=score,
    )