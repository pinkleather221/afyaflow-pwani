"""Load public synthetic scenarios for tests, notebooks, and demos."""

from __future__ import annotations

from datetime import date
import json
from pathlib import Path
from typing import Any

from .schemas import FacilityInventory, StockReport


def _parse_date(value: str | None) -> date | None:
    if value in {None, ""}:
        return None
    return date.fromisoformat(value)


def load_facility_inventory(path: str | Path) -> list[FacilityInventory]:
    """Load synthetic inventory records from JSON."""

    records = json.loads(Path(path).read_text(encoding="utf-8"))
    return [FacilityInventory(**record) for record in records]


def stock_report_from_expected(example: dict[str, Any], confidence: float = 0.9) -> StockReport:
    """Build a StockReport from a synthetic expected-output example."""

    expected = example["expected"]
    return StockReport(
        facility=expected["facility"],
        item=expected["item"],
        balance_units=expected["balance_units"],
        average_daily_use=expected["average_daily_use"],
        expiry_date=_parse_date(expected.get("expiry_date")),
        report_date=_parse_date(expected["report_date"]),
        source_type=example["source_type"],
        source_language=example["source_language"],
        confidence=confidence,
        patient_footfall_today=expected.get("patient_footfall_today"),
    )


def load_stock_report_examples(path: str | Path) -> list[dict[str, Any]]:
    """Load synthetic stock-report examples from JSON."""

    return json.loads(Path(path).read_text(encoding="utf-8"))
