"""Part 1 — internal validity WITHIN each silo (strategy / finance / accounting) on set S (541 papers). Deterministic counts, no LLM.
Per silo x mechanism (paper-level units): papers, causal-design share, mean support, rejected/mixed share, and within-silo replication of
mechanism->outcome pairings. Grade: single (1 paper) · thin (2-3) · replicated (>=4) · credible (>=4 papers, >=1 causal, support >=.70)."""
import pandas as pd, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
f = pd.read_csv('../findings_eval_tax.csv')
f['sup'] = f.support.map({'supported': 1, 'rejected': 0, 'mixed': .5})
CAUSAL = ('natural_experiment', 'did', 'difference_in_differences', 'instrumental', 'iv', 'regression_discontinuity', 'rdd', 'field_experiment', 'lab_experiment', 'quasi_experiment')
f['causal'] = f.identification.fillna('').str.lower().str.split(r'[;, ]+').apply(lambda t: any(x in CAUSAL for x in t))
f = f[f.field.isin(['strategy', 'finance', 'accounting']) & f.sup.notna()]
pm = f.groupby(['field', 'mech_g', 'paper_id']).agg(sup=('sup', 'mean'), causal=('causal', 'max'), rej=('sup', lambda s: (s < 1).mean())).reset_index()
m = pm.groupby(['field', 'mech_g']).agg(papers=('paper_id', 'nunique'), support=('sup', 'mean'), causal_share=('causal', 'mean'), not_supported=('rej', 'mean')).reset_index()
def grade(r):
    if r.papers == 1: return 'single'
    if r.papers <= 3: return 'thin'
    return 'credible' if (r.causal_share > 0 and r.support >= .70) else 'replicated'
m['grade'] = m.apply(grade, axis=1)
cells = f.groupby(['field', 'mech_g', 'Y_tax']).paper_id.nunique().reset_index(name='papers')
out = []
P = lambda *a: (print(*a), out.append(' '.join(map(str, a))))
P('=== grades per silo (count of mechanisms)'); P(pd.crosstab(m.field, m.grade).reindex(columns=['single', 'thin', 'replicated', 'credible']).to_string())
P('\n=== pairings (mechanism x outcome) within silo: share tested by ONE paper')
P(cells.groupby('field').agg(pairings=('papers', 'size'), once=('papers', lambda s: round((s == 1).mean(), 3)), ge2=('papers', lambda s: int((s >= 2).sum()))).to_string())
P('\n=== design: share of papers with a causal design, per silo')
P(pm.groupby('field').causal.mean().round(3).to_string())
for fl in ['finance', 'strategy', 'accounting']:
    s = m[(m.field == fl) & (m.papers >= 4)].sort_values('papers', ascending=False).head(10)
    P(f'\n--- {fl}: top mechanisms (>=4 papers)'); P(s[['mech_g', 'papers', 'support', 'causal_share', 'grade']].round(2).to_string(index=False))
cr = m[m.grade == 'credible'].groupby('mech_g').field.apply(lambda s: ','.join(sorted(s)))
P('\n=== credible mechanisms and the silos where they are credible'); P(cr.value_counts().to_string())
P('\nmechanisms credible in 2+ silos:', sorted(cr[cr.str.contains(',')].index.tolist()))
m.to_csv('grades_by_silo.csv', index=False, float_format='%.10g'); open('RESULTS_internal.txt', 'w').write('\n'.join(out) + '\n')
