"""OS pilot on the eval set S (541 papers): (a) accumulation WITHIN each market, (b) CONNECT markets for mechanisms credible in
both. Deterministic counts on coded fields (no LLM). Inputs: ../findings_eval_tax.csv, market_maps.py.
Market: F = a firm evaluates a firm (factor market); C = investors evaluate a firm. Investor side restricted to DEAL-TRIGGERED
evaluations (EVENT=='D'); 'U' (unclear) shown as a sensitivity. Units: paper-level (a paper counts once per mechanism x market).
Credible = >=4 papers, >=1 causal-design paper, paper-level support >=0.70, >=2 fields. Sensitivity: looser/stricter cutoffs."""
import pandas as pd, numpy as np, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '.')
from market_maps import MARKET, EVENT, RAW_MARKET, RAW_EVENT
f = pd.read_csv('../findings_eval_tax.csv')
f['market'] = f.Y.map(RAW_MARKET).fillna(f.Y_tax.map(MARKET)).fillna('O'); f['event'] = f.Y.map(RAW_EVENT).fillna(f.Y_tax.map(EVENT))
f['sup'] = f.support.map({'supported': 1, 'rejected': 0, 'mixed': .5})
CAUSAL = ('natural_experiment', 'did', 'difference_in_differences', 'instrumental', 'iv', 'regression_discontinuity', 'rdd', 'field_experiment', 'lab_experiment', 'quasi_experiment')
f['causal'] = f.identification.fillna('').str.lower().str.split(r'[;, ]+').apply(lambda t: any(x in CAUSAL for x in t))
f['fld'] = f.field.where(f.field.isin(['strategy', 'finance', 'accounting']), 'other')
f['era'] = pd.cut(f.year, [0, 1999, 2009, 2100], labels=['<2000', '2000s', '2010+'])
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s)
def side(df, inv='D'):
    keep = (df.market == 'F') | ((df.market == 'C') & df.event.isin(list(inv)))
    return df[keep & df.sup.notna()]
def paper_level(d):
    return d.groupby(['market', 'mech_g', 'paper_id']).agg(sup=('sup', 'mean'), causal=('causal', 'max'), fld=('fld', 'first'), era=('era', 'first')).reset_index()
def grades(pm, n=4, s=.70, fields=2, need_causal=True):
    m = pm.groupby(['market', 'mech_g']).agg(papers=('paper_id', 'nunique'), support=('sup', 'mean'), causal=('causal', 'sum'), fields=('fld', 'nunique')).reset_index()
    m['credible'] = (m.papers >= n) & (m.support >= s) & (m.fields >= fields) & ((m.causal >= 1) if need_causal else True)
    return m
d = side(f); pm = paper_level(d)
P('=== S: rows', len(f), '| F rows', int((f.market == 'F').sum()), '| C rows', int((f.market == 'C').sum()),
  '(D', int(((f.market == 'C') & (f.event == 'D')).sum()), 'E', int(((f.market == 'C') & (f.event == 'E')).sum()), 'U', int(((f.market == 'C') & (f.event == 'U')).sum()), ')')
P('\n=== (a) ACCUMULATION WITHIN EACH MARKET (investor side = deal-triggered)')
cells = d.groupby(['market', 'mech_g', 'Y_tax']).paper_id.nunique().reset_index(name='papers')
for mk in ['F', 'C']:
    c = cells[cells.market == mk]
    P(f'{mk}: finding cells (mechanism x outcome) {len(c)} | tested by ONE paper {(c.papers == 1).mean():.1%} | by >=3 papers {(c.papers >= 3).mean():.1%}')
g = grades(pm)
for mk in ['F', 'C']:
    m = g[g.market == mk]
    P(f'{mk}: mechanisms {len(m)} | single-paper {int((m.papers == 1).sum())} | credible {int(m.credible.sum())}')
both = sorted(set(g[(g.market == 'F') & g.credible].mech_g) & set(g[(g.market == 'C') & g.credible].mech_g))
P('credible in BOTH markets:', len(both), both)
def compare(pmx, mechs, label):
    x = pmx[pmx.mech_g.isin(mechs)]
    sF, sC = x[x.market == 'F'].sup.mean(), x[x.market == 'C'].sup.mean()
    P(f'{label:<40} F {sF:.3f} (n={int((x.market == "F").sum())})  C {sC:.3f} (n={int((x.market == "C").sum())})  gap {sF - sC:+.3f}')
