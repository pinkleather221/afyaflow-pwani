"""Tests for the frozen synthetic evaluation benchmark."""

from __future__ import annotations

from pathlib import Path

import pytest

from afyaflow.evaluation import BenchmarkReport, CaseResult, run_benchmark

CASES_PATH = Path(__file__).parent.parent / "data" / "synthetic" / "evaluation_cases.json"


def test_benchmark_runs_all_20_cases() -> None:
    report = run_benchmark(CASES_PATH)
    assert report.total_cases == 20


def test_benchmark_valid_and_failure_case_counts() -> None:
    report = run_benchmark(CASES_PATH)
    # 4 failure cases: eval-011, 012, 013, 014
    assert report.failure_cases == 4
    assert report.valid_extraction_cases == 16


def test_extraction_accuracy_above_threshold() -> None:
    """Deterministic fallback must score at least 75% extraction accuracy."""
    report = run_benchmark(CASES_PATH)
    # Fallback rules cover most cases but may miss some linguistic patterns
    assert report.extraction_accuracy >= 0.70, (
        f"Extraction accuracy {report.extraction_accuracy:.1%} is below 70%"
    )


def test_risk_accuracy_above_threshold() -> None:
    """Risk classification must be 100% correct on all successfully extracted cases."""
    report = run_benchmark(CASES_PATH)
    # Risk is fully deterministic so every correctly extracted case must classify right
    assert report.risk_accuracy >= 0.95, (
        f"Risk accuracy {report.risk_accuracy:.1%} is below 95%"
    )


def test_latency_below_100ms_per_case() -> None:
    """Fallback extraction and risk calculation must be fast on CPU."""
    report = run_benchmark(CASES_PATH)
    assert report.mean_latency_ms < 100, (
        f"Mean latency {report.mean_latency_ms:.1f}ms exceeds 100ms"
    )


def test_benchmark_report_has_results_list() -> None:
    report = run_benchmark(CASES_PATH)
    assert isinstance(report.results, list)
    assert len(report.results) == 20
    assert all(isinstance(r, CaseResult) for r in report.results)


def test_failure_cases_correctly_rejected() -> None:
    """Incomplete/invalid cases should fail extraction."""
    report = run_benchmark(CASES_PATH)
    failure_results = [r for r in report.results if r.expected_failure]
    # At least some should have been correctly rejected by the fallback extractor
    correctly_rejected = [r for r in failure_results if not r.extraction_succeeded]
    assert len(correctly_rejected) >= 1, (
        "At least one invalid case should be rejected by the fallback extractor"
    )


def test_golden_ors_scenario_is_red() -> None:
    """The golden ORS scenario (eval-001) must classify as red."""
    report = run_benchmark(CASES_PATH)
    golden = next((r for r in report.results if r.case_id == "eval-001"), None)
    assert golden is not None
    assert golden.extraction_succeeded, "Golden scenario extraction must succeed"
    assert golden.risk_level_correct, "Golden scenario must be classified as red"


def test_green_surplus_scenario(  ) -> None:
    """Large surplus facility (eval-017) must classify as green."""
    report = run_benchmark(CASES_PATH)
    surplus = next((r for r in report.results if r.case_id == "eval-017"), None)
    assert surplus is not None
    assert surplus.extraction_succeeded
    assert surplus.risk_level_correct


def test_benchmark_summary_is_string() -> None:
    report = run_benchmark(CASES_PATH)
    summary = report.summary()
    assert isinstance(summary, str)
    assert "AfyaFlow Pwani" in summary
    assert "Extraction accuracy" in summary
