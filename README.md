# Lawgorithm: Evaluation Benchmark & Reproduction Package

[![Verification Status](https://img.shields.io/badge/Audit-100%25%20Verified-brightgreen)](verify_paper_tables.py)
[![Target Venue](https://img.shields.io/badge/Springer-IC--DIGICOM%202026-blue)](https://www.springer.com)

This repository contains the official evaluation benchmark, real run artifacts, and audit scripts for the paper:

> **"Lawgorithm: A Retrieval-Grounded ReAct Agent for Legal Clause Simplification and Risk Classification"**  
> *Targeted for IC-DIGICOM 2026 (Springer Nature Proceedings)*

---

## 1. Directory Structure

```text
lawgorithm-pilot-benchmark/
├── index/
│   ├── build_statute_library.py       # Script to build the JSON statute library from source
│   ├── ingest_laws.py                 # Script to ingest statutes into hybrid vector/keyword index
│   ├── table_a1_statutes.csv          # Complete CSV of all 26 Acts + Model Tenancy Act with section counts
│   └── statute_corpus_manifest.json   # Machine-readable manifest of the 2,273 statutory sections
├── evaluation/
│   ├── gold_clauses.json              # The 50 authentic gold-standard clauses with ground-truth labels
│   ├── split.json                     # 24 Development / 26 Test holdout split
│   ├── inter_annotator_agreement_cohen_kappa.json  # Full dual-annotator study dataset and metrics
│   ├── run_accuracy_eval.py           # Evaluation runner for accuracy, grounding, and hallucinations
│   ├── eval_routing.py                # Routing evaluator for human-in-the-loop review queue
│   └── calibrate_thresholds.py       # Confidence threshold calibration script (tau)
├── runs/
│   ├── per_clause_predictions.json    # Full raw predictions and explanations for all 50 clauses
│   ├── latest_metrics.json            # Exact metrics matching Tables 4 and 5 in the paper
│   ├── routing_report.json            # Confidence-gated routing results matching Table 9
│   ├── calibration_report.json        # Platt scaling and ECE/Brier calibration data
│   ├── table6_confusion_matrix.json   # 3x3 confusion matrix matching Table 6
│   ├── ablations_offline.json         # Retrieval and baseline classification ablations (Tables 7 & 8)
│   └── table10_provenance_log_example.json # Example provenance audit log entry (Table 10)
├── verify_paper_tables.py             # Single-command automated verification of all paper tables
└── README.md
```

---

## 2. Statutory Sources & Portals

The statute corpus indexes **2,273 sections** across **26 Acts** and the **Model Tenancy Act, 2021**. All texts were obtained from official government repositories:

| Category | Enactments | Official Source Portal | Citation |
| :--- | :--- | :--- | :--- |
| **Central Commercial & Contract Acts** | Indian Contract Act (1872), Transfer of Property Act (1882), Specific Relief Act (1963), Registration Act (1908), Indian Stamp Act (1899), Limitation Act (1963), Arbitration Act (1996), Negotiable Instruments Act (1881), Consumer Protection Act (2019), Copyright Act (1957), IT Act (2000) | **India Code** (`indiacode.nic.in`), Ministry of Law & Justice, Govt. of India | *Digital repository of Central Acts under Section 52(1)(q), Copyright Act, 1957.* |
| **New Labour Codes** | Code on Wages (2019), Industrial Relations Code (2020), Code on Social Security (2020), OSH Working Conditions Code (2020) | **The Gazette of India** & **PRS Legislative Research** (`prsindia.org`) | *Acts of Parliament (in force since 21 Nov 2025).* |
| **State Tenancy & Rent Control Laws** | Delhi (1958), Maharashtra (1999), Karnataka (1999), Tamil Nadu (2017), UP (2021), West Bengal (1997), Kerala (1965), AP Shops Act (1988) | **Official State Gazettes** & **India Code State Enactments** | *State legislative assemblies; hosted by India Code / PRS.* |
| **Model Tenancy Framework** | Model Tenancy Act (2021) | **Ministry of Housing & Urban Affairs (MoHUA)** (`mohua.gov.in`) | *Union Cabinet approved guideline provisions for state adoption.* |

A complete CSV listing each Act, its section count, jurisdiction, and official PDF portal link is provided in [`index/table_a1_statutes.csv`](index/table_a1_statutes.csv).

---

## 3. Instant Reproducibility Check

To audit and verify all published paper numbers on your local machine:

```bash
python3 verify_paper_tables.py
```

### Expected Output:
```text
========================================================================
  LAWGORITHM BENCHMARK REPRODUCIBILITY AUDIT: AUDITING ALL TABLES
========================================================================

1. Auditing Table 2: Statutory Corpus & Manifest (index/)...
  [PASS] Total statutes = 27 (26 Acts + Model Tenancy Act), got 27
  [PASS] Total statutory sections == 2,273, got 2273

2. Auditing Table 3: Gold Dataset Dev/Test Split (evaluation/)...
  [PASS] Dev split = 24 clauses, got 24
  [PASS] Test split = 26 clauses, got 26
  [PASS] Total gold clauses = 50, got 50

3. Auditing Table 4: Overall Performance Measures (runs/latest_metrics.json)...
  [PASS] Risk accuracy == 92.0% (46/50), got 92.0%
  [PASS] Grounding precision == 93.8% (60/64), got 93.8%
  [PASS] Unsupported claims == 0.0% (0/75), got 0.0%
  [PASS] Risk accuracy CI low == 0.812
  [PASS] Risk accuracy CI high == 0.968
  [PASS] Grounding precision CI low == 0.850
  [PASS] Grounding precision CI high == 0.975

4. Auditing Table 5: Per-Class Performance (runs/latest_metrics.json)...
  [PASS] Red: n=14, F1=92.9%
  [PASS] Amber: n=15, F1=86.7%
  [PASS] Green: n=21, F1=95.2%
  [PASS] Macro F1 == 91.6%, got 91.6%

5. Auditing Table 6: Risk Confusion Matrix (runs/table6_confusion_matrix.json)...
  [PASS] Gold Red -> [13, 1, 0]
  [PASS] Gold Amber -> [1, 13, 1]
  [PASS] Gold Green -> [0, 1, 20]

6. Auditing Table 7: Retrieval Recall Across Pipeline Variants (runs/ablations_offline.json)...
  [PASS] Vector only all: 4/39 (10.3%)
  [PASS] BM25 only all: 4/39 (10.3%)
  [PASS] + Clause hint all: 18/39 (46.2%)
  [PASS] + Central first all: 20/39 (51.3%)
  [PASS] + Full anchors all: 39/39 (100.0%)

7. Auditing Table 8: Macro-F1 Classifier Baselines (runs/ablations_offline.json)...
  [PASS] Majority baseline Macro-F1 == 0.20
  [PASS] Rule baseline Macro-F1 == 0.35

8. Auditing Table 9: Routing & Threshold Calibration (runs/routing_report.json)...
  [PASS] Dev (tau=0.56): 5 released, 100% precision
  [PASS] Test (tau=0.56): 10 released, 80% precision, 2 under-flagged
  [PASS] Test (tau=0.95): 3 released, 100% precision, 0 under-flagged

9. Auditing Inter-Annotator Reliability (evaluation/inter_annotator_agreement_cohen_kappa.json)...
  [PASS] Raw agreement == 94.0% (47/50), got 94.0%
  [PASS] Cohen Kappa == 0.905, got 0.9048
  [PASS] Standard Error == 0.053, got 0.0533
  [PASS] Linear Kappa == 0.932, got 0.9322
  [PASS] Quadratic Kappa == 0.957, got 0.957

========================================================================
  SUCCESS: ALL BENCHMARK METRICS AUDITED AND 100% BIT-EXACT VERIFIED!
========================================================================
```

---

## 4. Reproducibility Guarantee

* **Evaluating the Benchmark Artifacts (`runs/`):** Running the evaluation and table verification scripts produces **100% bit-exact, deterministic results** across every platform.
* **Statute Retrieval:** The hybrid BM25 + dense embedding index is **100% deterministic**.
* **Live LLM Inference:** Re-running against the live model (`gpt-oss-120b` / `qwen3.8-27b`) with temperature $T=0.2$ produces statistically consistent results within the reported Wilson 95% confidence intervals (Risk Accuracy $92.0\% \in [81.2\%, 96.8\%]$). The full saved outputs in `runs/per_clause_predictions.json` provide the immutable reference record.
