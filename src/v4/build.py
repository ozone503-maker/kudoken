"""Kudoken v4: five static pages with a shared nav, footer, CSS and JS. Run from the repo root: python3 src/v4/build.py"""
import re,os
R=os.path.abspath(os.path.dirname(__file__)+'/../..')
os.chdir(R)
BUY='https://app.uniswap.org/swap?chain=mainnet&outputCurrency=0x09851dD4760a8ed111f850affb38B10f84e80C8A'
CONTRACT='0x09851dD4760a8ed111f850affb38B10f84e80C8A'
SITE='https://kudoken.space'
FB=open('src/fb-inline.html').read()
DEFS=open('src/fb-defs.html').read()
ARROW='<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M7 4h9v9M16 4 4 16" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
BIG='<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M8 24h30M26 11l13 13-13 13" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="square"/></svg>'
PAGES=[ # slug, file, nav label, title, description, body class
 ('', 'home','Home','Kudoken (KDU) | Energy is currency','Kudoken (KDU) is a fixed-supply token on Ethereum, started in 2021 by Jessie Sponberg and Gabriel Rogers. The unofficial token of galactivism.','p-home'),
 ('story/','story','Story','The story | Kudoken (KDU)','From a first try in 2017 to a 2021 launch, five years in cold storage, and a return right on schedule in October 2026.','p-story'),
 ('token/','token','Token','The token | Kudoken (KDU)','One billion KDU, fixed. No mint, no burn, no tax, no admin. The contract, how to buy on Uniswap, and the move to Base.','p-token'),
 ('ecosystem/','ecosystem','Ecosystem','The ecosystem | Kudoken (KDU)','FlashTown, Monkey Jockey, Outlet Mall and Brobots: the places Kudoken is meant to be spent.','p-eco'),
 ('wallet/','wallet','Wallet','The wallet | Kudoken (KDU)','Try the Kudoken wallet on the Base Sepolia test network with play money.','p-wallet'),
]
def pic(m,mobile):
    name,alt,w,h=m.group(1).split('|')
    ms=(f'<source media="(max-width: 699px)" type="image/webp" srcset="/images/v4/{name}-m.webp"><source media="(max-width: 699px)" srcset="/images/v4/{name}-m.jpg">' if mobile else '')
    return (f'<picture>{ms}<source type="image/webp" srcset="/images/v4/{name}.webp">'
            f'<img src="/images/v4/{name}.jpg" width="{w}" height="{h}" loading="lazy" decoding="async" alt="{alt}"></picture>')
def nav(cur):
    links=''.join(f'<a href="/{s}"{" aria-current=\"page\"" if f==cur else ""}>{lab}</a>' for s,f,lab,*_ in PAGES[1:])
    pg=''.join(f'<a class="pg" href="/{s}"{" aria-current=\"page\"" if f==cur else ""}>{lab}</a>' for s,f,lab,*_ in PAGES)
    return f'''<header class="nav"><div class="w">
  <a class="brand" href="/" aria-label="Kudoken home">{FB}<span>KUDOKEN</span></a>
  <nav class="links" aria-label="Main">{links}</nav>
  <a class="btn buy" href="{BUY}" target="_blank" rel="noopener">Buy KDU</a>
  <details class="menu"><summary aria-label="Open menu">Menu</summary><nav class="panel" aria-label="Main">{pg}<a class="btn" href="{BUY}" target="_blank" rel="noopener">Buy KDU on Uniswap</a></nav></details>
</div></header>'''
FOOT=f'''<footer><div class="w">
  <div class="top">
    <a class="brand" href="/" aria-label="Kudoken home">{FB}<span>KUDOKEN</span></a>
    <nav aria-label="Footer">
      <a href="/story/">Story</a><a href="{BUY}" target="_blank" rel="noopener">Buy on Uniswap</a>
      <a href="/token/">Token</a><a href="https://etherscan.io/token/{CONTRACT}" target="_blank" rel="noopener">Etherscan</a>
      <a href="/ecosystem/">Ecosystem</a><a href="https://github.com/KudokenToken/Kudoken" target="_blank" rel="noopener">Whitepaper</a>
      <a href="/wallet/">Wallet</a><a href="https://web.archive.org/web/20221203163118/https://kudoken.io/" target="_blank" rel="noopener">The 2021 site</a>
    </nav>
  </div>
  <p class="fine">Kudoken (KDU) is a cryptocurrency token. Nothing on this site is financial advice. Anything marked coming or in development is not live yet and may change. The wallet demo uses test tokens with no value. Contract: {CONTRACT} on Ethereum. #EnergyIsCurrency</p>
</div></footer>'''
for slug,f,lab,title,desc,cls in PAGES:
    body=open(f'src/v4/pages/{f}.html').read()
    body=re.sub(r'\{\{picm ([^}]+)\}\}',lambda m:pic(m,True),body)
    body=re.sub(r'\{\{pic ([^}]+)\}\}',lambda m:pic(m,False),body)
    body=body.replace('{{fb}}',FB).replace('{{BUY}}',BUY).replace('{{CONTRACT}}',CONTRACT).replace('{{arrow}}',ARROW).replace('{{bigarrow}}',BIG)
    assert '{{' not in body,(f,re.findall(r'\{\{[^}]*',body)[:3])
    url=SITE+'/'+slug
    extra='<script src="/js/kudoken-wallet.js" defer></script>\n' if f=='wallet' else ''
    pre='<link rel="preload" href="/images/hero-honu-portrait.webp" as="image" media="(max-width: 899px)">\n' if f=='home' else ''
    html=f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Kudoken">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/images/v4/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}/images/v4/og.jpg">
<meta name="theme-color" content="#111315">
<link rel="icon" type="image/svg+xml" href="/images/v3/fb-coin.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/images/v3/fb-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/images/v3/fb-16.png">
<link rel="apple-touch-icon" href="/images/v3/fb-180.png">
<link rel="preload" href="/fonts/unb-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/hk-latin.woff2" as="font" type="font/woff2" crossorigin>
{pre}<link rel="stylesheet" href="/css/site.css?v=4">
</head>
<body class="{cls}">
{DEFS}
<a class="sr" href="#main">Skip to content</a>
{nav(f)}
<main id="main">
{body}
</main>
{FOOT}
<script src="/js/site.js?v=4" defer></script>
{extra}</body>
</html>
'''
    out=('index.html' if not slug else slug+'index.html')
    os.makedirs(os.path.dirname(out) or '.',exist_ok=True)
    open(out,'w').write(html)
# shared css: fonts with absolute paths + site css
fonts=open('src/fonts.css').read().replace('url(fonts/','url(/fonts/')
fonts='\n'.join(l for l in fonts.split('\n') if 'Big Shoulders' not in l and 'Chakra' not in l)
open('css/site.css','w').write(fonts+'\n'+open('src/v4/site.css').read())
open('js/site.js','w').write(open('src/v4/site.js').read())
print('built',[p[1] for p in PAGES])
