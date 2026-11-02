# -*- coding: utf-8 -*-
"""通用抽軌 solver: 吃任一活動的 track 模組, 用 (位置, 超激レア bitmask) 做 Dijkstra。"""
import heapq


class Solver:
    def __init__(self, track, ubers, cost_single, cost_guar, guar_draws, suspect=()):
        self.T = track
        self.UL = sorted(ubers)
        self.BIT = {u: 1 << i for i, u in enumerate(self.UL)}
        self.cs, self.cg, self.gd = cost_single, cost_guar, guar_draws
        self.suspect = set(suspect)

    def names(self, mask):
        return [u for u in self.UL if mask & self.BIT[u]]

    def mask_of(self, cats):
        m = 0
        for c in cats:
            if c in self.BIT:
                m |= self.BIT[c]
        return m

    def moves(self, pos):
        n, t = int(pos[:-1]), pos[-1]
        tbl = self.T[t]
        out = []
        if n + 1 in tbl and (t, n + 1) not in self.suspect:
            out.append(("單抽", self.cs, (tbl[n][0],), f"{n+1}{t}", (pos,)))
        guar, dest = tbl[n][1], tbl[n][2]
        if dest and not any((t, n + i) in self.suspect for i in range(1, self.gd)):
            k = self.gd - 1
            got = tuple(tbl[n + i][0] for i in range(k)) + (guar,)
            out.append((f"必中{self.gd}連", self.cg, got, dest,
                        tuple(f"{n+i}{t}" for i in range(k))))
        return out

    def search(self, start):
        dist = {(start, 0): 0}
        par = {}
        pq = [(0, start, 0)]
        while pq:
            c, pos, mask = heapq.heappop(pq)
            if dist.get((pos, mask), 1 << 60) < c:
                continue
            for label, cost, got, nxt, cells in self.moves(pos):
                nm = mask | self.mask_of(got)
                nc = c + cost
                if dist.get((nxt, nm), 1 << 60) > nc:
                    dist[(nxt, nm)] = nc
                    par[(nxt, nm)] = (pos, mask, label, got, cost, cells)
                    heapq.heappush(pq, (nc, nxt, nm))
        self.dist, self.par = dist, par
        return dist, par

    def trace(self, key):
        out = []
        while key in self.par:
            pos, mask, label, got, cost, cells = self.par[key]
            out.append({"label": label, "from": pos, "to": key[0], "cost": cost,
                        "got": list(got), "cells": list(cells),
                        "ubers": [g for g in got if g in self.BIT]})
            key = (pos, mask)
        return list(reversed(out))

    def cheapest_for(self, targets):
        need = self.mask_of(targets)
        best = None
        for (pos, mask), c in self.dist.items():
            if (mask & need) == need and (best is None or c < best[0]):
                best = (c, pos, mask)
        return best
