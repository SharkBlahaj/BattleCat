# -*- coding: utf-8 -*-
"""從指定起點出發, 求「保證拿到指定超激レア」的最省罐頭路徑。

動作:
  單抽 (150)      : NX -> (N+1)X, 獲得 result[N][X]
  必中11連 (1500) : NX -> 表上標示的跳轉點, 獲得 result[N..N+9][X] 共10隻 + 保底1隻

備註: godfat 在 60B / 93B / 97B 標了重抽換軌記號, 經過這些點的單抽路徑需人工複驗。
"""
import heapq, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "data"))
from track_data import TRACK, COST_SINGLE, COST_GUARANTEED

SUSPECT = {("B", 60), ("B", 93), ("B", 97)}  # godfat 標記的重抽換軌點


def parse(pos):
    return int(pos[:-1]), pos[-1]


def moves(pos):
    """回傳 (動作說明, 花費, 抽到的角色list, 新位置, 是否經過可疑換軌點)"""
    n, t = parse(pos)
    tbl = TRACK[t]
    out = []
    if n + 1 in tbl:
        out.append(("單抽", COST_SINGLE, [tbl[n][0]], f"{n+1}{t}",
                    (t, n + 1) in SUSPECT))
    guar, dest = tbl[n][1], tbl[n][2]
    if dest:
        got = [tbl[n + i][0] for i in range(10)] + [guar]
        risky = any((t, n + i) in SUSPECT for i in range(1, 10))
        out.append(("必中11連", COST_GUARANTEED, got, dest, risky))
    return out


def solve(start, targets, allow_risky=False):
    targets = list(targets)
    full = (1 << len(targets)) - 1

    def mask_of(cats):
        m = 0
        for c in cats:
            if c in targets:
                m |= 1 << targets.index(c)
        return m

    seen = {}
    pq = [(0, start, 0, ())]
    seen[(start, 0)] = 0
    while pq:
        cost, pos, mask, path = heapq.heappop(pq)
        if mask == full:
            return cost, path
        if seen.get((pos, mask), 1 << 60) < cost:
            continue
        for label, c, got, nxt, risky in moves(pos):
            if risky and not allow_risky:
                continue
            nm = mask | mask_of(got)
            nc = cost + c
            if seen.get((nxt, nm), 1 << 60) > nc:
                seen[(nxt, nm)] = nc
                heapq.heappush(pq, (nc, nxt, nm, path + ((label, pos, tuple(got), nxt),)))
    return None, None


def show(start, targets):
    cost, path = solve(start, targets)
    if path is None:
        print(f"{start} -> {targets}: 無解")
        return
    draws = sum(11 if s[0] == "必中11連" else 1 for s in path)
    print(f"起點 {start} / 目標 {'+'.join(targets)}")
    print(f"  總成本 {cost} 罐頭 ({cost//1500}張1500 等值) / 共 {draws} 抽\n")
    p = start
    for i, (label, frm, got, nxt) in enumerate(path, 1):
        hit = [g for g in got if g in targets]
        star = "  ★ " + "、".join(hit) if hit else ""
        print(f"  {i}. [{label}] {frm} → {nxt}{star}")
        print(f"       {'、'.join(got)}")
    print()


if __name__ == "__main__":
    show("4A", ["Saber", "間桐櫻"])
    print("-" * 60)
    show("4A", ["間桐櫻"])
    print("-" * 60)
    show("4A", ["Saber"])
