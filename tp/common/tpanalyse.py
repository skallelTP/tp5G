"""Outils communs d'analyse des résultats OMNeT++/Simu5G exportés avec tp-export (format CSV-R).

Usage dans un notebook :
    import sys; sys.path.append('/tp/common')
    from tpanalyse import load_scalars, kpi_par_run
"""
import pandas as pd

def load_scalars(csv_path):
    """Charge un export CSV-R et renvoie (scalaires, variables d'itération par run)."""
    df = pd.read_csv(csv_path)
    sca = df[df.type == 'scalar'][['run', 'module', 'name', 'value']].copy()
    sca['value'] = pd.to_numeric(sca['value'], errors='coerce')
    iv = df[df.type == 'itervar'][['run', 'attrname', 'attrvalue']]
    iv = iv.pivot_table(index='run', columns='attrname', values='attrvalue', aggfunc='first')
    for col in iv.columns:
        try: iv[col] = pd.to_numeric(iv[col])
        except (ValueError, TypeError): pass
    return sca, iv

def kpi_par_run(sca, iv, name, module_filter=None, agg='mean'):
    """Moyenne (ou autre agrégat) d'un scalaire sur tous les modules d'un run, jointe aux itervars.
    name : ex. 'voIPFrameDelay:mean'   module_filter : ex. 'ue['   agg : 'mean' | 'max' | 'sum'
    """
    d = sca[sca.name == name]
    if module_filter:
        d = d[d.module.str.contains(module_filter, regex=False)]
    g = d.groupby('run')['value'].agg(agg).rename(name)
    return iv.join(g, how='inner').reset_index()


def load_vectors(csv_path):
    """Charge un export CSV-R de vecteurs (tp-export-vec) et renvoie un DataFrame long :
    colonnes run, module, name, t (s), value — une ligne par point."""
    import numpy as np
    df = pd.read_csv(csv_path)
    vec = df[df.type == 'vector'][['run', 'module', 'name', 'vectime', 'vecvalue']]
    rows = []
    for _, r in vec.iterrows():
        t = np.fromstring(str(r.vectime), sep=' ')
        v = np.fromstring(str(r.vecvalue), sep=' ')
        rows.append(pd.DataFrame({'run': r.run, 'module': r.module, 'name': r['name'], 't': t, 'value': v}))
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(columns=['run','module','name','t','value'])
