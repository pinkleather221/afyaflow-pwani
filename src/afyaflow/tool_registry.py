"""Approved tool definitions and execution for Gemma function calling."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .risk_engine import calculate_stock_risk_with_transfers, rank_transfer_options
from .schemas import FacilityInventory, StockReport, StockRisk, TransferOption


@dataclass(frozen=True, slots=True)
class ToolCall:
    name: str
    arguments: dict[str, Any]


APPROVED_TOOLS = {
    "calculate_stock_risk",
    "find_transfer_options",
    "draft_handoff_message",
}


def validate_tool_call(call: ToolCall) -> None:
    """Reject unapproved tool calls before execution."""

    if call.name not in APPROVED_TOOLS:
        raise ValueError(f"Unapproved tool call: {call.name}")


def execute_tool_call(
    call: ToolCall,
    report: StockReport,
    inventory: list[FacilityInventory],
) -> StockRisk | list[TransferOption] | str:
    """Execute one approved deterministic tool call."""

    validate_tool_call(call)
    if call.name == "calculate_stock_risk":
        return calculate_stock_risk_with_transfers(report, inventory)
    if call.name == "find_transfer_options":
        limit = int(call.arguments.get("max_options", 3))
        return rank_transfer_options(report, inventory, max_options=limit)
    if call.name == "draft_handoff_message":
        language = str(call.arguments.get("language", "en"))
        risk = calculate_stock_risk_with_transfers(report, inventory)
        first_option = risk.transfer_rank[0] if risk.transfer_rank else None
        if language.startswith("sw"):
            destination = first_option.facility if first_option else "ghala ya kaunti"
            return (
                f"Tahadhari: {report.facility} ina {report.balance_units} za {report.item}, "
                f"takriban siku {risk.days_of_stock}. Tafadhali hakiki na panga usaidizi "
                f"kutoka {destination}."
            )
        destination = first_option.facility if first_option else "the district store"
        return (
            f"Alert: {report.facility} has {report.balance_units} {report.item} remaining, "
            f"about {risk.days_of_stock} days of stock. Please verify and coordinate support "
            f"from {destination}."
        )
    raise AssertionError("unreachable approved tool branch")
