import sys, re
s = open(sys.argv[1], encoding='utf-8').read()
j = s.find("pick('%s')" % sys.argv[2])
blk = s[max(0, j-200):j+2600]
print(re.sub(r'\n\s*\n+', '\n', blk))
