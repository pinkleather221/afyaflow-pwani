"""End-to-end report-to-alert workflow orchestration."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from .audit import append_audit_event
from .data_loader import load_facility_inventory
from .gemma_client import GemmaClient
from .schemas import SourceType, StockReport, StockRisk
from .tool_registry import ToolCall, execute_tool_call


def run_report_workflow(
    raw_input: str,
    *,
    source_type: SourceType = "text",
    model_name: str = "google/gemma-4-E2B-it",
    inventory_path: str | Path = "data/synthetic/facility_inventory.json",
    audit_path: str | Path | None = None,
    handoff_language: str = "en",
) -> dict[str, Any]:
    """Run the complete extraction, risk, transfer, handoff, and audit workflow."""

    client = GemmaClient(model_name)
    report = client.extract_stock_report(raw_input, source_type=source_type)
    inventory = load_facility_inventory(inventory_path)
    risk = execute_tool_call(ToolCall(name="calculate_stock_risk", arguments={}), report, inventory)
    handoff = execute_tool_call(
        ToolCall(name="draft_handoff_message", arguments={"language": handoff_language}),
        report,
        inventory,
    )
    if not isinstance(risk, StockRisk):
        raise TypeError("calculate_stock_risk returned an unexpected result")
    if not isinstance(handoff, str):
        raise TypeError("draft_handoff_message returned an unexpected result")

    result = {
        "report": report,
        "risk": risk,
        "handoff": handoff,
        "model_name": model_name,
        "source_type": source_type,
    }
    if audit_path is not None:
        append_audit_event(
            audit_path,
            {
                "event": "workflow_completed",
                "model_name": model_name,
                "source_type": source_type,
                "report": _safe_dataclass(report),
                "risk": _safe_dataclass(risk),
                "handoff": handoff,
            },
        )
    return result


def _safe_dataclass(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    return value
