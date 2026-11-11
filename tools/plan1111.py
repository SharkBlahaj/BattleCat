# -*- coding: utf-8 -*-
"""2026-11-11 的規劃：24A 出發，39 金卷 / 3750 罐頭 / 白金卷 1 / 黑金卷 1。
必中只有 1080 與 926 有（1500 罐頭、換軌）。白金卷只能抽 1071，黑金卷只能抽 1072。
這兩個池都不是貓咪祭，所以 uber_fest／supa_fest 的格實際吐雜魚，不算數。
"""
import json, sys, os
sys.path.insert(0, '/home/user/BattleCat')
from data import player_profile as PP

D = sys.argv[1]
EV = {'1080': '2026-11-09_1080', '926': '2026-11-09_926',
      '1071': '2026-10-16_1071', '1072': '2026-10-16_1072'}
P = {k: json.load(open(os.path.join(D, 'dl1111', f'full_{e}.json'))) for k, e in EV.items()}
HI = {'exclusive', 'uber', 'legend'}
FOOD = ['1080', '926']          # 金卷／罐頭可抽，且有必中
TICKET = {'1071': 'plat', '1072': 'leg'}
GUAR_COST = 1500
SINGLE = 150


def res(k, s, n):
    return P[k]['res'][s].get(str(n))


def rr(k, s, n):
    return P[k]['reroll'][s].get(str(n))


def gu(k, s, n):
    return P[k]['guar'][s].get(str(n))


def options(s, n, got):
    """這一格有哪些「未持有且沒收過」的選擇 -> [(池, 角色, 付費種類)]"""
    out = []
    for k in FOOD:
        v = res(k, s, n)
        if v and v[1] in HI and v[0] not in PP.OWNED and v[0] not in got:
            out.append((k, v[0], 'food'))
    for k, kind in TICKET.items():
        v = res(k, s, n)
        if v and v[1] in HI and v[0] not in PP.OWNED and v[0] not in got:
            out.append((k, v[0], kind))
    return out


def step(k, s, n, last):
    v = res(k, s, n)
    if not v:
        return None
    c = v[0]
    if c != last:
        return c, (s, n + 1)
    x = rr(k, s, n)
    if not x:
        return None
    d = x[2]
    return x[0], (d[-1], int(d[:-1]))


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


def walk(s, n, last, tick, food, plat, leg, got, log):
    """一格一格走到資源用完；每格優先拿食物池的新超激，票券留給只有票券拿得到的格。"""
    got = set(got)
    while True:
        if not res('1080', s, n):
            break
        opts = options(s, n, got)
        pick = None
        for k, c, kind in opts:
            if kind == 'food':
                pick = (k, c, kind); break
        if pick is None:
            for k, c, kind in opts:
                if (kind == 'plat' and plat > 0) or (kind == 'leg' and leg > 0):
                    pick = (k, c, kind); break
        if pick is None:
            pick = ('1080', None, 'food')          # 過路
        k, c, kind = pick
        o = step(k, s, n, last)
        if not o:
            break
        cat, nxt = o
        isnew = (c is not None and cat == c)
        if kind == 'plat':
            if plat <= 0: break
            plat -= 1; pay = '白金卷'
        elif kind == 'leg':
            if leg <= 0: break
            leg -= 1; pay = '黑金卷'
        elif tick > 0:
            tick -= 1; pay = '金卷'
        elif food >= SINGLE:
            food -= SINGLE; pay = '罐頭'
        else:
            break
        if isnew:
            got.add(cat)
            log.append(f'{n}{s}  {pay}@{k} → {cat}  ★')
        else:
            log.append(f'{n}{s}  {pay}@{k} → {cat}')
        last = cat
        s, n = nxt
    return (s, n), last, tick, food, plat, leg, got


def trim(log, got):
    """砍掉最後一個 ★ 之後的過路步驟，不浪費資源。"""
    idx = max((i for i, x in enumerate(log) if x.endswith('★')), default=-1)
    return log[:idx + 1]


best = None
for k1 in range(0, 25):                      # 先用幾張金卷推進再打必中
    for gp in FOOD:
        log0 = []
        pos0, last0, t0, f0, p0, l0, got0 = walk(
            'A', 24, '黃金貓', k1, 0, 0, 0, set(), log0)
        if pos0 != ('A', 24 + k1):
            continue
        o = guar_pull(gp, 'A', 24 + k1, last0, got0)
        if not o:
            continue
        new, land, gcat = o
        got1 = set(got0) | set(new)
        line = (f'{24+k1}A  必中@{gp}（{GUAR_COST} 罐頭）→ 落點 {land[1]}{land[0]}，保底 {gcat}'
                + (f'　收 {"、".join(new)}' if new else '　無新收穫'))
        log2 = []
        pos2, _, t2, f2, p2, l2, got2 = walk(
            land[0], land[1], gcat, 39 - k1, 3750 - GUAR_COST, 1, 1, got1, log2)
        full = log0 + [line] + log2
        full = trim(full, got2)
        used_t = 39 - t2
        cand = (len(got2), -len(full), k1, gp, got2, full)
        if best is None or cand[:2] > best[:2]:
            best = cand

# 對照：完全不打必中
logA = []
posA, _, tA, fA, pA, lA, gotA = walk('A', 24, '黃金貓', 39, 3750, 1, 1, set(), logA)
logA = trim(logA, gotA)

print(f'【不打必中，留在 A 軌】收 {len(gotA)} 隻：{"、".join(sorted(gotA)) or "無"}')
print(f'【打一發必中換到 B 軌】收 {best[0]} 隻：{"、".join(sorted(best[4]))}')
print(f'　　必中位置 {24+best[2]}A @{best[3]}\n')
print('=' * 70)
for i, x in enumerate(best[5], 1):
    print(f'{i:3d}. {x}')
