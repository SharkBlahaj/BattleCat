import sys
sys.path.insert(0, '/home/user/BattleCat')
from data import track_1077_rock as R
from data import track_1078_fest as F
from data import track_legend_1064 as LG
from data import player_profile as P

HI = ('exclusive', 'uber', 'uber_fest', 'legend')
LBL = {'exclusive': 'Excl', 'uber': 'uber', 'uber_fest': 'uberF', 'legend': 'LEG'}

def f(cat, rar):
    if rar not in HI:
        return cat
    own = '已有' if cat in P.OWNED else '★未持有'
    return f'{cat}[{LBL[rar]}]{own}'

print('位置  | 1077 搖滾俏喵                   | 1078 超國王祭                   | 黑金卷 傳說轉蛋')
print('-' * 120)
for n in range(2, 47):
    cells = [f(R.A[n], R.RARITY['A'][n]), f(F.A[n], F.RARITY['A'][n]), f(LG.A[n], LG.RARITY['A'][n])]
    star = '  <<' if any('★' in c for c in cells) else ''
    print(f'{n:3d}A  | {cells[0]:30s} | {cells[1]:30s} | {cells[2]}{star}')

print('\n=== 2A~46A 高稀有格總表 ===')
for nm, A, RA in [('1077', R.A, R.RARITY['A']), ('1078', F.A, F.RARITY['A']),
                  ('黑金卷', LG.A, LG.RARITY['A'])]:
    hits = [(n, A[n], RA[n]) for n in range(2, 47) if RA[n] in HI]
    print(f'-- {nm} --')
    for n, c, r in hits:
        print(f'   {n:3d}A {LBL[r]:6s} {c:14s} {"已有" if c in P.OWNED else "★未持有"}')
