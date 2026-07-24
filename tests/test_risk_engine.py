from datetime import date
from pathlib import Path

from afyaflow.data_loader import (
    load_facility_inventory,
    load_stock_report_examples,
    stock_report_from_expected,
)
from afyaflow.risk_engine import (
    calculate_stock_risk,
    calculate_stock_risk_with_transfers,
    rank_transfer_options,
)
from afyaflow.schemas import StockReport

ROOT = Path(__file__).resolve().parents[1]


def make_report(
    *,
    balance_units: int = 12,
    average_daily_use: int = 6,
    patient_footfall_today: int | None = None,
) -> StockReport:
    return StockReport(
        facility="Old Town Health Centre",
        item="ORS sachets",
        balance_units=balance_units,
        average_daily_use=average_daily_use,
        expiry_date=date(2026, 10, 31),
        report_date=date(2026, 7, 31),
        source_type="text",
        source_language="sw",
        confidence=0.93,
        patient_footfall_today=patient_footfall_today,
    )


def test_calculate_stock_risk_red() -> None:
    risk = calculate_stock_risk(make_report())
    assert risk.level == "red"
    assert risk.days_of_stock == 2
    assert risk.adjusted_daily_use == 6


def test_patient_footfall_can_increase_demand_signal() -> None:
    risk = calculate_stock_risk(make_report(balance_units=30, average_daily_use=10, patient_footfall_today=25))
    assert risk.adjusted_daily_use == 13
    assert risk.level == "red"


def test_rank_transfer_options_prefers_nearby_surplus_facility() -> None:
    inventory = load_facility_inventory(ROOT / "data" / "synthetic" / "facility_inventory.json")
    options = rank_transfer_options(make_report(), inventory)
    assert options
    assert options[0].facility == "Tudor Community Health Centre"
    assert options[0].surplus_units > 0


def test_synthetic_examples_match_expected_risk_levels() -> None:
    examples = load_stock_report_examples(ROOT / "data" / "synthetic" / "stock_reports.json")
    for example in examples:
        report = stock_report_from_expected(example)
        risk = calculate_stock_risk_with_transfers(
            report,
            load_facility_inventory(ROOT / "data" / "synthetic" / "facility_inventory.json"),
        )
        assert risk.level == example["expected"]["risk_level"]
