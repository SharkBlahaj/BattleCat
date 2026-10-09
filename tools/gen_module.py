import sys, json
new = json.load(open(sys.argv[1]))
T = {s: {int(k): v for k, v in new[s].items()} for s in 'AB'}

# re-read raw classes from the html for fidelity
import re
s = open(sys.argv[2], encoding='utf-8').read()
CELL = re.compile(r'<td\s+rowspan="1"\s+class="position (cat|score)([^"]*)"\s*'
                  r'onclick="pick\(\'(\d+)([AB])(X?)\'\)"\s*>(.*?)</td>', re.S)
raw = {'A': {}, 'B': {}}
for m in CELL.finditer(s):
    k, cls, n, sd, x, body = m.groups()
    if k != 'cat' or x:
        continue
    r = [w[6:] for w in cls.split() if w.startswith('major_')][0]
    nm = re.search(r'title="[^"]*"[^>]*>([^<]+)</a>', body)
    raw[sd][int(n)] = (nm.group(1).strip(), r)

out = []
out.append('# -*- coding: utf-8 -*-')
out.append('"""黑金卷（傳說轉蛋）抽軌 — godfat event 2026-07-24_1064, seed 1830146318, last=595。')
out.append('')
out.append('單抽制，godfat 沒有提供 Guaranteed 欄（黑金卷一次一張，無必中 11 連），')
out.append('所以每抽就是在同一軌往前 1 格。')
out.append('')
out.append('與舊編號（track_data_v3 / track_tickets，以下稱 view3）的對應關係，')
out.append('已用重疊的 7 格逐格驗證，0 筆不符，且與 Fate/活動3/活動4 三張食物表全部不符')
out.append('（確認這張就是票池）：')
out.append('')
out.append('    本表 A[n] == view3 B[n+96]')
out.append('    本表 B[n] == view3 A[n+97]')
out.append('')
out.append('也就是軌道標籤又互換了一次。玩家目前位置 view3 98B == 本表 2A。')
out.append('')
out.append('RARITY 直接保留 godfat 自己的 class 名稱，不做二次解讀：')
out.append('    rare / supa / supa_fest / uber / uber_fest / exclusive / legend')
out.append('（godfat 色標說明：supa=Super、uber=Uber、legend=Legendary、')
out.append('  *_fest=只在 Uberfest/Epicfest/Royalfest 出現、exclusive=Exclusive）')
out.append('"""')
out.append('')
out.append('VIEW_OFFSET = {"A": ("B", 96), "B": ("A", 97)}  # 本表 side[n] == view3 other[n+off]')
out.append('')
for side in 'AB':
    out.append(f'{side} = {{')
    for n in range(1, 101):
        cat, _ = raw[side][n]
        out.append(f' {n:3d}: "{cat}",')
    out.append('}')
    out.append('')
for side in 'AB':
    out.append(f'RARITY_{side} = {{')
    for n in range(1, 101):
        _, r = raw[side][n]
        out.append(f' {n:3d}: "{r}",')
    out.append('}')
    out.append('')
out.append('LEGEND_1064 = {"A": dict(A), "B": dict(B)}')
out.append('RARITY = {"A": dict(RARITY_A), "B": dict(RARITY_B)}')
out.append('')
out.append('# godfat 在這 200 格裡標記的高稀有度格（exclusive / uber / uber_fest）')
out.append('TOP = {s: sorted(n for n, r in RARITY[s].items()')
out.append('                 if r in ("exclusive", "uber", "uber_fest"))')
out.append('       for s in "AB"}')
open(sys.argv[3], 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('wrote', sys.argv[3], len(out), 'lines')
