"""Structured extraction helpers for Gemma and local fallback modes."""

from __future__ import annotations

from datetime import date
import re
from typing import Any

from .schemas import SourceType, StockReport


class ExtractionError(ValueError):
    """Raised when unstructured input cannot be converted into a valid report."""


ITEM_PATTERNS = {
    "ORS sachets": re.compile(r"\b(?:ors|oral rehydration)\b", re.IGNORECASE),
    "Malaria RDT kits": re.compile(r"\b(?:malaria\s+rdt|rdt kits?|rapid diagnostic)\b", re.IGNORECASE),
    "Amoxicillin 250mg capsules": re.compile(r"\b(?:amoxicillin|amox)\b", re.IGNORECASE),
}

FACILITY_PATTERNS = [
    "Old Town Health Centre",
    "Likoni Community Health Centre",
    "Mtwapa Health Centre",
    "Tudor Community Health Centre",
    "Kisauni Primary Health Centre",
    "Changamwe Primary Health Centre",
    "Kilifi County Referral Outpatient Store",
]


def build_extraction_prompt(raw_input: str, source_type: SourceType) -> str:
    """Build a concise extraction prompt for Gemma 4."""

    return f"""You are AfyaFlow Pwani, a stock-report extraction assistant.
Extract only inventory-management facts from the user's {source_type} input.
Return strict JSON with these keys:
facility, item, balance_units, average_daily_use, expiry_date, report_date,
source_type, source_language, confidence, patient_footfall_today, notes.
Use null when a field is absent. Do not invent patient data or clinical advice.

Input:
{raw_input}
""".strip()


def parse_stock_report_payload(payload: dict[str, Any]) -> StockReport:
    """Validate a model-produced payload as a StockReport."""

    def parse_optional_date(value: str | None) -> date | None:
        if value in {None, ""}:
            return None
        return date.fromisoformat(str(value))

    try:
        return StockReport(
            facility=str(payload["facility"]),
            item=str(payload["item"]),
            balance_units=int(payload["balance_units"]),
            average_daily_use=int(payload["average_daily_use"]),
            expiry_date=parse_optional_date(payload.get("expiry_date")),
            report_date=date.fromisoformat(str(payload["report_date"])),
            source_type=payload.get("source_type", "text"),
            source_language=str(payload.get("source_language", "unknown")),
            confidence=float(payload.get("confidence", 0.0)),
            patient_footfall_today=(
                None
                if payload.get("patient_footfall_today") in {None, ""}
                else int(payload["patient_footfall_today"])
            ),
            notes=str(payload.get("notes", "")),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise ExtractionError(f"Invalid stock-report payload: {exc}") from exc


def extract_with_rules(raw_input: str, source_type: SourceType = "text") -> StockReport:
    """Extract a StockReport with deterministic rules for local tests and fallback demos.

    This is not a replacement for Gemma. It gives the application a safe offline
    path and lets tests run without downloading model weights.
    """

    lower = raw_input.lower()
    facility = next((name for name in FACILITY_PATTERNS if name.lower() in lower), "")
    item = next((name for name, pattern in ITEM_PATTERNS.items() if pattern.search(raw_input)), "")
    numbers = [int(match) for match in re.findall(r"\b\d+\b", raw_input)]
    balance = numbers[0] if numbers else None
    daily_use = numbers[1] if len(numbers) > 1 else None

    if not facility or not item or balance is None or daily_use is None:
        raise ExtractionError("Missing facility, item, balance, or daily-use value")

    language = "sw-en" if any(word in lower for word in {"tuko", "matumizi", "kwa siku"}) else "en"
    payload = {
        "facility": facility,
        "item": item,
        "balance_units": balance,
        "average_daily_use": daily_use,
        "expiry_date": None,
        "report_date": "2026-07-31",
        "source_type": source_type,
        "source_language": language,
        "confidence": 0.72,
        "patient_footfall_today": None,
        "notes": "Extracted by deterministic fallback rules.",
    }
    return parse_stock_report_payload(payload)
