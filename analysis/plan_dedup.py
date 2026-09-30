# -*- coding: utf-8 -*-
"""反覆求解，消除「同一條路線內部」的保底重複。

resource_planner 只比對玩家已擁有的清單，看不到路線自己抽到兩隻一樣的。
作法：解一次 → 找出重複的保底 → 把它們暫時加進 OWNED 再解一次，直到收斂。
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "data"))
import resource_planner as RP
import player_profile as P


def solve(targets, rounds=8, **kw):
    base = set(P.OWNED)
    penal = set()
    best = None
    for _ in range(rounds):
        P.OWNED = base | penal
        r = RP.plan(targets, **kw)
        if not r:
            break
        guars = [s["got"][-1] for s in r["steps"] if "必中" in s["label"]]
        dups = {g for g in guars if guars.count(g) > 1 and g not in targets}
        if best is None or (len(dups), r["food"]) < best[0]:
            best = ((len(dups), r["food"]), r, set(penal))
        if not dups:
            break
        if dups <= penal:
            break
        penal |= dups
    P.OWNED = base
    return best[1] if best else None
