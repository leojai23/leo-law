# -*- coding: utf-8 -*-
import re, json, sys
sys.stdout.reconfigure(encoding='utf-8')

t = open('concordance_uppolice.txt', encoding='utf-8').read()
t = re.sub(r'[ \t]*\n[ \t]*', ' ', t)
t = re.sub(r'\s{2,}', ' ', t)
# strip repeated running headers
t = t.replace('Bharatiya Nyaya Sanhita, 2023 (BNS) Indian Penal Code, 1860 (IPC)', ' | ')
t = re.sub(r'CHAPTER [IVXLC]+[A-Z]*', ' | ', t)
t = re.sub(r'\bOf [A-Za-z][a-z].*? (?=\d)', ' | ', t)   # "Of mischief Of Mischief "

# token stream: BNS subref | header (num. Title) | NEW | DEL
TOK = re.compile(r'(\d{1,3}\s*\((?:\d+|[IVXivx]+)\)(?:\s*,\s*\d{1,3}\s*\((?:\d+|[IVXivx]+)\))*)'
                 r'|(\d{1,3}[A-Z]{0,3})\.\s+([A-Z][^|]*?)(?=(?:\s\d{1,3}[A-Z]{0,3}\.\s+[A-Z])|(?:\s\d{1,3}\s*\()|(?:\s(?:New|Deleted|Repealed|Omitted|Explanation))|\s\||$)'
                 r'|\b(New Sub-?\s?Section|New Section|New|Deleted|Repealed|Omitted)\b')
toks = []
for m in TOK.finditer(t):
    if m.group(1):
        toks.append(('bref', re.sub(r'\s+', '', m.group(1))))
    elif m.group(2):
        toks.append(('head', m.group(2), m.group(3).strip()))
    elif m.group(4):
        toks.append(('none', m.group(4)))
    if t[m.start():m.start()+3] == ' | ':
        pass

# alternation walk: BNS first
ipc2bns = {}
pairs = []
active = []
slot = 'B'
i = 0
sepskip = 0
for tok in toks:
    k = tok[0]
    if k == 'bref':
        active = [x for x in tok[1].split(',')]
        slot = 'I'
        continue
    if k == 'none':
        if slot == 'I':
            pairs.append((None, list(active))); slot = 'B'
        continue
    if k == 'head':
        num, title = tok[1], tok[2]
        if slot == 'B':
            active = [num]; slot = 'I'
        else:
            pairs.append((num, list(active)))
            for b in active:
                bs = re.match(r'\d{1,3}', b).group()
                ipc2bns.setdefault(num, set()).add(bs)
            slot = 'B'
        continue

# ---- load DATA ----
html = open(r'g:\Leo-Workspace\Leo-Law\index.html', encoding='utf-8').read()
draw = html[html.index('var DATA=['):html.index('\n];', html.index('var DATA=['))]
rows = re.findall(r'\{f:"[^\n]*?\},?', draw)
def fld(rt, k):
    m = re.search(r'(?<![A-Za-z])' + k + r':"((?:[^"\\]|\\.)*)"', rt)
    return m.group(1) if m else ''
DATA = [dict(ipc=fld(r,'ipc'), bns=fld(r,'bns'), t=fld(r,'t'), s=fld(r,'s')) for r in rows]

def toks_ipc(s):
    s = s.replace('\u2013','-'); o=[]
    for p in re.split(r'[\/,]', s):
        p=p.strip()
        m=re.match(r'(\d{1,3})\s*-\s*(\d{1,3})$',p)
        if m: o+=[str(x) for x in range(int(m.group(1)),int(m.group(2))+1)]
        else:
            mm=re.match(r'(\d{1,3}[A-Z]{0,3})',p)
            if mm:o.append(mm.group(1))
    return o
def secs_bns(s):
    s=re.sub(r'\([^)]*\)','',s).replace('\u2013','-'); o=[]
    for p in re.split(r'[\/,]', s):
        p=p.strip()
        m=re.match(r'(\d{1,3})\s*-\s*(\d{1,3})$',p)
        if m: o+=[str(x) for x in range(int(m.group(1)),int(m.group(2))+1)]
        else:
            mm=re.match(r'(\d{1,3})',p)
            if mm:o.append(mm.group(1))
    return o

print('tokens %d | ipc2bns %d' % (len(toks), len(ipc2bns)))
bad=[]
for d in DATA:
    if d['s'] in ('gone','new'): continue
    mine=set(secs_bns(d['bns']))
    for ipc in toks_ipc(d['ipc']):
        w=ipc2bns.get(ipc)
        if not w:
            bad.append(('NO-ENTRY',d['ipc'],ipc,d['bns'],'',d['t'])); continue
        if not (mine & w):
            bad.append(('MISMATCH',d['ipc'],ipc,d['bns'],'/'.join(sorted(w,key=str)),d['t']))
print('\n%d issues\n'%len(bad))
for p in sorted(bad): print('%-9s IPC %-13s tok %-6s app=%-16s official=%-12s | %s'%p)
json.dump({k:sorted(v) for k,v in ipc2bns.items()}, open('cmap2.json','w',encoding='utf-8'), ensure_ascii=False, indent=0)
