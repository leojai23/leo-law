# -*- coding: utf-8 -*-
import re, json

raw = open('bns_full.txt', encoding='utf-8').read()
lines = raw.split('\n')

# ---- strip PDF page markers + pure-blank noise, keep a flat line list with line origin ----
clean = []
for ln in lines:
    if ln.startswith('===== PDF PAGE'):
        continue
    clean.append(ln.strip())

txt = '\n'.join(clean)

# ---- 1. arrangement of sections -> {num: heading} ----
# arrangement lives before the body. Body starts at "1. (1) This Act may be called".
body_start = txt.index('\n1. (1) This Act may be called the Bharatiya Nyaya Sanhita, 2023.')
arr_txt = txt[:body_start]
body_txt = txt[body_start+1:]

arr_lines = [l for l in arr_txt.split('\n')]
headings = {}
i = 0
prev = 0
while i < len(arr_lines):
    m = re.match(r'^(\d{1,3})\.\s*$', arr_lines[i].strip())
    if m:
        n = int(m.group(1))
        if n != prev + 1:            # hit a comparative table / out-of-order -> stop
            break
        prev = n
        j = i + 1
        buf = []
        while j < len(arr_lines):
            s = arr_lines[j].strip()
            if re.match(r'^\d{1,3}\.\s*$', s):
                break
            if s.startswith('Note:') or 'For Reference only' in s or len(' '.join(buf)) > 220:
                break
            is_divider = (s.startswith('CHAPTER') or s.startswith('Of ')
                          or (len(s) > 2 and s == s.upper() and s.lower() != s.upper()))
            if s == '' or is_divider:
                j += 1
                continue
            buf.append(s)
            j += 1
        h = ' '.join(buf)
        h = re.sub(r'\s+', ' ', h).strip().rstrip('.').strip()
        headings[n] = h
        i = j
    else:
        i += 1

print('arrangement parsed:', len(headings), 'sections; last =', prev)

# ---- 2. body: slice each section N from its "^N. " anchor to "^(N+1). " ----
def anchor(n):
    return re.compile(r'(?m)^%d\.(?=\s|\()' % n)

sections = {}
maxn = prev
# find start positions sequentially
pos = 0
starts = {}
for n in range(1, maxn + 1):
    m = anchor(n).search(body_txt, pos)
    if not m:
        # try a looser anchor: "^N." then newline+content
        m = re.compile(r'(?m)^%d\.$' % n).search(body_txt, pos)
    if not m:
        print('  !! no anchor for section', n)
        continue
    starts[n] = m.start()
    pos = m.end()

def strip_trailing_heading(s, nextn):
    if nextn not in headings:
        return s.rstrip()
    h = headings[nextn].strip().rstrip('.').strip()
    if not h:
        return s.rstrip()
    pat = r'\s+'.join(re.escape(w) for w in h.split())
    s2 = re.sub(pat + r'[\s.]*$', '', s, flags=re.I)
    return s2.rstrip()

for n in range(1, maxn + 1):
    if n not in starts:
        continue
    st = starts[n]
    en = starts.get(n + 1, len(body_txt))
    chunk = body_txt[st:en]
    # cut trailing next-chapter header block (appears only at chapter boundaries)
    mch = re.search(r'\bCHAPTER\s+[IVXLC]+\b', chunk)
    if mch and len(chunk) - mch.start() < 500:
        chunk = chunk[:mch.start()]
    # cut trailing PDF appendix junk after the final section
    for marker in ('Note: For Reference only', 'CORRESPONDING SECTION TABLE'):
        mk = chunk.find(marker)
        if mk != -1:
            chunk = chunk[:mk]
    chunk = strip_trailing_heading(chunk, n + 1)
    # strip trailing decorative rule / dash run
    chunk = re.sub(r'[\s‒-―─-╿_*·]+$', '', chunk)
    # drop leading "N."
    chunk = re.sub(r'^\d{1,3}\.[ \t]*', '', chunk.strip())
    # join wrapped lines -> single spaces
    one = re.sub(r'\s*\n\s*', ' ', chunk)
    one = re.sub(r'[ \t]{2,}', ' ', one).strip()
    # re-introduce paragraph breaks
    one = re.sub(r'\s+(Illustrations?\.)', r'\n\n\1', one)
    one = re.sub(r'\s+(Explanation(?:\s+\d+)?\.\s*[—-])', r'\n\n\1', one)
    one = re.sub(r'\s+(Exception\s+\d+\.\s*[—-])', r'\n\n\1', one)
    one = re.sub(r'\s+(Provided (?:further )?that)', r'\n\1', one)
    one = re.sub(r'(?<=[.;:])\s+(\(\d+[A-Za-z]?\)\s)', r'\n\n\1', one)   # sub-sections
    one = re.sub(r'(?<=[;:])\s+(\([a-z]\)\s)', r'\n\1', one)             # lettered clauses
    one = one.strip()
    sections[n] = {'heading': headings.get(n, ''), 'text': one}

json.dump(sections, open('bns_sections.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('body parsed:', len(sections), 'sections written to bns_sections.json')

# quick sanity dump
for k in (100, 101, 103, 104, 115, 118, 316, 318, 351, 63, 64, 69, 111):
    if k in sections:
        s = sections[k]
        print('\n----', k, '|', s['heading'], '----')
        print(s['text'][:700])
