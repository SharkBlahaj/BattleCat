# -*- coding: utf-8 -*-
"""跨活動聯合規劃：所有池子共用同一個位置計數器。

一個動作 = 在某個池子抽一次（單抽／必中連抽／用一張票）。
不論用哪個池子，位置都會前進；拿到的角色則取決於該池子的表。

狀態 = (位置, 目標到手 bitmask, 已用白金卷, 已用黑金卷)
票是獨立的有限資源，所以放進狀態而不是成本。
"""
import heapq, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "data"))
import track_data_v3 as FATE
import track_ep3 as EP3
import track_ep4 as EP4
import track_tickets as TK

COST_SINGLE = 150
MAX_PLAT = 3
MAX_LEG = 3

GACHA = [("Fate", FATE), ("活動3", EP3), ("活動4", EP4)]
TICKETS = [("白金卷", TK.PLATINUM, "p"), ("黑金卷", TK.LEGEND, "l")]


def make(targets):
    BIT = {t: 1 << i for i, t in enumerate(targets)}
    FULL = (1 << len(targets)) - 1

    def mask_of(cats):
        m = 0
        for c in cats:
            if c in BIT:
                m |= BIT[c]
        return m

    def moves(pos, pu, lu):
        n, t = int(pos[:-1]), pos[-1]
        out = []
        for name, M in GACHA:
            tbl = M.TRACK[t]
            if n + 1 in tbl and (t, n + 1) not in getattr(M, "SUSPECT", ()):
                out.append((f"{name} 單抽", COST_SINGLE, (tbl[n][0],),
                            f"{n+1}{t}", pu, lu, (pos,)))
            guar, dest = tbl[n][1], tbl[n][2]
            gd = M.GUAR_DRAWS
            if dest and not any((t, n + i) in getattr(M, "SUSPECT", ())
                                for i in range(1, gd)):
                got = tuple(tbl[n + i][0] for i in range(gd - 1)) + (guar,)
                out.append((f"{name} 必中{gd}連", M.COST_GUARANTEED, got, dest,
                            pu, lu, tuple(f"{n+i}{t}" for i in range(gd - 1))))
        for name, TT, kind in TICKETS:
            if kind == "p" and pu >= MAX_PLAT:
                continue
            if kind == "l" and lu >= MAX_LEG:
                continue
            if n + 1 not in TT[t]:
                continue
            out.append((f"{name}", 0, (TT[t][n],), f"{n+1}{t}",
                        pu + (kind == "p"), lu + (kind == "l"), (pos,)))
        return out

    def solve(start):
        s0 = (start, 0, 0, 0)
        dist = {s0: 0}
        par = {}
        pq = [(0, start, 0, 0, 0)]
        while pq:
            c, pos, mask, pu, lu = heapq.heappop(pq)
            if dist.get((pos, mask, pu, lu), 1 << 60) < c:
                continue
            for label, cost, got, nxt, npu, nlu, cells in moves(pos, pu, lu):
                nm = mask | mask_of(got)
                nc = c + cost
                k = (nxt, nm, npu, nlu)
                if dist.get(k, 1 << 60) > nc:
                    dist[k] = nc
                    par[k] = (pos, mask, pu, lu, label, got, cost, cells)
                    heapq.heappush(pq, (nc, nxt, nm, npu, nlu))
        return dist, par

    def trace(par, key):
        out = []
        while key in par:
            pos, mask, pu, lu, label, got, cost, cells = par[key]
            out.append({"label": label, "from": pos, "to": key[0],
                        "cost": cost, "got": list(got), "cells": list(cells)})
            key = (pos, mask, pu, lu)
        return list(reversed(out))

    return BIT, FULL, solve, trace


def merge(steps):
    o = []
    for s in steps:
        if o and s["label"] == o[-1]["label"] and "單抽" in s["label"] and o[-1]["to"] == s["from"]:
            p = o[-1]
            p["to"] = s["to"]; p["cost"] += s["cost"]
            p["got"] += s["got"]; p["cells"] += s["cells"]
        else:
            o.append(dict(s))
    return o
