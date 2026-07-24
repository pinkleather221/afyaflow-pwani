# AfyaFlow Pwani

AfyaFlow Pwani is an offline-first Gemma 4 assistant that turns multilingual
text, short voice reports, and photographed stock cards into verified medicine
inventory records, early stock-out warnings, and explainable resource-redistribution
recommendations for primary and community health centres.

**Competition:** [Build with Gemma Pwani](https://www.kaggle.com/competitions/build-with-gemma-gdg-pwani)
**Track:** 3 — Smart Health: AI-Driven Health Center & Supply Chain Management

---

## Problem

PHCs and CHCs in coastal Kenya report stock levels via paper cards and short
WhatsApp messages in mixed English/Swahili. Shortages become visible to district
supply chains only after patients have been turned away. AfyaFlow Pwani closes
that gap.

## Pipeline

```
Multilingual input (text / image / audio)
          |
          v
   Gemma 4 Extraction              <-- structured field extraction
          |  (fallback: deterministic rules, no GPU needed)
          v
   Human Confirmation               <-- editable fields, explicit confirm
          |
          v
   Stock-Risk Engine                <-- green / amber / red (deterministic)
          |  + patient footfall demand adjustment
          v
   Transfer Ranking                 <-- nearby surplus facilities, closest-first
          |
          v
   Bilingual Handoff (EN / SW)     <-- administrator alert message
          |
          v
   Audit Log (JSONL)               <-- append-only, pre-action record
```

## Key Numbers (Frozen Benchmark)

| Metric | Score |
|---|---|
| Extraction accuracy (20 cases) | **95.0%** |
| Risk classification accuracy | **100.0%** |
| Latency per case (CPU, fallback) | **< 1 ms** |
| Test suite | **26 passing** |

## Safety

- Synthetic data only — no real patient records or facility credentials.
- Human confirmation required before every inventory action.
- Risk arithmetic is deterministic, transparent, and fully unit-tested.
- Gemma outputs are schema-validated; unapproved tool calls are blocked.
- Prototype thresholds are documented as assumptions, not policy.

## Development Setup

The full Gemma stack targets Python 3.11–3.13 to match Kaggle runtimes and
current ML-library support.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux / macOS:
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest
```

Install application and model dependencies when needed:

```bash
python -m pip install -e ".[app,gemma,dev]"
python -m streamlit run app/main.py
```

Copy `.env.example` to `.env` for local configuration. Never commit secrets
or Kaggle credentials.

## Running the Benchmark

```bash
python -m pytest tests/test_evaluation.py -v
python -m afyaflow.evaluation
```

## Repository Layout

```text
app/                    Interactive Streamlit application
src/afyaflow/           Domain and Gemma integration package
  extraction.py         Extraction prompt builder and fallback rules
  risk_engine.py        Deterministic stock-risk and transfer ranking
  tool_registry.py      Approved tool allowlist and execution
  evaluation.py         Frozen 20-case synthetic benchmark
  workflow.py           End-to-end orchestration
data/synthetic/         Public synthetic demonstration data
  evaluation_cases.json 20-case frozen benchmark (hand-labelled)
  facility_inventory.json 7 synthetic PHC/CHC inventory records
  stock_reports.json    3 golden example reports
notebooks/              Reproducible Kaggle notebook (Gemma 4 GPU demo)
tests/                  26 unit and benchmark tests
docs/                   Architecture, evaluation, safety, and write-up
```

## Scope

The prototype solves one operational workflow well:

- **In scope:** medicine stock levels, test-kit availability, patient footfall
  as a demand signal, bilateral EN/SW handoff messages.
- **Out of scope for this sprint:** bed availability, clinician attendance,
  diagnosis, prescribing, patient records.

## License

Code is released under the Apache License 2.0. Model weights and external
datasets remain subject to their respective licenses and terms.
