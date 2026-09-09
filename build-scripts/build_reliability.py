# -*- coding: utf-8 -*-
import json

SRC = r"g:\Leo-Workspace\Leo-Law\index.html"
meta = json.load(open('bns_meta.json', encoding='utf-8'))
blob = json.dumps(meta, ensure_ascii=False, separators=(',', ':')).replace('<', r'\u003c')

html = open(SRC, encoding='utf-8').read()

# 1. meta blob before main script
marker = '<script>\n/* ---------------- theme'
assert marker in html
html = html.replace(marker,
    '<script type="application/json" id="bns-meta">' + blob + '</script>\n' + marker, 1)

# 2. parse it
anchor = "var BNS_TEXT = JSON.parse(document.getElementById('bns-data').textContent);"
assert anchor in html
html = html.replace(anchor,
    anchor + "\nvar BNS_META = JSON.parse(document.getElementById('bns-meta').textContent);", 1)

# 3. classification helpers + detail integration
old_paras_end = """    return '<p'+cls+'>'+p.replace(/\\n/g,'<br>')+'</p>';
  }).join('');
}
function detailHTML(d){
  var h="";
  bnsNums(d).forEach(function(n){
    var s=BNS_TEXT[n];
    if(!s) return;
    h+='<div class="bns-sec"><h4>BNS '+n+' \u00b7 '+esc(s.heading)+'</h4><div class="txt">'+paras(s.text)+'</div></div>';
  });"""
new_paras_end = """    return '<p'+cls+'>'+p.replace(/\\n/g,'<br>')+'</p>';
  }).join('');
}
var COMP_LABEL={free:'Compoundable (BNSS s.359(1))',court:"Compoundable with the Court's permission (BNSS s.359(2))",both:'Compoundable \u2014 some sub-sections without and some with the Court\\'s permission (BNSS s.359)'};
function classBlock(n){
  var m=BNS_META[n];
  if(!m) return '';
  var rows=m.cls.map(function(r){
    return '<tr><td>'+esc(r.ref)+'</td><td>'+esc(r.c||'\u2014')+'</td><td>'+esc(r.b||'\u2014')+'</td><td>'+esc(r.court||'\u2014')+'</td></tr>';
  }).join('');
  var comp = m.comp ? '<div class="comp">'+esc(COMP_LABEL[m.comp])+'</div>' : '';
  return '<div class="cls-wrap"><div class="cls-h">Classification \u2014 BNSS First Schedule</div>'
    + '<table class="cls-tbl"><thead><tr><th>\u00a7</th><th>Cognizable</th><th>Bailable</th><th>Triable by</th></tr></thead><tbody>'
    + rows + '</tbody></table>' + comp + '</div>';
}
function uniformClass(n){
  var m=BNS_META[n]; if(!m) return null;
  var c=m.cls[0]; if(!c.c) return null;
  for(var i=1;i<m.cls.length;i++){ if(m.cls[i].c!==c.c||m.cls[i].b!==c.b) return null; }
  return c;
}
function classChip(d){
  var ns=bnsNums(d); if(!ns.length) return '';
  var c=uniformClass(ns[0]);
  if(!c){ return BNS_META[ns[0]] ? '<span class="chip-cls varies">classification varies \u2014 see detail</span>' : ''; }
  var cg=/^Cog/.test(c.c), nb=/^Non-bail/.test(c.b);
  return '<span class="chip-cls '+(cg?'cg':'ncg')+'">'+(cg?'Cognizable':'Non-cog.')+'</span>'
       + '<span class="chip-cls '+(nb?'nb':'bl')+'">'+(nb?'Non-bailable':'Bailable')+'</span>';
}
function detailHTML(d){
  var h="";
  bnsNums(d).forEach(function(n){
    var s=BNS_TEXT[n];
    if(!s) return;
    h+='<div class="bns-sec"><h4>BNS '+n+' \u00b7 '+esc(s.heading)+'</h4><div class="txt">'+paras(s.text)+'</div>'+classBlock(n)+'</div>';
  });"""
assert old_paras_end in html, "paras/detailHTML anchor not found"
html = html.replace(old_paras_end, new_paras_end, 1)

