# -*- coding: utf-8 -*-
"""在預算內最大化「不同超激レア」數量的路徑搜尋。

狀態 = (位置, 已收集超激レア的 bitmask)。超激レア只有 10 種 -> 1024 種組合,
位置 200 格, 共 ~20 萬狀態, Dijkstra 可完整解。
"""
import heapq, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "data"))
from track_data import TRACK, UBERS, COST_SINGLE, COST_GUARANTEED

UL = sorted(UBERS)
BIT = {u: 1 << i for i, u in enumerate(UL)}
SUSPECT = {("B", 60), ("B", 93), ("B", 97)}


def mask_of(cats):
    m = 0
    for c in cats:
        if c in BIT:
            m |= BIT[c]
    return m


def names(mask):
    return [u for u in UL if mask & BIT[u]]


def moves(pos):
    n, t = int(pos[:-1]), pos[-1]
    tbl = TRACK[t]
    out = []
    if n + 1 in tbl and (t, n + 1) not in SUSPECT:
        out.append(("單抽", COST_SINGLE, (tbl[n][0],), f"{n+1}{t}"))
    guar, dest = tbl[n][1], tbl[n][2]
    if dest and not any((t, n + i) in SUSPECT for i in range(1, 10)):
        got = tuple(tbl[n + i][0] for i in range(10)) + (guar,)
        out.append(("必中11連", COST_GUARANTEED, got, dest))
    return out


def search(start):
    """回傳 dist[(pos, mask)] = 最低成本, 以及 parent 供回溯"""
    dist = {(start, 0): 0}
    par = {}
    pq = [(0, start, 0)]
    while pq:
        c, pos, mask = heapq.heappop(pq)
        if dist.get((pos, mask), 1 << 60) < c:
            continue
        for label, cost, got, nxt in moves(pos):
            nm = mask | mask_of(got)
            nc = c + cost
            if dist.get((nxt, nm), 1 << 60) > nc:
                dist[(nxt, nm)] = nc
                par[(nxt, nm)] = (pos, mask, label, got, cost)
                heapq.heappush(pq, (nc, nxt, nm))
    return dist, par


def trace(par, key):
    steps = []
    while key in par:
        pos, mask, label, got, cost = par[key]
        steps.append((label, pos, got, key[0], cost))
        key = (pos, mask)
    return list(reversed(steps))


def best_for_budget(dist, budget, must=()):
    need = mask_of(must)
    best = None
    for (pos, mask), c in dist.items():
        if c > budget or (mask & need) != need:
            continue
        k = (bin(mask).count("1"), -c)
        if best is None or k > best[0]:
            best = (k, pos, mask, c)
    return best


if __name__ == "__main__":
    START = "4A"
    dist, par = search(START)

    # 1) 哪些格子一發必中就同時噴出兩隻以上不同超激レア?
    print("【一發必中就拿到 2 隻以上不同超激レア的格子】")
    for t, tbl in TRACK.items():
        for n in sorted(tbl):
            if not tbl[n][2]:
                continue
            got = [tbl[n + i][0] for i in range(10)] + [tbl[n][1]]
            u = [g for g in got if g in UBERS]
            if len(set(u)) >= 2:
                print(f"  {n}{t}: {'、'.join(u)}   (抽完跳到 {tbl[n][2]})")
    print()

    # 2) 走到 48A 並打出那一發的最低成本
    print("【從 4A 走到 48A 並打出那一發必中】")
    cands = [(c, m) for (p, m), c in dist.items() if p == "48A"]
    cheap = min(cands)[0]
    print(f"  抵達 48A 最低成本: {cheap} 罐頭 (再 +1500 打必中 = {cheap+1500})")
    best = max(((bin(m).count('1'), -c, c, m) for c, m in cands))
    print(f"  抵達 48A 且種類最多: {best[3].bit_count()} 種, {best[2]} 罐頭")
    print()
