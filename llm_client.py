"""Vendored Claude client. Accepts LITELLM_BASE_URL+LITELLM_API_KEY OR ANTHROPIC_API_KEY.

Do not import the anthropic SDK directly in agent code. Use get_client() from here.
"""
import os
from anthropic import Anthropic

DEFAULT_MODEL = os.environ.get("MODEL", "claude-sonnet-4-6")

CLAUDE_HAIKU = "claude-haiku-4-5-20251001"
CLAUDE_SONNET = "claude-sonnet-4-6"
CLAUDE_OPUS = "claude-opus-4-7"


def get_client() -> Anthropic:
    """Return an Anthropic client pointed at LiteLLM proxy if configured, else direct."""
    base_url = os.environ.get("LITELLM_BASE_URL")
    if base_url:
        api_key = os.environ.get("LITELLM_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "LITELLM_BASE_URL set but no API key — set LITELLM_API_KEY or ANTHROPIC_API_KEY"
            )
        return Anthropic(base_url=base_url, api_key=api_key)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "No Claude credential — set ANTHROPIC_API_KEY (personal) or "
            "LITELLM_BASE_URL+LITELLM_API_KEY (JW proxy). See PREREQUISITES.md."
        )
    return Anthropic(api_key=api_key)
