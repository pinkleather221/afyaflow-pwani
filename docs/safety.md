# Safety

## Responsible-AI Boundaries

AfyaFlow Pwani is a logistics-support prototype. It does not diagnose, treat,
prescribe, triage patients, or replace clinical or pharmaceutical judgment.

## Data Boundaries

- The public demonstration uses **synthetic facility and inventory data only**.
- No real patient records, clinical outcomes, or personal health information
  are used, stored, or transmitted at any stage.
- No facility credentials, API secrets, or private configuration are committed
  to the public repository.

## Human-in-the-Loop Requirement

Every extracted report must pass a **human confirmation step** before any
inventory action fires. The Streamlit application presents all Gemma-extracted
fields in editable form and requires explicit user confirmation. Unconfirmed
reports do not proceed through the risk or transfer pipeline.

## Deterministic Safeguards

Stock-risk classification and transfer ranking are computed with **deterministic
Python arithmetic**, not model-generated text. The rules are transparent,
unit-tested, and produce the same output for the same input on every run.

Risk thresholds (3 days → red, 7 days → amber) are **prototype assumptions**
defined in `risk_engine.py`. They are not official health-system policy and
must be validated against approved county health guidelines before any
real-world deployment.

## Gemma Output Constraints

All text produced by Gemma 4 passes through strict schema validation
(`StockReport` dataclass) before use. Gemma is permitted to call only three
approved tools from a fixed allowlist (`APPROVED_TOOLS` in `tool_registry.py`).
Attempts to call unapproved tools raise a `ValueError` and are blocked before
execution.

Gemma outputs are **never** used directly in medical recommendations, clinical
alerts, or supply-chain commands without deterministic re-scoring.

## Audit Trail

Every completed workflow event is recorded to an append-only JSONL audit log.
The log captures the model name, source type, extracted report fields, risk
classification, and handoff message. This supports post-hoc review and error
investigation.

## Offline-First Design

The system functions without a live Gemma runtime using the deterministic
`extract_with_rules()` fallback. Facilities with no network access can still
receive risk classifications and transfer recommendations from the rule-based
path.

## Limitations and Mitigations

| Limitation | Mitigation |
|---|---|
| Synthetic data only | Real deployment requires county-approved supply data |
| Prototype thresholds | Policy team must validate before any live use |
| Fallback rules are narrow | Cover only 3 items and 7 facilities in prototype |
| No real Gemma evaluation on live data | Kaggle GPU notebook provides evidence of real extraction |
| Swahili coverage limited | Identified for review by a fluent Swahili reviewer |
