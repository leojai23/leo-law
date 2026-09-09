# -*- coding: utf-8 -*-
import json, io

SRC = r"g:\Leo-Workspace\Leo-Law\index.html"
secs = json.load(open('bns_sections.json', encoding='utf-8'))
# compact blob, escape < to keep it safe inside a <script> element
blob = json.dumps(secs, ensure_ascii=False, separators=(',', ':')).replace('<', r'\u003c')

html = open(SRC, encoding='utf-8').read()

# ---------------------------------------------------------------- 1. data blob
marker = '<script>\n/* ---------------- theme'
assert marker in html, "theme marker not found"
data_tag = '<script type="application/json" id="bns-data">' + blob + '</script>\n'
html = html.replace(marker, data_tag + marker, 1)

# ---------------------------------------------------------------- 2. CSS
css = r"""
/* ---------- detail / expand ---------- */
.card-toggle{
  margin-left:auto; border:1px solid var(--line); background:var(--panel); color:var(--accent);
  font:inherit; font-size:.72rem; font-weight:700; cursor:pointer; border-radius:.4rem;
  padding:.2rem .5rem; white-space:nowrap;
}
.card-toggle:hover{background:var(--accent-soft)}
.card.exp .card-toggle{background:var(--accent); color:var(--accent-ink); border-color:var(--accent)}
.detail{
  margin-top:.7rem; padding-top:.7rem; border-top:1px solid var(--line);
  font-size:.86rem; line-height:1.55;
}
.bns-sec{margin:0 0 1rem}
.bns-sec h4{
  margin:0 0 .35rem; font-size:.82rem; color:var(--accent);
  font-family:Georgia,"Times New Roman",serif;
}
.bns-sec .txt p{margin:.35rem 0}
.bns-sec .txt p.cl{padding-left:1.1rem}
.bns-sec .txt p.hd{font-style:italic; color:var(--ink-soft); margin-top:.6rem}
.detail .dnote{
  margin:.6rem 0; padding:.55rem .7rem; background:var(--warn-bg);
  border-left:3px solid var(--warn); border-radius:.4rem; color:var(--ink-soft); font-size:.83rem;
}
.detail .dnote b{color:var(--warn)}
.detail .dmeta{margin:.5rem 0; color:var(--ink-soft); font-size:.8rem}
.detail .pend{font-style:italic; opacity:.8}
.detail .rel{margin:.5rem 0; font-size:.8rem; line-height:1.9}
.detail .rel a{
  display:inline-block; border:1px solid var(--line); border-radius:99px;
  padding:.1rem .55rem; margin:.1rem .25rem .1rem 0; color:var(--ink);
}
.detail .rel a:hover{background:var(--chip); text-decoration:none}
.detail .dcite{margin:.7rem 0 0; font-size:.74rem; color:var(--ink-soft)}
.card:target{outline:2px solid var(--accent); outline-offset:2px}
</style>"""
html = html.replace('</style>', css, 1)

# ---------------------------------------------------------------- 3. cardHTML
old_card = '''function cardHTML(d){
  var ipc = d.ipc && d.ipc!=="\u2014" ? '<span class="sec-tag ipc">IPC '+esc(d.ipc)+'</span>' : '<span class="sec-tag ipc">IPC \u2014</span>';
  var bns = d.bns && d.bns!=="\u2014" ? '<span class="sec-tag bns">BNS '+esc(d.bns)+'</span>' : '<span class="sec-tag bns">BNS \u2014</span>';
  var order = d.s==="gone"
      ? bns+' <span class="arrow">\u25c1</span> '+ipc
      : ipc+' <span class="arrow">\u25b6</span> '+bns;
  var pill='<span class="pill '+STATUS_CLASS[d.s]+'">'+STATUS_LABEL[d.s]+'</span>';
  var catName=(CATS.filter(function(c){return c[0]===d.f})[0]||["","\u2014"])[1];
  return '<div class="card">'
    + '<div class="rail">'+order+pill+'</div>'
    + '<h3>'+hi(d.t)+'</h3>'
    + (d.g?'<p>'+hi(d.g)+'</p>':'')
    + (d.n?'<div class="note">'+d.n+'</div>':'')
    + '<div class="cat-line">'+esc(catName)+'</div>'
    + '</div>';
}'''
assert old_card in html, "cardHTML block not found verbatim"

