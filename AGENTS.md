# For AI agents and reviewers

1. `pip install -r requirements.txt` (pandas, numpy).
2. Run `./reproduce.sh`. It reruns every analysis and prints MATCH or DIFFER for each result file.
3. Open `CLAIMS.md`. It maps each number in the proposal to the file and line that produces it.
4. `data/papers/` holds one JSON per paper with the released coded layers (no effect sizes). The papers' own text is not included (see README).
No step uses AI or the network. The scripts are deterministic.
