# -*- coding: utf-8 -*-
"""把 1077 規劃所需的資料打包成前端用的 JSON。"""
import json, sys
sys.path.insert(0, '/home/user/BattleCat')
from data import player_profile as PP
D = sys.argv[1]
SRC = {
 '1077': (D+'/dl1077/full1077.json', '搖滾俏喵', '10/09–10/16'),
 '1078': (D+'/dl1077/full1078.json', '超國王祭', '10/09–10/13'),
 '1043': (D+'/dl1077/full_2026-10-09_1043.json', '戰國武將', '10/09–10/11'),
 '946':  (D+'/dl1077/full_2026-10-11_946.json', '超古代勇者', '10/11–10/13'),
 '991':  (D+'/dl1077/full_2026-10-13_991.json', '偉大神們', '10/13–10/16'),
 '1059': (D+'/dl1077/full_2026-10-13_1059.json', '龍族', '10/13–10/16'),
 '942':  (D+'/dl1077/full_2026-10-05_942.json', '即戰力', '~10/09'),
 '黑金卷': (D+'/full1064.json', '傳說轉蛋', '~10/16'),
}
HI = ('exclusive', 'uber', 'uber_fest', 'legend')
out = {'pools': {}, 'order': list(SRC)}
for k, (path, label, period) in SRC.items():
    d = json.load(open(path))
    out['pools'][k] = {
        'label': label, 'period': period,
        'A': [[d['res']['A'][str(n)][0], d['res']['A'][str(n)][1]] for n in range(1, 101)],
        'B': [[d['res']['B'][str(n)][0], d['res']['B'][str(n)][1]] for n in range(1, 101)],
        'reroll': {f'{s}{n}': [v[0], v[2]] for s in 'AB' for n, v in d['reroll'][s].items()},
    }
out['hi'] = list(HI)
out['owned'] = sorted(PP.OWNED)
out['resources'] = PP.RESOURCES
out['position'] = '2A'
out['heuristics'] = PP.HEURISTICS
json.dump(out, open('artifact/board1077.json', 'w'), ensure_ascii=False, separators=(',', ':'))
import os
print('bytes:', os.path.getsize('artifact/board1077.json'))
