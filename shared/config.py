"""Config helpers: fail fast when env vars are missing."""
import os


def require_env(*names: str) -> dict[str, str]:
    """Return a dict of the requested env vars; raise if any are unset or empty."""
    missing = [n for n in names if not os.environ.get(n)]
    if missing:
        raise RuntimeError(
            f"Missing required env vars: {', '.join(missing)}. "
            "Check .env.local against PREREQUISITES.md."
        )
    return {n: os.environ[n] for n in names}
