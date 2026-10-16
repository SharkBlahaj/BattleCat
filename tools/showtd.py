import sys, re
s = open(sys.argv[1], encoding='utf-8').read()
CELL = re.compile(r'<td\s+rowspan="\d+"\s+class="position (cat|score)([^"]*)"\s*'
                  r'onclick="pick\(\'(\d+)([AB])(G|R|)(X?)\'\)"\s*>(.*?)</td>', re.S)
want = set(sys.argv[2:])
for m in CELL.finditer(s):
    kind, cls, n, side, suf, isX, body = m.groups()
    tag = n + side + suf + ('X' if isX else '')
    if kind != 'cat' or isX or tag not in want: continue
    nm = re.search(r'title="[^"]*"[^>]*>([^<]+)</a>', body)
    ar = re.findall(r'(?:-&gt;|&lt;-)\s*(\d+[AB])', body)
    print(f"{tag:6s} rar={[w[6:] for w in cls.split() if w.startswith('major_')]}  "
          f"cat={nm.group(1) if nm else '?':16s} arrows={ar}")