P('\n=== (b) CONNECT MARKETS — support, firms (F) vs investors (C), mechanisms credible in both; paper-level units')
compare(pm, both, 'MAIN (C = deal-triggered)')
pmU = paper_level(side(f, 'DU')); compare(pmU, both, 'sens: C incl. unclear (D+U)')
pmA = paper_level(side(f, 'DEU')); compare(pmA, both, 'sens: C all investor outcomes (D+E+U)')
allm = sorted(set(pm[pm.market == 'F'].mech_g) & set(pm[pm.market == 'C'].mech_g)); compare(pm, allm, 'sens: ALL mechanisms seen in both')
for lab, kw in [('looser (>=3 papers, >=.6, no causal req)', dict(n=3, s=.6, need_causal=False)), ('stricter (>=6 papers, >=.7, causal)', dict(n=6, s=.7))]:
    gg = grades(pm, **kw); bb = set(gg[(gg.market == 'F') & gg.credible].mech_g) & set(gg[(gg.market == 'C') & gg.credible].mech_g)
    compare(pm, bb, f'sens: cutoffs {lab} [{len(bb)} mech]')
P('\n--- by design (credible-in-both mechanisms)')
for cz, lab in [(True, 'causal'), (False, 'non-causal')]: compare(pm[pm.causal == cz], both, f'design {lab}')
P('--- by era')
for e in ['<2000', '2000s', '2010+']: compare(pm[pm.era == e], both, f'era {e}')
P('--- by field')
for fl in ['finance', 'strategy', 'accounting']: compare(pm[pm.fld == fl], both, f'field {fl}')
x = side(f).groupby(['paper_id', 'mech_g', 'market']).sup.mean().unstack().dropna()
x = x[x.index.get_level_values(1).isin(both)]
P(f'--- same paper, same mechanism, both markets: {len(x)} pairs | F {x.F.mean():.3f} C {x.C.mean():.3f}')
P('\n--- per mechanism (credible in both)')
t = pm[pm.mech_g.isin(both)].groupby(['mech_g', 'market']).agg(n=('paper_id', 'nunique'), s=('sup', 'mean')).unstack()
t[('gap', '')] = t[('s', 'F')] - t[('s', 'C')]
P(t.sort_values(('gap', '')).round(2).to_string())

# (c) INFORMATION MECHANISMS ONLY: the credible-in-both mechanisms that are also information mechanisms
# (information mechanism = one of the 14 groups in ../_work_measure/info_chains_by_measure_kind.csv)
INFO = set(pd.read_csv('../_work_measure/info_chains_by_measure_kind.csv').mech_g.unique())
both_info = [m for m in both if m in INFO]
P('\n=== (c) INFORMATION MECHANISMS ONLY: credible in both markets AND an information mechanism:', len(both_info), both_info)
def fc(x, label):
    P(f'{label:<40} F {x[x.market == "F"].sup.mean():.3f} (n={int((x.market == "F").sum())})  C {x[x.market == "C"].sup.mean():.3f} (n={int((x.market == "C").sum())})  gap {x[x.market == "F"].sup.mean() - x[x.market == "C"].sup.mean():+.3f}')
pi = pm[pm.mech_g.isin(both_info)]
fc(pi, 'MAIN information mechanisms')
fc(pi[pi.causal], 'design causal')
fc(pi[~pi.causal], 'design non-causal')
for fl in ['finance', 'strategy', 'accounting']: fc(pi[pi.fld == fl], 'field ' + fl)
xi = pi.groupby(['paper_id', 'mech_g', 'market']).sup.mean().unstack().dropna()
P(f'--- same paper, same mechanism, both markets: {len(xi)} pairs | F {xi.F.mean():.3f} C {xi.C.mean():.3f}')
g.to_csv('mechanism_market_grades.csv', index=False, float_format='%.10g'); t.to_csv('credible_both_by_mechanism.csv', float_format='%.10g')
open('RESULTS.txt', 'w').write('\n'.join(out) + '\n')
