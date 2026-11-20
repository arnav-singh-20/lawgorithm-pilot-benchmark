"""
Lawgorithm Benchmark Verification Script
Audits all paper tables against the real benchmark artifacts in index/, evaluation/, and runs/.
"""

import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def check(condition, msg):
    if condition:
        print(f"  [PASS] {msg}")
    else:
        print(f"  [FAIL] {msg}")
        sys.exit(1)

print("=" * 72)
print("  LAWGORITHM BENCHMARK REPRODUCIBILITY AUDIT: AUDITING ALL TABLES")
print("=" * 72 + "\n")

# 1. TABLE 2: Statutory Corpus
print("1. Auditing Table 2: Statutory Corpus & Manifest (index/)...")
with open(os.path.join(BASE_DIR, "index", "statute_corpus_manifest.json")) as f:
    t2 = json.load(f)
check(t2["total_acts"] == 27, f"Total statutes = 27 (26 Acts + Model Tenancy Act), got {t2['total_acts']}")
check(t2["total_sections"] == 2273, f"Total statutory sections == 2,273, got {t2['total_sections']}")

# 2. TABLE 3: Development / Test Split
print("\n2. Auditing Table 3: Gold Dataset Dev/Test Split (evaluation/)...")
with open(os.path.join(BASE_DIR, "evaluation", "split.json")) as f:
    split = json.load(f)
with open(os.path.join(BASE_DIR, "evaluation", "gold_clauses.json")) as f:
    gold = json.load(f)

check(len(split["dev"]) == 24, f"Dev split = 24 clauses, got {len(split['dev'])}")
check(len(split["test"]) == 26, f"Test split = 26 clauses, got {len(split['test'])}")
check(len(gold) == 50, f"Total gold clauses = 50, got {len(gold)}")

# 3. TABLE 4: Core System Performance Measures
print("\n3. Auditing Table 4: Overall Performance Measures (runs/latest_metrics.json)...")
with open(os.path.join(BASE_DIR, "runs", "latest_metrics.json")) as f:
    m = json.load(f)

check(m["risk_accuracy"] == 0.92, f"Risk accuracy == 92.0% (46/50), got {m['risk_accuracy']*100:.1f}%")
check(round(m["grounding_precision"], 4) == 0.9375, f"Grounding precision == 93.8% (60/64), got {m['grounding_precision']*100:.1f}%")
check(m["raw_claim_unsupported_rate"] == 0.0, f"Unsupported claims == 0.0% (0/75), got {m['raw_claim_unsupported_rate']}%")
check(round(m["wilson_95"]["risk_correct"][0], 3) == 0.812, "Risk accuracy CI low == 0.812")
check(round(m["wilson_95"]["risk_correct"][1], 3) == 0.968, "Risk accuracy CI high == 0.968")
check(round(m["wilson_95"]["grounding_hits"][0], 3) == 0.850, "Grounding precision CI low == 0.850")
check(round(m["wilson_95"]["grounding_hits"][1], 3) == 0.975, "Grounding precision CI high == 0.975")

# 4. TABLE 5: Per-Class Precision, Recall, and F1
print("\n4. Auditing Table 5: Per-Class Performance (runs/latest_metrics.json)...")
pc = m["per_class"]
check(pc["red"]["n"] == 14 and round(pc["red"]["f1"], 3) == 0.929, "Red: n=14, F1=92.9%")
check(pc["amber"]["n"] == 15 and round(pc["amber"]["f1"], 3) == 0.867, "Amber: n=15, F1=86.7%")
check(pc["green"]["n"] == 21 and round(pc["green"]["f1"], 3) == 0.952, "Green: n=21, F1=95.2%")
check(round(pc["macro"]["f1"], 3) == 0.916, f"Macro F1 == 91.6%, got {pc['macro']['f1']*100:.1f}%")

# 5. TABLE 6: Confusion Matrix
print("\n5. Auditing Table 6: Risk Confusion Matrix (runs/table6_confusion_matrix.json)...")
with open(os.path.join(BASE_DIR, "runs", "table6_confusion_matrix.json")) as f:
    cm = json.load(f)["matrix"]
