# -*- coding: utf-8 -*-
"""逐格模擬建議路徑，確認不會踩到重複 reroll，並列出收穫與各格可選項。"""
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

PLAN = ([(n, '1077', '稀有卷') for n in range(2, 19)]
        + [(19, '黑金卷', '黑金卷'), (20, '1077', '稀有卷'), (21, '黑金卷', '黑金卷')]
        + [(n, '1077', '稀有卷') for n in range(22, 28)]
        + [(n, '1077', '罐頭') for n in range(28, 36)])

last, food, rare, leg, haul = '冥佑天女露娜夏', 0, 0, 0, []
print('步驟  格   池      付費    抽到              備註')
for n, pool, pay in PLAN:
    cat, rar, _ = cell(pool, 'A', n)
    if cat == last:
        print(f'  !! {n}A 會與上一抽重複 ({cat}) -> 觸發 REROLL 換軌'); break
    food += 150 if pay == '罐頭' else 0
    rare += pay == '稀有卷'; leg += pay == '黑金卷'
    note = ''
    if rar in HI:
        note = '★超激 ' + ('已有' if cat in PP.OWNED else '未持有')
        haul.append((f'{n}A', cat, rar))
    print(f'      {n:3d}A {pool:6s} {pay:6s}  {cat:14s}  {note}')
    last = cat

print(f'\n→ 走到 36A。已用：罐頭 {food}、稀有卷 {rare}、黑金卷 {leg}')
print('\n最後一發：36A 打普通 11 連抽 1077（1500 罐頭）')
cur, L = 36, last
for i in range(11):
    cat, rar, _ = cell('1077', 'A', cur)
    if cat == L:
        print(f'  !! {cur}A 重複 -> REROLL'); break
    mark = '  ★超激 ' + ('已有' if cat in PP.OWNED else '未持有') if rar in HI else ''
    print(f'   第{i+1:2d}抽  {cur:3d}A  {cat}{mark}')
    if rar in HI: haul.append((f'{cur}A', cat, rar))
    L = cat; cur += 1
food += 1500
print(f'\n總計：罐頭 {food}、稀有卷 {rare}、黑金卷 {leg}')
print(f'手上：罐頭 {PP.RESOURCES["罐頭"]}、稀有卷 {PP.RESOURCES["稀有卷"]}、黑金卷 {PP.RESOURCES["黑金卷"]}'
      f'  → 缺罐頭 {food - PP.RESOURCES["罐頭"]}')
print('\n收穫的超激：')
for pos, cat, rar in haul:
    print(f'  {pos:5s} {cat:14s} [{rar}] ' + ('已有' if cat in PP.OWNED else '★未持有'))

print('\n=== 有選擇空間的格子（各池給什麼）===')
for n in (19, 21, 24, 26, 44, 46):
    opts = []
    for p in P:
        c, r, _ = cell(p, 'A', n)
        if r in HI:
            opts.append(f'{p}:{c}' + ('(已有)' if c in PP.OWNED else ''))
    print(f'  {n:3d}A  ' + ('  |  '.join(sorted(set(opts))) if opts else '(無超激)'))
