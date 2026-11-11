# -*- coding: utf-8 -*-
"""第五視圖（抽完搖滾俏喵之後）的規劃盤資料。"""
import json, sys, os
sys.path.insert(0, '/home/user/BattleCat')
from data import player_profile as PP
from data import history as H
D = sys.argv[1]
SRC = [
 ('1080', 'full_2026-11-09_1080.json', '龍一（熱血大運動會）',   '11/09–11/16', True,  '罐頭'),
 ('1079', 'full_2026-11-09_1079.json', '熱血大運動會（陣容更新）', '11/09–11/16', False, '罐頭'),
 ('926',  'full_2026-11-09_926.json',  '萬聖節限定',             '11/09–11/16', True,  '罐頭'),
 ('1071', 'full_2026-10-16_1071.json', '白金轉蛋',               '常駐',        False, '白金卷'),
 ('1072', 'full_2026-10-16_1072.json', '傳說轉蛋',               '常駐',        False, '黑金卷'),
]
out = {'pools': {}, 'order': [s[0] for s in SRC]}
for key, f, label, period, guar, pay in SRC:
    d = json.load(open(os.path.join(D, 'dl1111', f)))
    out['pools'][key] = {
        'label': label, 'period': period, 'guar': guar, 'pay': pay,
        'A': [[d['res']['A'][str(n)][0], d['res']['A'][str(n)][1]] for n in range(1, 101)],
        'B': [[d['res']['B'][str(n)][0], d['res']['B'][str(n)][1]] for n in range(1, 101)],
        'G': {s + str(n): [v[0], v[2]] for s in 'AB' for n, v in d['guar'][s].items()},
        'reroll': {s + n: [v[0], v[2]] for s in 'AB' for n, v in d['reroll'][s].items()},
    }
out['hi'] = ['exclusive', 'uber', 'legend']   # 非祭典池：uber_fest 格實際吐雜魚
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


json.dump(out, open('artifact/board_v5.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('route added')

ROUTE = {
    'title': '建議路線',
    'deadline': '1080 與 926 都有必中，到 11/16 為止。B 軌有 9 個你還沒有的超激格，A 軌只有 4 個 —— 必中是唯一的換軌手段',
    'summary': '24A 走一格 → 25A 打必中換到 B 軌 → 一路走到 80B 再打第二發必中。收 9 隻，資源剛好用完（1079 多給兩格的選擇，但不增加格數）',
    'cost': {'罐頭': 3750, '稀有卷': 39, '黑金卷': 1},
    'left': {'罐頭': 0, '稀有卷': 0, '黑金卷': 0},
    'steps': [
        {'pos': '24A', 'pay': '金卷 ×1', 'note': '過路（鬥牛士貓）', 'opts': []},
        {'pos': '25A', 'pay': '必中 · 1500 罐頭', 'note': '落點 35B',
         'opts': [['1080', '保底 猿帝・悟空貓 ★']]},
        {'pos': '35B–37B', 'pay': '金卷 ×3', 'note': '過路', 'opts': []},
        {'pos': '38B', 'pay': '金卷 ×1', 'note': '四選一',
         'opts': [['1080', '一寸法師'], ['1079', '金太郎'],
                  ['926', '惡魔珊迪亞（留給 39B）'], ['1072', '宵之伊邪那美（要用票）']]},
        {'pos': '39B', 'pay': '金卷 ×1', 'note': '',
         'opts': [['926', '惡魔珊迪亞']]},
        {'pos': '40B–54B', 'pay': '金卷 ×15', 'note': '過路', 'opts': []},
        {'pos': '55B', 'pay': '票券 ×1', 'note': '票券三選二之一',
         'opts': [['1071/1072', '幼獸加歐']]},
        {'pos': '56B', 'pay': '金卷 ×1', 'note': '',
         'opts': [['926', '南瓜索多姆'], ['1071', '天誅飛隼'], ['1072', '貓若丸']]},
        {'pos': '57B–61B', 'pay': '金卷 ×5', 'note': '過路', 'opts': []},
        {'pos': '62B', 'pay': '票券 ×1', 'note': '票券三選二之一',
         'opts': [['1071/1072', '閃電機兵飛雷']]},
        {'pos': '63B–69B', 'pay': '金卷 ×7', 'note': '過路', 'opts': []},
        {'pos': '70B', 'pay': '金卷 ×1', 'note': '四選一',
         'opts': [['1080', '龍騎士巴魯斯'], ['1079', '神龍卡姆庫拉'],
                  ['926', '龍騎士斯卡巴魯斯（留給 80B 保底）'], ['1072', '奇幻貓（要用票）']]},
        {'pos': '71B–74B', 'pay': '金卷 ×4', 'note': '金卷到此用罄', 'opts': []},
        {'pos': '75B/76B', 'pay': '票券 ×1', 'note': '票券三選二之一（與 55B／62B 擇二）',
         'opts': [['1071/1072', '歡笑揮舞孃']]},
        {'pos': '77B–78B', 'pay': '罐頭 ×2', 'note': '過路', 'opts': []},
        {'pos': '79B', 'pay': '罐頭 ×1', 'note': '',
         'opts': [['926', '甜心溫蒂'], ['1072', '終末兵器・異滅堂']]},
        {'pos': '80B', 'pay': '必中 · 1500 罐頭', 'note': '窗口在 84B 會 reroll，落點 91B',
         'opts': [['926', '保底 龍騎士斯卡巴魯斯 ★'], ['1080', '保底 象頭神迦內薩（已有）']]},
    ],
}
out['route'] = ROUTE
json.dump(out, open('artifact/board_v5.json', 'w'), ensure_ascii=False, separators=(',', ':'))
