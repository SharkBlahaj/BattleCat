# -*- coding: utf-8 -*-
"""輸出規劃結果，並在每一發必中連抽旁列出各活動在同一格的保底角色。

同一格用不同活動打必中，保底角色不同，落點也可能不同（各活動的重抽帶不一樣），
所以三個欄位都要列出來給玩家挑。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "data"))
import track_data_v3 as FATE, track_ep3 as EP3, track_ep4 as EP4
import track_tickets as TK
import player_profile as P

BANNERS = [("Fate", FATE), ("活動3", EP3), ("活動4", EP4)]


def guar_options(pos):
    """在 pos 打必中連抽，各活動分別給什麼保底、落到哪裡。"""
    n, t = int(pos[:-1]), pos[-1]
    out = []
    for name, M in BANNERS:
        guar, dest = M.TRACK[t][n][1], M.TRACK[t][n][2]
        if guar:
            out.append((name, guar, dest, guar in P.OWNED))
    return out


def single_options(pos):
    """在 pos 單抽／用票，各來源分別給什麼。"""
    n, t = int(pos[:-1]), pos[-1]
    out = []
    for name, M in BANNERS:
        rr = getattr(M, "REROLL", {}).get((t, n))
        if rr:
            out.append((name, rr[0], rr[1]))
        elif n + 1 in M.TRACK[t]:
            out.append((name, M.TRACK[t][n][0], f"{n+1}{t}"))
    if n in TK.PLATINUM[t]:
        out.append(("白金卷", TK.PLATINUM[t][n], f"{n+1}{t}"))
    if n in TK.LEGEND[t] and TK.LEGEND[t][n] != TK.PLATINUM[t][n]:
        out.append(("黑金卷", TK.LEGEND[t][n], f"{n+1}{t}"))
    return out


def show(plan_result, merge_fn, targets):
    r = plan_result
    print(f"  罐頭 {r['food']} · 稀有卷 {r['rare']}/{P.RESOURCES['稀有卷']} · "
          f"白金卷 {r['plat']}/3 · 黑金卷 {r['leg']}/3 · 終點 {r['end']}\n")
    for i, s in enumerate(merge_fn(r["steps"]), 1):
        cnt = f"×{s['n']}" if s["n"] > 1 else ""
        hit = [g for g in s["got"] if g in targets]
        tag = f"   ★ {'、'.join(dict.fromkeys(hit))}" if hit else ""
        print(f"  {i:>2}. [{s['label']}{cnt}] {s['from']} → {s['to']}  "
              f"{s['cost']} 罐頭{tag}")
        if "必中" in s["label"]:
            for nm, g, d, owned in guar_options(s["from"]):
                mark = "  ⚠ 已有" if owned else ("  ★ 目標" if g in targets else "")
                sel = "►" if nm in s["label"] else " "
                print(f"        {sel} {nm:<5} 保底 {g:<12} → {d}{mark}")


def uber_matrix(positions, targets=()):
    """給一組打必中的位置，列出三個活動各自的保底角色對照表。"""
    rows = []
    for pos in positions:
        row = {"pos": pos}
        for nm, g, d, owned in guar_options(pos):
            row[nm] = (g, d, owned)
        rows.append(row)
    return rows
