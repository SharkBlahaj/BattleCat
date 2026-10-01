# -*- coding: utf-8 -*-
"""兩個活動共用同一條種子軌道的聯合最佳化。

每一抽都推進同一個位置, 但你可以選擇抽哪一邊 — 拿到的是該活動的角色。
狀態 = (位置, 四個目標各自是否到手)，只有 200 x 16 種，可完整解。
"""
import heapq, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "data"))
import track_data as FATE
import track_data_ep2 as EP2

TARGETS = ["Saber", "間桐櫻", "拉斯沃斯", "地獄警官艾瑪"]
BIT = {t: 1 << i for i, t in enumerate(TARGETS)}
FULL = (1 << len(TARGETS)) - 1

BANNERS = [
    ("Fate", FATE.TRACK, 11, FATE.COST_GUARANTEED),
    ("新活動", EP2.TRACK, 15, EP2.COST_GUARANTEED),
]
COST_SINGLE = 150


def mask_of(cats):
    m = 0
    for c in cats:
        if c in BIT:
            m |= BIT[c]
    return m


def moves(pos):
    n, t = int(pos[:-1]), pos[-1]
    out = []
    for name, TR, gd, cg in BANNERS:
        tbl = TR[t]
        if n + 1 in tbl:
            out.append((f"{name} 單抽", COST_SINGLE, (tbl[n][0],), f"{n+1}{t}", name))
        guar, dest = tbl[n][1], tbl[n][2]
        if dest:
            got = tuple(tbl[n + i][0] for i in range(gd - 1)) + (guar,)
            out.append((f"{name} 必中{gd}連", cg, got, dest, name))
    return out


def solve(start):
    dist = {(start, 0): 0}
    par = {}
    pq = [(0, start, 0)]
    while pq:
        c, pos, mask = heapq.heappop(pq)
        if dist.get((pos, mask), 1 << 60) < c:
            continue
        for label, cost, got, nxt, bn in moves(pos):
            nm = mask | mask_of(got)
            nc = c + cost
            if dist.get((nxt, nm), 1 << 60) > nc:
                dist[(nxt, nm)] = nc
                par[(nxt, nm)] = (pos, mask, label, got, cost)
                heapq.heappush(pq, (nc, nxt, nm))
    return dist, par


def trace(par, key):
    out = []
    while key in par:
        pos, mask, label, got, cost = par[key]
        out.append((label, pos, key[0], cost, [g for g in got if g in BIT]))
        key = (pos, mask)
    return list(reversed(out))


def merge(steps):
    o = []
    for lab, f, t, c, u in steps:
        if o and lab == o[-1][0] and "單抽" in lab and o[-1][2] == f:
            p = o[-1]; o[-1] = (lab, p[1], t, p[3] + c, p[4] + u)
        else:
            o.append((lab, f, t, c, u))
    return o


if __name__ == "__main__":
    start = sys.argv[1] if len(sys.argv) > 1 else "4A"
    dist, par = solve(start)
    best = min(((c, p) for (p, m), c in dist.items() if m == FULL), default=None)
    if not best:
        print("無解"); sys.exit()
    cost, pos = best
    steps = merge(trace(par, (pos, FULL)))
    print(f"起點 {start} · 四個目標全拿的最低總成本: {cost} 罐頭")
    print(f"（各自單獨最省相加 = 5400 + 4500 = 9900，省下 {9900 - cost}）\n")
    for i, (lab, f, t, c, u) in enumerate(steps, 1):
        print(f"  {i}. [{lab}] {f} → {t}   {c} 罐頭" + (f"   ★ {'、'.join(u)}" if u else ""))
