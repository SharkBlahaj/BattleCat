# -*- coding: utf-8 -*-
"""列出所有「經過 48A 並在該格拿到 Saber」且最終持有 Saber+間桐櫻的超激レア組合。

分兩段跑 Dijkstra:
  段1  4A -> (48A, mask)
  段2  在 48A 取 Saber (單抽150 -> 49A, 或必中1500 -> 58B 順便再拿一隻櫻)
       之後繼續走, 直到手上同時有 Saber 和 間桐櫻
"""
import heapq, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "data"))
from uber_maximizer import moves, mask_of, names, BIT
from track_data import TRACK, UBERS

SAB, SAK = BIT["Saber"], BIT["間桐櫻"]


def dijkstra(seeds):
    dist = dict(seeds)
    par = {}
    pq = [(c, p, m) for (p, m), c in seeds.items()]
    heapq.heapify(pq)
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


def trace(par, key, stop):
    out = []
    while key in par and key != stop:
        pos, mask, label, got, cost = par[key]
        out.append((label, pos, got, key[0], cost))
        key = (pos, mask)
    return list(reversed(out))


d1, p1 = dijkstra({("4A", 0): 0})

# 在 48A 取 Saber 的兩種方式
seeds, origin = {}, {}
for (pos, mask), c in d1.items():
    if pos != "48A":
        continue
    for label, cost, got, nxt in moves("48A"):
        nm = mask | mask_of(got)
        nc = c + cost
        if seeds.get((nxt, nm), 1 << 60) > nc:
            seeds[(nxt, nm)] = nc
            origin[(nxt, nm)] = (mask, label, got, cost, c)

d2, p2 = dijkstra(seeds)

best = {}
for (pos, mask), c in d2.items():
    if (mask & SAB) and (mask & SAK):
        if mask not in best or best[mask][0] > c:
            best[mask] = (c, pos)

if __name__ == "__main__":
    print(f"經過 48A 取 Saber、最終同時持有 Saber+間桐櫻的不同組合: {len(best)} 種\n")
    rows = sorted(((bin(m).count("1"), c, m, pos) for m, (c, pos) in best.items()),
                  key=lambda r: (r[1] / r[0], r[1]))
    print(f"{'罐頭':>6} {'種類':>4} {'均攤':>6}  組合")
    for n, c, m, pos in rows:
        print(f"{c:>6} {n:>4} {round(c/n):>6}  {'、'.join(names(m))}")
