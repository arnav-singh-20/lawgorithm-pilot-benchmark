"""
Verification Script: Lawgorithm Paper Tables vs. Real Benchmark Data
Runs an automated consistency check between every table in the paper and the
underlying raw JSON files in this directory.
"""

import json
import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__))

def check(condition, msg):
    if condition:
        print(f"  [PASS] {msg}")
    else:
        print(f"  [FAIL] {msg}")
        sys.exit(1)

print("=" * 70)
print("LAWGORITHM PAPER VERIFICATION: AUDITING REAL DATA AGAINST ALL TABLES")
print("=" * 70 + "\n")

# 1. TABLE 2: Statutory Corpus
print("Auditing Table 2: Statutory Corpus & Manifest...")
with open(os.path.join(DIR, "table2_statute_corpus_manifest.json")) as f:
    t2 = json.load(f)
check(t2["total_acts"] == 27, f"Total statutes + MTA = 27 (26 Acts + Model Tenancy Act), got {t2['total_acts']}")
check(t2["total_sections"] == 2273, f"Total statutory sections == 2,273, got {t2['total_sections']}")

# 2. TABLE 3: Development / Test Split
print("\nAuditing Table 3: Gold Dataset Dev/Test Split...")
with open(os.path.join(DIR, "table3_gold_dataset_and_split.json")) as f:
    t3 = json.load(f)
check(t3["dev_clauses_n"] == 24, f"Dev split = 24 clauses, got {t3['dev_clauses_n']}")
check(t3["test_clauses_n"] == 26, f"Test split = 26 clauses, got {t3['test_clauses_n']}")
check(len(t3["clauses"]) == 50, f"Total gold clauses = 50, got {len(t3['clauses'])}")

# 3. TABLE 4: Core System Performance Measures
print("\nAuditing Table 4: Overall Performance Measures & Point Estimates...")
with open(os.path.join(DIR, "table4_and_table5_performance_metrics.json")) as f:
    t4 = json.load(f)
check(t4["risk_accuracy"] == 0.92, f"Risk accuracy == 92.0% (46/50), got {t4['risk_accuracy']*100:.1f}%")
check(round(t4["grounding_precision"], 4) == 0.9375, f"Grounding precision == 93.8% (60/64), got {t4['grounding_precision']*100:.1f}%")
check(t4["raw_claim_unsupported_rate"] == 0.0, f"Unsupported claims == 0.0% (0/75), got {t4['raw_claim_unsupported_rate']}%")
check(round(t4["wilson_95"]["risk_correct"][0], 3) == 0.812, "Risk accuracy CI low == 0.812")
check(round(t4["wilson_95"]["risk_correct"][1], 3) == 0.968, "Risk accuracy CI high == 0.968")
check(round(t4["wilson_95"]["grounding_hits"][0], 3) == 0.850, "Grounding precision CI low == 0.850")
check(round(t4["wilson_95"]["grounding_hits"][1], 3) == 0.975, "Grounding precision CI high == 0.975")

# 4. TABLE 5: Per-Class Precision, Recall, and F1
print("\nAuditing Table 5: Per-Class Performance...")
per_class = t4["per_class"]
check(per_class["red"]["n"] == 14 and round(per_class["red"]["f1"], 3) == 0.929, "Red: n=14, F1=92.9%")
check(per_class["amber"]["n"] == 15 and round(per_class["amber"]["f1"], 3) == 0.867, "Amber: n=15, F1=86.7%")
check(per_class["green"]["n"] == 21 and round(per_class["green"]["f1"], 3) == 0.952, "Green: n=21, F1=95.2%")
check(round(per_class["macro"]["f1"], 3) == 0.916, f"Macro F1 == 91.6%, got {per_class['macro']['f1']*100:.1f}%")

# 5. TABLE 6: Confusion Matrix
print("\nAuditing Table 6: Risk Confusion Matrix...")
with open(os.path.join(DIR, "table6_confusion_matrix.json")) as f:
    t6 = json.load(f)["matrix"]
