"""Counts quoted in the proposal that come straight from the released data (no AI, deterministic)."""
import pandas as pd
s = pd.read_csv('data/selection_1558.csv'); i = s[s.include == 'yes']
f = pd.read_csv('analysis/findings_eval_tax.csv')
fc = i.field.value_counts()
out = [f'papers judged for selection: {len(s)}', f'papers selected: {len(i)}',
       f'selected by field: finance {fc.get("finance", 0)}, strategy {fc.get("strategy", 0)}, accounting {fc.get("accounting", 0)}, other {len(i) - fc.get("finance", 0) - fc.get("strategy", 0) - fc.get("accounting", 0)}',
       'selected by evaluator: ' + ', '.join(f'{k} {v}' for k, v in i.evaluator.value_counts().items()),
       f'coded claims: {len(f)}', f'journals: {f.journal.nunique()}']
open('RESULTS_counts.txt', 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
