# AfyaFlow Pwani: From Paper Stock Cards to Action in Seconds

## The Problem

Primary and community health centres (PHCs/CHCs) in coastal Kenya face a
preventable operational failure: medicine stock-outs and test-kit shortages
that accumulate invisibly. Facility workers fill in paper stock cards or
send short WhatsApp messages in a mix of English and Swahili. By the time a
shortage becomes visible to the district supply chain, patients have already
been turned away.

The problem is not data — the data exists. The problem is that it arrives
unstructured, multilingual, and siloed.

## The Solution

**AfyaFlow Pwani** uses Gemma 4 to transform that unstructured input into
verified inventory records, deterministic stock-out warnings, and explainable
redistribution recommendations — in seconds, with a human always in the loop.

### Seven-step workflow

1. A health worker submits a stock report as text, a photographed stock card,
   or a short voice message — in English, Swahili, or mixed.
2. **Gemma 4 extracts** a structured inventory record with facility name, item,
   balance units, daily consumption, expiry date, and patient footfall.
3. An administrator reviews all extracted fields in an editable form and
   **confirms before any action fires**.
4. **Deterministic risk arithmetic** classifies the stock as green (≥ 7 days),
   amber (3–7 days), or red (< 3 days).
5. The system **ranks nearby transfer options** from synthetic facility inventory,
   closest-first with a 7-day safety buffer preserved at the donor site.
6. A **bilingual handoff message** (English and Swahili) is generated for the
   district administrator.
7. An **append-only audit event** is recorded before any action.

## Why Gemma 4

Gemma 4 is central, not peripheral:

- **Multilingual**: handles English, Swahili, and code-switched input natively.
- **Multimodal**: supports photographed stock cards as image input.
- **Constrained tool calling**: calls only three pre-approved tools from a
  fixed allowlist; unapproved calls are blocked by `tool_registry.py`.
- **Offline-friendly**: a deterministic fallback covers the same extraction
  domain when no GPU is available, keeping facilities functional.

## Evidence

### Frozen Synthetic Benchmark (Deterministic Fallback Mode)

| Metric | Score |
|---|---|
| Extraction accuracy | **95.0%** (19 / 20 cases) |
| Risk classification accuracy | **100.0%** (16 / 16 valid cases) |
| Mean latency per case | **< 1 ms** (CPU, no model) |
| Invalid-record rejection | **75%** (3 / 4 failure cases caught) |

The benchmark covers 20 hand-labelled cases: English, Swahili, mixed-language,
incomplete, invalid, zero-stock, high-footfall, and boundary inputs.

### Test Suite

- **26 passing tests** covering schemas, extraction, risk engine, tool registry,
  workflow, and the frozen benchmark.
- All tests run offline without model weights.

### Kaggle Notebook

The notebook (`notebooks/afyaflow_gemma_demo.ipynb`) demonstrates real Gemma 4
extraction on the golden ORS scenario, malaria RDT case, and Swahili-only input.
Full rendered outputs from the Kaggle GPU run will be linked here once available.

## Safety

- Synthetic data only in the public demo. No patient records, no real facility
  credentials, no clinical advice.
- Human confirmation required before every inventory action.
- Risk arithmetic is deterministic and fully unit-tested.
- Gemma outputs are schema-validated before use. Unapproved tool calls are
  blocked at the registry boundary.
- Prototype thresholds are explicitly documented as assumptions, not policy.

## Limitations

- The prototype covers three items (ORS sachets, Malaria RDT kits,
  Amoxicillin 250mg capsules) and seven synthetic Mombasa/Kilifi facilities.
- Bed availability, doctor attendance, diagnosis, and patient records are
  deliberately out of scope for this sprint.
- Real deployment requires county-approved supply data and policy validation
  of risk thresholds.

## Repository

**GitHub:** https://github.com/pinkleather221/afyaflow-pwani

**License:** Apache 2.0

**Competition:** Build with Gemma Pwani — Track 3: Smart Health