check(t6["Gold_RED"]["Pred_RED"] == 13 and t6["Gold_RED"]["Pred_AMBER"] == 1 and t6["Gold_RED"]["Pred_GREEN"] == 0, "Gold Red -> [13, 1, 0]")
check(t6["Gold_AMBER"]["Pred_RED"] == 1 and t6["Gold_AMBER"]["Pred_AMBER"] == 13 and t6["Gold_AMBER"]["Pred_GREEN"] == 1, "Gold Amber -> [1, 13, 1]")
check(t6["Gold_GREEN"]["Pred_RED"] == 0 and t6["Gold_GREEN"]["Pred_AMBER"] == 1 and t6["Gold_GREEN"]["Pred_GREEN"] == 20, "Gold Green -> [0, 1, 20]")

# 6. TABLE 7: Retrieval Recall Ablations
print("\nAuditing Table 7: Retrieval Recall Across Pipeline Variants...")
with open(os.path.join(DIR, "table7_retrieval_ablations.json")) as f:
    t7 = json.load(f)
check(t7["vector only (clause text)"]["all"][:2] == [4, 39], "Vector only all: 4/39 (10.3%)")
check(t7["BM25 only (clause text)"]["all"][:2] == [4, 39], "BM25 only all: 4/39 (10.3%)")
check(t7["+ clause-type hint query (revised hints)"]["all"][:2] == [18, 39], "+ Clause hint all: 18/39 (46.2%)")
check(t7["+ central Acts first"]["all"][:2] == [20, 39], "+ Central first all: 20/39 (51.3%)")
check(t7["+ statute anchors (full system)"]["all"][:2] == [39, 39], "+ Full anchors all: 39/39 (100.0%)")

# 7. TABLE 8: Baseline Ablations
print("\nAuditing Table 8: Macro-F1 Classifier Baselines...")
with open(os.path.join(DIR, "table8_baseline_ablations.json")) as f:
    t8 = json.load(f)
check(round(t8["majority class (green, from dev)"]["per_class"]["macro"]["f1"], 2) == 0.20, "Majority baseline Macro-F1 == 0.20")
check(round(t8["clause-type rule (risk-prone type -> amber, else green)"]["per_class"]["macro"]["f1"], 2) == 0.35, "Rule baseline Macro-F1 == 0.35")

# 8. TABLE 9: Routing and Confidence Threshold Calibration
print("\nAuditing Table 9: Routing & Threshold Calibration...")
with open(os.path.join(DIR, "table9_routing_and_threshold_calibration.json")) as f:
    t9 = json.load(f)
check(t9["dev"]["tau"] == 0.56 and t9["dev"]["released"] == 5 and t9["dev"]["released_accuracy"] == 1.0, "Dev (tau=0.56): 5 released, 100% precision")
check(t9["test"]["tau"] == 0.56 and t9["test"]["released"] == 10 and t9["test"]["released_accuracy"] == 0.8, "Test (tau=0.56): 10 released, 80% precision, 2 under-flagged")
check(t9["paper_threshold_0.95_test"]["tau"] == 0.95 and t9["paper_threshold_0.95_test"]["released"] == 3 and t9["paper_threshold_0.95_test"]["released_accuracy"] == 1.0, "Test (tau=0.95): 3 released, 100% precision, 0 under-flagged")

# 9. INTER-ANNOTATOR RELIABILITY (COHEN'S KAPPA)
print("\nAuditing Inter-Annotator Agreement (Cohen's Kappa Study)...")
with open(os.path.join(DIR, "inter_annotator_agreement_cohen_kappa.json")) as f:
    tk = json.load(f)["summary"]
check(tk["observed_raw_agreement_pct"] == 94.0, f"Raw agreement == 94.0% (47/50), got {tk['observed_raw_agreement_pct']}%")
check(round(tk["cohen_kappa_unweighted"], 3) == 0.905, f"Cohen Kappa == 0.905, got {tk['cohen_kappa_unweighted']}")
check(round(tk["standard_error"], 3) == 0.053, f"Standard Error == 0.053, got {tk['standard_error']}")
check(round(tk["linear_weighted_kappa"], 3) == 0.932, f"Linear Kappa == 0.932, got {tk['linear_weighted_kappa']}")
check(round(tk["quadratic_weighted_kappa"], 3) == 0.957, f"Quadratic Kappa == 0.957, got {tk['quadratic_weighted_kappa']}")

print("\n" + "=" * 70)
print("SUCCESS: ALL AUDIT CHECKS PASSED WITH 100% NUMERICAL CONSISTENCY!")
print("=" * 70)
