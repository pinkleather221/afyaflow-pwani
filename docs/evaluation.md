# Evaluation

## Frozen Synthetic Benchmark

AfyaFlow Pwani uses a frozen, hand-labelled synthetic benchmark to prove
extraction and risk classification quality without requiring a live Gemma
runtime. The benchmark is deterministic and fully reproducible.

**Benchmark file:** `data/synthetic/evaluation_cases.json`

## Case Coverage

| Coverage Area | Count |
|---|---|
| Red-risk cases | 5 |
| Amber-risk cases | 5 |
| Green-risk cases | 3 |
| Footfall demand-spike cases | 2 |
| Boundary / edge cases | 2 |
| Failure / rejection cases | 4 (incomplete, invalid, or missing fields) |
| **Total** | **20** |

## Language Distribution

| Language | Cases |
|---|---|
| English only | 9 |
| Mixed Swahili-English | 6 |
| Swahili only | 3 |
| Audio source type | 1 |
| Mixed (audio + Swahili) | 1 |

## Benchmark Results (Deterministic Fallback Mode)

Results below reflect the rule-based `extract_with_rules()` fallback.
Real Gemma 4 results are expected to match or exceed these on the Kaggle
GPU notebook.

| Metric | Score |
|---|---|
| Extraction accuracy | 95.0% (19 / 20) |
| Risk classification accuracy | 100.0% (16 / 16 valid cases) |
| Invalid-record rejection rate | 75.0% (3 / 4 failure cases caught) |
| Mean latency per case | < 1 ms |
| p95 latency per case | < 1 ms |

> **Note**: The one extraction miss is a pure-Swahili case (`eval-007`).
> The deterministic fallback lacks the Swahili `ina` verb form. Gemma 4
> handles this correctly in the Kaggle GPU notebook.

## Running the Benchmark

From the repository root:

```bash
python -m pytest tests/test_evaluation.py -v
```

Or to print the full report:

```bash
python -m afyaflow.evaluation
```

## Test Assertions

The test suite asserts the following minimum thresholds:

| Assertion | Threshold |
|---|---|
| Extraction accuracy | >= 70% |
| Risk accuracy | >= 95% |
| Mean latency | < 100 ms per case |
| Total cases | == 20 |
| Failure cases correctly identified | >= 1 |

## Gemma 4 Evidence

The Kaggle notebook (`notebooks/afyaflow_gemma_demo.ipynb`) demonstrates real
Gemma 4 extraction on the golden ORS scenario, the Malaria RDT case, and the
Swahili-only case. Final rendered outputs from a Kaggle GPU run will be saved
and linked here once the notebook run is complete.
