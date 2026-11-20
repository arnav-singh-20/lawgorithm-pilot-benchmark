"""
Evaluates the release rule (R4): a clause is released without review
only if it is not Red, gamma >= tau, its citations were all retrieved and
no routing flag fired. tau is chosen on the DEV half (the lowest tau at
which every released dev clause had the correct risk label) and then
applied unchanged to the TEST half.

Usage:
    python -m scripts.eval_routing data/evaluation/runs/<run>/per_clause_predictions.json
"""

import json
import sys
from pathlib import Path

from backend.config import EVALUATION_DIR
from eval.metrics import wilson_interval


def released(p, tau):
    return (p["risk_level"] != "red" and p["confidence"] >= tau
            and p.get("citation_valid", True) and not p.get("review_flags"))


def summarise(preds, tau):
    rel = [p for p in preds if released(p, tau)]
    ok = [p for p in rel if p["risk_level"] == p["gold_risk_label"]]
    under = [p["clause_id"] for p in rel
             if (p["gold_risk_label"], p["risk_level"]) in {("red", "amber"), ("red", "green"), ("amber", "green")}]
    return {"tau": tau, "clauses": len(preds), "released": len(rel), "routed_to_review": len(preds) - len(rel),
            "released_correct": [len(ok), len(rel)],
            "released_accuracy": len(ok) / len(rel) if rel else None,
            "released_accuracy_ci": wilson_interval(len(ok), len(rel)) if rel else None,
            "released_under_flagged": under}


def main(pred_path):
    preds = {p["clause_id"]: p for p in json.loads(Path(pred_path).read_text())}
    split = json.loads((EVALUATION_DIR / "split.json").read_text())
    dev = [preds[c] for c in split["dev"] if c in preds]
    test = [preds[c] for c in split["test"] if c in preds]

    candidates = sorted({round(p["confidence"], 4) for p in dev} | {1.01})
    tau = next(t for t in candidates
               if all(p["risk_level"] == p["gold_risk_label"] for p in dev if released(p, t)))

    report = {"tau_chosen_on_dev": tau, "dev": summarise(dev, tau), "test": summarise(test, tau),
              "paper_threshold_0.95_test": summarise(test, 0.95)}
    print(json.dumps(report, indent=2))
    out = Path(pred_path).parent / "routing_report.json"
    out.write_text(json.dumps(report, indent=2))
    print(f"Saved {out}")


if __name__ == "__main__":
    main(sys.argv[1])
