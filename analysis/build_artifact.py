# -*- coding: utf-8 -*-
"""從 track_data 產生互動式抽軌路徑圖 (單一 HTML)。"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "data"))
from track_data import A, B, TRACK, UBERS, COST_SINGLE, COST_GUARANTEED

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

ROUTES = [
    route("五隻超激レア", "39A 一發吃 Saber＋間桐櫻，51B 再吃士郎＋Gilgamesh，最後 62B 單抽撿 Lancer。均攤 810，現階段最佳",
          [("s", "35A", 4), ("g", "39A"), ("s", "49B", 2), ("g", "51B"), ("s", "62B", 1)]),
    route("四隻超激レア", "兩發必中連打，不插單抽。均攤 900，抽數最少的高效方案",
          [("s", "35A", 4), ("g", "39A"), ("g", "49B")]),
    route("最短收尾", "只補完 Saber 和間桐櫻。四隻目標全拿的總支出剛好落在聯合最佳解 6600",
          [("s", "35A", 4), ("g", "39A")]),
    route("三隻超激レア", "改走 43A 那一發，抽完在 53B 單抽撿衛宮士郎",
          [("s", "35A", 8), ("g", "43A"), ("s", "53B", 1)]),
]

DATA = {"cells": cells(), "routes": ROUTES, "targets": sorted(TARGETS),
        "ubers": sorted(UBERS), "start": "35A",
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
