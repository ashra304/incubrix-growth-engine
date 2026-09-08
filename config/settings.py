import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "logs"

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def require_youtube_api_key() -> str:
    """Return the configured key only when a live API call is about to run."""
    if not YOUTUBE_API_KEY:
        raise RuntimeError(
            "YOUTUBE_API_KEY is not configured. "
            "Set it as an environment variable before running the engine."
        )
    return YOUTUBE_API_KEY