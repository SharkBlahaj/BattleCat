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
from solver import Solver

_CORE = ["Saber", "間桐櫻"]
_combos = combos_from.build(TRACK, UBERS, COST_SINGLE, COST_GUARANTEED, 11,
                            "1A", _CORE)
for _c in _combos:
    for _s in _c["steps"]:
        _s.pop("got", None)

# 指定目標組 → 取最省路線
_SPECS = [
    ("最短收尾", _CORE,
     "只補完兩隻必收。5A 那一發保底是間桐櫻，涵蓋的第 10 格 14A 結果欄正是 Saber"),
    ("＋遠坂凜", _CORE + ["遠坂凜"],
     "只多插一次單抽改打 16B，凜和衛宮士郎一起進袋。加碼 1650 換兩隻，均攤最低"),
    ("四隻目標全收", _CORE + ["遠坂凜", "真Assassin"],
     "在上一條後面再走一格打 28A 收真Assassin。四隻想要的全到齊，還附送衛宮士郎"),
    ("最佳均攤", _CORE + ["Gilgamesh", "Lancer"],
     "不收凜和真Assassin，改走 17B／28B 那條線。均攤 810 是全表最低，但拿不到你點名的兩隻"),
    ("全十隻", sorted(UBERS),
     "本活動十隻超激レア一網打盡，不留遺憾"),
]


def _by_targets(targets):
    s = Solver(TRACK, UBERS, COST_SINGLE, COST_GUARANTEED, 11)
    s.search("1A")
    r = s.cheapest_for(targets)
    if not r:
        return None
    cost, pos, mask = r
    steps = combos_from.merge_singles(s.trace((pos, mask)))
    assert sum(x["cost"] for x in steps) == cost
    u = s.names(mask)
    return {"cost": cost, "n": len(u), "avg": round(cost / len(u)), "ubers": u,
            "end": pos,
            "draws": sum(len(x["cells"]) if "單抽" in x["label"] else 11 for x in steps),
            "steps": [{"kind": "g" if x["label"].startswith("必中") else "s",
                       "from": x["from"], "to": x["to"], "cost": x["cost"],
                       "count": 11 if x["label"].startswith("必中") else len(x["cells"]),
                       "cells": x["cells"], "ubers": x["ubers"]} for x in steps]}


ROUTES = []
for _name, _tg, _blurb in _SPECS:
    _r = _by_targets(_tg)
    if not _r:
        continue
    _r["name"] = _name
    _r["blurb"] = _blurb
    ROUTES.append(_r)

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
