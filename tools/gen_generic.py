import sys, re, json
html, out, modname, title = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
s = open(html, encoding='utf-8').read()
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

L = ['# -*- coding: utf-8 -*-', f'"""{title}', '',
     '編號與 track_legend_1064 相同（seed=1830146318, last=595）。',
     '這張表 godfat 預設沒有 Guaranteed 欄 → 本活動沒有原生必中 11 連，',
     '只能單抽或普通 11 連（11 次連續單抽，同軌前進 11 格，不換軌）。',
     '',
     'RARITY 保留 godfat 原始 class：rare / supa / supa_fest / uber / uber_fest / exclusive / legend',
     '"""', '']
for side in 'AB':
    L.append(f'{side} = {{')
    for n in range(1, 101):
        L.append(f' {n:3d}: "{raw[side][n][0]}",')
    L += ['}', '']
for side in 'AB':
    L.append(f'RARITY_{side} = {{')
    for n in range(1, 101):
        L.append(f' {n:3d}: "{raw[side][n][1]}",')
    L += ['}', '']
L += [f'{modname} = {{"A": dict(A), "B": dict(B)}}',
      'RARITY = {"A": dict(RARITY_A), "B": dict(RARITY_B)}',
      'HAS_NATIVE_GUARANTEED = False',
      '',
      'TOP = {s: sorted(n for n, r in RARITY[s].items()',
      '                 if r in ("exclusive", "uber", "uber_fest", "legend"))',
      '       for s in "AB"}']
open(out, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('wrote', out)
