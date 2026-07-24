"""Audit helpers for traceable prototype actions."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


def append_audit_event(path: str | Path, event: dict[str, Any]) -> None:
    """Append one JSONL audit event."""

    payload = dict(event)
    payload.setdefault("timestamp_utc", datetime.now(timezone.utc).isoformat())
    if is_dataclass(payload.get("record")):
        payload["record"] = asdict(payload["record"])
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")
