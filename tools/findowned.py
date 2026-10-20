import sys, re
s = open(sys.argv[1], encoding='utf-8').read()
print('--- 含 owned 的片段 ---')
for m in re.finditer(r'owned', s):
    seg = s[max(0,m.start()-120):m.start()+120].replace('\n',' ')
    print(' …', re.sub(r'\s+',' ',seg))
print('\n--- 所有 form / input / textarea ---')
for m in re.finditer(r'<(form|input|textarea|button)([^>]*)>', s):
    t = re.sub(r'\s+',' ',m.group(0))
    if 'hidden' in t and 'seed' in t: continue
    print(' ', t[:190])
