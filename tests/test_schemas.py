from datetime import date

import pytest

from afyaflow.schemas import FacilityInventory, StockReport


def test_stock_report_rejects_negative_balance() -> None:
    with pytest.raises(ValueError, match="balance_units"):
        StockReport(
            facility="Old Town Health Centre",
            item="ORS sachets",
            balance_units=-1,
            average_daily_use=6,
            expiry_date=date(2026, 10, 31),
            report_date=date(2026, 7, 31),
            source_type="text",
            source_language="sw",
            confidence=0.9,
        )


def test_facility_inventory_rejects_invalid_level() -> None:
    with pytest.raises(ValueError, match="level"):
        FacilityInventory(
            facility="Demo Facility",
            level="hospital",  # type: ignore[arg-type]
            county="Mombasa",
            item="ORS sachets",
            balance_units=20,
            average_daily_use=3,
            distance_km=2.0,
        )
