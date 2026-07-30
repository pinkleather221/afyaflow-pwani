# Notebooks

Judged Kaggle notebook: `afyaflow_gemma_demo.ipynb`

## How this notebook is meant to run on Kaggle

This notebook is **self-contained**. Link it from GitHub in Kaggle (notebook file only). You do **not** need to clone the full repository.

### Required Kaggle settings

1. Accelerator: **GPU**
2. Add Input: **Keras Gemma 4** model (`gemma4` / V2)
3. Internet: On (only for `pip install keras-hub`)
4. Run All

### What it does

- Embeds AfyaFlow schemas, risk engine, transfer ranking, and handoff logic
- Loads your attached Gemma 4 preset from `/kaggle/input`
- Extracts structured stock reports with Gemma
- Computes deterministic risk + transfer recommendation + Swahili handoff
