# Gold-standard files (no review text)

`doc_id` is `sha256("paper1b-which-instrument-2026|{original_review_id}")[:16]`.
The mapping is not released, so these IDs cannot be joined to Inside Airbnb or to the Paper 1A analytic file.

| File | Unit | Notes |
|---|---|---|
| `gold_frame.csv` | 532 documents | Human majority labels (ties → absent), dictionary hits/presence, encoder scores, NLI scores, LLM scores, length `band`, `n_coders` |
| `annotations_long.csv` | coder × document | Retained 10-coder files only; `flag=1` is uncodeable; annotations faster than 2 seconds were dropped |
| `llm_labels.csv` | document | `qwen/qwen3.8-27b`, Groq, 2026-09-10, zero-shot Appendix A |
| `table5_snippets.csv` | 5 excerpts | Host names replaced by `[Host]` |

Upstream reviews: Inside Airbnb, CC BY 4.0. This package does not redistribute comment strings.