new_card = '''var BNS_TEXT = JSON.parse(document.getElementById('bns-data').textContent);
DATA.forEach(function(d,i){ d._i=i; });

function bnsNums(d){
  if(!d.bns || d.bns==="\u2014") return [];
  var m=d.bns.match(/\\d+/g)||[]; var seen={}, out=[];
  m.forEach(function(x){ if(!seen[x]){ seen[x]=1; out.push(x); } });
  return out;
}
function ipcNums(d){
  if(!d.ipc || d.ipc==="\u2014") return [];
  var m=d.ipc.match(/\\d+[A-Z]*/g)||[]; return m;
}
function paras(txt){
  return esc(txt).split(/\\n\\n+/).map(function(p){
    var cls="";
    if(/^\\([0-9a-z]+\\)/.test(p)) cls=" class=\\"cl\\"";
    else if(/^(Explanation|Exception|Illustrations?|Provided)/.test(p)) cls=" class=\\"hd\\"";
    return '<p'+cls+'>'+p.replace(/\\n/g,'<br>')+'</p>';
  }).join('');
}
function detailHTML(d){
  var h="";
  bnsNums(d).forEach(function(n){
    var s=BNS_TEXT[n];
    if(!s) return;
    h+='<div class="bns-sec"><h4>BNS '+n+' \u00b7 '+esc(s.heading)+'</h4><div class="txt">'+paras(s.text)+'</div></div>';
  });
  if(!h && d.s==="gone"){
    h+='<div class="bns-sec"><h4>Not re-enacted in the BNS</h4><div class="txt"><p>There is no corresponding Bharatiya Nyaya Sanhita provision. See the note below.</p></div></div>';
  }
  if(d.n) h+='<div class="dnote"><b>What changed:</b> '+d.n+'</div>';
  var ipcs=ipcNums(d);
  if(ipcs.length) h+='<div class="dmeta">Corresponding IPC: '+esc(ipcs.join(', '))+' \u2014 <span class="pend">full IPC section text is planned for a later update</span></div>';
  // related
  var mine={}; bnsNums(d).forEach(function(n){mine[n]=1;});
  var rel=DATA.filter(function(o){
    if(o===d) return false;
    if(o.f===d.f) return true;
    return bnsNums(o).some(function(n){return mine[n];});
  }).slice(0,8);
  if(rel.length){
    h+='<div class="rel"><b>Related:</b> '+rel.map(function(o){
      return '<a href="#c'+o._i+'">'+esc((o.ipc&&o.ipc!=="\u2014"?"IPC "+o.ipc:"BNS "+o.bns))+' \u00b7 '+esc(o.t.split(/[\u2014(]/)[0].trim())+'</a>';
    }).join(' ')+'</div>';
  }
  h+='<p class="dcite">Statutory text reproduced from the Bharatiya Nyaya Sanhita, 2023 (Gazette of India \u2014 public domain). Confirm against indiacode.nic.in before citing.</p>';
  return h;
}

function cardHTML(d){
  var ipc = d.ipc && d.ipc!=="\u2014" ? '<span class="sec-tag ipc">IPC '+esc(d.ipc)+'</span>' : '<span class="sec-tag ipc">IPC \u2014</span>';
  var bns = d.bns && d.bns!=="\u2014" ? '<span class="sec-tag bns">BNS '+esc(d.bns)+'</span>' : '<span class="sec-tag bns">BNS \u2014</span>';
  var order = d.s==="gone"
      ? bns+' <span class="arrow">\u25c1</span> '+ipc
      : ipc+' <span class="arrow">\u25b6</span> '+bns;
  var pill='<span class="pill '+STATUS_CLASS[d.s]+'">'+STATUS_LABEL[d.s]+'</span>';
  var catName=(CATS.filter(function(c){return c[0]===d.f})[0]||["","\u2014"])[1];
  var hasDetail = bnsNums(d).length>0 || d.s==="gone" || !!d.n;
  return '<article class="card" id="c'+d._i+'" data-idx="'+d._i+'">'
    + '<div class="rail">'+order+pill
    + (hasDetail?'<button class="card-toggle" aria-expanded="false">bare act \u25be</button>':'')
    + '</div>'
    + '<h3>'+hi(d.t)+'</h3>'
    + (d.g?'<p>'+hi(d.g)+'</p>':'')
    + '<div class="cat-line">'+esc(catName)+'</div>'
    + '<div class="detail" hidden></div>'
    + '</article>';
}'''
html = html.replace(old_card, new_card, 1)

# ---------------------------------------------------------------- 4. expand wiring
old_sw = "/* ---------------- service worker ---------------- */"
assert old_sw in html
wiring = '''/* ---------------- expand / detail ---------------- */
listEl.addEventListener('click',function(e){
  var btn=e.target.closest('.card-toggle');
  if(!btn) return;
  var card=btn.closest('.card'), det=card.querySelector('.detail');
  var open=card.classList.toggle('exp');
  btn.setAttribute('aria-expanded',open?'true':'false');
  btn.textContent = open ? 'bare act \\u25b4' : 'bare act \\u25be';
  if(open){
    if(!det.dataset.filled){ det.innerHTML=detailHTML(DATA[+card.dataset.idx]); det.dataset.filled="1"; }
    det.hidden=false;
  } else {
    det.hidden=true;
  }
});

''' + old_sw
html = html.replace(old_sw, wiring, 1)

open(SRC, 'w', encoding='utf-8', newline='\n').write(html)
print('written', len(html), 'bytes to', SRC)
print('bns sections embedded:', len(secs))
