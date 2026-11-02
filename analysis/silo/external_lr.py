"""Part 2 — external validity (Levinthal & Rosenkopf): hold each mechanism fixed and sort its tests by contextual attribute.
Mechanisms: the 17 credible in >=2 silos (grades_by_silo.csv). Attributes: setting codes from _work_attr/out (prompt of record
setting_attributes v1: country scope, industry scope, target listing, sample years), who evaluates (market_maps), field.
Paper-level units (a paper counts once per mechanism x attribute level). Deterministic, no LLM.
Per mechanism x attribute (both levels >=3 papers): HOLDS if both levels >=.70 support; SPLITS if |gap| >= .25; else PARTIAL."""
import pandas as pd, json, glob, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lib')); import idkit
os.chdir(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '../market')
from market_maps import MARKET, EVENT, RAW_MARKET, RAW_EVENT
f = pd.read_csv('../findings_eval_tax.csv'); f['sup'] = f.support.map({'supported': 1, 'rejected': 0, 'mixed': .5}); f = f[f.sup.notna()].drop(columns=['year_start', 'year_end'], errors='ignore')
a = pd.DataFrame([json.loads(l) for g in sorted(glob.glob('../_work_attr/out/a*.jsonl')) for l in open(g) if l.strip()])
f['k'] = f.paper_id.astype(str).map(idkit.dn); a['k'] = a.paper_id.astype(str).map(idkit.dn)
f = f.merge(a[['k', 'country_scope', 'industry_scope', 'target_listing', 'year_start', 'year_end']], on='k', how='left')
mid = (pd.to_numeric(f.year_start, errors='coerce') + pd.to_numeric(f.year_end, errors='coerce')) / 2
f['sample_era'] = pd.cut(mid, [0, 1994.5, 2004.5, 2100], labels=['pre-1995', '1995-2004', '2005+'])
f['country'] = f.country_scope.map({'us_only': 'US', 'non_us': 'non-US', 'multi_incl_us': 'non-US'})
f['industry'] = f.industry_scope.map({'single': 'single/few', 'few': 'single/few', 'cross': 'cross'})
f['target'] = f.target_listing.map({'public': 'public', 'private': 'private'})
mk = f.Y.map(RAW_MARKET).fillna(f.Y_tax.map(MARKET)); ev = f.Y.map(RAW_EVENT).fillna(f.Y_tax.map(EVENT))
f['evaluator'] = mk.where(mk == 'F').map({'F': 'firm'}).fillna(((mk == 'C') & (ev == 'D')).map({True: 'investors', False: None}))
f['silo'] = f.field.where(f.field.isin(['strategy', 'finance', 'accounting']))
g = pd.read_csv('grades_by_silo.csv'); cr = g[g.grade == 'credible'].groupby('mech_g').field.nunique()
# DD-ANYWHERE (2026-11-01): count due diligence wherever it appears in a chain (X, mechanism or Y), using the
# high-confidence labels judged by reading (_work_dd/dd_labels.jsonl); such rows are added under mech_g='due_diligence'.
_L = [json.loads(l) for l in open('../_work_dd/dd_labels.jsonl') if l.strip()]
_S = {r['role']: set() for r in _L}
for r in _L:
    if r['confidence'] == 'high': _S[r['role']].add(r['label'])
_dd = f[f.X.isin(_S.get('X', set())) | f.mechanism.isin(_S.get('mechanism', set())) | f.Y.isin(_S.get('Y', set()))].copy()
_dd['mech_g'] = 'due_diligence'
f = pd.concat([f[f.mech_g != 'due_diligence'], _dd])
M = sorted(cr[cr >= 2].index); f = f[f.mech_g.isin(M)]
out = []; P = lambda *x: (print(*x), out.append(' '.join(map(str, x))))
ATTR = {'evaluator': ('firm', 'investors'), 'country': ('US', 'non-US'), 'industry': ('single/few', 'cross'), 'target': ('public', 'private'),
        'sample_era': ('pre-1995', '2005+')}
P(f'=== {len(M)} mechanisms credible in >=2 silos | rows {len(f)} | papers {f.paper_id.nunique()}')
P('coverage:', {k: int(f[k].notna().sum()) for k in ATTR})
P('\n=== pooled support by attribute level (paper x mechanism units)')
for at, (lo, hi) in ATTR.items():
    u = f.dropna(subset=[at]).groupby([at, 'mech_g', 'paper_id'], observed=True).sup.mean().reset_index()
    s = u.groupby(at, observed=True).sup.agg(['mean', 'count'])
    P(f'{at:<11} ' + ' | '.join(f'{lv}: {s.loc[lv, "mean"]:.2f} (n={int(s.loc[lv, "count"])})' for lv in s.index))
P('\n=== per mechanism x attribute: HOLDS / PARTIAL / SPLITS (both levels >=3 papers); blank = too thin to test')
rows = []
for m in M:
    r = {'mechanism': m}
    for at, (lo, hi) in ATTR.items():
        u = f[(f.mech_g == m)].dropna(subset=[at]).groupby([at, 'paper_id'], observed=True).sup.mean().reset_index()
        s = u.groupby(at, observed=True).sup.agg(['mean', 'count'])
        if lo in s.index and hi in s.index and s.loc[lo, 'count'] >= 3 and s.loc[hi, 'count'] >= 3:
            a1, a2 = s.loc[lo, 'mean'], s.loc[hi, 'mean']
            r[at] = 'HOLDS' if (a1 >= .7 and a2 >= .7) else ('SPLITS' if abs(a1 - a2) >= .25 else 'PARTIAL')
            r[at + '_detail'] = f'{lo} {a1:.2f}/{int(s.loc[lo,"count"])} vs {hi} {a2:.2f}/{int(s.loc[hi,"count"])}'
        else: r[at] = ''
    rows.append(r)
t = pd.DataFrame(rows); P(t[['mechanism'] + list(ATTR)].to_string(index=False))
tested = (t[list(ATTR)] != '').sum().sum(); holds = (t[list(ATTR)] == 'HOLDS').sum().sum(); splits = (t[list(ATTR)] == 'SPLITS').sum().sum()
P(f'\ncells testable {tested} of {len(M) * len(ATTR)} | HOLDS {holds} | PARTIAL {tested - holds - splits} | SPLITS {splits}')
P('\nSPLITS detail:')
for r in rows:
    for at in ATTR:
        if r.get(at) == 'SPLITS': P(f'  {r["mechanism"]:<32} {at:<11} {r[at + "_detail"]}')
t.to_csv('external_lr_cells.csv', index=False, float_format='%.10g'); open('RESULTS_external.txt', 'w').write('\n'.join(out) + '\n')
