import sys, re
s = open(sys.argv[1], encoding='utf-8').read()
i = s.find('<table>')
print(s[i:i+700])
print('...')
j = s.find("pick('46A')")
print(s[max(0,j-1500):j+900])
