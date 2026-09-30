# -*- coding: utf-8 -*-
"""產生多活動規劃盤（單一 HTML）。"""
import json, os, sys
D = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(D, "data"))
import track_data_v3 as F, track_ep3 as E3, track_ep4 as E4
import track_tickets as TK, player_profile as P

BAN = {"Fate": F, "活動3": E3, "活動4": E4}
TOP = [52, 60, 64, 71, 77, 80, 94]
ALL_UBERS = sorted(F.UBERS | E3.UBERS | E4.UBERS)
LEGEND_ONLY = sorted(set(TK.LEGEND_OVERRIDE_A.values()))


def tracks():
    out = {}
    for name, M in BAN.items():
        out[name] = {t: {str(n): [v[0], v[1], v[2]] for n, v in M.TRACK[t].items()}
                     for t in ("A", "B")}
        out[name]["reroll"] = {f"{t}{n}": list(v)
                               for (t, n), v in getattr(M, "REROLL", {}).items()}
        out[name]["ubers"] = sorted(M.UBERS)
        out[name]["guarDraws"] = M.GUAR_DRAWS
    out["白金卷"] = {t: {str(n): [v, None, None] for n, v in TK.PLATINUM[t].items()}
                   for t in ("A", "B")}
    out["黑金卷"] = {t: {str(n): [v, None, None] for n, v in TK.LEGEND[t].items()}
                   for t in ("A", "B")}
    return out


def build(plan_path):
    plan = json.load(open(plan_path, encoding="utf-8"))
    # 展開每一步實際覆蓋的格子與所用池子
    for s in plan["merged"]:
        n, t = int(s["from"][:-1]), s["from"][-1]
        ban = next((b for b in BAN if b in s["label"]), None)
        if ban is None:
            ban = "黑金卷" if "黑金" in s["label"] else ("白金卷" if "白金" in s["label"] else None)
        s["banner"] = ban
        if "必中" in s["label"]:
            s["cover"] = [f"{n+i}{t}" for i in range(BAN[ban].GUAR_DRAWS - 1)]
            s["kind"] = "g"
        else:
            cnt = s.get("n", 1)
            s["cover"] = [f"{n+i}{t}" for i in range(cnt)]
            s["kind"] = "s"
    data = {
        "position": P.POSITION, "resources": P.RESOURCES,
        "owned": sorted(P.OWNED), "targets": plan["targets"],
        "wanted": P.WANTED, "heuristics": P.HEURISTICS,
        "top": TOP, "allUbers": ALL_UBERS, "legendOnly": LEGEND_ONLY,
        "tracks": tracks(), "plan": plan,
    }
    tpl = open(os.path.join(D, "analysis", "board.html"), encoding="utf-8").read()
    html = tpl.replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False))
    out = os.path.join(D, "artifact", "gacha_track.html")
    open(out, "w", encoding="utf-8").write(html)
    print("wrote", out, len(html), "bytes")


if __name__ == "__main__":
    build(os.path.join(D, "artifact", "plan.json"))
