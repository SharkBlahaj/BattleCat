import sys, itertools
sys.path.insert(0, '/home/user/BattleCat')
from data import player_profile as P

START, GOAL = 2, 46          # A 軌，2A 出發，目標 46A 的單抽結果
RARE, LEG, FOOD = 24, 2, 1000
SINGLE, ELEVEN = 150, 1500

best = []
# 情形一：最後用普通 11 連，起點 p 使窗口 [p, p+10] 含 46
# 情形二：走到 46A 再單抽一次
for mode in ('11連收尾', '單抽收尾'):
    for g in range(0, 4):                      # 推進途中用幾次普通 11 連
        for t in range(0, 60):
            for k in range(0, LEG + 1):
                if mode == '11連收尾':
                    for p in range(GOAL - 10, GOAL + 1):
                        m = p - START          # 收尾 11 連前要推進的格數
                        s = m - t - k - 11 * g
                        if s < 0: continue
                        food = s * SINGLE + (g + 1) * ELEVEN
                        best.append((food, t, k, s, g + 1, mode, p))
                else:
                    m = GOAL - START           # 走到 46A
                    s = m - t - k - 11 * g
                    if s < 0: continue
                    # 46A 這一抽：優先用剩下的稀有卷，沒有就花 150 罐頭
                    if t < RARE:
                        food = s * SINGLE + g * ELEVEN; tt = t + 1
                    else:
                        food = (s + 1) * SINGLE + g * ELEVEN; tt = t
                    best.append((food, tt, k, s, g, mode, GOAL))

best.sort()
print(f'{"罐頭":>6} {"稀有卷":>6} {"黑金卷":>6} {"單抽":>5} {"11連":>5}  收尾方式   11連起點')
seen = set()
for food, t, k, s, g, mode, p in best[:400]:
    key = (food, t, k, mode)
    if key in seen: continue
    seen.add(key)
    if len(seen) > 12: break
    print(f'{food:6d} {t:6d} {k:6d} {s:5d} {g:5d}  {mode}   {p}A')

print(f'\n手上資源：罐頭 {FOOD}、稀有卷 {RARE}、黑金卷 {LEG}')
feasible = [b for b in best if b[0] <= FOOD and b[1] <= RARE and b[2] <= LEG]
print('現有資源可行方案數:', len(feasible))
cheapest = min(b for b in best if b[1] <= RARE and b[2] <= LEG)
print(f'最省罐頭方案：罐頭 {cheapest[0]}（稀有卷 {cheapest[1]}、黑金卷 {cheapest[2]}、'
      f'單抽 {cheapest[3]}、11連 {cheapest[4]}、{cheapest[5]}）→ 還缺罐頭 {cheapest[0]-FOOD}')
# 若不加罐頭，需要幾張稀有卷
for extra in range(0, 60):
    ok = [b for b in best if b[0] <= FOOD and b[1] <= RARE + extra and b[2] <= LEG]
    if ok:
        b = min(ok)
        print(f'不補罐頭的話：需要稀有卷 {b[1]} 張（再補 {b[1]-RARE} 張），'
              f'罐頭用 {b[0]}、黑金卷 {b[2]}、單抽 {b[3]}、11連 {b[4]}、{b[5]}')
        break
