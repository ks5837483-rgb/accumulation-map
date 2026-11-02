"""Is the information itself measured? Claims that run through one of the 14 information mechanisms (the mechanism groups in
../_work_measure/info_chains_by_measure_kind.csv, whose cause-kind labels were coded by AI with prompts/info_measure_type_prompt.txt).
Reports how often the mechanism node is measured (coded field mechanism_measured) and the mix of cause kinds. Deterministic, no LLM."""
import os, pandas as pd
os.chdir(os.path.dirname(os.path.abspath(__file__)))
k = pd.read_csv('../_work_measure/info_chains_by_measure_kind.csv')
f = pd.read_csv('../findings_eval_tax.csv')
s = f[f.mech_g.isin(k.mech_g.unique())]
out = [f'information mechanisms: {k.mech_g.nunique()}', f'claims through them: {len(s)}',
       f'mechanism measured: {int(s.mechanism_measured.astype(str).eq("True").sum())} ({s.mechanism_measured.astype(str).eq("True").mean():.1%})',
       'cause kind (share of claims):'] + [f'  {i}: {v:.1%}' for i, v in k.kind.value_counts(normalize=True).items()]
open('RESULTS_measured.txt', 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