# 4. provenance line (replace dcite)
old_cite = '''  h+='<p class="dcite">Statutory text reproduced from the Bharatiya Nyaya Sanhita, 2023 (Gazette of India \u2014 public domain). Confirm against indiacode.nic.in before citing.</p>';'''
new_cite = '''  h+='<p class="dcite"><b>Provenance.</b> BNS text \u2014 Bharatiya Nyaya Sanhita, 2023, Gazette of India (public domain). IPC\u2194BNS mapping \u2014 cross-checked against the official Ministry / State-Police IPC\u2013BNS concordance. Classification \u2014 BNSS, 2023 First Schedule; compounding \u2014 BNSS s.359. Reconciled 9 Sep 2026. This is a finding aid: confirm the current text against indiacode.nic.in and check for later amendments and notifications before citing.</p>';'''
assert old_cite in html, "dcite anchor not found"
html = html.replace(old_cite, new_cite, 1)

# 5. card rail chip
old_rail = '''    + (hasDetail?'<button class="card-toggle" aria-expanded="false">bare act \u25be</button>':'')
    + '</div>\''''
new_rail = '''    + classChip(d)
    + (hasDetail?'<button class="card-toggle" aria-expanded="false">bare act \u25be</button>':'')
    + '</div>\''''
assert old_rail in html
html = html.replace(old_rail, new_rail, 1)

# 6. Sources & method details block
old_main = '<main>\n  <div class="count" id="count"></div>'
new_main = '''<main>
  <details class="sources">
    <summary>Sources &amp; method &mdash; how reliable is this?</summary>
    <div class="sources-body">
      <p><b>Bare-act text.</b> Every BNS section is reproduced verbatim from the official <b>Gazette of India</b> text of the Bharatiya Nyaya Sanhita, 2023 (public domain under s.52(1)(q) of the Copyright Act, 1957), machine-parsed and structurally checked. All 358 sections are embedded.</p>
      <p><b>IPC &harr; BNS mapping.</b> Hand-compiled, then reconciled against the official <b>IPC&ndash;BNS corresponding-sections concordance</b>; every flagged discrepancy was checked by hand against the concordance and the section text. Six mapping errors were found and fixed in the 9 Sep 2026 pass.</p>
      <p><b>Classification.</b> Cognizable / bailable / court-triable are taken from the <b>BNSS, 2023 First Schedule</b>; compounding from <b>BNSS s.359</b>. Shown per sub-section where the Schedule distinguishes them.</p>
      <p><b>Not a substitute for the Gazette.</b> This is a finding aid for practitioners, not an authority. Section numbers, punishments and classification should be confirmed against <b>indiacode.nic.in</b>, and you must check for amendments and commencement notifications after 1 July 2024 (e.g. BNS 106(2)). No case law is included.</p>
    </div>
  </details>
  <div class="count" id="count"></div>'''
assert old_main in html
html = html.replace(old_main, new_main, 1)

# 7. CSS
css = r"""
/* ---------- classification ---------- */
.cls-wrap{margin:.55rem 0 .2rem}
.cls-h{font-size:.72rem;text-transform:uppercase;letter-spacing:.05em;color:var(--ink-soft);font-weight:700;margin-bottom:.25rem}
.cls-tbl{width:100%;border-collapse:collapse;font-size:.78rem}
.cls-tbl th,.cls-tbl td{border:1px solid var(--line);padding:.2rem .4rem;text-align:left;vertical-align:top}
.cls-tbl th{background:var(--chip);color:var(--chip-ink);font-weight:700}
.cls-wrap .comp{margin-top:.3rem;font-size:.78rem;color:var(--ink-soft)}
.chip-cls{font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.03em;
  padding:.12rem .4rem;border-radius:.35rem;margin-left:.3rem;white-space:nowrap}
.chip-cls.cg{background:var(--gone-bg);color:var(--gone)}
.chip-cls.ncg{background:var(--ok-bg);color:var(--ok)}
.chip-cls.nb{background:var(--gone-bg);color:var(--gone)}
.chip-cls.bl{background:var(--ok-bg);color:var(--ok)}
.chip-cls.varies{background:var(--chip);color:var(--chip-ink);text-transform:none;letter-spacing:0}
.detail .dcite b{color:var(--ink)}
/* ---------- sources ---------- */
details.sources{border:1px solid var(--line);border-radius:.6rem;background:var(--panel);margin:.3rem 0 .2rem;font-size:.84rem}
details.sources>summary{cursor:pointer;padding:.6rem .8rem;font-weight:700;color:var(--accent)}
details.sources .sources-body{padding:0 .9rem .7rem;color:var(--ink-soft);line-height:1.55}
details.sources .sources-body p{margin:.5rem 0}
details.sources .sources-body b{color:var(--ink)}
@media(max-width:560px){.chip-cls{display:none}}
</style>"""
html = html.replace('</style>', css, 1)

open(SRC, 'w', encoding='utf-8', newline='\n').write(html)
print('written', len(html), 'bytes; meta sections', len(meta))
