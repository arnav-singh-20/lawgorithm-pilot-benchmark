# Lawgorithm: Pilot Benchmark and Run Artifacts
 
Evaluation data, saved run outputs, and table-checking scripts for the paper
 
> **Lawgorithm: A Retrieval-Grounded ReAct Agent for Legal Clause Simplification and Risk Classification**
> Samriddhi Bisht, Arnav Singh, Sarthak, Sakshi Siwal, and Tanaya Gupta
> Department of Computer Science and Engineering, ABES Engineering College, Ghaziabad, India
> IC-DIGICOM 2026 (Springer Nature proceedings)
 
This repository accompanies the paper. It lets readers inspect the statute index, the 50-clause gold set, the dual-annotator study, and the saved outputs behind the paper's tables. The agent implementation itself is **not** included (see [Scope and limitations](#5-scope-and-limitations)).
 
## Contents
 
1. [Repository layout](#1-repository-layout)
2. [Statute corpus and sources](#2-statute-corpus-and-sources)
3. [Checking the paper's tables](#3-checking-the-papers-tables)
4. [Paper table to file map](#4-paper-table-to-file-map)
5. [Scope and limitations](#5-scope-and-limitations)
6. [Citation](#6-citation)
---
 
## 1. Repository layout
 
```text
lawgorithm-pilot-benchmark/
├── index/
│   ├── build_statute_library.py        # Builds the JSON statute library from source texts
│   ├── ingest_laws.py                  # Ingests statutes into the hybrid BM25 + vector index
│   ├── table_a1_statutes.csv           # All 26 Acts + Model Tenancy Act with section counts
│   └── statute_corpus_manifest.json    # Manifest of the 2,273 indexed sections
├── evaluation/
│   ├── gold_clauses.json               # The 50 gold clauses with labels
│   ├── split.json                      # 24 development / 26 test split
│   ├── inter_annotator_agreement_cohen_kappa.json   # Dual-annotator data and agreement metrics
│   ├── run_accuracy_eval.py            # Accuracy, grounding and hallucination evaluation
│   ├── eval_routing.py                 # Release-rule (routing) evaluation
│   └── calibrate_thresholds.py         # Confidence threshold (tau) calibration
├── runs/
│   ├── per_clause_predictions.json     # Raw predictions and explanations for all 50 clauses
│   ├── latest_metrics.json             # Metrics behind Tables 4 and 5
│   ├── routing_report.json             # Release-rule results (Table 9)
│   ├── calibration_report.json         # Platt scaling, ECE and Brier data
│   ├── table6_confusion_matrix.json    # Confusion matrix (Table 6)
│   ├── ablations_offline.json          # Retrieval and baseline results (Tables 7 and 8)
│   └── table10_provenance_log_example.json   # Example provenance log entry
├── verify_paper_tables.py              # Checks paper tables against the saved files
└── README.md
```
 
## 2. Statute corpus and sources
 
The index contains **2,273 sections** from **26 Acts** and the **Model Tenancy Act, 2021** (3 benchmark provisions).
 
| Group | Acts | Sections |
| :--- | :--- | ---: |
| General contract and commercial law (11 Acts) | Indian Contract Act 1872; Transfer of Property Act 1882; Negotiable Instruments Act 1881; Indian Stamp Act 1899; Registration Act 1908; Specific Relief Act 1963; Limitation Act 1963; Arbitration and Conciliation Act 1996; Copyright Act 1957; Information Technology Act 2000; Consumer Protection Act 2019 | 1,223 |
| Labour and employment (8 Acts) | Code on Wages 2019; Industrial Relations Code 2020; Code on Social Security 2020; Occupational Safety, Health and Working Conditions Code 2020; Apprentices Act 1961; Rights of Persons with Disabilities Act 2016; Sexual Harassment of Women at Workplace Act 2013; Andhra Pradesh Shops and Establishments Act 1988 | 712 |
| State tenancy and rent control (7 Acts) | Delhi 1958; Maharashtra 1999; Karnataka 1999; Tamil Nadu 2017; Uttar Pradesh 2021; West Bengal 1997; Kerala 1965 | 335 |
| Model Tenancy framework | Model Tenancy Act 2021 (benchmark provisions) | 3 |
| **Total** | | **2,273** |
 
The full per-Act list with section counts is in [`index/table_a1_statutes.csv`](index/table_a1_statutes.csv).
 
**Source portals**
 
- India Code (`indiacode.nic.in`), Ministry of Law and Justice, Government of India: central Acts
- The Gazette of India and PRS Legislative Research (`prsindia.org`): the Labour Codes
- Official state gazettes and India Code state enactments: state Acts
- Ministry of Housing and Urban Affairs (`mohua.gov.in`): Model Tenancy Act, 2021
The Constitution of India is not indexed. Corpus text derived from scanned documents was OCR'd and checked by lawyers.
 
## 3. Checking the paper's tables
 
```bash
python3 verify_paper_tables.py
```
 
The script reads the saved files in `index/`, `evaluation/` and `runs/` and checks that the numbers printed in the paper's tables match them: corpus size, dev/test split, accuracy and grounding precision with Wilson intervals, per-class results, confusion matrix, retrieval and baseline results, release-rule results, and the inter-annotator statistics.
 
**What this does and does not show.** It confirms that the paper is consistent with the stored run artifacts. It does **not** call the language model or re-run the agent, so it cannot show that the stored predictions would be reproduced by a fresh run.
 
Abbreviated output:
 
```text
1. Auditing Table 2: Statutory Corpus & Manifest ...
  [PASS] Total statutory sections == 2,273, got 2273
3. Auditing Table 4: Overall Performance Measures ...
  [PASS] Risk accuracy == 92.0% (46/50), got 92.0%
  [PASS] Grounding precision == 93.8% (60/64), got 93.8%
  [PASS] Unsupported claims == 0.0% (0/75), got 0.0%
8. Auditing Table 9: Routing & Threshold Calibration ...
  [PASS] Test (tau=0.56): 10 released, 80% precision, 2 under-flagged
9. Auditing Inter-Annotator Reliability ...
  [PASS] Cohen Kappa == 0.905, got 0.9048
```
 
## 4. Paper table to file map
 
| Paper table | Content | File |
| :--- | :--- | :--- |
| Table 2 | Corpus and benchmark status | `index/statute_corpus_manifest.json`, `index/table_a1_statutes.csv` |
| Table 3 | Development / test split | `evaluation/split.json` |
| Tables 4, 5 | Overall and per-class results | `runs/latest_metrics.json` |
| Table 6 | Confusion matrix | `runs/table6_confusion_matrix.json` |
| Tables 7, 8 | Retrieval ablation and non-LLM baselines | `runs/ablations_offline.json` |
| Table 9 | Release rule | `runs/routing_report.json` |
| Section 5.2 | Inter-annotator agreement | `evaluation/inter_annotator_agreement_cohen_kappa.json` |
 
`runs/table10_provenance_log_example.json` is an example provenance record. It is not tied to a table in the final paper.
 
## 5. Scope and limitations
 
- **Pilot-scale data.** The gold set has 50 clauses (24 development, 26 test), labelled by the authors and verified by an advocate. Two independent annotators later labelled all 50 clauses; agreement with each other is high (kappa = 0.905), and lower with the gold labels (kappa = 0.784 and 0.690). The paper reports these limits in Section 7.
- **Not an independent test.** Retrieval and evaluation choices were made while all 50 clauses were visible, so results show performance on this set, not generalization.
- **Single run.** The reported results come from one run at temperature 0.2. Run-to-run variance was not measured.
- **Agent code not included.** `evaluation/run_accuracy_eval.py` and related scripts need the Lawgorithm agent implementation, which is not part of this repository. A live re-run therefore requires that code and API access to the models named in the paper.
- **Retrieval is deterministic; model output is not guaranteed to be.** The BM25 + embedding index gives repeatable retrieval for a fixed corpus. Language-model outputs can vary between runs, so the saved files in `runs/` are the reference record for the paper's numbers.
- **Not legal advice.** Lawgorithm is a research prototype. Its outputs must be reviewed by a qualified person.
## 6. Citation
 
If you use this benchmark, please cite the paper:
 
```text
Bisht, S., Singh, A., Sarthak, Siwal, S., Gupta, T.:
Lawgorithm: A Retrieval-Grounded ReAct Agent for Legal Clause Simplification
and Risk Classification. In: IC-DIGICOM 2026, Springer Nature (to appear).
```
 
Contact: see the corresponding-author details in the paper.
 
