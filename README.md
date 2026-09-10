# Which instrument, for which construct? (Paper 1B) — replication package

Replication materials for:

> *Which Instrument, for Which Construct? Human-anchored adjudication of three text-derived measures of the same psychological constructs, on 706,921 documents.*

This repository covers **Paper 1B only** (dictionary vs encoder vs NLI vs a zero-shot generative LLM, against a 10-coder gold standard). The sealed-window intention → behaviour test is Paper 1A:

- Code/data: https://github.com/occbuu/sealed-window-tpb
- Archive: https://doi.org/10.5281/zenodo.22274705

## What is in this package

| Path | Contents |
|---|---|
| `data/gold_frame.csv` | 532 gold-eligible documents: human labels, dictionary/encoder/NLI/LLM scores, length band. **No review text.** Document IDs are salted SHA-256 prefixes |
| `data/annotations_long.csv` | Coder-level presence labels (anonymised `coder_01`…`coder_10`). No text |
| `data/llm_labels.csv` | Zero-shot Qwen3.8-27B labels (Groq, 10 September 2026) |
| `data/table5_snippets.csv` | De-identified Table 5 excerpts (`[Host]` substituted) |
| `tables/` | Manuscript CSV sources (reliability, agreement, adjudication, word-budget, LLM, protocol) |
| `src/tpb_lexicon.py` | Published regular-expression dictionary |
| `src/reproduce_tables.py` | Recomputes Table 3 and Table 7 from `gold_frame.csv` |
| `src/llm_zeroshot.py` | Frozen Groq protocol (needs `GROQ_API_KEY` **and** `data/private_texts.csv`; texts are not in this repo) |
| `codebook/appendix_A.md` | Annotation codebook |

Raw Inside Airbnb reviews and the 599-document source texts are **not** distributed. Inside Airbnb files remain available at [insideairbnb.com/get-the-data](https://insideairbnb.com/get-the-data/) under CC BY 4.0.

## Reproduce reported gold-standard tables

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
python src/reproduce_tables.py
```

This recomputes Table 3 (AUC, precision, recall, F1 vs the human reference) and Table 7 (length-stratified SN–BI rank correlations) from `data/gold_frame.csv`. It does not re-download reviews or call an LLM.

Table 4 in the manuscript is an **annotation-level** coder-bootstrap estimand (302 / 829 disagreement annotations). The CSV in `tables/table_gold_adjudication.csv` is the reported table. A simpler document-level disagreement share can be computed from `gold_frame.csv` but is not the same estimand.

## Generative LLM protocol (already run)

- Model: `qwen/qwen3.8-27b` on Groq, 10 September 2026, temperature 0
- Prompt: Appendix A codebook only (no human labels, no dictionary/NLI scores)
- 593 of 599 sampled documents labelled before the provider token cap; **all 532 gold-eligible documents are complete**
- This gold sample is **not** a fresh hold-out
- This is **not** GPT-4o

To recode locally you need review text that this package deliberately omits, plus `GROQ_API_KEY`. Do not commit API keys.

## Mint a DOI (Zenodo)

1. Push this folder to a **public** GitHub repository (do not upload review text or `.env` keys).
2. Sign in to [Zenodo](https://zenodo.org) with GitHub and enable the repository.
3. Create a GitHub Release (e.g. `v1.0.0`).
4. Paste the Zenodo DOI into the manuscript data-availability statement.

## Licence

- Code: MIT (`LICENSE`).
- Labels and scores: derived from Inside Airbnb reviews (CC BY 4.0). Retain that attribution.
- We do not redistribute review text.

## Headline numbers this package supports

- Reliability (shared 100 documents, 10 coders): BI α = 0.873; SN α = 0.736; PBC 0.438; SAT 0.267; ATT 0.147.
- Table 3, revisit intention: dictionary AUC 0.747 / NLI 0.951 / LLM 0.940.
- Table 3, subjective norm: dictionary AUC 0.828 / NLI 0.813 / LLM 0.911; NLI prevalence 0.808 vs human 0.265 vs LLM 0.393.
- Human SN–BI association stays negative at every length band (Table 7); it does not show the dictionary's length attenuation.
