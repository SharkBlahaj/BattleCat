import sys
sys.path.insert(0, '/home/user/BattleCat')
from data import track_legend_1064 as L
from data import player_profile as P

LBL = {'rare':'稀有', 'supa':'激レア', 'supa_fest':'激レア(祭限定)',
       'uber':'超激レア', 'uber_fest':'超激レア(祭限定)',
       'exclusive':'Exclusive 限定', 'legend':'傳說レア'}
HI = ('exclusive', 'uber', 'uber_fest')

print('玩家目前位置：view3 98B == 本表 2A\n')
print('=== 下 100 格 高稀有度格（godfat 標記 exclusive / uber / uber_fest）===')
for side in 'AB':
    print(f'\n-- {side} 軌 --')
    for n in L.TOP[side]:
        cat = L.LEGEND_1064[side][n]
        r = L.RARITY[side][n]
        own = '已有' if cat in P.OWNED else '★未持有'
        v3 = f'view3 {n+96}{"B" if side=="A" else ""}' if side == 'A' else f'view3 {n+97}A'
        if side == 'A':
            v3 = f'view3 {n+96}B'
        print(f'  {n:3d}{side}  {LBL[r]:16s} {cat:12s} {own}   ({v3})')

print('\n=== 未持有且是高稀有度的格子（黑金卷可直接拿）===')
seen = {}
for side in 'AB':
    for n in L.TOP[side]:
        cat = L.LEGEND_1064[side][n]
        if cat not in P.OWNED:
            seen.setdefault(cat, []).append(f'{n}{side}')
for cat, pos in sorted(seen.items(), key=lambda kv: int(kv[1][0][:-1])):
    print(f'  {cat:14s} {", ".join(pos)}')

print('\n=== 從 2A 出發，A 軌單抽可走到的前幾個未持有高稀有格 ===')
for n in L.TOP['A']:
    if n < 2: continue
    cat = L.LEGEND_1064['A'][n]
    if cat in P.OWNED: continue
    print(f'  {n}A  需推進 {n-2} 格  {LBL[L.RARITY["A"][n]]:16s} {cat}')
