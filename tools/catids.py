import sys, re, json
s = open(sys.argv[1], encoding='utf-8').read()
CELL = re.compile(r'<td\s+rowspan="\d+"\s+class="position (cat)([^"]*)"\s*'
                  r'onclick="pick\(\'(\d+)([AB])(G|R|)(X?)\'\)"\s*>(.*?)</td>', re.S)
ids = {}
for m in CELL.finditer(s):
    _, cls, n, side, suf, isX, body = m.groups()
    if suf or isX: continue
    nm = re.search(r'title="[^"]*"[^>]*>([^<]+)</a>', body)
    cid = re.search(r'/cats/(\d+)\?', body)
    if nm and cid: ids[f'{n}{side}'] = (nm.group(1), cid.group(1))
for k in ['1A','2A','3A','1B','2B']:
    print(k, ids.get(k))
json.dump(ids, open(sys.argv[2],'w'), ensure_ascii=False)
