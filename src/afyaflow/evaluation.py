"""Frozen synthetic benchmark evaluation for AfyaFlow Pwani.

This module scores the fallback extraction and risk classification pipeline
against 20 hand-labelled cases. It is intentionally deterministic so that
results are fully reproducible without a GPU or Gemma runtime.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .data_loader import load_facility_inventory, load_stock_report_examples
from .extraction import ExtractionError, extract_with_rules
from .risk_engine import calculate_stock_risk


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class CaseResult:
    """Outcome of a single evaluation case."""

    case_id: str
    category: str
    source_language: str
    expected_failure: bool
    extraction_succeeded: bool
    risk_level_correct: bool | None
    latency_ms: float
    notes: str
    error: str = ""


@dataclass
class BenchmarkReport:
    """Aggregate metrics for the full evaluation set."""

    total_cases: int
    valid_extraction_cases: int
    failure_cases: int
    extraction_correct: int
    extraction_wrong: int
    risk_correct: int
    risk_wrong: int
    extraction_accuracy: float
    risk_accuracy: float
    mean_latency_ms: float
    p95_latency_ms: float
    results: list[CaseResult] = field(default_factory=list)

    def summary(self) -> str:
        lines = [
            "AfyaFlow Pwani — Frozen Synthetic Benchmark",
            "=" * 48,
            f"Total cases          : {self.total_cases}",
            f"Valid-extraction cases: {self.valid_extraction_cases}",
            f"Failure cases        : {self.failure_cases}",
            "",
            "Extraction accuracy  : "
            f"{self.extraction_accuracy:.1%}  "
            f"({self.extraction_correct}/{self.valid_extraction_cases + self.failure_cases})",
            f"Risk accuracy        : "
            f"{self.risk_accuracy:.1%}  "
            f"({self.risk_correct}/{self.valid_extraction_cases})",
            "",
            f"Mean latency (ms)    : {self.mean_latency_ms:.1f}",
            f"p95  latency (ms)    : {self.p95_latency_ms:.1f}",
        ]
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Field-level scoring helpers
# ---------------------------------------------------------------------------

_RISK_LEVELS = {"red", "amber", "green"}


def _score_risk_level(predicted: str, expected: str) -> bool:
    return predicted.lower() == expected.lower()


# ---------------------------------------------------------------------------
# Single-case runner
# ---------------------------------------------------------------------------


def _run_case(case: dict[str, Any]) -> CaseResult:
    case_id = case["id"]
    category = case.get("category", "")
    source_language = case.get("source_language", "unknown")
    source_type = case.get("source_type", "text")
    raw_input = case["raw_input"]
    expected = case["expected"]
    notes = case.get("notes", "")

    expected_failure = bool(expected.get("extraction_should_fail", False))
    expected_risk = expected.get("risk_level")

    t0 = time.perf_counter()
    try:
        report = extract_with_rules(raw_input, source_type=source_type)
        extraction_succeeded = True
        error_msg = ""
    except ExtractionError as exc:
        extraction_succeeded = False
        report = None
        error_msg = str(exc)
    finally:
        latency_ms = (time.perf_counter() - t0) * 1000

    # Determine risk classification if we have a valid report
    risk_level_correct: bool | None = None
    if extraction_succeeded and report is not None and expected_risk:
        risk = calculate_stock_risk(report)
        risk_level_correct = _score_risk_level(risk.level, expected_risk)

    return CaseResult(
        case_id=case_id,
        category=category,
        source_language=source_language,
        expected_failure=expected_failure,
        extraction_succeeded=extraction_succeeded,
        risk_level_correct=risk_level_correct,
        latency_ms=latency_ms,
        notes=notes,
        error=error_msg,
    )


# ---------------------------------------------------------------------------
# Benchmark runner
# ---------------------------------------------------------------------------


def run_benchmark(
    cases_path: str | Path = "data/synthetic/evaluation_cases.json",
) -> BenchmarkReport:
    """Run the full frozen evaluation set and return aggregate metrics."""

    cases = json.loads(Path(cases_path).read_text(encoding="utf-8"))
    results: list[CaseResult] = [_run_case(c) for c in cases]

    # Extraction accuracy: for failure cases, success = extraction DID fail;
    # for valid cases, success = extraction DID succeed.
    extraction_correct = sum(
        1
        for r in results
        if (r.expected_failure and not r.extraction_succeeded)
        or (not r.expected_failure and r.extraction_succeeded)
    )

    # Risk accuracy: among valid extraction cases that expected a risk level
    risk_scored = [r for r in results if r.risk_level_correct is not None]
    risk_correct = sum(1 for r in risk_scored if r.risk_level_correct)

    valid_cases = [r for r in results if not r.expected_failure]
    failure_cases = [r for r in results if r.expected_failure]

    latencies = sorted(r.latency_ms for r in results)
    mean_latency = sum(latencies) / len(latencies) if latencies else 0.0
    p95_idx = max(0, int(len(latencies) * 0.95) - 1)
    p95_latency = latencies[p95_idx] if latencies else 0.0

    extraction_denom = len(results)
    risk_denom = len(risk_scored) if risk_scored else 1

    return BenchmarkReport(
        total_cases=len(results),
        valid_extraction_cases=len(valid_cases),
        failure_cases=len(failure_cases),
        extraction_correct=extraction_correct,
        extraction_wrong=extraction_denom - extraction_correct,
        risk_correct=risk_correct,
        risk_wrong=len(risk_scored) - risk_correct,
        extraction_accuracy=extraction_correct / extraction_denom,
        risk_accuracy=risk_correct / risk_denom,
        mean_latency_ms=mean_latency,
        p95_latency_ms=p95_latency,
        results=results,
    )


if __name__ == "__main__":
    report = run_benchmark()
    print(report.summary())
    print()
    for r in report.results:
        status = "PASS" if (
            (r.expected_failure and not r.extraction_succeeded)
            or (not r.expected_failure and r.extraction_succeeded)
        ) else "FAIL"
        risk_tag = ""
        if r.risk_level_correct is not None:
            risk_tag = " [risk PASS]" if r.risk_level_correct else " [risk FAIL]"
        print(f"  {status} {r.case_id} ({r.category}){risk_tag}  {r.latency_ms:.1f}ms")
        if r.error:
            print(f"      error: {r.error}")
