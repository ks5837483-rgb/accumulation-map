# Is knowledge accumulating? Repository for the acquisition demonstration

This repository accompanies the proposal "Is Knowledge Accumulating? An AI-Built Map of What a Literature Has Established" (Organization Science special issue on AI-enabled frontiers). It contains the coded data and code behind the acquisition analysis reported in the proposal. The rest of the evidence base (about 8,000 papers across five topics) will be released as the project develops.

## Quick start

Run `./reproduce.sh` to rerun every analysis and compare it with `expected/`. Then open `CLAIMS.md`, which maps each number in the proposal to the file and line that produces it. `AGENTS.md` gives the same steps for an AI agent.

## What is here

| Folder | Contents |
|---|---|
| `analysis/findings_eval_tax.csv` | 3,529 coded claims from 541 acquisition papers in 28 journals. One row is one cause, mechanism, and outcome claim from one tested hypothesis, with its support status, research design, setting, and mechanism and outcome groups. Any text value that shares an 8-word run with the paper's full text is replaced with `[withheld: wording matches the source]`. Effect sizes are coded in the evidence base but not released. |
| `analysis/_work_attr/out/` | Setting attributes, in batched JSONL files with one record per paper (country scope, industry scope, target listing, sample years), coded by AI with `prompts/setting_attributes_prompt.txt`. |
| `analysis/_work_side/` | Who evaluates each outcome (a firm or investors), coded by AI with `prompts/outcome_evaluator_prompt.txt`. |
| `analysis/_work_measure/` | The kind of cause in each claim through an information mechanism, coded by AI with `prompts/info_measure_type_prompt.txt` (used by `measured_info.py`). |
| `analysis/_work_dd/` | Labels marking which cause, mechanism, and outcome names refer to due diligence. |
| `analysis/silo/`, `analysis/market/`, `analysis/market_pivot/` | The scripts that produce every number in the proposal, and their outputs (`RESULTS_internal.txt`, `RESULTS_external.txt`, `RESULTS_measured.txt`, `RESULTS.txt`). |
| `data/papers/` | One JSON file per paper (541 files) with four coded layers merged: mechanism, context, measures, and future directions. The effect-size and interaction-effect layers are not released. Every verbatim field from the papers is removed, and any remaining text field that shares an 8-word run with the paper's full text is replaced with `[withheld: wording matches the source]` (6.1% of text fields). |
| `data/selection_1558.csv` | The AI selection decision for each of the 1,558 empirical acquisition papers (whether a firm is evaluated through an information mechanism, and by whom). 541 are included. |
| `prompts/` | The prompts of record used to code the papers and run each step, with 16-character SHA-256 fingerprints in `SHA256_16.txt`. |
| `video/extraction_demo.mp4` | A short narrated video showing one paper (Testoni 2021, Strategic Management Journal, open access under CC BY 4.0) read field by field, next to the sentence or table cell each field came from. |
| `lib/idkit.py` | The paper-id helper used for joins. |

## How to reproduce the results

Tested with Python 3.11 and pandas 2.3.3 or 3.1 (`pip install -r requirements.txt`). Run `./reproduce.sh`. It runs these steps and compares nine output files with the copies in `expected/`.

```
python3 check_counts.py                      # RESULTS_counts.txt
cd analysis/silo
python3 internal_by_silo.py                  # RESULTS_internal.txt, grades_by_silo.csv
python3 external_lr.py                       # RESULTS_external.txt, external_lr_cells.csv
python3 measured_info.py                     # RESULTS_measured.txt
cd ../market
python3 analysis_eval.py                     # RESULTS.txt, mechanism_market_grades.csv, credible_both_by_mechanism.csv
```

The scripts are deterministic and use no AI. CSV numbers are written with 10 significant digits, so results match across pandas versions.

- `check_counts.py` counts the papers, claims, journals, and fields quoted in the proposal.
- `internal_by_silo.py` answers the first question (is a mechanism solid where it was tested?) for each field.
- `external_lr.py` answers the second question (does it hold in other settings?) across five contexts.
- `measured_info.py` counts how often the information mechanism itself is measured (6 of 891 claims, 0.7%).
- `analysis_eval.py` compares firms and investors as evaluators, including the 88% vs. 78% result.

## What is not here, and why

The papers were read under institutional access for research. Publisher terms do not allow us to share them, so this repository contains no PDFs, no full text, no abstracts, and no quoted sentences from the papers. Each claim is identified by the paper's DOI, so anyone with access can check it against the source. The extraction itself can be rerun on open-access and working-paper versions with the prompts in `prompts/`.

## Models

For the acquisition papers released here, Claude Opus 4.8 read and coded each paper, pinned to that version. The later coding steps (grouping mechanism and outcome names, who evaluates, setting attributes, selection, and the kind of cause) were run by Claude agents with the prompts in `prompts/`, without a pinned model version. The analysis scripts use no AI.
