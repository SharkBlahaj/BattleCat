import sys, re
s = open(sys.argv[1], encoding='utf-8').read()
for tag in sys.argv[2:]:
    j = s.find("pick('%s')" % tag)
    if j < 0: print(tag, 'NOT FOUND'); continue
    blk = s[j:j+800]
    nm = re.search(r'title="[^"]*"[^>]*>([^<]+)</a>', blk)
    cls = s.rfind('class="position', 0, j)
    arrow = re.search(r'(?:-&gt;|&lt;-)\s*(\d+[AB])', blk)
    print(f"{tag:6s} class={s[cls+15:j-20].strip()[:52]!r}")
    print(f"        cat={nm.group(1) if nm else '?'}  arrow={arrow.group(1) if arrow else None}")
