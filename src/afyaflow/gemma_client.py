"""Gemma adapter boundary for structured extraction and tool calling."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from .extraction import build_extraction_prompt, extract_with_rules, parse_stock_report_payload
from .schemas import SourceType, StockReport


@dataclass(frozen=True, slots=True)
class GemmaResponse:
    """Normalized model response."""

    text: str
    raw: dict[str, Any]


class ModelRuntime(Protocol):
    """Protocol implemented by real Gemma runtimes."""

    def generate_json(self, prompt: str) -> dict[str, Any]:
        """Generate one JSON-compatible object from a prompt."""


class GemmaClient:
    """Adapter boundary for the selected Gemma runtime.

    If no runtime is provided, the client uses deterministic fallback extraction
    so tests and demos can run without network access or model weights.
    """

    def __init__(self, model_name: str, runtime: ModelRuntime | None = None) -> None:
        self.model_name = model_name
        self.runtime = runtime

    def extract_stock_report(self, raw_input: str, source_type: SourceType = "text") -> StockReport:
        """Extract a validated StockReport from unstructured input."""

        if self.runtime is None:
            return extract_with_rules(raw_input, source_type=source_type)
        prompt = build_extraction_prompt(raw_input, source_type)
        payload = self.runtime.generate_json(prompt)
        payload.setdefault("source_type", source_type)
        return parse_stock_report_payload(payload)

    def extract(self, prompt: str) -> GemmaResponse:
        """Legacy text generation boundary retained for notebook experiments."""

        if self.runtime is None:
            return GemmaResponse(text=prompt, raw={"mode": "fallback"})
        payload = self.runtime.generate_json(prompt)
        return GemmaResponse(text=str(payload), raw=payload)
