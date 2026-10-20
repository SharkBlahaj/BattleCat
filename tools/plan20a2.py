# -*- coding: utf-8 -*-
"""從 20A 的線性規劃：走路是一條線，決策只有「必中打在哪一格」與「每格抽哪個池」。"""
import json, sys, os
sys.path.insert(0, '/home/user/BattleCat')
from data import player_profile as PP

D = sys.argv[1]
F = {'1043': 'full_2026-10-18_1043.json', '1021': 'full_2026-10-18_1021.json',
     '1070': 'full_2026-10-20_1070.json', '1004': 'full_2026-10-20_1004.json',
     '947':  'full_2026-10-20_947.json',  '1071': 'full_2026-10-16_1071.json',
     '1072': 'full_2026-10-16_1072.json'}
P = {k: json.load(open(os.path.join(D, 'dl1020', f))) for k, f in F.items()}
HI = {'exclusive', 'uber', 'uber_fest', 'legend'}
GUAR = ['1043', '1021']                              # 今天最後一天有必中
FOOD = ['1043', '1021', '1070', '1004', '947']       # 金卷／罐頭可抽
LEGP = '1072'                                        # 黑金卷專用


def res(k, s, n):
    return P[k]['res'][s].get(str(n))


def rr(k, s, n):
    return P[k]['reroll'][s].get(str(n))


def gu(k, s, n):
    return P[k]['guar'][s].get(str(n))


def best_at(s, n, got, leg_ok):
    """這一格最好的選擇 -> (角色, 池, 是否新超激, 是否動用黑金卷)"""
    for k in FOOD:
        v = res(k, s, n)
        if v and v[1] in HI and v[0] not in PP.OWNED and v[0] not in got:
            return v[0], k, True, False
    if leg_ok:
        v = res(LEGP, s, n)
        if v and v[1] in HI and v[0] not in PP.OWNED and v[0] not in got:
            return v[0], LEGP, True, True
    v = res('1043', s, n)
    return (v[0] if v else '?'), '1043', False, False


def walk(s, n, last, tickets, food, leg, got, log):
    got = set(got)
    while True:
        if not res('1043', s, n):
            break
        cat, pool, new, useleg = best_at(s, n, got, leg > 0)
        if cat == last:                       # 重複 -> reroll 換軌
            x = rr(pool, s, n)
            if not x:
                break
            cat = x[0]
            d = x[2]
            nxt = (d[-1], int(d[:-1]))
            new = False
        else:
            nxt = (s, n + 1)
        if useleg:
            leg -= 1
            pay = '黑金卷'
        elif tickets > 0:
            tickets -= 1
            pay = '金卷'
        elif food >= 150:
            food -= 150
            pay = '罐頭'
        else:
            break
        if new:
            got.add(cat)
        log.append(f'{n}{s} {pay}@{pool} → {cat}' + ('  ★新超激' if new else ''))
        last = cat
        s, n = nxt
    return (s, n), last, tickets, food, leg, got


def guar_pull(k, s, n, last, got):
    g = gu(k, s, n)
    if not g:
        return None
    cur, L, ub = (s, n), last, []
    for _ in range(10):
        v = res(k, cur[0], cur[1])
        if not v:
            return None
        c, r, _ = v
        if c == L:
            x = rr(k, cur[0], cur[1])
            if not x:
                return None
            c = x[0]
            d = x[2]
            cur = (d[-1], int(d[:-1]))
            r = 'rare'
        else:
            cur = (cur[0], cur[1] + 1)
        if r in HI:
            ub.append(c)
        L = c
    ub.append(g[0])
    d = g[2]
    new = [c for c in ub if c not in PP.OWNED and c not in got]
    return new, (d[-1], int(d[:-1])), g[0]


RARE, FOODB, LEG = 15, 1500, 1
plans = []

log = []
pos, last, t, f, l, got = walk('A', 20, '火精靈梅拉', RARE, FOODB, LEG, set(), log)
plans.append(('不打必中，全部拿來走路', got, log, pos, (t, f, l)))

for k in range(0, RARE + 1):
    log1 = []
    pos1, last1, _, _, _, got1 = walk('A', 20, '火精靈梅拉', k, 0, 0, set(), log1)
    if pos1[1] != 20 + k or pos1[0] != 'A':
        continue
    for gk in GUAR:
        o = guar_pull(gk, pos1[0], pos1[1], last1, got1)
        if not o:
            continue
        new, np_, gcat = o
        line = (f'{pos1[1]}{pos1[0]} 必中@{gk}（1500 罐頭）→ 落點 {np_[1]}{np_[0]}，保底 {gcat}'
                + (f'　收 {"、".join(new)}' if new else '　無新收穫'))
        got2 = set(got1) | set(new)
        log3 = []
        pos3, _, t3, f3, l3, got3 = walk(np_[0], np_[1], gcat,
                                         RARE - k, FOODB - 1500, LEG, got2, log3)
        plans.append((f'金卷走 {k} 格後在 {20+k}A 打 {gk} 的必中',
                      got3, log1 + [line] + log3, pos3, (t3, f3, l3)))

plans.sort(key=lambda p: (-len(p[1]), len(p[2])))
print(f'{"方案":<36}{"收穫":>4}  角色')
for name, got, log, pos, left in plans[:8]:
    print(f'{name:<36}{len(got):>4}  {"、".join(sorted(got))}')

name, got, log, pos, left = plans[0]
print('\n' + '=' * 72)
print(f'最佳：{name}')
print(f'收 {len(got)} 隻　結束在 {pos[1]}{pos[0]}　'
      f'剩 金卷 {left[0]}／罐頭 {left[1]}／黑金卷 {left[2]}')
for i, x in enumerate(log, 1):
    print(f'  {i:2d}. {x}')
