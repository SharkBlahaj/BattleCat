# -*- coding: utf-8 -*-
"""輸出決策表：每一發必中、每一個會碰到超激的普通格，列出各活動的選項。"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "data"))
import track_data_v3 as F, track_ep3 as E3, track_ep4 as E4, track_tickets as TK
import player_profile as P

BAN = {"Fate": F, "活動3": E3, "活動4": E4}
TOP = [52, 60, 64, 71, 77, 80, 94]          # 只出現在 A 軌
ALL_UBERS = F.UBERS | E3.UBERS | E4.UBERS
LEGEND_ONLY = set(TK.LEGEND_OVERRIDE_A.values())


def flag(name):
    if name in P.OWNED:
        return " ⚠已有"
    if name in P.WANTED:
        return " ★目標"
    if name in LEGEND_ONLY:
        return " 🏆傳說"
    return ""


def window(pos, banner):
    """該活動在 pos 打必中，會經過哪些格、保底是誰、落到哪。"""
    n, t = int(pos[:-1]), pos[-1]
    M = BAN[banner]
    tbl = M.TRACK[t]
    if not tbl[n][2]:
        return None
    cells = [(n + i, t) for i in range(10)]
    return {"guar": tbl[n][1], "dest": tbl[n][2], "cells": cells,
            "results": [tbl[n + i][0] for i in range(10)]}


def sheet(steps):
    out = []
    for s in steps:
        pos = s["from"]
        n, t = int(pos[:-1]), pos[-1]
        if "必中" in s["label"]:
            chosen = next(b for b in BAN if b in s["label"])
            rows = []
            for b in BAN:
                w = window(pos, b)
                if not w:
                    continue
                tops = [(c, BAN[b].TRACK[tt][c][0])
                        for c, tt in w["cells"] if tt == "A" and c in TOP]
                rows.append((b, w["guar"], w["dest"], tops, b == chosen))
            out.append(("必中", pos, rows))
        else:
            if t == "A" and n in TOP:
                opts = []
                for b in BAN:
                    opts.append((b, BAN[b].TRACK[t][n][0]))
                opts.append(("白金卷", TK.PLATINUM[t][n]))
                if TK.LEGEND[t][n] != TK.PLATINUM[t][n]:
                    opts.append(("黑金卷", TK.LEGEND[t][n]))
                out.append(("單格", pos, opts))
    return out
