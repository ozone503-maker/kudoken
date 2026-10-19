import sys
from playwright.sync_api import sync_playwright
B='/workspace/kudoken/brand/fireball/'
fb=open(B+'kudoken-fireball.svg').read(); coin=open(B+'kudoken-coin.svg').read()
ld=open(B+'kudoken-lockup-on-dark.svg').read(); ll=open(B+'kudoken-lockup-on-light.svg').read()
def sz(svg,w): return svg.replace('<svg ',f'<svg style="width:{w}px;height:auto;display:block" ',1)
def favs(): return ''.join(f'<figure>{sz(coin,s)}<figcaption>{s}</figcaption></figure>' for s in (64,32,16))+''.join(f'<figure>{sz(fb,s)}<figcaption>{s} full</figcaption></figure>' for s in (64,32))
html=f'''<html><head><meta charset="utf-8"><style>body{{margin:0;width:1500px;font:600 14px system-ui}}
h1{{margin:0;padding:20px 40px;background:#10293a;color:#fbf7ef;font:700 24px system-ui}}
section{{padding:44px 40px;display:grid;grid-template-columns:auto 1fr;gap:40px 60px;align-items:center}}
.d{{background:radial-gradient(circle at 30% 20%,#1d4a66,#0b2131 70%);color:#c9d6de}} .l{{background:#f1e8d8;color:#386b86}}
.favs{{display:flex;gap:22px;align-items:flex-end}} figure{{margin:0;text-align:center}} figcaption{{margin-top:8px}}
.lock svg{{height:120px;width:auto}}
</style></head><body><h1>Kudoken fireball v2 (vector, Unbounded K)</h1>
<section class="d">{sz(fb,640)}<div><div class="lock">{ld}</div><div class="favs" style="margin-top:30px">{favs()}</div></div></section>
<section class="l">{sz(fb,640)}<div><div class="lock">{ll}</div><div class="favs" style="margin-top:30px">{favs()}</div></div></section></body></html>'''
open('/tmp/fbs.html','w').write(html)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':1500,'height':600}); pg.goto('file:///tmp/fbs.html'); pg.wait_for_timeout(300)
    pg.screenshot(path=sys.argv[1],full_page=True); b.close()
