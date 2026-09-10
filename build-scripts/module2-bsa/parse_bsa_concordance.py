# -*- coding: utf-8 -*-
import re, json, sys
sys.stdout.reconfigure(encoding='utf-8')

t = open('bsa_concordance.txt', encoding='utf-8').read()
t = re.sub(r'[ \t]*\n[ \t]*', ' ', t)
t = re.sub(r'\s{2,}', ' ', t)
for junk in ['HomePage', 'Note: For Reference only',
             'Corresponding Section Table of BSA with Repealed Act',
             'BHARATIYA SAKSHYA ADHINIYAM, 2023 INDIAN EVIDENCE ACT, 1872',
             'BHARATIYA SAKSHYA ADHINIYAM, 2023', 'INDIAN EVIDENCE ACT, 1872']:
    t = t.replace(junk, ' | ')
t = re.sub(r'P\s*a\s*g\s*e\s*\|\s*\d+', ' | ', t)
t = re.sub(r'(PART|CHAPTER)\s+[IVXLC0-9]+[A-Z]*', ' | ', t)

# entry starts
TOK = re.compile(
    r'(\d{1,3})\.\s+(Proviso\s+\d+|Explanation(?:\s+\d+)?|Illustration[s]?)\b'   # sub-ref
    r'|(\d{1,3})\.\s+([A-Z][^|]*?)(?=(?:\s\d{1,3}\.\s+(?:[A-Z]|Proviso|Explanation))|(?:\s(?:New Section|New|Repealed|Omitted|Deleted))|\s\||$)'
    r'|\b(New Section|New|Repealed|Omitted|Deleted)\b')
toks = []
for m in TOK.finditer(t):
    if m.group(1):
        toks.append(('sub', m.group(1), m.group(2).strip()))
    elif m.group(3):
        toks.append(('head', m.group(3), m.group(4).strip().rstrip('.').strip()))
    elif m.group(5):
        toks.append(('none', m.group(5)))

# alternation: BSA first, IEA second
bsa = {}            # bsa_sec -> {heading, iea:set}
iea_head = {}       # iea_sec -> heading
slot = 'BSA'
cur_bsa = None
cur_bsa_sub = None
for tk in toks:
    if tk[0] == 'head':
        n, h = tk[1], tk[2]
        if slot == 'BSA':
            cur_bsa = n; cur_bsa_sub = None
            bsa.setdefault(n, {'heading': h, 'iea': set()})
            if not bsa[n]['heading']:
                bsa[n]['heading'] = h
            slot = 'IEA'
        else:
            if cur_bsa:
                bsa.setdefault(cur_bsa, {'heading': '', 'iea': set()})
                bsa[cur_bsa]['iea'].add(n)
                iea_head[n] = h
            slot = 'BSA'
    elif tk[0] == 'sub':
        # "22. Proviso 1"  -> still BSA section cur, another mapping slot
        if slot == 'BSA':
            cur_bsa = tk[1]
            slot = 'IEA'
        # else ignore (IEA-side proviso label)
    elif tk[0] == 'none':
        if slot == 'IEA':
            slot = 'BSA'   # BSA section with no IEA equivalent (New Section)

out = {'bsa': {k: {'heading': v['heading'], 'iea': sorted(v['iea'], key=lambda x: int(x))}
               for k, v in bsa.items()},
       'iea_head': iea_head}
json.dump(out, open('bsa_map.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print('BSA sections in concordance:', len(bsa), '| IEA headings:', len(iea_head))
for k in ['1', '2', '3', '15', '22', '23', '24', '61', '62', '63', '105', '120', '170']:
    if k in bsa:
        print('BSA %-4s %-55s -> IEA %s' % (k, bsa[k]['heading'][:55], bsa[k]['iea']))
