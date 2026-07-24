"""Configuration helpers for AfyaFlow Pwani."""

from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True, slots=True)
class Settings:
    """Runtime settings loaded from environment variables."""

    gemma_model: str = os.getenv("AFYAFLOW_GEMMA_MODEL", "google/gemma-4-E2B-it")
    device: str = os.getenv("AFYAFLOW_DEVICE", "auto")
    data_dir: str = os.getenv("AFYAFLOW_DATA_DIR", "data/synthetic")
    log_level: str = os.getenv("AFYAFLOW_LOG_LEVEL", "INFO")
    offline_mode: bool = os.getenv("AFYAFLOW_OFFLINE_MODE", "false").lower() == "true"


settings = Settings()
