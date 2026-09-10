# -*- coding: utf-8 -*-
# Reliable BSA<->IEA mapping by heading similarity (sidesteps 2-column PDF order ambiguity).
import re, json, sys
sys.stdout.reconfigure(encoding='utf-8')

bsa = json.load(open('bsa_sections.json', encoding='utf-8'))            # {n:{heading,text}}
iea_head = json.load(open('bsa_map.json', encoding='utf-8'))['iea_head']  # {ieaN: heading}

# also pull ALL IEA headings straight from the concordance stream (more complete)
t = open('bsa_concordance.txt', encoding='utf-8').read()
t = re.sub(r'[ \t]*\n[ \t]*', ' ', t); t = re.sub(r'\s{2,}', ' ', t)
t = re.sub(r'P\s*a\s*g\s*e\s*\|\s*\d+', ' ', t)
# IEA side headings: after collecting, we just harvest every "<n>. <Titlecase...>." and keep the
# ones that look like Evidence-Act sections (1..167). Ambiguous with BSA numbers, so we keep a MULTI dict.
cand = {}
for m in re.finditer(r'(?<![\d(])\b(\d{1,3})\.\s+([A-Z][^.]{4,}?\.)', t):
    n, h = m.group(1), m.group(2).strip().rstrip('.').strip()
    cand.setdefault(n, set()).add(h)

STOP = set('the of a an or to for by in and etc with on as is are be no not when which that this section'.split())
def toks(s):
    return {w for w in re.findall(r'[a-z]+', s.lower()) if w not in STOP and len(w) > 2}

# Build IEA heading pool: prefer iea_head; supplement with cand where key not a known BSA-only high number
iea_pool = {}
for k, v in iea_head.items():
    iea_pool.setdefault(k, set()).add(v)
for k, vs in cand.items():
    if int(k) <= 167:
        for v in vs:
            iea_pool.setdefault(k, set()).add(v)

rows = []
for n in map(str, range(1, 171)):
    bh = bsa[n]['heading']
    # trim trailing leaked side-heading: keep text up to first '. ' that is followed by a capital AND
    # the remaining looks like a separate short phrase -- conservative: only if >1 '. '
    bt = toks(bh)
    best, bestj = None, 0.0
    for ie, hs in iea_pool.items():
        for h in hs:
            it = toks(h)
            if not it or not bt:
                continue
            j = len(bt & it) / len(bt | it)
            if j > bestj:
                bestj, best = j, (ie, h)
    status = 'renum'
    iea = None
    if best and bestj >= 0.5:
        iea = best[0]
        if iea == n and bestj > 0.85:
            status = 'mapped'
    elif bh.lower().startswith('repeal'):
        iea, status = None, 'mapped'
    else:
        status = 'new'
    rows.append({'bsa': n, 'iea': iea, 'heading': bh, 'status': status,
                 'match': round(bestj, 2), 'iea_head': best[1] if best else ''})

json.dump(rows, open('bsa_rows.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
weak = [r for r in rows if r['status'] != 'mapped' and (r['match'] < 0.6)]
print('rows:', len(rows), '| new/weak:', len(weak))
for r in rows:
    if r['bsa'] in ('1','2','3','4','6','15','19','20','22','23','24','25','54','58','61','62','63','105','120','143','170') or r['status']=='new':
        print('BSA %-4s -> IEA %-5s  j=%.2f  %-8s | %s' % (r['bsa'], r['iea'], r['match'], r['status'], r['heading'][:52]))
