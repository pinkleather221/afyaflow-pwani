# Notebooks

Judged Kaggle notebook: `afyaflow_gemma_demo.ipynb`

## Kaggle run checklist

1. Accelerator: GPU.
2. Add the Keras Gemma 4 model Input (`gemma4` V2 preset files).
3. Clone or attach this repository so `src/afyaflow` is available.
4. Run all cells top-to-bottom.

The notebook loads the attached local preset with `Gemma4CausalLM.from_preset`, extracts structured stock reports through `GemmaClient`, then runs deterministic risk, approved tools, and bilingual handoff.
