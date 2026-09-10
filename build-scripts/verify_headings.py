# -*- coding: utf-8 -*-
# 1.2 (partial): cross-check BNS section boundaries + headings from our parse
# against the INDEPENDENT official IPC-BNS concordance (different govt PDF).
import re, json, sys
sys.stdout.reconfigure(encoding='utf-8')

# ---- our parse ----
mine = json.load(open('bns_sections.json', encoding='utf-8'))  # {"1": {"heading":...,"text":...}}

# ---- concordance: pull BNS headings ----
t = open('concordance_uppolice.txt', encoding='utf-8').read()
t = re.sub(r'[ \t]*\n[ \t]*', ' ', t)
t = re.sub(r'\s{2,}', ' ', t)
# The concordance lists, for each BNS section:  "<n>. <BNS heading>. [(Change)]"  followed by IPC "<m>. <heading>."
# Collect the FIRST occurrence of "<n>. <Titlecase...>" that is plausibly the BNS side.
conc = {}
for m in re.finditer(r'(?<![\d(])\b(\d{1,3})\.\s+([A-Z][^.]*?(?:\.[^.]*?){0,3}?\.)(?=\s|\()', t):
    n = m.group(1)
    h = m.group(2)
    if n in conc:
        continue
    conc[n] = h

def norm(s):
    s = s.lower()
    s = re.sub(r'\(change\)|\(new\)|\(new section\)', ' ', s)
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    # drop very common filler to compare loosely
    return s

def toks(s):
    return set(norm(s).split()) - {'of','the','a','an','or','to','for','by','in','and','etc','with','on','punishment'}

print('our sections: %d | concordance BNS headings captured: %d' % (len(mine), len(conc)))
miss = []
weak = []
for n in map(str, range(1, 359)):
    if n not in mine:
        miss.append(('MISSING-IN-PARSE', n, '', conc.get(n, '')))
        continue
    mh = mine[n]['heading']
    ch = conc.get(n)
    if not ch:
        weak.append(('no-concordance-heading', n, mh, ''))
        continue
    a, b = toks(mh), toks(ch)
    if not a or not b:
        continue
    j = len(a & b) / max(1, len(a | b))
    if j < 0.45:
        miss.append(('HEADING-DIVERGES j=%.2f' % j, n, mh, ch))

print('\n==== %d heading divergences / missing ====' % len(miss))
for r in miss:
    print('%-22s BNS %-4s | ours: %-55s | concordance: %s' % (r[0], r[1], r[2][:55], r[3][:70]))
print('\n(%d sections had no clean concordance heading to compare — expected for consolidated/new provisions)' % len(weak))
