# -*- coding: utf-8 -*-
import re, json, sys
sys.stdout.reconfigure(encoding='utf-8')

raw = open('concordance_uppolice.txt', encoding='utf-8').read()
lines = [l.rstrip() for l in raw.split('\n')]

# ---- join wrapped lines into entries ----
START = re.compile(r'^\s*(\d{1,3}[A-Z]{0,3}\.\s+[A-Za-z(]|\d{1,3}\s*\([0-9IVXivx]+\)\s*(,\s*\d{1,3}\s*\([0-9IVXivx]+\)\s*)*[.,]?\s*$|New Sub|New Section|New\b|Deleted|Repealed|Omitted|CHAPTER\s|Of\s[a-z]|OF\s[A-Z])')
entries = []
buf = ''
for ln in lines:
    s = ln.strip()
    if not s:
        continue
    if START.match(s):
        if buf: entries.append(buf.strip())
        buf = s
    else:
        buf += ' ' + s
if buf: entries.append(buf.strip())

SUBREF = re.compile(r'^(\d{1,3}\s*\([0-9IVXivx]+\)\s*)(,\s*\d{1,3}\s*\([0-9IVXivx]+\)\s*)*[.,]?\s*$')
HEAD   = re.compile(r'^(\d{1,3}[A-Z]{0,3})\.\s+(.*)$')
STOP = {'the','of','a','an','or','to','for','with','in','by','and','any','such','on','which',
        'person','punishment','etc','when','from','be','it','his','her','other','definition'}
def words(s):
    return {w for w in re.findall(r'[a-z]+', s.lower()) if w not in STOP and len(w) > 2}

def refs_of(e):
    return [re.sub(r'\s+', '', x) for x in re.findall(r'\d{1,3}\s*\([0-9IVXivx]+\)', e)]
def secnum(r):
    return re.match(r'(\d{1,3})', r).group(1)

# ---- local adjacency pairing ----
ipc2bns = {}
def add(ipc, bns_secs):
    for b in bns_secs:
        ipc2bns.setdefault(ipc, set()).add(b)

for i in range(len(entries) - 1):
    a, b = entries[i], entries[i + 1]
    # case 1: BNS subref  ->  IPC header
    if SUBREF.match(a):
        mb = HEAD.match(b)
        if mb and not SUBREF.match(b):
            add(mb.group(1), {secnum(r) for r in refs_of(a)})
        continue
    # case 2: BNS header  ->  IPC header  (headings must overlap)
    ma, mb = HEAD.match(a), HEAD.match(b)
    if ma and mb and not SUBREF.match(a) and not SUBREF.match(b):
        wa, wb = words(ma.group(2)), words(mb.group(2))
        if len(wa & wb) >= 2 or (wa and wa <= wb) or (wb and wb <= wa):
            add(mb.group(1), {ma.group(1)})

# ---------- load app DATA ----------
html = open(r'g:\Leo-Workspace\Leo-Law\index.html', encoding='utf-8').read()
draw = html[html.index('var DATA=['):html.index('\n];', html.index('var DATA=['))]
rowtxts = re.findall(r'\{f:"[^\n]*?\},?', draw)
def field(rt, key):
    m = re.search(r'(?<![A-Za-z])' + key + r':"((?:[^"\\]|\\.)*)"', rt)
    return m.group(1) if m else ''
DATA = [dict(ipc=field(r,'ipc'), bns=field(r,'bns'), t=field(r,'t'), s=field(r,'s')) for r in rowtxts]

def ipc_tokens(s):
    s = s.replace('\u2013', '-'); out = []
    for part in re.split(r'[\/,]', s):
        part = part.strip()
        m = re.match(r'(\d{1,3})\s*-\s*(\d{1,3})$', part)
        if m: out += [str(x) for x in range(int(m.group(1)), int(m.group(2)) + 1)]
        else:
            mm = re.match(r'(\d{1,3}[A-Z]{0,3})', part)
            if mm: out.append(mm.group(1))
    return out
def bns_secnums(s):
    s = re.sub(r'\([^)]*\)', '', s).replace('\u2013', '-'); out = []
    for part in re.split(r'[\/,]', s):
        part = part.strip()
        m = re.match(r'(\d{1,3})\s*-\s*(\d{1,3})$', part)
        if m: out += [str(x) for x in range(int(m.group(1)), int(m.group(2)) + 1)]
        else:
            mm = re.match(r'(\d{1,3})', part)
            if mm: out.append(mm.group(1))
    return out

print('entries %d | ipc2bns keys %d | DATA %d' % (len(entries), len(ipc2bns), len(DATA)))
issues = []
for d in DATA:
    if d['s'] in ('gone', 'new'): continue
    mine = set(bns_secnums(d['bns']))
    for ipc in ipc_tokens(d['ipc']):
        want = ipc2bns.get(ipc)
        if not want:
            issues.append(('NO-ENTRY', d['ipc'], ipc, d['bns'], '', d['t'])); continue
        if not (mine & want):
            issues.append(('MISMATCH', d['ipc'], ipc, d['bns'],
                           '/'.join(sorted(want, key=str)), d['t']))
print('\n%d issues (MISMATCH = concordance disagrees; NO-ENTRY = not found by parser)\n' % len(issues))
for p in sorted(issues):
    print('%-9s IPC %-13s tok %-6s app=%-16s concordance=%-12s | %s' % p)

json.dump({k: sorted(v) for k, v in ipc2bns.items()},
          open('concordance_map.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
