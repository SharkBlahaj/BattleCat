import sys, re
s = open(sys.argv[1], encoding='utf-8').read()
for sel in re.finditer(r'<select([^>]*)>(.*?)</select>', s, re.S):
    nm = re.search(r'name="([^"]+)"', sel.group(1))
    print('=== select', nm.group(1) if nm else '?', '===')
    for o in re.finditer(r'<option([^>]*)>(.*?)</option>', sel.group(2), re.S):
        v = re.search(r'value="([^"]*)"', o.group(1))
        mark = ' *SELECTED*' if 'selected' in o.group(1) else ''
        t = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', o.group(2))).strip()
        if mark or (v and '1064' in (v.group(1) or '')) or '金' in t or '傳說' in t or 'チケ' in t:
            print(f'  {v.group(1) if v else "":22s} {t[:110]}{mark}')
