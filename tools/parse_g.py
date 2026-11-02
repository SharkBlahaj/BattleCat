import sys, re, json
s = open(sys.argv[1], encoding='utf-8').read()
CELL = re.compile(
    r'<td\s+rowspan="1"\s+class="position (cat|score)([^"]*)"\s*'
    r'onclick="pick\(\'(\d+)([AB])(G?)(X?)\'\)"\s*>(.*?)</td>', re.S)
res, guar = {'A': {}, 'B': {}}, {'A': {}, 'B': {}}
for m in CELL.finditer(s):
    kind, cls, num, side, isG, isX, body = m.groups()
    if kind != 'cat' or isX:
        continue
    nm = re.search(r'title="[^"]*"[^>]*>([^<]+)</a>', body)
    cat = nm.group(1).strip() if nm else '?'
    rar = [w[6:] for w in cls.split() if w.startswith('major_')]
    rar = rar[0] if rar else '?'
    n = int(num)
    if isG:
        d = re.search(r'(?:-&gt;|&lt;-)\s*(\d+)([AB])', body)
        guar[side][n] = (cat, rar, (d.group(1) + d.group(2)) if d else None)
    else:
        res[side][n] = (cat, rar)
print('result A/B:', len(res['A']), len(res['B']), ' guar A/B:', len(guar['A']), len(guar['B']))
json.dump({'res': res, 'guar': guar}, open(sys.argv[2], 'w'), ensure_ascii=False)
TARGET = sys.argv[3] if len(sys.argv) > 3 else '搖滾俏喵'
print(f'\n=== {TARGET} 出現在哪 ===')
for side in 'AB':
    for n, (c, r) in sorted(res[side].items()):
        if c == TARGET:
            print(f'  單抽結果: {n}{side}  [{r}]')
for side in 'AB':
    for n, (c, r, d) in sorted(guar[side].items()):
        if c == TARGET:
            print(f'  11連必中: {n}{side} -> 落點 {d}  [{r}]')
