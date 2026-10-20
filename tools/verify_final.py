# -*- coding: utf-8 -*-
import json, sys
sys.path.insert(0, '/home/user/BattleCat')
from data import player_profile as PP
D = sys.argv[1]; THIRD = int(sys.argv[2])     # 第三張黑金卷放哪格
POOLS = {'1077': D+'/dl1077/full1077.json', '1078': D+'/dl1077/full1078.json',
         '1043': D+'/dl1077/full_2026-10-09_1043.json', '991': D+'/dl1077/full_2026-10-13_991.json',
         '946': D+'/dl1077/full_2026-10-11_946.json', '1059': D+'/dl1077/full_2026-10-13_1059.json',
         '942': D+'/dl1077/full_2026-10-05_942.json', '黑金卷': D+'/full1064.json'}
P = {k: json.load(open(v)) for k, v in POOLS.items()}
HI = ('exclusive', 'uber', 'uber_fest', 'legend')
def cell(p, n): return P[p]['res']['A'][str(n)]
LEGCELLS = {19, 21, THIRD}
CHOICE = {24: '1077', 26: '1077', 44: '1077', 46: '1077', 47: '1077'}

last, rare, leg, haul, ok = '冥佑天女露娜夏', 0, 0, [], True
print(f'第三張黑金卷放 {THIRD}A\n格    池       抽到                 備註')
for n in range(2, 48):
    pool = '黑金卷' if n in LEGCELLS else CHOICE.get(n, '1077')
    cat, rar, _ = cell(pool, n)
    if cat == last:
        print(f'{n:3d}A  !! 與上一抽重複 ({cat}) -> REROLL 換軌'); ok = False; break
    if pool == '黑金卷': leg += 1
    else: rare += 1
    note = ''
    if rar in HI:
        dup = cat in PP.OWNED or cat in [h[1] for h in haul]
        note = '★超激 ' + ('重複!' if dup else '未持有')
        if not dup: haul.append((n, cat, pool, rar))
    print(f'{n:3d}A  {pool:7s} {cat:16s} {note}')
    last = cat
print(f'\n驗證：{"全程不觸發 reroll ✓" if ok else "有問題 ✗"}')
print(f'成本：稀有卷 {rare}、黑金卷 {leg}、罐頭 0'
      f'   （手上 稀有卷 {PP.RESOURCES["稀有卷"]}、黑金卷 {PP.RESOURCES["黑金卷"]}、罐頭 {PP.RESOURCES["罐頭"]}）')
print(f'剩餘：稀有卷 {PP.RESOURCES["稀有卷"]-rare}、黑金卷 {PP.RESOURCES["黑金卷"]-leg}、罐頭 2000')
print(f'\n收穫 {len(haul)} 隻未持有超激：')
for n, c, p, r in haul:
    print(f'  {n:3d}A  {c:16s} [{r}]  ({p})')
