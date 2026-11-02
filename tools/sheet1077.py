import sys, json
sys.path.insert(0, '/home/user/BattleCat')
from data import track_legend_1064 as LG
from data import player_profile as P

D = sys.argv[1]
r77 = json.load(open(D + '/rows1077.json'))
r78 = json.load(open(D + '/rows1078.json'))
A77 = {int(k): v for k, v in r77['A'].items()}
A78 = {int(k): v for k, v in r78['A'].items()}

HI = ('exclusive', 'uber', 'uber_fest')
def tag(cell):
    cat, rar = cell
    if rar not in HI: return ''
    return ' ★' + ('已有' if cat in P.OWNED else '未持有')

print('位置  | 1077 搖滾俏喵池          | 1078 超國王祭            | 黑金卷(傳說轉蛋)')
print('-' * 108)
for n in range(2, 47):
    a, b = A77[n], A78[n]
    c = (LG.A[n], LG.RARITY['A'][n])
    def f(x):
        return f'{x[0]}{tag(x)}'
    print(f'{n:3d}A  | {f(a):24s} | {f(b):24s} | {f(c)}')

print()
print('=== 2A→46A 這段，各池的高稀有格 ===')
for nm, T in [('1077', A77), ('1078', A78), ('黑金卷', {n: (LG.A[n], LG.RARITY["A"][n]) for n in LG.A})]:
    hits = [(n, v[0], v[1]) for n, v in sorted(T.items())
            if 2 <= n <= 46 and v[1] in HI]
    print(f'\n-- {nm} --')
    for n, cat, rar in hits:
        own = '已有' if cat in P.OWNED else '★未持有'
        print(f'  {n:3d}A  {rar:10s} {cat:14s} {own}')
