import pytest

from afyaflow.extraction import ExtractionError, build_extraction_prompt, extract_with_rules
from afyaflow.gemma_client import GemmaClient


def test_build_extraction_prompt_requires_strict_json() -> None:
    prompt = build_extraction_prompt("Old Town Health Centre has 12 ORS sachets", "text")
    assert "strict JSON" in prompt
    assert "Do not invent patient data" in prompt


def test_rule_fallback_extracts_multilingual_stock_report() -> None:
    report = extract_with_rules(
        "Old Town Health Centre tuko na ORS sachets 12 tu, matumizi ni 6 kwa siku."
    )
    assert report.facility == "Old Town Health Centre"
    assert report.item == "ORS sachets"
    assert report.balance_units == 12
    assert report.average_daily_use == 6
    assert report.source_language == "sw-en"


def test_rule_fallback_rejects_incomplete_report() -> None:
    with pytest.raises(ExtractionError):
        extract_with_rules("We are running low today")


def test_gemma_client_uses_fallback_without_runtime() -> None:
    client = GemmaClient("google/gemma-4-E2B-it")
    report = client.extract_stock_report(
        "Likoni Community Health Centre has 28 malaria RDT kits and uses 12 per day."
    )
    assert report.item == "Malaria RDT kits"
    assert report.balance_units == 28
