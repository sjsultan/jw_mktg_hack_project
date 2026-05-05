"""Audit log: records every model call and external write target.

Never disable. Reviewed on demo day to answer "what did my agent actually do?"
"""
import datetime
import json
import os
from pathlib import Path

LOG_PATH = Path(os.environ.get("RUN_LOG_PATH", "run_log.jsonl"))


def log(event_type: str, **fields) -> None:
    """Append an event to run_log.jsonl."""
    row = {
        "ts": datetime.datetime.utcnow().isoformat() + "Z",
        "event": event_type,
        **fields,
    }
    with LOG_PATH.open("a") as f:
        f.write(json.dumps(row) + "\n")


def log_model_call(model: str, prompt_tokens: int | None = None, completion_tokens: int | None = None, **extra) -> None:
    log("model_call", model=model, prompt_tokens=prompt_tokens, completion_tokens=completion_tokens, **extra)


def log_external_write(tool: str, destination: str, payload_preview: str, confirmed: bool) -> None:
    log("external_write", tool=tool, destination=destination, payload_preview=payload_preview[:200], confirmed=confirmed)
