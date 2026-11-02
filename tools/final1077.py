# -*- coding: utf-8 -*-
import json, sys
sys.path.insert(0, '/home/user/BattleCat')
from data import player_profile as PP
D = sys.argv[1]
POOLS = {'1077': D+'/dl1077/full1077.json', '1078': D+'/dl1077/full1078.json',
         '1043': D+'/dl1077/full_2026-10-09_1043.json', '991': D+'/dl1077/full_2026-10-13_991.json',
         '946': D+'/dl1077/full_2026-10-11_946.json', '1059': D+'/dl1077/full_2026-10-13_1059.json',
         '942': D+'/dl1077/full_2026-10-05_942.json', '黑金卷': D+'/full1064.json'}
P = {k: json.load(open(v)) for k, v in POOLS.items()}
HI = ('exclusive', 'uber', 'uber_fest', 'legend')
def cell(p, s, n): return P[p]['res'][s][str(n)]

print('=== 2A~70A A 軌每一個高稀有格，各池給什麼 ===')
print('（粗體=你沒有的；黑金卷那欄食物池給雜魚時才值得用票）\n')
for n in range(2, 71):
    opts = {}
    for p in P:
        c, r, _ = cell(p, 'A', n)
        if r in HI:
            opts.setdefault(c, []).append(p)
    if not opts: continue
    food_has = any(p != '黑金卷' for ps in opts.values() for p in ps)
    flag = '' if food_has else '   ← 只有黑金卷拿得到'
    print(f'{n:3d}A{flag}')
    for c, ps in sorted(opts.items(), key=lambda kv: kv[0]):
        own = '已有' if c in PP.OWNED else '★'
        print(f'      {own} {c:14s}  ({", ".join(sorted(ps))})')
