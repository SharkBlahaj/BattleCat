# -*- coding: utf-8 -*-
"""含資源上限的跨池規劃：罐頭、稀有卷、白金卷、黑金卷。

推進一格可以用：稀有卷(0罐頭,上限54) / 單抽(150罐頭) / 白金卷(上限3) / 黑金卷(上限3)
必中連抽：該池的價格，一次推進 10 格並翻軌

狀態 = (位置, 目標bitmask, 已用稀有卷, 已用白金卷, 已用黑金卷)
"""
import heapq, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "data"))
import track_data_v3 as FATE, track_ep3 as EP3, track_ep4 as EP4, track_tickets as TK
import player_profile as P

GACHA = [("Fate", FATE), ("活動3", EP3), ("活動4", EP4)]
FOOD_SINGLE = 150

# 影子價格：反映玩家的資源優先序 稀有卷 > 150罐頭 > 白金卷 > 黑金卷。
# 只用於排序決策；實際罐頭花費另外累計。
SHADOW = {"rare": 1, "single": 150, "plat": 400, "leg": 1500}


def plan(targets, start="1A", n_rare=54, n_plat=3, n_leg=3):
    BIT = {t: 1 << i for i, t in enumerate(targets)}
    FULL = (1 << len(targets)) - 1

    def mk(cats):
        m = 0
        for c in cats:
            if c in BIT:
                m |= BIT[c]
        return m

    def moves(pos, r, p, l):
        n, t = int(pos[:-1]), pos[-1]
        nxt1 = f"{n+1}{t}"
        out = []
        # 推進一格：各池的結果欄都可選，成本看用什麼資源
        # 一般單抽（同軌 +1）與重抽單抽（換軌跳轉）分開處理
        singles, rerolls = {}, {}
        for name, M in GACHA:
            tbl = M.TRACK[t]
            rr = getattr(M, "REROLL", {}).get((t, n))
            if rr:
                rerolls[name] = rr
            elif n + 1 in tbl:
                singles[name] = tbl[n][0]
        for name, (cat, dest) in rerolls.items():
            if r < n_rare:
                out.append((f"稀有卷·{name}(重抽)", 0, SHADOW["rare"],
                            (cat,), dest, r + 1, p, l))
            out.append((f"單抽·{name}(重抽)", FOOD_SINGLE, SHADOW["single"],
                        (cat,), dest, r, p, l))
        if singles:
            best = max(singles.items(), key=lambda kv: (kv[1] in BIT, kv[0]))
            if r < n_rare:
                out.append((f"稀有卷·{best[0]}", 0, SHADOW["rare"],
                            tuple(singles.values()), nxt1, r + 1, p, l))
            out.append((f"單抽·{best[0]}", FOOD_SINGLE, SHADOW["single"],
                        tuple(singles.values()), nxt1, r, p, l))
        if n + 1 in TK.PLATINUM[t] and p < n_plat:
            out.append(("白金卷", 0, SHADOW["plat"], (TK.PLATINUM[t][n],),
                        nxt1, r, p + 1, l))
        if n + 1 in TK.LEGEND[t] and l < n_leg:
            out.append(("黑金卷", 0, SHADOW["leg"], (TK.LEGEND[t][n],),
                        nxt1, r, p, l + 1))
        # 必中連抽
        for name, M in GACHA:
            tbl = M.TRACK[t]
            guar, dest = tbl[n][1], tbl[n][2]
            gd = M.GUAR_DRAWS
            if dest:
                got = tuple(tbl[n + i][0] for i in range(gd - 1)) + (guar,)
                out.append((f"{name} 必中{gd}連", M.COST_GUARANTEED,
                            M.COST_GUARANTEED, got, dest, r, p, l))
        return out

    s0 = (start, 0, 0, 0, 0)
    dist = {s0: 0}
    food = {s0: 0}
    par = {}
    pq = [(0, *s0)]
    while pq:
        c, pos, mask, r, p, l = heapq.heappop(pq)
        if dist.get((pos, mask, r, p, l), 1 << 60) < c:
            continue
        for label, fcost, scost, got, nxt, nr, np_, nl in moves(pos, r, p, l):
            nm = mask | mk(got)
            nc = c + scost
            k = (nxt, nm, nr, np_, nl)
            if dist.get(k, 1 << 60) > nc:
                dist[k] = nc
                food[k] = food[(pos, mask, r, p, l)] + fcost
                par[k] = (pos, mask, r, p, l, label, got, fcost)
                heapq.heappush(pq, (nc, *k))

    done = [(c, k) for k, c in dist.items() if k[1] == FULL]
    if not done:
        return None
    # 同成本下，偏好少用白金卷、再少用黑金卷
    best = min(done, key=lambda x: (x[0], x[1][4], x[1][3], x[1][2]))
    k = best[1]
    steps = []
    while k in par:
        pos, mask, r, p, l, label, got, c2 = par[k]
        steps.append({"label": label, "from": pos, "to": k[0], "cost": c2,
                      "got": list(got)})
        k = (pos, mask, r, p, l)
    steps.reverse()
    return {"food": food[best[1]], "rare": best[1][2], "plat": best[1][3],
            "leg": best[1][4], "end": best[1][0], "steps": steps}


def merge(steps):
    o = []
    for s in steps:
        if o and s["label"] == o[-1]["label"] and o[-1]["to"] == s["from"] \
           and ("稀有卷" in s["label"] or "單抽" in s["label"]):
            p = o[-1]
            p["to"] = s["to"]; p["cost"] += s["cost"]; p["n"] = p.get("n", 1) + 1
            p["got"] += s["got"]
        else:
            s = dict(s); s["n"] = 1
            o.append(s)
    return o
