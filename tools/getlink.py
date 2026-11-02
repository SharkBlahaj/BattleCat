import sys, re
s = open(sys.argv[1], encoding='utf-8').read()
j = s.find("pick('%s')" % sys.argv[2])
blk = s[j:j+900]
m = re.search(r'href="(//bc\.godfat\.org/\?seed=\d+&amp;last=\d+[^"]*)"', blk)
print('https:' + m.group(1).replace('&amp;', '&'))
