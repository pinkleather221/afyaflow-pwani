# Architecture

AfyaFlow Pwani uses a small, testable pipeline:

1. Multilingual text, image, or audio input.
2. Gemma 4 extraction into a strict stock-report schema.
3. Human confirmation of extracted fields.
4. Deterministic stock-risk calculation.
5. Approved tool calling for save, risk, transfer, and handoff actions.
6. Audited alert output for the judge demo.
