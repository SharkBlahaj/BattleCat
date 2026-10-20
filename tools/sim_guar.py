# -*- coding: utf-8 -*-
"""模擬一發必中 11 連：走 10 格普通抽（含重複 reroll 會換軌），再加保底那一抽。
用 godfat 自己的落點回頭驗證模擬是否正確。"""
import json, sys
D = sys.argv[1]
d = json.load(open(D))
TARGETS = set(sys.argv[2:]) or {'真田幸村', '成田甲斐'}

res = {s: {int(n): v for n, v in d['res'][s].items()} for s in 'AB'}
rr  = {s: {int(n): v for n, v in d['reroll'][s].items()} for s in 'AB'}
gu  = {s: {int(n): v for n, v in d['guar'][s].items()} for s in 'AB'}

def step(side, n, last):
    """一次普通單抽 -> (抽到的貓, 下一個位置)。重複時走 godfat 的 reroll 落點。"""
    if n not in res[side]: return None
    cat = res[side][n][0]
    if cat != last:
        return cat, (side, n + 1)
    r = rr[side].get(n)
    if not r: return None                     # 會重複但沒有 reroll 資料 -> 無法判定
    dest = r[2]
    return r[0], (dest[-1], int(dest[:-1]))

def sim(side, n, last=None):
    """10 格普通抽 + 保底。回傳 (收穫清單, 保底角色, 模擬落點, godfat 落點)。"""
    got, cur, L = [], (side, n), last
    for _ in range(10):
        r = step(cur[0], cur[1], L)
        if r is None: return None
        cat, cur = r
        got.append(cat); L = cat
    g = gu[side].get(n)
    if not g: return None
    # 保底那一抽吃 1 格：從 cur 的起始槽再往前半步
    s2, n2 = cur
    mine = f'{n2}B' if s2 == 'A' else f'{n2+1}A'
    return got, g[0], mine, g[2]

ok = bad = 0
for s in 'AB':
    for n in sorted(gu[s]):
        out = sim(s, n)
        if out is None: continue
        if out[2] == out[3]: ok += 1
        else: bad += 1
print(f'落點驗證：模擬與 godfat 相符 {ok} 筆，不符 {bad} 筆')

print(f'\n=== 哪些起點的一發必中能同時拿到 {"、".join(sorted(TARGETS))} ===')
for s in 'AB':
    for n in sorted(gu[s]):
        out = sim(s, n)
        if out is None: continue
        got, guar, mine, gf = out
        allg = set(got) | {guar}
        if TARGETS <= allg:
            ub = [c for c in got if c in TARGETS]
            print(f'  {n}{s} -> 落點 {gf}；保底 {guar}；窗口內 {ub}')
