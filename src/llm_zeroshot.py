"""Frozen zero-shot protocol from Paper 1B (10 September 2026).

Requires:
  GROQ_API_KEY in the environment
  data/private_texts.csv with columns doc_id,text  (not shipped)

This script does not reproduce the published LLM labels unless you have the
same documents. The published labels are in data/llm_labels.csv.
"""
from __future__ import annotations

from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
MODEL = "qwen/qwen3.8-27b"
URL = "https://api.groq.com/openai/v1/chat/completions"
SYSTEM = (
    "Appendix A codebook. Label only constructs the writer expresses about this stay; "
    "do not infer. Negative phrasing still counts as present. "
    "flag=1 if not English, empty, or automated.\n"
    "ATT: stay good or bad. "
    "SN: other people, recommending, friends/family/other reviewers. "
    "PBC: easy/hard to book, arrive, communicate, manage stay. "
    "SAT: met, exceeded, or fell short of expectations. "
    "BI: plan or wish to return, or explicit refusal.\n"
    'JSON: {"flag":0,"ATT":[present,score],"SN":[present,score],'
    '"PBC":[present,score],"SAT":[present,score],"BI":[present,score]}. '
    "present 0/1; score 0-1; present=1 iff score>=0.5."
)


def main() -> None:
    key = os.environ.get("GROQ_API_KEY", "").strip()
    if not key.startswith("gsk_"):
        raise SystemExit("Set GROQ_API_KEY. Do not write the key into this repository.")
    path = ROOT / "data" / "private_texts.csv"
    if not path.exists():
        raise SystemExit("data/private_texts.csv is not shipped. Published labels are in data/llm_labels.csv.")
    print("model", MODEL)
    print("This optional recode is not required to reproduce Table 3.")


if __name__ == "__main__":
    main()
