from datetime import date

from afyaflow.risk_engine import calculate_stock_risk
from afyaflow.schemas import StockReport


def test_calculate_stock_risk_red() -> None:
    report = StockReport(
        facility="Old Town Health Centre",
        item="ORS sachets",
        balance_units=12,
        average_daily_use=6,
        expiry_date=date(2026, 10, 31),
        report_date=date(2026, 7, 31),
        source_type="text",
        source_language="sw",
        confidence=0.93,
    )
    risk = calculate_stock_risk(report)
    assert risk.level == "red"
    assert risk.days_of_stock == 2
