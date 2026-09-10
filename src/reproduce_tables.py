"""Recompute Paper 1B Tables 3 and 7 from the public gold frame (no raw text)."""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score

ROOT = Path(__file__).resolve().parents[1]
CONS_KEEP = ["BI", "SN"]
BANDS = ["15-40", "40-70", "70-120", "120+"]


def metrics(y, score, hard):
    return {
        "auc": round(float(roc_auc_score(y, score)), 3),
        "precision": round(float(precision_score(y, hard, zero_division=0)), 3),
        "recall": round(float(recall_score(y, hard, zero_division=0)), 3),
        "f1": round(float(f1_score(y, hard, zero_division=0)), 3),
        "instrument_prevalence": round(float(np.mean(hard)), 3),
        "human_prevalence": round(float(np.mean(y)), 3),
    }


def main():
    m = pd.read_csv(ROOT / "data" / "gold_frame.csv")
    print(f"n = {len(m)} gold-eligible documents")
    rows = []
    for c in CONS_KEEP:
        y = m[c].to_numpy()
        specs = [
            ("dictionary", np.log1p(m[f"hits_{c}"]), m[f"pres_{c}"]),
            ("encoder", m[f"enc_{c}"], (m[f"enc_{c}"] > 0).astype(int)),
            ("entailment", m[f"nli_{c}"], (m[f"nli_{c}"] > 0.5).astype(int)),
        ]
        if f"llm_score_{c}" in m.columns:
            specs.append((
                "LLM",
                m[f"llm_score_{c}"].fillna(0),
                m[f"llm_{c}"].fillna(0).astype(int),
            ))
        for name, score, hard in specs:
            row = {"construct": c, "instrument": name}
            row.update(metrics(y, np.asarray(score, dtype=float), np.asarray(hard, dtype=int)))
            rows.append(row)
    t3 = pd.DataFrame(rows)
    print("\n=== Table 3 (recomputed) ===")
    print(t3.to_string(index=False))
    t3.to_csv(ROOT / "tables" / "table3_recomputed.csv", index=False)

    print("\n=== Table 7 word-budget Spearman rho (SN, BI) ===")
    rows = []
    for b in BANDS:
        s = m[m.band.astype(str) == b]
        rows.append({
            "band": b, "n": len(s),
            "human": round(float(spearmanr(s.SN, s.BI).statistic), 3),
            "dictionary": round(float(spearmanr(np.log1p(s.hits_SN), np.log1p(s.hits_BI)).statistic), 3),
            "entailment": round(float(spearmanr(s.nli_SN, s.nli_BI).statistic), 3),
        })
    t7 = pd.DataFrame(rows)
    print(t7.to_string(index=False))
    t7.to_csv(ROOT / "tables" / "table7_recomputed.csv", index=False)


if __name__ == "__main__":
    main()
