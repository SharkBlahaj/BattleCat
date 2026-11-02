# -*- coding: utf-8 -*-
"""產生「經 48A 取 Saber」全部組合的資料 (含可重建的逐步路徑)。"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "data"))
import via_48a as V
from uber_maximizer import names, BIT
from track_data import TRACK, UBERS, COST_SINGLE, COST_GUARANTEED


def step_obj(label, frm, to, cost):
    n, t = int(frm[:-1]), frm[-1]
    tbl = TRACK[t]
    if label == "必中11連":
        got = [tbl[n + i][0] for i in range(10)] + [tbl[n][1]]
        cells = [f"{n+i}{t}" for i in range(10)]
    else:
        got = [tbl[n][0]]
        cells = [frm]
    return {"kind": "g" if label == "必中11連" else "s", "from": frm, "to": to,
            "count": 11 if label == "必中11連" else 1, "cost": cost,
            "got": got, "cells": cells,
            "ubers": [g for g in got if g in UBERS]}


def merge_singles(steps):
    """把連續單抽合併成一步, 顯示比較乾淨"""
    out = []
    for s in steps:
        if out and s["kind"] == "s" and out[-1]["kind"] == "s" and out[-1]["to"] == s["from"]:
            p = out[-1]
            p["to"] = s["to"]; p["count"] += 1; p["cost"] += s["cost"]
            p["got"] += s["got"]; p["cells"] += s["cells"]; p["ubers"] += s["ubers"]
        else:
            out.append(dict(s))
    return out


def rebuild(mask):
    """回溯出到達這個組合的完整步驟"""
    cost, endpos = V.best[mask]
    key = (endpos, mask)
    tail = []
    while key in V.p2:
        pos, m, label, got, c = V.p2[key]
        tail.append(step_obj(label, pos, key[0], c))
        key = (pos, m)
    tail.reverse()
    premask, label, got, c, _ = V.origin[key]      # 在 48A 取 Saber 的那一步
    mid = [step_obj(label, "48A", key[0], c)]
    head = []
    k2 = ("48A", premask)
    while k2 in V.p1:
        pos, m, lab, g2, c2 = V.p1[k2]
        head.append(step_obj(lab, pos, k2[0], c2))
        k2 = (pos, m)
    head.reverse()
    return merge_singles(head + mid + tail)


def build():
    out = []
    for mask, (cost, endpos) in V.best.items():
        steps = rebuild(mask)
        assert sum(s["cost"] for s in steps) == cost, (mask, cost)
        u = names(mask)
        out.append({"cost": cost, "n": len(u), "avg": round(cost / len(u)),
                    "ubers": u, "end": endpos,
                    "draws": sum(s["count"] for s in steps), "steps": steps})
    out.sort(key=lambda r: (r["avg"], r["cost"]))
    return out


if __name__ == "__main__":
    combos = build()
    print(f"{len(combos)} 組，全部通過成本校驗")
    for c in combos[:3]:
        print(f"\n{c['cost']} 罐頭 / {c['n']} 種 / 均攤 {c['avg']} / {c['draws']} 抽")
        print("  " + "、".join(c["ubers"]))
        for s in c["steps"]:
            lab = "必中11連" if s["kind"] == "g" else f"單抽 ×{s['count']}"
            print(f"    [{lab}] {s['from']} → {s['to']}  {s['cost']}" +
                  (f"   ★ {'、'.join(s['ubers'])}" if s["ubers"] else ""))
