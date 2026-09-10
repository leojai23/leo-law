# -*- coding: utf-8 -*-
import re, json, sys
sys.stdout.reconfigure(encoding='utf-8')

raw = open('bns_full.txt', encoding='utf-8').read()
lines = [l.strip() for l in raw.split('\n') if not l.startswith('===== PDF PAGE')]
txt = '\n'.join(lines)
body_start = txt.index('\n1. (1) This Act may be called the Bharatiya Nyaya Sanhita, 2023.')
arr = txt[:body_start].split('\n')

toc = {}
i = 0
prev = 0
while i < len(arr):
    m = re.match(r'^(\d{1,3})\.\s*$', arr[i].strip())
    if m:
        n = int(m.group(1))
        if n != prev + 1:
            break
        prev = n
        j = i + 1
        buf = []
        while j < len(arr):
            s = arr[j].strip()
            if re.match(r'^\d{1,3}\.\s*$', s):
                break
            if s.startswith('Note:') or 'For Reference only' in s or len(' '.join(buf)) > 220:
                break
            div = s.startswith('CHAPTER') or s.startswith('Of ') or (len(s) > 2 and s == s.upper() and s.lower() != s.upper())
            if s == '' or div:
                j += 1
                continue
            buf.append(s)
            j += 1
        toc[str(n)] = re.sub(r'\s+', ' ', ' '.join(buf)).strip().rstrip('.')
        i = j
    else:
        i += 1

body = json.load(open('bns_sections.json', encoding='utf-8'))
def norm(s):
    return re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()

diff = [(n, body[n]['heading'], toc.get(n, '')) for n in body if n in toc and norm(body[n]['heading']) != norm(toc[n])]
print('ToC entries: %d | body sections: %d | heading mismatches: %d' % (len(toc), len(body), len(diff)))
for n, a, b in diff:
    print('  BNS %s\n     body: %s\n     toc : %s' % (n, a, b))
missing = [n for n in map(str, range(1, 359)) if n not in body]
extra = [n for n in body if not (1 <= int(n) <= 358)]
print('missing from body parse:', missing)
print('extra keys:', extra)
