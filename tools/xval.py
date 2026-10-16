import sys, json, importlib
sys.path.insert(0, '/home/user/BattleCat')
new = json.load(open(sys.argv[1]))
newT = {s: {int(k): v for k, v in new[s].items()} for s in 'AB'}

from data import track_data_v3 as V3
from data import track_ep3 as E3
from data import track_ep4 as E4
from data import track_tickets as TK

def norm(d):
    out = {}
    for k, v in d.items():
        out[int(k)] = v[0] if isinstance(v, (tuple, list)) else v
    return out

tables = {
    'Fate(v3)':  {'A': norm(V3.A), 'B': norm(V3.B)},
    'ep3':       {'A': norm(E3.A), 'B': norm(E3.B)},
    'ep4':       {'A': norm(E4.A), 'B': norm(E4.B)},
    'platinum':  {'A': norm(TK.PLATINUM['A']), 'B': norm(TK.PLATINUM['B'])},
    'legend':    {'A': norm(TK.LEGEND['A']),   'B': norm(TK.LEGEND['B'])},
}

print('--- test: new[ns][n] == old[os][n+off] ---')
for name, T in tables.items():
    for ns, os_, off in [('A','B',96), ('B','A',97)]:
        ok = bad = 0; badl = []
        for n, (cat, rar) in sorted(newT[ns].items()):
            o = T[os_].get(n + off)
            if o is None: continue
            if o == cat: ok += 1
            else: bad += 1; badl.append((f'{n}{ns}', cat, o))
        print(f'{name:10s} new{ns} vs old{os_}+{off}: ok={ok} bad={bad} {badl}')
