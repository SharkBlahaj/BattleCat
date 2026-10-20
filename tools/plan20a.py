# -*- coding: utf-8 -*-
"""從 20A 出發，用 15 金卷 / 1500 罐頭 / 1 黑金卷 盡量多收「未持有」超激。
必中只有 1043、1021 有，且今天到期；必中是唯一的換軌手段。"""
import json, sys, os
from functools import lru_cache
sys.path.insert(0, '/home/user/BattleCat')
from data import player_profile as PP
D = sys.argv[1]
F = {'1043':'full_2026-10-18_1043.json','1021':'full_2026-10-18_1021.json',
     '1070':'full_2026-10-20_1070.json','1004':'full_2026-10-20_1004.json',
     '947':'full_2026-10-20_947.json','1071':'full_2026-10-16_1071.json',
     '1072':'full_2026-10-16_1072.json'}
P = {k: json.load(open(os.path.join(D,'dl1020',f))) for k,f in F.items()}
HI = {'exclusive','uber','uber_fest','legend'}
GUAR = ['1043','1021']                 # 有原生必中
FOOD = ['1043','1021','1070','1004','947']   # 金卷／罐頭可抽
TICKET = {'1072':'黑金卷'}             # 黑金卷專用
START = ('A', 20)
LAST0 = '火精靈梅拉'

def res(k,s,n):
    v = P[k]['res'][s].get(str(n))
    return v if v else None
def rr(k,s,n):
    return P[k]['reroll'][s].get(str(n))
def gu(k,s,n):
    return P[k]['guar'][s].get(str(n))

def draw(k, s, n, last):
    v = res(k,s,n)
    if not v: return None
    c, r, _ = v
    if c != last:
        return c, r, (s, n+1)
    x = rr(k,s,n)
    if not x: return None
    d = x[2]
    return x[0], 'rare', (d[-1], int(d[:-1]))

def guar_pull(k, s, n, last):
    """10 格普通抽 + 保底。回傳 (收到的超激清單, 落點, 最後一隻貓)。"""
    g = gu(k,s,n)
    if not g: return None
    cur, L, ub = (s,n), last, []
    for _ in range(10):
        o = draw(k, cur[0], cur[1], L)
        if o is None: return None
        c, r, cur = o
        if r in HI: ub.append(c)
        L = c
    ub.append(g[0])
    d = g[2]
    return ub, (d[-1], int(d[:-1])), g[0]

best = {'n': -1}
def rec(pos, last, rare, food, leg, used_g, got, path):
    key = len(got)
    if key > best['n'] or (key == best['n'] and len(path) < len(best.get('path', []))):
        best.update(n=key, got=set(got), path=list(path), left=(rare, food, leg))
    s, n = pos
    if n > 95: return
    # 必中（1500 罐頭，只有今天）
    if food >= 1500 and not used_g:
        for k in GUAR:
            o = guar_pull(k, s, n, last)
            if not o: continue
            ub, np_, L = o
            new = [c for c in ub if c not in PP.OWNED and c not in got]
            rec(np_, L, rare, food-1500, leg, True, got | set(new),
                path + [f'{n}{s} 必中@{k} → {np_[1]}{np_[0]}' + (f'  收{"、".join(new)}' if new else '  無收穫')])
    # 單抽：金卷／罐頭（食物池）或黑金卷（1072）
    for k in FOOD + list(TICKET):
        o = draw(k, s, n, last)
        if not o: continue
        c, r, np_ = o
        new = (r in HI) and c not in PP.OWNED and c not in got
        if k in TICKET:
            if leg <= 0: continue
            opts = [(rare, food, leg-1, '黑金卷')]
        else:
            opts = []
            if rare > 0: opts.append((rare-1, food, leg, '金卷'))
            if food >= 150: opts.append((rare, food-150, leg, '罐頭'))
        for r2, f2, l2, pay in opts:
            if not new and not (r in HI):
                # 純過路：只保留最省的一種付費，避免爆炸
                if pay == '罐頭' and rare > 0: continue
            rec(np_, c, r2, f2, l2, used_g, got | ({c} if new else set()),
                path + ([f'{n}{s} {pay}@{k} → {c} ★'] if new else [f'{n}{s} {pay}@{k}']))

sys.setrecursionlimit(10000)
rec(START, LAST0, 15, 1500, 1, False, frozenset(), [])
print(f'最多能收 {best["n"]} 隻未持有超激：{"、".join(sorted(best["got"]))}')
print(f'剩餘：金卷 {best["left"][0]}、罐頭 {best["left"][1]}、黑金卷 {best["left"][2]}')
print('\n路線：')
for i, step in enumerate(best['path'], 1):
    print(f'  {i:2d}. {step}')
