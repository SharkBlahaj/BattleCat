# -*- coding: utf-8 -*-
"""從 20A：先用金卷走到第 k 格打必中，之後只走到最後一個超激格就收手，
不把資源花光。列出每個 k 與每個必中池的收穫與剩餘資源。"""
import json, sys, os
sys.path.insert(0, '/home/user/BattleCat')
from data import player_profile as PP

D = sys.argv[1]
F = {'1043': 'full_2026-10-18_1043.json', '1021': 'full_2026-10-18_1021.json',
     '1070': 'full_2026-10-20_1070.json', '1004': 'full_2026-10-20_1004.json',
     '947':  'full_2026-10-20_947.json',  '1071': 'full_2026-10-16_1071.json',
     '1072': 'full_2026-10-16_1072.json', '1069': 'full_2026-10-30_1069.json'}
P = {k: json.load(open(os.path.join(D, 'dl1020', f))) for k, f in F.items()}
HI = {'exclusive', 'uber', 'uber_fest', 'legend'}
NOW = ['1043', '1021', '1070', '1004', '947']      # 現在抽得到的食物池
GUAR = ['1043', '1021']


def res(k, s, n):
    return P[k]['res'][s].get(str(n))


def gu(k, s, n):
    return P[k]['guar'][s].get(str(n))


def new_at(s, n, got, pools):
    """這一格有哪些「未持有且還沒收過」的選項 -> [(池, 角色)]"""
    out = []
    for k in pools:
        v = res(k, s, n)
        if v and v[1] in HI and v[0] not in PP.OWNED and v[0] not in got:
            out.append((k, v[0]))
    return out


def guar_pull(k, s, n, got):
    g = gu(k, s, n)
    if not g:
        return None
    ub = []
    for i in range(10):
        v = res(k, s, n + i)
        if not v:
            return None
        if v[1] in HI:
            ub.append(v[0])
    ub.append(g[0])
    new = [c for c in ub if c not in PP.OWNED and c not in got]
    d = g[2]
    return new, (d[-1], int(d[:-1])), g[0]


rows = []
for k in range(0, 8):
    start = 20 + k
    for gk in GUAR:
        o = guar_pull(gk, 'A', start, set())
        if not o:
            continue
        new, (ds, dn), gcat = o
        got = set(new)
        steps = []
        pos = dn
        # 從落點往前走，直到最後一個還能收的超激格
        cells = []
        for n in range(dn, dn + 20):
            opts = new_at(ds, n, got, NOW)
            if opts:
                cells.append((n, opts))
                got.add(opts[0][1])
        if not cells:
            continue
        last_n = cells[-1][0]
        walk = last_n - dn + 1
        total_tickets = k + walk
        if total_tickets > 15:
            continue
        rows.append((k, start, gk, gcat, new, ds, dn, cells, total_tickets, got))

rows.sort(key=lambda r: (-len(r[9]), r[8]))
print(f'{"必中位置":<10}{"池":<6}{"保底":<10}{"落點":<7}{"金卷":<5}{"收穫":<4} 角色')
for k, start, gk, gcat, new, ds, dn, cells, tk, got in rows[:10]:
    print(f'{start}A{"":<6}{gk:<6}{gcat:<10}{dn}{ds:<5}{tk:<5}{len(got):<4} {"、".join(sorted(got))}')

print('\n' + '=' * 76)
k, start, gk, gcat, new, ds, dn, cells, tk, got = rows[0]
print(f'建議：金卷走 {k} 格到 {start}A → 打 {gk} 的必中（1500 罐頭）→ 落點 {dn}{ds}')
print(f'　　　再用 {tk - k} 張金卷走到 {cells[-1][0]}{ds}，共用 {tk} 張金卷，剩 {15 - tk} 張')
print(f'\n沿途可收（每格可換池）：')
print(f'  保底 @{start}A：' + '　'.join(f'{g}:{gu(g, "A", start)[0]}' for g in GUAR))
for n, opts in cells:
    print(f'  {n}{ds}（走 {n - dn + 1} 格）：' + '　'.join(f'{a}:{b}' for a, b in opts))
