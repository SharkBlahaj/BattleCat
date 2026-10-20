# -*- coding: utf-8 -*-
"""考慮「重複 reroll 會換軌」的最短成本搜尋：2A -> 抽到搖滾俏喵。

狀態 = (軌, 格號, 上一隻抽到的貓, 剩餘稀有卷, 剩餘黑金卷)
動作 = 在某個池單抽，或在 1077/1078 打一發普通 11 連（11 次連抽，同池）
成本 = 罐頭（稀有卷/黑金卷視為免費但有張數上限）
"""
import json, heapq, sys

D = sys.argv[1]
POOLS = {
    '1077': D + '/dl1077/full1077.json',
    '1078': D + '/dl1077/full1078.json',
    '1043': D + '/dl1077/full_2026-10-09_1043.json',
    '991':  D + '/dl1077/full_2026-10-13_991.json',
    '946':  D + '/dl1077/full_2026-10-11_946.json',
    '1059': D + '/dl1077/full_2026-10-13_1059.json',
    '942':  D + '/dl1077/full_2026-10-05_942.json',
    '黑金卷': D + '/full1064.json',
}
P = {}
for k, v in POOLS.items():
    d = json.load(open(v))
    P[k] = {
        'res': {s: {int(n): t for n, t in d['res'][s].items()} for s in 'AB'},
        'rr':  {s: {int(n): t for n, t in d['reroll'][s].items()} for s in 'AB'},
    }
FOOD_POOLS = [k for k in P if k != '黑金卷']
TICKET_POOLS = ['黑金卷']          # 稀有卷只能抽食物池；黑金卷只能抽傳說轉蛋

SINGLE, ELEVEN = 150, 1500
import sys as _s; _s.path.insert(0,'/home/user/BattleCat')
from data import player_profile as PP
HI = ('exclusive', 'uber', 'uber_fest', 'legend')
UBER_BONUS = int(__import__('os').environ.get('UBER_BONUS', '0'))   # 每隻未持有超激折抵的罐頭
LEG_SHADOW = int(__import__('os').environ.get('LEG_SHADOW', '0'))   # 黑金卷的影子成本

def value(pool, side, n, cat):
    t = P[pool]['res'][side].get(n)
    if not t or t[1] not in HI: return 0
    if cat in PP.OWNED: return 0
    return -UBER_BONUS
RARE0, LEG0 = 50, 3
TARGET = '搖滾俏喵'

def nxt(side, n):
    return ('A', n + 1) if side == 'A' else ('B', n + 1)

def step(pool, side, n, last):
    """回傳 (抽到的貓, 下一個位置, 是否 reroll)；無法判定時回 None。"""
    cat = P[pool]['res'][side].get(n)
    if cat is None:
        return None
    cat = cat[0]
    if cat != last:
        return cat, nxt(side, n), False
    rr = P[pool]['rr'][side].get(n)
    if rr is None:
        return None                      # 會重複但沒有 godfat 的 reroll 資料 -> 保守不走
    rcat, _, dest = rr
    return rcat, (dest[-1], int(dest[:-1])), True

def eleven(pool, side, n, last):
    """普通 11 連：同池連抽 11 次。回傳 (抽到的貓清單, 終點, last)。"""
    got, cur, L = [], (side, n), last
    for _ in range(11):
        r = step(pool, cur[0], cur[1], L)
        if r is None:
            return None
        cat, cur, _ = r
        got.append(cat)
        L = cat
    return got, cur, L

START = ('A', 2, '冥佑天女露娜夏', RARE0, LEG0)
dist = {START: 0}
prev = {}
pq = [(0, START)]
goal = None
while pq:
    c, st = heapq.heappop(pq)
    if c > dist.get(st, 1 << 60):
        continue
    side, n, last, nr, nl = st
    if n > 96:
        continue
    def push(cost, ns, how):
        if cost < dist.get(ns, 1 << 60):
            dist[ns] = cost
            prev[ns] = (st, how)
            heapq.heappush(pq, (cost, ns))
    # 單抽
    for pool in P:
        r = step(pool, side, n, last)
        if r is None:
            continue
        cat, (s2, n2), rr = r
        if pool == '黑金卷':
            if nl == 0: continue
            opts = [(LEG_SHADOW, nr, nl - 1, '黑金卷')]
        else:
            opts = [(SINGLE, nr, nl, '罐頭')] + ([(0, nr - 1, nl, '稀有卷')] if nr else [])
        for addc, nr2, nl2, pay in opts:
            if pool != '黑金卷' and cat == TARGET:
                if c + addc < dist.get('GOAL', 1 << 60):
                    dist['GOAL'] = c + addc
                    prev['GOAL'] = (st, f'{n}{side} 用{pay}抽 {pool} -> {TARGET}')
                continue
            push(c + addc + value(pool, side, n, cat), (s2, n2, cat, nr2, nl2),
                 f'{n}{side} {pay}抽{pool} -> {cat}' + (' [REROLL換軌]' if rr else ''))
    # 普通 11 連（只在食物池）
    for pool in FOOD_POOLS:
        e = eleven(pool, side, n, last)
        if e is None:
            continue
        got, (s2, n2), L = e
        if TARGET in got:
            if c + ELEVEN < dist.get('GOAL', 1 << 60):
                dist['GOAL'] = c + ELEVEN
                prev['GOAL'] = (st, f'{n}{side} 11連@{pool} -> 含{TARGET}')
            continue
        v = 0
        cur2 = (side, n); L2 = last
        for g in got:
            v += value(pool, cur2[0], cur2[1], g)
            r2 = step(pool, cur2[0], cur2[1], L2); cur2 = r2[1]; L2 = g
        push(c + ELEVEN + v, (s2, n2, L, nr, nl), f'{n}{side} 11連@{pool}')

print('最低罐頭成本:', dist.get('GOAL', '無解'))
path, cur = [], 'GOAL'
while cur in prev:
    st, how = prev[cur]
    path.append(how)
    cur = st
for i, h in enumerate(reversed(path), 1):
    print(f'{i:3d}. {h}')
