import sys, re
s = open(sys.argv[1], encoding='utf-8').read()
m = re.search(r'<select[^>]*name="event"[^>]*>(.*?)</select>', s, re.S)
for o in re.finditer(r'<option([^>]*)>(.*?)</option>', m.group(1), re.S):
    v = re.search(r'value="([^"]*)"', o.group(1))
    mark = ' *SEL*' if 'selected' in o.group(1) else ''
    t = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', o.group(2))).strip()
    print(f'{(v.group(1) if v else ""):20s} {t[:100]}{mark}')
print()
fg = re.search(r'<select[^>]*name="force_guaranteed"[^>]*>(.*?)</select>', s, re.S)
print('force_guaranteed select raw:', repr(fg.group(1)[:300]) if fg else 'ABSENT')
