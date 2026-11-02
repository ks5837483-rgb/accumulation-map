# Where each number in the proposal comes from

Run `./reproduce.sh` first. It regenerates every file below and compares it with `expected/`. Line numbers refer to the files in `expected/`.

## Reproducible from this repository

| Proposal section | Claim | Source |
|---|---|---|
| Abstract, 6 | 541 papers selected | `RESULTS_counts.txt` line 2 |
| 6 | 1,558 papers with coded hypotheses were judged for selection | `RESULTS_counts.txt` line 1 |
| 6 | 234 finance, 163 strategy, 95 accounting, 49 other papers | `RESULTS_counts.txt` line 3 |
| Appendix E | 169 firm, 228 investor, 144 both | `RESULTS_counts.txt` line 4 |
| 6, 8 | 3,529 coded claims | `RESULTS_counts.txt` line 5 |
| 8 | 28 journals | `RESULTS_counts.txt` line 6 |
| 7, Table 1 | Information asymmetry credible in all three fields | `grades_by_silo.csv` (mech_g = information_asymmetry) and `RESULTS_internal.txt` lines 23, 36, 49 |
| 7, Table 1 | Information asymmetry holds in all five contexts | `RESULTS_external.txt` line 19 |
| 7, Table 1 | Signal credibility credible in accounting and finance | `grades_by_silo.csv` (mech_g = signal_credibility) |
| 7, Table 1 | Signal credibility holds partly, splits by era | `RESULTS_external.txt` lines 26, 36 |
| 7, Table 1 | Private information access replicated in strategy with no causal design | `grades_by_silo.csv` (field = strategy, mech_g = private_information_access) |
| 7, Table 1 | Private information access not tested in five contexts | `RESULTS_internal.txt` line 70 lists the 17 mechanisms credible in two or more fields, which are the ones tested; it is not among them (see also `RESULTS_external.txt` lines 13–29) |
| 7, Table 1 | Due diligence credible in finance and strategy | `grades_by_silo.csv` (mech_g = due_diligence) |
| 7, Table 1 | Due diligence holds on four contexts, era untested | `RESULTS_external.txt` line 18 |
| 7 | 8 information mechanisms credible both when firms and when investors evaluate | `RESULTS.txt` line 50 (the 14 credible on both sides are on line 8; information mechanisms are the 14 groups in `analysis/_work_measure/info_chains_by_measure_kind.csv`) |
| 7 | Supported 88% (firm) vs. 77% (investors) | `RESULTS.txt` line 51 (88.3% vs. 77.4%) |
| 7 | Gap within papers that test both sides, 94% vs. 90% | `RESULTS.txt` line 57 |
| 7 | Gap largest in finance | `RESULTS.txt` lines 54–56 |
| 7 | Gap smaller under causal designs, few papers | `RESULTS.txt` lines 52, 53 |
| Appendix E | Table A4 (main rows: 8 information mechanisms; other rows: all 14 and looser or stricter rules) | `RESULTS.txt` lines 11–29 and 50–57 |
| Appendix E | Firms better on hidden information, investors on public signals | `RESULTS.txt` lines 35, 47, 48 give the gaps; calling these mechanisms hidden or public is our reading of the mechanism names |
| Appendix E | 60% firm or deal proxies, 5% direct information attributes | `RESULTS_measured.txt` lines 5–11 |

## From project records (not reproducible from this repository)

These numbers describe the full corpus or the audits. They need the papers, which we cannot share.

| Proposal section | Claim | Record |
|---|---|---|
| 3, Abstract | Nearly 8,000 papers coded (7,852) | Counts of the coded records across five topics |
| 6 | 85,510 PDFs and 1,795 empirical acquisition papers | Corpus and topic-screen records |
| 8 | Second-vendor audit of 300 papers, 99.4% of numbered hypotheses | Audit round R005 |
| 8 | 90 of 91 checkable papers had no effect-size error | Effect-size audits of 100 papers (effect sizes are not released) |
| 7, 9 | 2,031 newer papers in the same journals | Bibliographic records from Crossref |
| Appendix E | Private targets bring higher returns in 17 of 17 papers | Incidental-control analysis |
