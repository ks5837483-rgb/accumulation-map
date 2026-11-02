#!/usr/bin/env bash
# Reproduce every analysis result in the proposal from the released data, then compare with expected/.
# Deterministic, no AI, no network. Tested with Python 3.11, pandas 2.3.3 and 3.1, numpy 2.3.5 (pip install -r requirements.txt).
# CSV floats are written with 10 significant digits so results match across pandas versions.
set -euo pipefail
cd "$(dirname "$0")"
python3 check_counts.py > /dev/null
( cd analysis/silo && python3 internal_by_silo.py > /dev/null && python3 external_lr.py > /dev/null && python3 measured_info.py > /dev/null )
( cd analysis/market && python3 analysis_eval.py > /dev/null )
fail=0
for pair in RESULTS_counts.txt:RESULTS_counts.txt analysis/silo/RESULTS_internal.txt:RESULTS_internal.txt \
            analysis/silo/RESULTS_external.txt:RESULTS_external.txt analysis/silo/RESULTS_measured.txt:RESULTS_measured.txt \
            analysis/market/RESULTS.txt:RESULTS.txt analysis/silo/grades_by_silo.csv:grades_by_silo.csv \
            analysis/silo/external_lr_cells.csv:external_lr_cells.csv analysis/market/mechanism_market_grades.csv:mechanism_market_grades.csv \
            analysis/market/credible_both_by_mechanism.csv:credible_both_by_mechanism.csv; do
  got=${pair%%:*}; exp=expected/${pair##*:}
  if cmp -s "$got" "$exp"; then echo "MATCH   $got"; else echo "DIFFER  $got"; fail=1; fi
done
[ $fail -eq 0 ] && echo "All results reproduced." || { echo "Some results differ (see above)."; exit 1; }
