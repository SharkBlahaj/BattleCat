import sys, re, json
s = open(sys.argv[1], encoding='utf-8').read()
CELL = re.compile(
    r'<td\s+rowspan="\d+"\s+class="position (cat|score)([^"]*)"\s*'
    r'onclick="pick\(\'(\d+)([AB])(G|R|)(X?)\'\)"\s*>(.*?)</td>', re.S)
out = {'res': {'A': {}, 'B': {}}, 'reroll': {'A': {}, 'B': {}}, 'guar': {'A': {}, 'B': {}}}
for m in CELL.finditer(s):
    kind, cls, num, side, suf, isX, body = m.groups()
    if kind != 'cat' or isX:
        continue
    nm = re.search(r'title="[^"]*"[^>]*>([^<]+)</a>', body)
    cat = nm.group(1).strip() if nm else '?'
    rar = ([w[6:] for w in cls.split() if w.startswith('major_')] or ['?'])[0]
    d = re.search(r'(?:-&gt;|&lt;-)\s*(\d+)([AB])', body)
    dest = (d.group(1) + d.group(2)) if d else None
    key = {'': 'res', 'R': 'reroll', 'G': 'guar'}[suf]
    out[key][side][int(num)] = (cat, rar, dest)
for k in out:
    print(k, {s2: len(out[k][s2]) for s2 in 'AB'})
json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False)
print('\nreroll 格（會換軌）:')
for side in 'AB':
    for n, (c, r, dd) in sorted(out['reroll'][side].items()):
        print(f'  {n}{side} -> {dd}   重抽成 {c}')
