"""Approved tool definitions for Gemma function calling."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ToolCall:
    name: str
    arguments: dict[str, Any]


APPROVED_TOOLS = {
    "save_stock_report",
    "calculate_stock_risk",
    "find_transfer_options",
    "draft_handoff_message",
}
