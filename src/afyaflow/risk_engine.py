"""Deterministic stock-risk logic for AfyaFlow Pwani."""

from __future__ import annotations

from .schemas import StockReport, StockRisk


def calculate_stock_risk(report: StockReport) -> StockRisk:
    """Compute an explainable stock-risk classification."""

    daily_use = max(report.average_daily_use, 1)
    days_of_stock = report.balance_units / daily_use
    if days_of_stock < 3:
        level = "red"
        reason = "Less than 3 days of stock remaining."
    elif days_of_stock < 7:
        level = "amber"
        reason = "Between 3 and 7 days of stock remaining."
    else:
        level = "green"
        reason = "At least 7 days of stock remaining."
    return StockRisk(days_of_stock=days_of_stock, level=level, reason=reason)
