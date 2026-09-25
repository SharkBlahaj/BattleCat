# -*- coding: utf-8 -*-
"""從指定起點列出「所有含指定目標的超激レア組合」及各自最省路線。"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "data"))
from solver import Solver


def merge_singles(steps):
    out = []
    for s in steps:
        if out and "單抽" in s["label"] and "單抽" in out[-1]["label"] and out[-1]["to"] == s["from"]:
            p = out[-1]
            p["to"] = s["to"]; p["cost"] += s["cost"]
            p["got"] += s["got"]; p["cells"] += s["cells"]; p["ubers"] += s["ubers"]
        else:
            out.append(dict(s))
    return out


def build(track, ubers, cost_single, cost_guar, guar_draws, start, targets):
    s = Solver(track, ubers, cost_single, cost_guar, guar_draws)
    s.search(start)
    need = s.mask_of(targets)
    best = {}
    for (pos, mask), c in s.dist.items():
        if (mask & need) != need:
            continue
        if mask not in best or best[mask][0] > c:
            best[mask] = (c, pos)
    out = []
    for mask, (cost, pos) in best.items():
        steps = merge_singles(s.trace((pos, mask)))
        assert sum(x["cost"] for x in steps) == cost
        u = s.names(mask)
        out.append({
            "cost": cost, "n": len(u), "avg": round(cost / len(u)), "ubers": u,
            "end": pos,
            "draws": sum(len(x["cells"]) if "單抽" in x["label"] else guar_draws for x in steps),
            "steps": [{"kind": "g" if x["label"].startswith("必中") else "s",
                       "from": x["from"], "to": x["to"], "cost": x["cost"],
                       "count": guar_draws if x["label"].startswith("必中") else len(x["cells"]),
                       "cells": x["cells"], "ubers": x["ubers"]} for x in steps],
        })
    out.sort(key=lambda r: (r["avg"], r["cost"]))
    return out
