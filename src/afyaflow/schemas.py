"""Typed contracts for extracted stock reports and risk results."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Literal


RiskLevel = Literal["green", "amber", "red"]
SourceType = Literal["text", "image", "audio"]


@dataclass(frozen=True, slots=True)
class StockReport:
    facility: str
    item: str
    balance_units: int
    average_daily_use: int
    expiry_date: date | None
    report_date: date
    source_type: SourceType
    source_language: str
    confidence: float
    notes: str = ""


@dataclass(frozen=True, slots=True)
class StockRisk:
    days_of_stock: float
    level: RiskLevel
    reason: str
    transfer_rank: list[str] = field(default_factory=list)
