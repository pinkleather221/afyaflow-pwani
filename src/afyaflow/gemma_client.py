"""Minimal Gemma adapter placeholder for structured extraction and tool calling."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GemmaResponse:
    text: str
    raw: dict


class GemmaClient:
    """Adapter boundary for the selected Gemma runtime."""

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    def extract(self, prompt: str) -> GemmaResponse:
        raise NotImplementedError("Gemma runtime integration will be added in the next milestone.")
