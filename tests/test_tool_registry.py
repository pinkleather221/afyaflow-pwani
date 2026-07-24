from pathlib import Path

import pytest

from afyaflow.data_loader import load_facility_inventory, load_stock_report_examples, stock_report_from_expected
from afyaflow.schemas import StockRisk, TransferOption
from afyaflow.tool_registry import ToolCall, execute_tool_call, validate_tool_call

ROOT = Path(__file__).resolve().parents[1]


def make_report_and_inventory():
    examples = load_stock_report_examples(ROOT / "data" / "synthetic" / "stock_reports.json")
    report = stock_report_from_expected(examples[0])
    inventory = load_facility_inventory(ROOT / "data" / "synthetic" / "facility_inventory.json")
    return report, inventory


def test_validate_tool_call_rejects_unknown_tool() -> None:
    with pytest.raises(ValueError, match="Unapproved"):
        validate_tool_call(ToolCall(name="delete_inventory", arguments={}))


def test_execute_stock_risk_tool() -> None:
    report, inventory = make_report_and_inventory()
    result = execute_tool_call(ToolCall(name="calculate_stock_risk", arguments={}), report, inventory)
    assert isinstance(result, StockRisk)
    assert result.level == "red"


def test_execute_transfer_tool() -> None:
    report, inventory = make_report_and_inventory()
    result = execute_tool_call(ToolCall(name="find_transfer_options", arguments={"max_options": 1}), report, inventory)
    assert isinstance(result, list)
    assert isinstance(result[0], TransferOption)


def test_execute_handoff_tool_in_swahili() -> None:
    report, inventory = make_report_and_inventory()
    result = execute_tool_call(ToolCall(name="draft_handoff_message", arguments={"language": "sw"}), report, inventory)
    assert isinstance(result, str)
    assert "Tahadhari" in result
    assert report.facility in result
