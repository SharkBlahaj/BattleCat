import sys, re
for p in sys.argv[1:]:
    s = open(p, encoding='utf-8').read()
    G = re.compile(r'<td\s+rowspan="1"\s+class="position cat\s*"\s*>(.*?)</td>', re.S)
    cells = [g.group(1) for g in G.finditer(s)]
    ne = [c for c in cells if c.strip()]
    ev = re.search(r'<option[^>]*value="([^"]*)"[^>]*selected', s)
    # rowspan>1 on cat cells = a guaranteed spanning several rows
    spans = re.findall(r'<td\s+rowspan="(\d+)"\s+class="position cat', s)
    big = [x for x in spans if x != '1']
    print(f'{p.split("/")[-1]:26s} guar cells={len(cells):4d} non-empty={len(ne):4d} rowspan>1={len(big)}')