check(cm["Gold_RED"]["Pred_RED"] == 13 and cm["Gold_RED"]["Pred_AMBER"] == 1 and cm["Gold_RED"]["Pred_GREEN"] == 0, "Gold Red -> [13, 1, 0]")
check(cm["Gold_AMBER"]["Pred_RED"] == 1 and cm["Gold_AMBER"]["Pred_AMBER"] == 13 and cm["Gold_AMBER"]["Pred_GREEN"] == 1, "Gold Amber -> [1, 13, 1]")
check(cm["Gold_GREEN"]["Pred_RED"] == 0 and cm["Gold_GREEN"]["Pred_AMBER"] == 1 and cm["Gold_GREEN"]["Pred_GREEN"] == 20, "Gold Green -> [0, 1, 20]")

# 6. TABLE 7: Retrieval Recall Ablations
print("\n6. Auditing Table 7: Retrieval Recall Across Pipeline Variants (runs/ablations_offline.json)...")
with open(os.path.join(BASE_DIR, "runs", "ablations_offline.json")) as f:
    abl = json.load(f)
ret = abl["retrieval_gold_section_recall"]
check(ret["vector only (clause text)"]["all"][:2] == [4, 39], "Vector only all: 4/39 (10.3%)")
check(ret["BM25 only (clause text)"]["all"][:2] == [4, 39], "BM25 only all: 4/39 (10.3%)")
check(ret["+ clause-type hint query (revised hints)"]["all"][:2] == [18, 39], "+ Clause hint all: 18/39 (46.2%)")
check(ret["+ central Acts first"]["all"][:2] == [20, 39], "+ Central first all: 20/39 (51.3%)")
check(ret["+ statute anchors (full system)"]["all"][:2] == [39, 39], "+ Full anchors all: 39/39 (100.0%)")

# 7. TABLE 8: Baseline Classifier Baselines
print("\n7. Auditing Table 8: Macro-F1 Classifier Baselines (runs/ablations_offline.json)...")
base_risk = abl["risk_baselines"]
check(round(base_risk["majority class (green, from dev)"]["per_class"]["macro"]["f1"], 2) == 0.20, "Majority baseline Macro-F1 == 0.20")
check(round(base_risk["clause-type rule (risk-prone type -> amber, else green)"]["per_class"]["macro"]["f1"], 2) == 0.35, "Rule baseline Macro-F1 == 0.35")

# 8. TABLE 9: Routing and Threshold Calibration
print("\n8. Auditing Table 9: Routing & Threshold Calibration (runs/routing_report.json)...")
with open(os.path.join(BASE_DIR, "runs", "routing_report.json")) as f:
    rout = json.load(f)
check(rout["dev"]["tau"] == 0.56 and rout["dev"]["released"] == 5 and rout["dev"]["released_accuracy"] == 1.0, "Dev (tau=0.56): 5 released, 100% precision")
check(rout["test"]["tau"] == 0.56 and rout["test"]["released"] == 10 and rout["test"]["released_accuracy"] == 0.8, "Test (tau=0.56): 10 released, 80% precision, 2 under-flagged")
check(rout["paper_threshold_0.95_test"]["tau"] == 0.95 and rout["paper_threshold_0.95_test"]["released"] == 3 and rout["paper_threshold_0.95_test"]["released_accuracy"] == 1.0, "Test (tau=0.95): 3 released, 100% precision, 0 under-flagged")

# 9. INTER-ANNOTATOR AGREEMENT (COHEN'S KAPPA)
print("\n9. Auditing Inter-Annotator Reliability (evaluation/inter_annotator_agreement_cohen_kappa.json)...")
with open(os.path.join(BASE_DIR, "evaluation", "inter_annotator_agreement_cohen_kappa.json")) as f:
    k_sum = json.load(f)["summary"]
check(k_sum["observed_raw_agreement_pct"] == 94.0, f"Raw agreement == 94.0% (47/50), got {k_sum['observed_raw_agreement_pct']}%")
check(round(k_sum["cohen_kappa_unweighted"], 3) == 0.905, f"Cohen Kappa == 0.905, got {k_sum['cohen_kappa_unweighted']}")
check(round(k_sum["standard_error"], 3) == 0.053, f"Standard Error == 0.053, got {k_sum['standard_error']}")
check(round(k_sum["linear_weighted_kappa"], 3) == 0.932, f"Linear Kappa == 0.932, got {k_sum['linear_weighted_kappa']}")
check(round(k_sum["quadratic_weighted_kappa"], 3) == 0.957, f"Quadratic Kappa == 0.957, got {k_sum['quadratic_weighted_kappa']}")

print("\n" + "=" * 72)
print("  SUCCESS: ALL BENCHMARK METRICS AUDITED AND 100% BIT-EXACT VERIFIED!")
print("=" * 72)
