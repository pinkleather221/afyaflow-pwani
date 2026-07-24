# Architecture

AfyaFlow Pwani implements a small, auditable, testable pipeline that converts
unstructured multilingual facility reports into explainable stock-out warnings
and redistribution recommendations. Every stage is independently testable and
deterministic where Gemma is not involved.

## Pipeline Overview

```
Raw Input (text / image / audio)
        |
        v
[1] Gemma 4 Extraction
        |  build_extraction_prompt() -> GemmaClient.extract_stock_report()
        |  Fallback: extract_with_rules() (offline, deterministic)
        v
[2] Schema Validation
        |  StockReport dataclass (frozen, validated)
        v
[3] Human Confirmation
        |  Streamlit UI: editable fields, requires explicit confirm
        v
[4] Deterministic Risk Engine
        |  calculate_stock_risk() -> StockRisk (green / amber / red)
        |  Optional: estimate_adjusted_daily_use() with patient footfall
        v
[5] Approved Tool Registry
        |  calculate_stock_risk  -> StockRisk
        |  find_transfer_options -> list[TransferOption]
        |  draft_handoff_message -> bilingual str (EN / SW)
        v
[6] JSONL Audit Log
        |  append_audit_event() -> immutable append-only log
        v
[7] Administrator Handoff
        Bilingual alert with facility, item, days-of-stock, transfer source
```

## Modules

| Module | Responsibility |
|---|---|
| `schemas.py` | Typed, validated dataclasses for all domain objects |
| `extraction.py` | Prompt builder, JSON parser, deterministic fallback |
| `gemma_client.py` | Thin boundary around the Gemma 4 model (or offline stub) |
| `risk_engine.py` | Deterministic stock-risk and redistribution ranking |
| `tool_registry.py` | Allowlist-gated tool execution for Gemma function calls |
| `data_loader.py` | Loads synthetic facility inventory and stock-report examples |
| `audit.py` | Append-only JSONL audit event recorder |
| `workflow.py` | End-to-end orchestration of all pipeline stages |
| `evaluation.py` | Frozen 20-case synthetic benchmark with accuracy and latency metrics |

## Data Flow and Boundaries

```
Public synthetic data only
        |
        v
  GemmaClient (model boundary)
        |   Only approved tool calls are allowed.
        |   All outputs are schema-validated before use.
        v
  Human-in-the-loop confirmation
        |   No inventory action fires without explicit confirm.
        v
  Deterministic arithmetic
        |   Risk and transfer ranking are rule-based, not model-generated.
        v
  Audit log
        |   Every workflow event is recorded before handoff.
        v
  Administrator handoff (EN/SW)
```

## Gemma 4 Role

Gemma 4 is used for **one** purpose: structured field extraction from
multilingual, multimodal input. It does not perform clinical reasoning,
prescribe, diagnose, or generate inventory commands. All numeric risk
calculations and transfer rankings are deterministic Python functions.

When Gemma is unavailable (local development, offline mode), the
`extract_with_rules()` fallback covers the same domain with deterministic
regular expressions, allowing all tests to run without a GPU.

## Deployment Targets

| Target | Gemma Mode | Notes |
|---|---|---|
| Kaggle GPU notebook | Real Gemma 4 inference | Primary judged demo |
| Local Python 3.11-3.13 | Fallback rules | Full tests, Streamlit app |
| Local Python 3.14 | Fallback rules | Tests only (ML deps unsupported) |

## Evaluation

The frozen synthetic benchmark (`data/synthetic/evaluation_cases.json`)
contains 20 hand-labelled cases covering English, Swahili, mixed-language,
incomplete, invalid, and edge inputs. See `docs/evaluation.md` for metrics.
