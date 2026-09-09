# -*- coding: utf-8 -*-
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

sched = json.load(open('bnss_schedule.json', encoding='utf-8'))['by_sec']
comp = json.load(open('compound.json', encoding='utf-8'))

def cleanref(r):
    return r.replace('(I)', '(1)').replace('( ', '(').replace(' )', ')').replace(' ', '')

# compoundable set keyed by section number -> mode
comp_by_sec = {}
for k, v in comp.items():
    k = cleanref(k)
    n = re.match(r'\d+', k).group()
    # keep the "stronger" (free beats court for display simplicity? no—keep both)
    comp_by_sec.setdefault(n, set()).add(v)

meta = {}
for sec, rows in sched.items():
    out_rows = []
    seen = set()
    for r in rows:
        ref = cleanref(r.get('sec') or sec)
        key = (ref, r['c'], r['b'], r['court'])
        if key in seen:
            continue
        seen.add(key)
        if not r['c'] and not r['b'] and not r['court']:
            continue
        out_rows.append({'ref': ref, 'c': r['c'], 'b': r['b'], 'court': r['court'],
                         'off': re.sub(r'\s+', ' ', r['off']).strip()[:80]})
    if not out_rows:
        continue
    m = {'cls': out_rows}
    if sec in comp_by_sec:
        modes = comp_by_sec[sec]
        if 'free' in modes and 'court' in modes:
            m['comp'] = 'both'
        elif 'free' in modes:
            m['comp'] = 'free'
        else:
            m['comp'] = 'court'
    meta[sec] = m

json.dump(meta, open('bns_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('BNS_META sections:', len(meta))
for k in ['103', '105', '115', '117', '118', '303', '316', '318', '351', '85', '64', '69', '324']:
    if k in meta:
        print('\n', k, '| comp=', meta[k].get('comp'))
        for r in meta[k]['cls']:
            print('   ', r['ref'], '|', r['c'], '|', r['b'], '|', r['court'])
