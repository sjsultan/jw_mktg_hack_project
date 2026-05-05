"""Granola transcript source.

Within a Claude Code session the Granola MCP is already OAuth'd.
Use the helper command to fetch a transcript and save it locally:

    Run /fetch-granola in your Claude Code session, or ask Claude to call
    mcp__granola__list_meetings / mcp__granola__get_meeting_transcript
    and save the result to transcripts/<meeting-id>.json

This module reads those saved files for the Python pipeline.
"""
import json
from pathlib import Path


def load_transcript(path: str) -> str:
    """Load a Granola transcript from a saved JSON or plain-text file."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Transcript not found: {path}")

    if p.suffix == ".json":
        data = json.loads(p.read_text())
        # Granola MCP returns {transcript: "...", title: "...", ...}
        if isinstance(data, dict):
            parts = []
            if data.get("title"):
                parts.append(f"Meeting: {data['title']}")
            if data.get("transcript"):
                parts.append(data["transcript"])
            elif data.get("content"):
                parts.append(data["content"])
            else:
                parts.append(json.dumps(data, indent=2))
            return "\n\n".join(parts)
        return str(data)

    return p.read_text()
