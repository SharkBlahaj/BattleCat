import json, sys
d = json.load(open(sys.argv[1]))
res={s:{int(n):v for n,v in d['res'][s].items()} for s in 'AB'}
rr ={s:{int(n):v for n,v in d['reroll'][s].items()} for s in 'AB'}
gu ={s:{int(n):v for n,v in d['guar'][s].items()} for s in 'AB'}
HI={'exclusive','uber','uber_fest','legend'}
for tag in sys.argv[2:]:
    side, n0 = tag[-1], int(tag[:-1])
    g = gu[side].get(n0)
    if not g: print(f'{tag}: 無必中資料'); continue
    cur=(side,n0); L=None; ubers=[]
    print(f'=== 從 {tag} 打必中 11 連 → 落點 {g[2]} ===')
    for i in range(10):
        s,n=cur; c,r,_=res[s][n]
        if c==L:
            x=rr[s][n]; c=x[0]; dest=x[2]; cur=(dest[-1],int(dest[:-1])); tag2=' [REROLL 換軌]'
        else:
            cur=(s,n+1); tag2=''
        mark=' ★超激' if r in HI else ''
        if r in HI: ubers.append(c)
        print(f'   {i+1:2d}. {n}{s}  {c}{mark}{tag2}')
        L=c
    print(f'   11. 保底  {g[0]}  ★超激')
    ubers.append(g[0])
    print(f'   → 超激：{"、".join(ubers)}\n')
