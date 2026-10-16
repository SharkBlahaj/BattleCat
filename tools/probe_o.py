import sys, re
s = open(sys.argv[1], encoding='utf-8').read()
for kw in ["'o'", '"o"', 'name="o"', '\\bo\\b=']:
    pass
print('--- JS 裡提到 o 的地方 ---')
for m in re.finditer(r"[^\n]{0,110}\bo\b\s*[=:\.\[][^\n]{0,110}", s):
    t = m.group(0).strip()
    if any(k in t for k in ('owned', 'name="o"', "'o'", '"o"', 'params', 'query')):
        print('  ', re.sub(r'\s+', ' ', t)[:200])
print('\n--- 連到 /cats 或設定頁的連結 ---')
seen = set()
for m in re.finditer(r'href="([^"]*(?:cats|owned|my)[^"]*)"', s):
    h = m.group(1)
    k = h.split('?')[0]
    if k in seen: continue
    seen.add(k); print('  ', h[:120])
