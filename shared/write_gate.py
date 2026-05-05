"""Write gate: 🔴 shared-tool writes must pass through here.

Pattern:
    write_gate("asana", "project:12345", payload_dict, confirm=args.confirm)

Default (no --confirm, no AGENT_AUTOCONFIRM=1): prints dry-run preview, does not execute.
With either flag: records the intent in run_log and executes via the callable.
"""
import json
import os
from typing import Any, Callable

from .run_log import log_external_write


def write_gate(
    tool: str,
    destination: str,
    payload: Any,
    *,
    confirm: bool = False,
    execute: Callable[[], Any] | None = None,
) -> Any | None:
    """Gate a red-tier write.

    - tool: short name (e.g., "asana", "slack", "contentful")
    - destination: explicit target (channel, project GID, env, etc.)
    - payload: what's being written (dict, str, or anything JSON-serializable)
    - confirm: pass True (from --confirm flag) to actually execute
    - execute: the callable that performs the write; returns its result

    Honors AGENT_AUTOCONFIRM=1 for scripted runs (use sparingly).
    """
    preview = json.dumps(payload, default=str, indent=2)[:500]
    auto = os.environ.get("AGENT_AUTOCONFIRM") == "1"

    print(f"\n━━━ 🔴 WRITE GATE: {tool} → {destination} ━━━")
    print(preview)

    if not (confirm or auto):
        print(f"\n[DRY-RUN] pass --confirm (or set AGENT_AUTOCONFIRM=1) to execute.")
        log_external_write(tool=tool, destination=destination, payload_preview=preview, confirmed=False)
        return None

    log_external_write(tool=tool, destination=destination, payload_preview=preview, confirmed=True)
    if execute is None:
        return None
    return execute()
