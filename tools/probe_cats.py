import sys, re
s = open(sys.argv[1], encoding='utf-8').read()
print('--- 表單 / 控制項 ---')
for m in re.finditer(r'<(form|input|textarea|select|button|label)([^>]*)>', s):
    t = re.sub(r'\s+', ' ', m.group(0))
    print('  ', t[:170])
print('\n--- 說明文字 ---')
for m in re.finditer(r'<(p|li|h2|h3)[^>]*>(.*?)</\1>', s, re.S):
    t = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', m.group(2))).strip()
    if t and ('owned' in t.lower() or '持有' in t or 'Owned' in t or len(t) > 40):
        print('  ', t[:200])
