# -*- coding: utf-8 -*-
"""從 track_data 產生互動式抽軌路徑圖 (單一 HTML)。"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "data"))
from track_data_now import A, B, TRACK, UBERS, COST_SINGLE, COST_GUARANTEED

SHORT = {"Gilgamesh": "Gil", "衛宮士郎": "士郎", "遠坂凜": "凜",
         "間桐櫻": "櫻", "伊莉雅蘇菲爾": "伊莉雅", "真Assassin": "Assassin"}
TARGETS = {"Saber", "間桐櫻"}

def cells():
    out = {}
    for t, tbl in (("A", A), ("B", B)):
        for n, (res, guar, dest) in tbl.items():
            run = None
            if dest:
                run = [tbl[n + i][0] for i in range(10)] + [guar]
            out[f"{n}{t}"] = {
                "n": n, "t": t, "res": res,
                "resUber": res in UBERS,
                "guar": guar, "short": SHORT.get(guar, guar) if guar else None,
                "dest": dest, "run": run,
            }
    return out

def route(name, blurb, steps):
    """steps: list of ('s', from, count) 單抽 | ('g', from) 必中11連"""
    cost = 0; draws = 0; detail = []; ubers = []
    for kind, *rest in steps:
        if kind == "s":
            pos, cnt = rest
            n, t = int(pos[:-1]), pos[-1]
            got = [TRACK[t][n + i][0] for i in range(cnt)]
            cost += COST_SINGLE * cnt; draws += cnt
            detail.append({"kind": "s", "from": pos, "to": f"{n+cnt}{t}",
                           "count": cnt, "cost": COST_SINGLE * cnt, "got": got,
                           "cells": [f"{n+i}{t}" for i in range(cnt)]})
            ubers += [g for g in got if g in UBERS]
        else:
            pos = rest[0]
            n, t = int(pos[:-1]), pos[-1]
            tbl = TRACK[t]
            got = [tbl[n + i][0] for i in range(10)] + [tbl[n][1]]
            cost += COST_GUARANTEED; draws += 11
            detail.append({"kind": "g", "from": pos, "to": tbl[n][2],
                           "count": 11, "cost": COST_GUARANTEED, "got": got,
                           "cells": [f"{n+i}{t}" for i in range(10)]})
            ubers += [g for g in got if g in UBERS]
    return {"name": name, "blurb": blurb, "cost": cost, "draws": draws,
            "ubers": ubers, "steps": detail,
            "end": detail[-1]["to"], "start": steps[0][1]}

import combos_from
_combos = combos_from.build(TRACK, UBERS, COST_SINGLE, COST_GUARANTEED, 11,
                            "1A", ["Saber", "間桐櫻"])
for _c in _combos:
    for _s in _c["steps"]:
        _s.pop("got", None)

BLURB = {
    2: "只補完 Saber 和間桐櫻。5A 那一發的保底是間桐櫻，涵蓋的第 10 格 14A 結果欄正是 Saber",
    3: "改走 9A 那一發，抽完在 19B 單抽撿衛宮士郎",
    4: "兩發必中連打不插單抽，15B 那發同時吃到 19B 的衛宮士郎和保底的 Archer",
    5: "17B 那發吃衛宮士郎＋Gilgamesh，最後在 28B 花 150 撿 Lancer。均攤最低",
    6: "再往下多打一發必中",
    7: "高預算區", 8: "高預算區", 9: "高預算區",
}

_by_n = {}
for _c in _combos:
    if _c["n"] not in _by_n or _by_n[_c["n"]]["cost"] > _c["cost"]:
        _by_n[_c["n"]] = _c
_best_avg = min(_combos, key=lambda c: (c["avg"], c["cost"]))

ROUTES = []
for _n in sorted(_by_n):
    if _n > 6:
        continue
    _c = dict(_by_n[_n])
    _c["name"] = f"{_n} 隻超激レア"
    _c["blurb"] = BLURB.get(_n, "")
    if _c["cost"] == _best_avg["cost"] and _c["n"] == _best_avg["n"]:
        _c["blurb"] += "　← 全表最佳均攤"
    ROUTES.append(_c)
ROUTES.sort(key=lambda r: (r["avg"], r["cost"]))

DATA = {"cells": cells(), "routes": ROUTES, "targets": sorted(TARGETS),
        "ubers": sorted(UBERS), "start": "1A",
        "costSingle": COST_SINGLE, "costGuar": COST_GUARANTEED}

import combos_from
_combos = combos_from.build(TRACK, UBERS, COST_SINGLE, COST_GUARANTEED, 11,
                            "35A", ["Saber", "間桐櫻"])
for _c in _combos:                       # 瘦身: 逐格內容改由點軌道查看
    for _s in _c["steps"]:
        _s.pop("got", None)
DATA["combos"] = _combos

html = open(os.path.join(os.path.dirname(__file__), "template.html"), encoding="utf-8").read()
html = html.replace("/*__DATA__*/null", json.dumps(DATA, ensure_ascii=False))
out = os.path.join(os.path.dirname(__file__), "..", "artifact", "gacha_track.html")
open(out, "w", encoding="utf-8").write(html)
print("wrote", os.path.realpath(out), len(html), "bytes")
