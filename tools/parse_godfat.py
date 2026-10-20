import sys, re, json
src = open(sys.argv[1], encoding='utf-8').read()

# page header / event info
ttl = re.search(r'<title>(.*?)</title>', src, re.S)
print("TITLE:", ttl.group(1).strip() if ttl else "?")
for m in re.finditer(r'<h2[^>]*>(.*?)</h2>', src, re.S):
    t = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    if t: print("H2:", t[:160])
ul = re.search(r'<div class="seed">(.*?)</div>', src, re.S)

# every cat cell: onclick="pick('NA')" (no trailing X)
CELL = re.compile(
    r'<td\s+rowspan="1"\s+class="position (cat|score)([^"]*)"\s*'
    r'onclick="pick\(\'(\d+)([AB])(X?)\'\)"\s*>(.*?)</td>', re.S)

rows = {'A': {}, 'B': {}}
for m in CELL.finditer(src):
    kind, cls, num, side, isX, body = m.groups()
    if kind != 'cat' or isX:
        continue
    name = re.search(r'title="([^"]*)"[^>]*>([^<]+)</a>', body)
    cat = name.group(2).strip() if name else re.sub(r'<[^>]+>', '', body).strip()
    if 'exclusive' in cls: rar = '超激'
    elif 'legend' in cls:  rar = '傳說'
    elif 'rare' in cls:    rar = '激'
    else:                  rar = '?'
    rows[side][int(num)] = (cat, rar)

print("A cells:", len(rows['A']), "B cells:", len(rows['B']))
print("max A:", max(rows['A']), "max B:", max(rows['B']))
json.dump(rows, open(sys.argv[2], 'w'), ensure_ascii=False, indent=0)

# any non-empty guaranteed cell anywhere?
G = re.compile(r'<td\s+rowspan="1"\s+class="position cat\s*"\s*>(.*?)</td>', re.S)
ne = [g.group(1) for g in G.finditer(src) if g.group(1).strip()]
print("non-empty guaranteed cells:", len(ne), "/ total guar cells:", len(list(G.finditer(src))))
