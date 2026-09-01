from typing import Optional


def generate_personalization_hook(
    creator_name: str,
    creator_segment: str,
    commercial_signal: bool,
    incubrix_need: bool,
    active_30d: bool,
    long_form_60d: bool,
) -> Optional[str]:
    """
    Generate a short, evidence-based personalization hook.

    The hook is based only on signals already collected
    by the discovery and evidence layers.
    """

    if not creator_name.strip():
        return None

    name = creator_name.strip()

    if commercial_signal and incubrix_need:
        return (
            f"{name} is actively commercializing content "
            "and shows a relevant creator-business need."
        )

    if commercial_signal:
        return (
            f"{name} shows active commercial activity "
            "through public creator content."
        )

    if incubrix_need:
        return (
            f"{name} shows a public signal of a "
            "creator workflow or business-growth need."
        )

    if active_30d and long_form_60d:
        return (
            f"{name} is consistently publishing both "
            "recent and long-form content."
        )

    if active_30d:
        return (
            f"{name} has recent creator activity "
            "within the last 30 days."
        )

    if long_form_60d:
        return (
            f"{name} has published long-form content "
            "within the last 60 days."
        )

    return (
        f"{name} is a {creator_segment.strip().lower()} "
        "identified through creator discovery."
    )