from playwright.sync_api import sync_playwright
B='/workspace/kudoken/brand/blue/'; V='/workspace/kudoken/images/v3/'
dark=open(B+'kudoken-lockup-on-dark.svg').read(); light=open(B+'kudoken-lockup-on-light.svg').read()
def favs(): 
    return ''.join(f'<figure><img src="file://{V}{f}" style="width:{s}px;height:{s}px;image-rendering:auto"><figcaption>{s}px{" coin" if "coin" in f else ""}</figcaption></figure>' for f,s in (('fav-512.png',64),('fav-32.png',32),('fav-coin-32.png',32),('fav-coin-16.png',16),('fav-16.png',16)))
html=f'''<html><head><meta charset="utf-8"><style>body{{margin:0;width:1500px;font:600 14px system-ui}}
h1{{margin:0;padding:20px 40px;background:#10293a;color:#fbf7ef;font:700 24px system-ui}}
section{{padding:50px 40px;display:flex;align-items:center;gap:60px}}
.d{{background:radial-gradient(circle at 30% 20%,#1d4a66,#0b2131 70%);color:#c9d6de}} .l{{background:#f1e8d8;color:#386b86}}
.lock svg{{height:150px;width:auto}} .favs{{display:flex;gap:22px;align-items:flex-end}} figure{{margin:0;text-align:center}} figcaption{{margin-top:8px}}
.tab{{display:flex;align-items:center;gap:8px;background:#dfe3e8;border-radius:10px 10px 0 0;padding:8px 14px;color:#222;font:500 13px system-ui;width:220px}}
</style></head><body><h1>Kudoken lockup: original fireball mark + Unbounded wordmark, electric ocean blue</h1>
<section class="d"><div class="lock">{dark}</div><div class="favs">{favs()}</div></section>
<section class="l"><div class="lock">{light}</div><div class="favs">{favs()}<div class="tab"><img src="file://{V}fav-coin-16.png" width="16" height="16">Kudoken (KDU) | Energy is…</div></div></section></body></html>'''
open('/tmp/lockup.html','w').write(html)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--allow-file-access-from-files'])
    pg=b.new_page(viewport={'width':1500,'height':600}); pg.goto('file:///tmp/lockup.html'); pg.wait_for_timeout(500)
    pg.screenshot(path='/workspace/kudoken-shots/logo-lockup-blue.png',full_page=True); b.close()
