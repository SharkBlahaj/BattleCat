# -*- coding: utf-8 -*-
"""反推 2026-10-20 的實際走法：1A --金卷--> 必中(真田) --金卷--> 成田甲斐。"""
import json, sys, os
sys.path.insert(0, '/home/user/BattleCat')
from data import player_profile as PP
D = sys.argv[1]
POOLS = {k: json.load(open(os.path.join(D, 'dl1020', f))) for k, f in {
    '1043': 'full_2026-10-18_1043.json', '1021': 'full_2026-10-18_1021.json',
    '1070': 'full_2026-10-20_1070.json', '1004': 'full_2026-10-20_1004.json',
    '947':  'full_2026-10-20_947.json',  '1071': 'full_2026-10-16_1071.json',
    '1072': 'full_2026-10-16_1072.json'}.items()}
HI = {'exclusive', 'uber', 'uber_fest', 'legend'}
d = POOLS['1043']
res = {s: {int(n): v for n, v in d['res'][s].items()} for s in 'AB'}
rr  = {s: {int(n): v for n, v in d['reroll'][s].items()} for s in 'AB'}
gu  = {s: {int(n): v for n, v in d['guar'][s].items()} for s in 'AB'}

def sim_guar(side, n0):
    cur, L, ub = (side, n0), None, []
    for _ in range(10):
        s, n = cur
        c, r, _ = res[s][n]
        if c == L:
            x = rr[s][n]; c = x[0]; dest = x[2]; cur = (dest[-1], int(dest[:-1]))
        else: cur = (s, n + 1)
        if r in HI: ub.append(c)
        L = c
    g = gu[side][n0]
    return ub + [g[0]], g[0], g[2]

print('候選：從 1A 用金卷推進 k 格後打必中，保底是真田幸村、且這發不含前田慶次，')
print('      落點之後還走得到 15A（成田甲斐）\n')
for k in range(0, 20):
    p = 1 + k
    if p not in gu['A']: continue
    ub, guar, dest = sim_guar('A', p)
    if guar != '真田幸村' or '前田慶次' in ub: continue
    ds, dn = dest[-1], int(dest[:-1])
    if ds != 'A' or dn > 15: continue
    after = 15 - dn + 1          # 落點起算，抽到 15A 需要幾次單抽
    print(f'  推進 {k} 格 -> 在 {p}A 打必中（{"、".join(ub)}）-> 落點 {dest}')
    print(f'     之後再用 {after} 張金卷就會抽到 15A 成田甲斐，結束在 {15+1}A')
    print(f'     金卷合計 {k + after} 張，罐頭 1500')

print('\n推進用的 1A／2A 這兩格，各池給什麼：')
for k, dd in POOLS.items():
    row = [dd['res']['A'][str(n)] for n in (1, 2)]
    mark = lambda t: f'{t[0]}{"  ★超激" if t[1] in HI else ""}{"（已有）" if t[0] in PP.OWNED else ""}'
    print(f'  {k:5s} 1A={mark(row[0]):28s} 2A={mark(row[1])}')
print('\n必中落點後的 14A／15A：')
for k, dd in POOLS.items():
    row = [dd['res']['A'][str(n)] for n in (14, 15)]
    mark = lambda t: f'{t[0]}{"  ★超激" if t[1] in HI else ""}{"（已有）" if t[0] in PP.OWNED else ""}'
    print(f'  {k:5s} 14A={mark(row[0]):28s} 15A={mark(row[1])}')
