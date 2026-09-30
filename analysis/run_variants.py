# -*- coding: utf-8 -*-
"""算出多個方案版本，寫成 artifact/plans.json 供網頁切換。"""
import json, os, sys, time
D = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(D, "analysis")); sys.path.insert(0, os.path.join(D, "data"))
import plan_dedup, player_profile as P, resource_planner as RP
from resource_planner import merge

FATE5 = ["Archer", "Rider", "Gilgamesh", "Lancer", "伊莉雅蘇菲爾"]
W = P.WANTED

VARIANTS = [
    ("全收 · 最省罐頭", "四個主目標 ＋ Fate 缺的五隻，罐頭壓到最低",
     W + FATE5, dict(n_leg=0)),
    ("全收 · 省稀有卷", "同樣全收，但把稀有卷限制在 12 張，多出來的距離改用必中連抽",
     W + FATE5, dict(n_leg=0, n_rare=12)),
    ("全收 ＋ 黑金卷", "開放 3 張黑金卷；踩到最高階格時可換傳說レア",
     W + FATE5, dict(n_leg=3)),
    ("只要四主目標", "只收凱斯莉、希莉烏斯、吳仲力、京坂七穗，不追 Fate",
     W, dict(n_leg=0)),
    ("四主目標 · 省稀有卷", "只收四隻，且稀有卷限 12 張——這就是先前那條 9000 罐頭的版本",
     W, dict(n_leg=0, n_rare=12)),
]

out = []
for name, blurb, targets, kw in VARIANTS:
    t0 = time.time()
    r = plan_dedup.solve(targets, **kw)
    if not r:
        print(f"[skip] {name}: 無解", flush=True)
        continue
    r["name"], r["blurb"], r["targets"] = name, blurb, targets
    r["merged"] = merge(r["steps"])
    allu = [x for s in r["steps"] for x in s["got"]
            if x in RP.ALL_UBERS or x in targets]
    r["haul"] = [x for x in dict.fromkeys(allu) if x not in P.OWNED]
    r["pulls"] = sum(1 for s in r["steps"] if "必中" in s["label"])
    out.append(r)
    print(f"[ok] {name}: 罐頭 {r['food']} 稀有卷 {r['rare']} 白金 {r['plat']} "
          f"黑金 {r['leg']} 收穫 {len(r['haul'])} ({time.time()-t0:.0f}s)", flush=True)

json.dump(out, open(os.path.join(D, "artifact", "plans.json"), "w"),
          ensure_ascii=False)
print("wrote plans.json with", len(out), "variants")
