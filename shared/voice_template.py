"""Voice profile template.

Fill in your team's voice — tone, do's, don'ts, 1-2 examples.
If your project generates customer-facing content, prefer calling the Brand Guidelines MCP
over defining voice locally. Use this only for internal voice (team tone for Slack posts, etc.)
that isn't already in the brand system.
"""

VOICE_PROFILE = {
    "tone": "",          # e.g., "direct, factual, no filler"
    "do": [
        # e.g., "state facts, then recommendation"
    ],
    "dont": [
        # e.g., "never use 'great', 'exciting', 'huge'"
    ],
    "examples": [
        # {"prompt": "...", "good": "...", "bad": "..."}
    ],
}


def voice_context() -> str:
    """Render the voice profile as a system-prompt fragment. Empty if unfilled."""
    if not any(VOICE_PROFILE.values()):
        return ""
    lines = []
    if VOICE_PROFILE["tone"]:
        lines.append(f"Tone: {VOICE_PROFILE['tone']}")
    if VOICE_PROFILE["do"]:
        lines.append("Do: " + "; ".join(VOICE_PROFILE["do"]))
    if VOICE_PROFILE["dont"]:
        lines.append("Don't: " + "; ".join(VOICE_PROFILE["dont"]))
    return "\n".join(lines)
