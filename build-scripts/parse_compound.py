# -*- coding: utf-8 -*-
import pymupdf, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')
d=pymupdf.open(r'C:\Users\leojai\.claude\projects\g--Leo-Workspace\576236a6-f7e9-4116-bd82-8969c16208cb\tool-results\webfetch-1788963181095-lpz5om.pdf')
# find the two s.359 tables by page text
free_pages=[]; court_pages=[]
started=False; mode=None
for i in range(d.page_count):
    tx=d[i].get_text('text')
    if '359. (1) The offences punishable' in tx: mode='free'; started=True
    if 'permission of the Court before which any prosecution' in tx: mode='court'
    if '360.' in tx and started and 'compounding' not in tx.lower(): 
        # end after table 2
        pass
    if started and mode=='free' and ('compounded by' in tx or re.search(r'\n\d{1,3}\s*\([0-9IVi]+\)',tx)):
        free_pages.append(i)
    if started and mode=='court':
        court_pages.append(i)
    if started and '360.' in tx and 'Bharatiya' in tx and i>court_pages[0] if court_pages else False:
        break
# simpler: scan 190..205
comp={}
for i in range(188,206):
    tx=d[i].get_text('text')
    m='court' if 'permission of the Court before which' in ''.join(d[k].get_text('text') for k in range(188,i+1)) else 'free'
    for t in d[i].find_tables().tables:
        for r in t.extract():
            if len(r)<3: continue
            cell=r[1] or ''
            for ref in re.findall(r'\d{1,3}\s*\([0-9IVXivx]+\)|(?<![\d(])\b\d{2,3}\b(?![\d)])', cell):
                key=re.sub(r'\s+','',ref)
                if re.match(r'\d',key) and key not in ('1','2','3'):
                    comp.setdefault(key, m)
print(len(comp),'compoundable refs')
for k,v in sorted(comp.items(), key=lambda x:(int(re.match(r'\d+',x[0]).group()),x[0])):
    print(k,v)
json.dump(comp, open('compound.json','w',encoding='utf-8'), indent=0)
