# -*- coding: utf-8 -*-
"""第五視圖（抽完搖滾俏喵之後）的規劃盤資料。"""
import json, sys, os
sys.path.insert(0, '/home/user/BattleCat')
from data import player_profile as PP
from data import history as H
D = sys.argv[1]
SRC = [
 ('1043', 'full_2026-10-18_1043.json', '日本戰國時代武將',   '~10/20 今天最後一天', True,  '罐頭'),
 ('1021', 'full_2026-10-18_1021.json', '電腦少女',           '~10/20 今天最後一天', True,  '罐頭'),
 ('1070', 'full_2026-10-20_1070.json', '孤月騎士路諾斯',     '10/20–10/26',        False, '罐頭'),
 ('1004', 'full_2026-10-20_1004.json', '宇宙盡頭的精靈',     '10/20–10/23',        False, '罐頭'),
 ('947',  'full_2026-10-20_947.json',  '正義與黑暗的救世主', '10/20–10/23',        False, '罐頭'),
 ('1071', 'full_2026-10-16_1071.json', '白金轉蛋',           '常駐',               False, '白金卷'),
 ('1072', 'full_2026-10-16_1072.json', '傳說轉蛋',           '常駐',               False, '黑金卷'),
 ('1069', 'full_2026-10-30_1069.json', '超級貓咪祭',         '10/30–11/02',        False, '罐頭'),
]
out = {'pools': {}, 'order': [s[0] for s in SRC]}
for key, f, label, period, guar, pay in SRC:
    d = json.load(open(os.path.join(D, 'dl1020', f)))
    out['pools'][key] = {
        'label': label, 'period': period, 'guar': guar, 'pay': pay,
        'A': [[d['res']['A'][str(n)][0], d['res']['A'][str(n)][1]] for n in range(1, 101)],
        'B': [[d['res']['B'][str(n)][0], d['res']['B'][str(n)][1]] for n in range(1, 101)],
        'G': {s + str(n): [v[0], v[2]] for s in 'AB' for n, v in d['guar'][s].items()},
        'reroll': {s + n: [v[0], v[2]] for s in 'AB' for n, v in d['reroll'][s].items()},
    }
out['hi'] = ['exclusive', 'uber', 'uber_fest', 'legend']
# 現役池裡出現、但不在已確認名冊內的超激／傳說 —— 要請玩家勾選的清單
HI_SET = set(out['hi'])
seen = {}
for key in out['order']:
    pl = out['pools'][key]
    for side in 'AB':
        for i, (c, r) in enumerate(pl[side]):
            if r in HI_SET:
                seen.setdefault(c, set()).add(key)
out['unknown'] = sorted(
    ({'name': c, 'pools': sorted(ps)} for c, ps in seen.items() if c not in PP.OWNED),
    key=lambda d: (-len(d['pools']), d['name']))
out['roster'] = {'ubers': PP.ROSTER_TRUTH['超激レア'],
                 'legends': PP.ROSTER_TRUTH['傳說レア'],
                 'legendOwned': sorted(PP.LEGEND_OWNED)}
out['owned'] = sorted(PP.OWNED)
out['resources'] = PP.RESOURCES
out['position'] = PP.POSITION
out['positionPending'] = PP.POSITION is None
out['positionLast'] = getattr(PP, 'POSITION_LAST_KNOWN', None)
out['positionNote'] = ('2026-10-20 戰國武神那發必中對不上任何起點：能一發同時拿到真田幸村和'
                       '成田甲斐的只有 9A 和 75A，但兩者都會帶到前田慶次，而你說這次沒抽到。'
                       '推測成田甲斐來自另一次單抽。需要你目前的 godfat 網址才能定位。')
_era = H.ERAS[-1]
out['done'] = {
    'title': _era['era'] + '：' + _era['note'].split('。')[0],
    'span': _era['note'],
    'cost': _era['cost'],
    'got': [g for st in _era['steps'] for g in st[4]],
    'steps': [{'pay': st[0], 'pool': st[1], 'from': st[2], 'to': st[3], 'got': st[4]}
              for st in _era['steps']],
}
json.dump(out, open('artifact/board_v5.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('bytes:', os.path.getsize('artifact/board_v5.json'))
print('1A 各池:', {k: out['pools'][k]['A'][0] for k in out['order']})
