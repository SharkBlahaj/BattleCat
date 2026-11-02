# -*- coding: utf-8 -*-
"""驗證玩家實際走的路線（2A→46A），並列出收穫與資源消耗。"""
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
def cell(p, n): return P[p]['res']['A'][str(n)]

# 玩家實際的選擇
LEG = {19, 21}                     # 只用了兩張黑金卷
CHOICE = {44: '991'}               # 44A 抽偉大神們
PREV_OWNED = set(PP.OWNED)

last, rare, leg, haul = '冥佑天女露娜夏', 0, 0, []
ok = True
for n in range(2, 47):
    pool = '黑金卷' if n in LEG else CHOICE.get(n, '1077')
    cat, rar, _ = cell(pool, n)
    if cat == last:
        print(f'{n}A  !! 與上一抽重複（{cat}）→ 會觸發 reroll 換軌'); ok = False; break
    if pool == '黑金卷': leg += 1
    else: rare += 1
    if rar in HI and cat not in PREV_OWNED and cat not in [h[1] for h in haul]:
        haul.append((n, cat, pool, rar))
        print(f'  {n:3d}A  {pool:7s} {cat:16s} [{rar}] ★新收')
    last = cat

print(f'\n逐格驗證：{"全程不觸發 reroll ✓" if ok else "✗"}')
print(f'抽數 {rare + leg}（稀有卷 {rare} + 黑金卷 {leg}），罐頭 0')
r = PP.RESOURCES
print(f'\n資源：稀有卷 {r["稀有卷"]} - {rare} = {r["稀有卷"]-rare}'
      f'  |  黑金卷 {r["黑金卷"]} - {leg} = {r["黑金卷"]-leg}'
      f'  |  罐頭 {r["罐頭"]} 不變')
print(f'\n新收 {len(haul)} 隻超激：' + '、'.join(h[1] for h in haul))
json.dump([h[1] for h in haul], open(D + '/haul.json', 'w'), ensure_ascii=False)
