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
    route("三隻超激レア", "多花 900 罐頭換一整隻額外的超激レア，每隻均攤 2100 — 全場最划算",
          [("s", "4A", 2), ("g", "6A"), ("s", "16B", 10), ("g", "26B"), ("g", "37A")]),
    route("最省罐頭", "只要 Saber 和間桐櫻兩隻，這是絕對下限，再也壓不下去",
          [("s", "4A", 6), ("g", "10A"), ("s", "20B", 10), ("g", "30B")]),
    route("B軌硬走", "不換軌，一路單抽到 35B。只省 150 罐頭卻少一隻超激レア — 不建議",
          [("s", "4A", 2), ("g", "6A"), ("s", "16B", 19), ("g", "35B")]),
    route("只要間桐櫻", "預算有限時的最短路徑，兩步就位",
          [("s", "4A", 2), ("g", "6A")]),
    route("只要 Saber", "預算有限且只想要 Saber",
          [("s", "4A", 6), ("g", "10A")]),
]

DATA = {"cells": cells(), "routes": ROUTES, "targets": sorted(TARGETS),
        "ubers": sorted(UBERS), "start": "4A",
        "costSingle": COST_SINGLE, "costGuar": COST_GUARANTEED}

html = open(os.path.join(os.path.dirname(__file__), "template.html"), encoding="utf-8").read()
html = html.replace("/*__DATA__*/null", json.dumps(DATA, ensure_ascii=False))
out = os.path.join(os.path.dirname(__file__), "..", "artifact", "gacha_track.html")
open(out, "w", encoding="utf-8").write(html)
print("wrote", os.path.realpath(out), len(html), "bytes")
