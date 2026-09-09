# -*- coding: utf-8 -*-
import pymupdf, re, json

PDF = r'C:\Users\leojai\.claude\projects\g--Leo-Workspace\576236a6-f7e9-4116-bd82-8969c16208cb\tool-results\webfetch-1788963181095-lpz5om.pdf'
d = pymupdf.open(PDF)

# locate First Schedule (BNS offences) page span
full = "".join(d[i].get_text('text') for i in range(d.page_count))
def page_of(sub):
    idx = full.index(sub)
    return full.count('===PAGE', 0, idx)  # not reliable without markers; use direct scan below

# direct: find start / end pages by text on page
start = end = None
for i in range(d.page_count):
    tx = d[i].get_text('text')
    if 'CLASSIFICATION OF OFFENCES' in tx and 'EXPLANATORY NOTES' in tx:
        start = i
    if 'CLASSIFICATION OF OFFENCES AGAINST OTHER LAWS' in tx:
        end = i
        break
print('First Schedule (BNS) pages:', start+1, 'to', end+1)

def norm(s):
    s = re.sub(r'\s+', ' ', (s or '').strip())
    return s

def clas_c(s):
    s = norm(s).lower().rstrip('.')
    if s.startswith('non-cognizable') or s.startswith('non- cognizable') or s.startswith('non cognizable'): return 'Non-cognizable'
    if s.startswith('cognizable'): return 'Cognizable'
    if 'according as' in s: return 'As per abetted/principal offence'
    return norm(s)

def clas_b(s):
    s = norm(s).lower().rstrip('.')
    if s.startswith('non-bailable') or s.startswith('non- bailable') or s.startswith('non bailable'): return 'Non-bailable'
    if s.startswith('bailable'): return 'Bailable'
    if 'according as' in s: return 'As per abetted/principal offence'
    return norm(s)

def court(s):
    s = norm(s).rstrip('.')
    s2 = s.lower()
    if 'court of session' in s2: return 'Court of Session'
    if 'magistrate of the first class' in s2: return 'Magistrate of the first class'
    if s2.startswith('any magistrate'): return 'Any Magistrate'
    if 'court by which offence abetted' in s2: return 'Court trying the principal offence'
    return s

rows = []
cur = None
for i in range(start, end + 1):
    tabs = d[i].find_tables()
    for t in tabs.tables:
        for r in t.extract():
            if len(r) < 6:
                continue
            sec = norm(r[0])
            off = norm(r[1])
            pun = norm(r[2])
            c = norm(r[3]); b = norm(r[4]); ct = norm(r[5])
            if sec == 'Section' or sec == '1' or (not sec and not off and not pun):
                continue
            if sec:
                cur = sec
                rows.append({'sec': sec, 'off': off, 'pun': pun,
                             'c': clas_c(c), 'b': clas_b(b), 'court': court(ct)})
            else:
                # continuation / variant row -> new sub-row under current section
                if off or pun or c or b:
                    rows.append({'sec': cur, 'off': off, 'pun': pun,
                                 'c': clas_c(c), 'b': clas_b(b), 'court': court(ct), 'variant': True})

print('rows parsed:', len(rows))

# index by leading integer section number
by_sec = {}
for r in rows:
    m = re.match(r'(\d+)', r['sec'])
    if not m:
        continue
    by_sec.setdefault(m.group(1), []).append(r)

print('distinct BNS sections with classification:', len(by_sec))
json.dump({'rows': rows, 'by_sec': by_sec},
          open('bnss_schedule.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

for k in ['103', '105', '115', '117', '118', '124', '303', '316', '318', '351', '85', '64', '69', '111', '318']:
    if k in by_sec:
        for r in by_sec[k]:
            print(k, '|', r['sec'], '|', r['c'], '|', r['b'], '|', r['court'], '|', r['off'][:45])
