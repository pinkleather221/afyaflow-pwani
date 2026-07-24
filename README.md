# AfyaFlow Pwani

AfyaFlow Pwani is an offline-first Gemma 4 assistant that turns multilingual text, short voice reports, and photographed stock cards into verified medicine inventory records, early stock-out warnings, and explainable resource-redistribution recommendations.

The project targets **Track 3: Smart Health - AI-Driven Health Center & Supply Chain Management** in the [Build with Gemma Pwani](https://www.kaggle.com/competitions/build-with-gemma-gdg-pwani) hackathon.

## Focus

The prototype deliberately solves one operational workflow well:

1. Capture an English or Swahili stock report as text, image, or short audio.
2. Use Gemma 4 to extract a structured inventory record.
3. Require a human to review and confirm extracted fields.
4. Calculate stock risk with deterministic, testable rules.
5. Recommend a transfer from synthetic nearby-facility inventory.
6. Generate a concise bilingual handoff for an administrator.
7. Record an explainable audit event.

Patient footfall is used only as an optional demand signal. Bed availability, clinician attendance, diagnosis, prescribing, and patient records are outside the judged prototype scope.

## Safety and data

- The public demonstration uses synthetic facility and inventory data only.
- AfyaFlow Pwani does not diagnose, prescribe, triage patients, or replace clinical judgment.
- Gemma outputs are schema-validated and require human confirmation before an inventory action.
- Stock-risk arithmetic and transfer ranking are deterministic.
- Prototype thresholds are assumptions until validated against approved health policy.

## Project status

The repository is under active development for the 31 July 2026 competition sprint. The first milestone establishes reproducible packaging, quality checks, and safe contribution boundaries. Domain logic, Gemma integration, the application, evaluation, and Kaggle notebook will be added as independently tested milestones.

## Development setup

The full Gemma stack targets Python 3.11-3.13 to match common Kaggle runtimes and current ML-library support.

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest
ruff check .
ruff format --check .
```

Install application and model dependencies only when needed:

```bash
python -m pip install -e ".[app,gemma,dev]"
```

Copy `.env.example` to `.env` for local configuration. Never commit secrets or Kaggle credentials.

## Repository layout

```text
app/                 Interactive application
src/afyaflow/        Domain and Gemma integration package
data/synthetic/      Public synthetic demonstration data
notebooks/           Reproducible Kaggle notebook
tests/               Unit and integration tests
docs/                Architecture, evaluation, safety, and demo notes
```

## License

Code is released under the Apache License 2.0. Model weights and external datasets remain subject to their respective licenses and terms.
