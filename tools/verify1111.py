# -*- coding: utf-8 -*-
"""逐格驗證 11/11 的完整路線，並對帳資源。"""
import json, sys, os
sys.path.insert(0, '/home/user/BattleCat')
from data import player_profile as PP

D = sys.argv[1]
TICKET_PICK = sys.argv[2] if len(sys.argv) > 2 else '55,62'   # 票券放哪兩格
EV = {'1080': '2026-11-09_1080', '926': '2026-11-09_926',
      '1071': '2026-10-16_1071', '1072': '2026-10-16_1072'}
P = {k: json.load(open(os.path.join(D, 'dl1111', f'full_{e}.json'))) for k, e in EV.items()}
HI = {'exclusive', 'uber', 'legend'}
picks = {int(x) for x in TICKET_PICK.split(',')}


def res(k, s, n): return P[k]['res'][s].get(str(n))
def rr(k, s, n):  return P[k]['reroll'][s].get(str(n))
def gu(k, s, n):  return P[k]['guar'][s].get(str(n))


tick, food, plat, leg = 39, 3750, 1, 1
got, last = set(), '黃金貓'
pos = ('A', 24)
log = []


def single(pool, pay):
    global pos, last, tick, food, plat, leg
    s, n = pos
    v = res(pool, s, n)
    c, r = v[0], v[1]
    assert c != last, f'{n}{s} 與上一抽重複（{c}）→ 會觸發 reroll'
    new = r in HI and c not in PP.OWNED and c not in got
    if pay == '金卷':   tick -= 1
    elif pay == '罐頭': food -= 150
    elif pay == '白金卷': plat -= 1
    elif pay == '黑金卷': leg -= 1
    if new: got.add(c)
    log.append((f'{n}{s}', pay + '@' + pool, c, new))
    last = c
    pos = (s, n + 1)


def guaranteed(pool):
    global pos, last, food
    s, n = pos
    g = gu(pool, s, n)
    assert g, f'{n}{s} 沒有必中資料'
    cur, L, ub = (s, n), last, []
    for _ in range(10):
        v = res(pool, cur[0], cur[1])
        c, r = v[0], v[1]
        if c == L:                                  # 窗口內重複 -> reroll，多吃一格並換軌
            x = rr(pool, cur[0], cur[1])
            assert x, f'{cur[1]}{cur[0]} 重複但沒有 reroll 資料'
            log.append((f'{cur[1]}{cur[0]}', '　└ reroll', f'{c} 重複 → 重抽成 {x[0]}，跳到 {x[2]}', False))
            c = x[0]; d = x[2]; cur = (d[-1], int(d[:-1])); r = 'rare'
        else:
            cur = (cur[0], cur[1] + 1)
        if r in HI: ub.append(c)
        L = c
    ub.append(g[0])
    food -= 1500
    new = [c for c in ub if c not in PP.OWNED and c not in got]
    got.update(new)
    d = g[2]
    log.append((f'{n}{s}', f'必中@{pool}', f'保底 {g[0]} → 落點 {d}' +
                (f'（收 {"、".join(new)}）' if new else ''), bool(new)))
    last = g[0]
    pos = (d[-1], int(d[:-1]))


single('1080', '金卷')                 # 24A
guaranteed('1080')                     # 25A → 35B
for n in range(35, 80):                # 35B..79B
    if n in picks:
        single('1071' if plat else '1072', '白金卷' if plat else '黑金卷')
    elif n == 38: single('1080', '金卷' if tick else '罐頭')
    elif n == 39: single('926',  '金卷' if tick else '罐頭')
    elif n == 56: single('926',  '金卷' if tick else '罐頭')
    elif n == 70: single('1080', '金卷' if tick else '罐頭')
    elif n == 79: single('926',  '金卷' if tick else '罐頭')
    else:         single('1080', '金卷' if tick else '罐頭')
guaranteed('926')                      # 80B → 91B

print(f'收穫 {len(got)} 隻：{"、".join(sorted(got))}\n')
for p, pay, c, new in log:
    if new or '必中' in pay:
        print(f'  {p:5s} {pay:12s} {c}' + ('  ★' if new and "必中" not in pay else ''))
print(f'\n結束在 {pos[1]}{pos[0]}')
print(f'資源：金卷 39→{tick}、罐頭 3750→{food}、白金卷 1→{plat}、黑金卷 1→{leg}')
assert tick >= 0 and food >= 0 and plat >= 0 and leg >= 0, '資源超支！'
print('逐格驗證：全程不觸發 reroll ✓，資源沒有超支 ✓')
