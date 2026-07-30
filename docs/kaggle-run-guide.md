# Kaggle Notebook and Continuation Guide

This guide explains how to continue AfyaFlow Pwani from the current GitHub state, run the notebook on Kaggle, and prepare the competition submission.

## 1. Current GitHub state

Repository:

- https://github.com/pinkleather221/afyaflow-pwani

Current local validation:

- `python -m pytest` passes with 26 tests.
- The local branch is clean against `origin/main`.
- Synthetic evaluation files are already tracked in the repository.

## 2. What is already working

The repository already includes:

- Public project scaffold.
- Synthetic PHC/CHC facility inventory.
- Synthetic stock-report scenarios.
- Validated stock-report contracts.
- Deterministic stock-risk engine.
- Patient-footfall demand adjustment.
- Transfer recommendation logic.
- Gemma extraction adapter boundary.
- Deterministic fallback extraction for local/offline testing.
- Approved tool registry and safe tool execution.
- Streamlit report-to-alert demo workflow.
- Kaggle-style notebook.
- Frozen synthetic evaluation tests.

## 3. How to run locally

From the repository root:

```bash
cd afyaflow-pwani
python -m pytest
```

If app dependencies are installed, run the demo app:

```bash
python -m streamlit run app/main.py
```

If `streamlit` is not found, install app/dev dependencies:

```bash
python -m pip install --ignore-requires-python -e ".[app,dev]"
```

The `--ignore-requires-python` flag is only for this local machine because it has Python 3.14 while the project targets Kaggle-compatible Python 3.11-3.13.

## 4. How to run the notebook on Kaggle

### Option A: Pull directly from GitHub inside a Kaggle notebook

1. Go to Kaggle.
2. Open **Code**.
3. Create a new notebook.
4. In Notebook settings:
   - Accelerator: GPU.
   - Internet: On, if allowed by the competition.
5. Add this first cell:

```bash
!git clone https://github.com/pinkleather221/afyaflow-pwani.git
%cd afyaflow-pwani
```

6. Add this second cell:

```bash
!python -m pip install -q -e ".[dev]"
!python -m pytest
```

7. Open or copy the cells from:

```text
notebooks/afyaflow_gemma_demo.ipynb
```

8. Run the notebook top-to-bottom.

### Option B: Upload the notebook manually

1. Download or open `notebooks/afyaflow_gemma_demo.ipynb` from GitHub.
2. Upload it to Kaggle as a notebook.
3. Add the GitHub clone cell at the top so the notebook has access to `src/`, `data/`, and tests.
4. Run all cells.

## 5. How to connect real Gemma 4 on Kaggle

The repository uses deterministic fallback extraction locally so tests run without model weights.

On Kaggle GPU, the notebook `notebooks/afyaflow_gemma_demo.ipynb` already wires a live KerasHub runtime:

1. Add the **Keras Gemma 4** model as a notebook Input (for example `gemma4` / V2 with `config.json`, `tokenizer.json`, `model.weights.json`, and `model_*.weights.h5`).
2. Enable **GPU**.
3. Clone or attach the AfyaFlow repository so `src/afyaflow` is available.
4. Run all cells top-to-bottom.

The notebook auto-discovers the preset under `/kaggle/input`, loads it with:

```python
gemma_lm = keras_hub.models.Gemma4CausalLM.from_preset(str(GEMMA_PRESET), dtype="bfloat16")
```

and passes a `KaggleGemmaRuntime` into `GemmaClient` / `run_report_workflow(..., runtime=runtime)`.

Important: keep these safeguards unchanged:

- strict schema validation;
- human confirmation;
- deterministic stock-risk calculations;
- approved tool registry;
- audit trail;
- synthetic data only for public demo.

## 6. What to capture from Kaggle

After running the notebook on Kaggle, save proof of:

- notebook ran top-to-bottom;
- GPU was enabled;
- Gemma model loaded successfully;
- Gemma produced a structured stock report;
- deterministic risk engine produced the alert;
- tool calling or tool simulation produced handoff/transfer output;
- final evaluation table is visible.

Use these outputs in:

- Kaggle write-up;
- demo video;
- final README evidence section;
- pitch deck.

## 7. Remaining steps to completion

### Step 1: Complete real Gemma notebook run

- Run the notebook on Kaggle GPU.
- Add or document real Gemma runtime cell.
- Save outputs.

### Step 2: Finalize evaluation documentation

- Update `docs/evaluation.md` with benchmark results.
- Include field extraction, stock-risk accuracy, invalid-case handling, and end-to-end completion.

### Step 3: Strengthen public docs

Update:

- `README.md`
- `docs/architecture.md`
- `docs/safety.md`
- `docs/demo-script.md`
- `docs/writeup-draft.md`

### Step 4: Record demo video

Recommended flow:

1. Show the problem: paper/voice stock report.
2. Show extraction.
3. Show human confirmation.
4. Show red/amber/green risk.
5. Show transfer recommendation.
6. Show handoff message.
7. Close with the safety boundary.

### Step 5: Prepare Kaggle write-up

The write-up should include:

- title;
- problem story;
- why Track 3;
- why we focused on stock/test availability;
- why Gemma 4 is necessary;
- architecture;
- demo screenshots;
- evaluation table;
- safety and limitations;
- links to GitHub, notebook, and video.

### Step 6: Final submission audit

Before submitting:

- all links open while logged out;
- notebook is public or visible as required;
- GitHub repo is public;
- no secrets are committed;
- no patient data is used;
- write-up status is Submitted, not Draft;
- submission is completed before the internal deadline.

## 8. Suggested next commit after Kaggle run

After real Kaggle execution, use a commit like:

```text
docs(evaluation): add Kaggle Gemma run evidence and benchmark results
```

Commit body should include:

- what notebook was run;
- whether GPU was enabled;
- model used;
- evaluation result summary;
- known limitations.
