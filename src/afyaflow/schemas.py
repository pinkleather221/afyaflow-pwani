"""Typed contracts for extracted stock reports and risk results."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Literal


RiskLevel = Literal["green", "amber", "red"]
SourceType = Literal["text", "image", "audio"]
FacilityLevel = Literal["PHC", "CHC"]


@dataclass(frozen=True, slots=True)
class StockReport:
    """A human-confirmed inventory report extracted from unstructured input."""

    facility: str
    item: str
    balance_units: int
    average_daily_use: int
    expiry_date: date | None
    report_date: date
    source_type: SourceType
    source_language: str
    confidence: float
    patient_footfall_today: int | None = None
    notes: str = ""

    def __post_init__(self) -> None:
        if not self.facility.strip():
            raise ValueError("facility is required")
        if not self.item.strip():
            raise ValueError("item is required")
        if self.balance_units < 0:
            raise ValueError("balance_units cannot be negative")
        if self.average_daily_use <= 0:
            raise ValueError("average_daily_use must be greater than zero")
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")
        if self.patient_footfall_today is not None and self.patient_footfall_today < 0:
            raise ValueError("patient_footfall_today cannot be negative")
        if self.source_type not in {"text", "image", "audio"}:
            raise ValueError("source_type must be text, image, or audio")


@dataclass(frozen=True, slots=True)
class FacilityInventory:
    """Synthetic facility inventory used for redistribution recommendations."""

    facility: str
    level: FacilityLevel
    county: str
    item: str
    balance_units: int
    average_daily_use: int
    distance_km: float

    def __post_init__(self) -> None:
        if not self.facility.strip():
            raise ValueError("facility is required")
        if self.level not in {"PHC", "CHC"}:
            raise ValueError("level must be PHC or CHC")
        if not self.item.strip():
            raise ValueError("item is required")
        if self.balance_units < 0:
            raise ValueError("balance_units cannot be negative")
        if self.average_daily_use <= 0:
            raise ValueError("average_daily_use must be greater than zero")
        if self.distance_km < 0:
            raise ValueError("distance_km cannot be negative")


@dataclass(frozen=True, slots=True)
class TransferOption:
    """A candidate redistribution option from a synthetic nearby facility."""

    facility: str
    item: str
    surplus_units: int
    days_of_stock_after_transfer: float
    distance_km: float
    reason: str


@dataclass(frozen=True, slots=True)
class StockRisk:
    """Explainable deterministic risk output."""

    days_of_stock: float
    adjusted_daily_use: int
    level: RiskLevel
    reason: str
    transfer_rank: list[TransferOption] = field(default_factory=list)
