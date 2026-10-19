from playwright.sync_api import sync_playwright
import base64
B='/workspace/kudoken/brand/fireball/'; O='/workspace/kudoken/images/v3/'
coin=open(B+'kudoken-coin.svg').read(); fb=open(B+'kudoken-fireball.svg').read(); lock=open(B+'kudoken-lockup-on-dark.svg').read()
fnt=base64.b64encode(open('/workspace/kudoken/fonts/unb-latin.woff2','rb').read()).decode()
hero=base64.b64encode(open('/workspace/kudoken/images/hero-honu-1100.jpg','rb').read()).decode()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for s in (16,32,48,512):
        pg=b.new_page(viewport={'width':s,'height':s}); pg.set_content(f'<body style="margin:0;background:transparent">{coin.replace("<svg ",f"<svg width={s} height={s} ",1)}</body>')
        pg.screenshot(path=O+f'fb-{s}.png',omit_background=True); pg.close()
    pg=b.new_page(viewport={'width':180,'height':180}); pg.set_content(f'<body style="margin:0;background:radial-gradient(circle at 40% 35%,#1d4a66,#0b2131 75%);display:grid;place-items:center;height:180px">{coin.replace("<svg ","<svg width=136 height=136 ",1)}</body>')
    pg.screenshot(path=O+'fb-180.png'); pg.close()
    pg=b.new_page(viewport={'width':1200,'height':630})
    pg.set_content(f'''<html><head><style>@font-face{{font-family:U;src:url(data:font/woff2;base64,{fnt}) format("woff2");font-weight:500 900}}</style></head><body style="margin:0;width:1200px;height:630px;background:url(data:image/jpeg;base64,{hero}) 0% 70%/130% auto;font-family:U">
    <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(8,26,38,.9),rgba(8,26,38,.62) 48%,rgba(8,26,38,0) 75%)"></div>
    <div style="position:absolute;left:70px;top:90px">{lock.replace("<svg ","<svg style='height:120px;width:auto;display:block' ",1)}
    <div style="margin-top:46px;color:#fbf7ef;font:800 74px/1 U;text-transform:uppercase">Energy<br><span style="background:linear-gradient(100deg,#c4fcff,#6fe0ff,#69a2ff);-webkit-background-clip:text;color:transparent">is currency</span></div>
    <div style="margin-top:28px;color:#d6e2e8;font:500 26px system-ui">KDU on Ethereum. 1,000,000,000 fixed supply.</div></div></body></html>''')
    pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(800); pg.screenshot(path='/tmp/og.png'); b.close()
