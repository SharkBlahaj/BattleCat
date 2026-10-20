# -*- coding: utf-8 -*-
"""沿 A 軌單抽前進，累計成本與「不重複」的未持有超激收穫。
reroll 牆：食物池在 19A/21A/50A 會重複而換軌，只有黑金卷能拆。"""
import json, sys
sys.path.insert(0, '/home/user/BattleCat')
from data import player_profile as PP
D = sys.argv[1]
POOLS = {'1077': D+'/dl1077/full1077.json', '1078': D+'/dl1077/full1078.json',
         '1043': D+'/dl1077/full_2026-10-09_1043.json', '991': D+'/dl1077/full_2026-10-13_991.json',
         '946': D+'/dl1077/full_2026-10-11_946.json', '1059': D+'/dl1077/full_2026-10-11_946.json',
         '942': D+'/dl1077/full_2026-10-05_942.json', '黑金卷': D+'/full1064.json'}
POOLS['1059'] = D+'/dl1077/full_2026-10-13_1059.json'
P = {k: json.load(open(v)) for k, v in POOLS.items()}
HI = ('exclusive', 'uber', 'uber_fest', 'legend')
WALL = {19, 21, 50}          # 食物池會觸發 reroll 的格
def cell(p, n): return P[p]['res']['A'][str(n)]

picked, draws, leg = [], 0, 0
rows = []
for n in range(2, 71):
    if n in WALL:
        c, r, _ = cell('黑金卷', n)
        leg += 1; draws += 1
        new = c not in PP.OWNED and c not in [x[1] for x in picked]
        if r in HI and new: picked.append((n, c, '黑金卷'))
        rows.append((n, f'黑金卷(拆reroll) -> {c}' + ('  ★' if r in HI and new else ''), draws, leg))
        continue
    best = None
    for p in P:
        if p == '黑金卷': continue
        c, r, _ = cell(p, n)
        if r in HI and c not in PP.OWNED and c not in [x[1] for x in picked]:
            best = (c, p); break
    draws += 1
    if best:
        picked.append((n, best[0], best[1]))
        rows.append((n, f'{best[1]} -> {best[0]}  ★超激', draws, leg))
    else:
        rows.append((n, '', draws, leg))

print('走到    用掉抽數  其中黑金卷  需稀有卷  累計未持有超激')
for n, what, d, l in rows:
    if what:
        got = len([1 for x in picked if x[0] <= n])
        print(f'{n:3d}A   {d:6d}    {l:6d}      {d-l:6d}     {got:2d}   {what}')
print(f'\n手上：稀有卷 {PP.RESOURCES["稀有卷"]}、黑金卷 {PP.RESOURCES["黑金卷"]}、罐頭 {PP.RESOURCES["罐頭"]}')
for n, what, d, l in rows:
    if d - l <= PP.RESOURCES['稀有卷'] and l <= PP.RESOURCES['黑金卷']:
        far = (n, d, l)
print(f'只用卷（0 罐頭）最遠可走到 {far[0]}A：共 {far[1]} 抽 = 稀有卷 {far[1]-far[2]} + 黑金卷 {far[2]}')
print('\n沿途可收（不重複）：')
for n, c, p in picked:
    if n <= far[0]:
        print(f'  {n:3d}A  {c:14s} ({p})')
