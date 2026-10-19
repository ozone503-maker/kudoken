import re
BUY='https://app.uniswap.org/swap?chain=mainnet&outputCurrency=0x09851dD4760a8ed111f850affb38B10f84e80C8A'
head=open('/tmp/head.css').read() if False else open('src/fonts.css').read()
css=open('src/style.css').read()+'\n'+open('src/themes.css').read()+'\n'+open('src/fireball.css').read()
body=open('src/body.html').read()
def pic(m):
    name,alt,w,h=m.group(1).split('|')
    return (f'<picture class="bg"><source media="(max-width: 699px)" type="image/webp" srcset="images/v2/{name}-m.webp">'
            f'<source media="(max-width: 699px)" srcset="images/v2/{name}-m.jpg"><source type="image/webp" srcset="images/v2/{name}.webp">'
            f'<img src="images/v2/{name}.jpg" width="{w}" height="{h}" loading="lazy" decoding="async" alt="{alt}"></picture>')
def pc(m):
    n,alt=m.group(1).split('|')
    return f'<figure><picture><source type="image/webp" srcset="images/v2/pc-{n}.webp"><img src="images/v2/pc-{n}.jpg" width="480" height="600" loading="lazy" decoding="async" alt="{alt}"></picture></figure>'
X='<svg viewBox="0 0 26 26" aria-hidden="true"><circle cx="13" cy="13" r="12" style="fill:var(--accent-fill)"/><path d="M8.5 8.5l9 9m0-9-9 9" style="stroke:var(--on-accent)" stroke-width="2.6" stroke-linecap="round"/></svg>'
OK='<svg viewBox="0 0 26 26" aria-hidden="true"><circle cx="13" cy="13" r="12" fill="#55703f"/><path d="M7.5 13.5l3.6 3.6 7.4-7.6" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
dots='<i class="cold"></i><i class="pool"></i>'+'<i></i>'*188
NEW='''<svg class="mark-new" viewBox="0 0 100 100" aria-hidden="true"><defs><linearGradient id="nmg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" style="stop-color:var(--a1,#ff8a63)"/><stop offset=".5" style="stop-color:var(--a2,#b8381f)"/><stop offset="1" style="stop-color:var(--a3,#b8381f)"/></linearGradient></defs><circle cx="50" cy="50" r="48" fill="url(#nmg)"/><path fill="#0b2131" d="M30.7 24.7L44 24.7L44 46L61.3 24.7L77.3 24.7L56 50L77.3 75.3L61.3 75.3L44 54L44 75.3L30.7 75.3Z"/></svg>'''
body=re.sub(r'\{\{pic ([^}]+)\}\}',pic,body)
body=re.sub(r'\{\{pc ([^}]+)\}\}',pc,body)
body=body.replace('{{x}}',X).replace('{{ok}}',OK).replace('{{dots}}',dots).replace('{{BUY}}',BUY).replace('{{newmark}}',NEW).replace('{{fbdefs}}',open('src/fb-defs.html').read()).replace('{{fb}}',open('src/fb-inline.html').read().replace('class="fb"','class="fb mark-fb"',1))
assert '{{' not in body, re.findall(r'\{\{[^}]*',body)[:3]
js=open('src/main.js').read()
headjs='''<script>/* theme preview switch for the themes branch: ?theme=lime|purple&font=unbounded|chakra&mark=new */(function(){var q=new URLSearchParams(location.search),h=document.documentElement;['theme','font','mark'].forEach(function(k){var v=q.get(k);if(v&&/^[a-z]+$/.test(v))h.dataset[k]=v});if(h.dataset.mark==='fireball'){document.write('<link rel="icon" type="image/svg+xml" href="images/v3/fb-coin.svg"><link rel="icon" type="image/png" sizes="32x32" href="images/v3/fb-32.png"><link rel="icon" type="image/png" sizes="16x16" href="images/v3/fb-16.png"><link rel="apple-touch-icon" href="images/v3/fb-180.png">')}})()</script>'''
html=f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kudoken (KDU) | Energy is currency</title>
<meta name="description" content="Kudoken (KDU) is a fixed-supply ERC-20 token on Ethereum, launched in 2021 by Jessie Sponberg and Gabriel Rogers. The unofficial token of galactivism. #EnergyIsCurrency">
<meta property="og:title" content="Kudoken (KDU) | Energy is currency">
<meta property="og:description" content="The unofficial token of galactivism. 1,000,000,000 fixed supply on Ethereum. No mint, no burn, no tax, no admin.">
<meta property="og:type" content="website">
<meta property="og:image" content="https://kudoken.vercel.app/images/v3/og-blue.jpg">
<meta name="theme-color" content="#10293a">
<link rel="icon" type="image/png" href="favicon.png">
<link rel="preload" href="fonts/bss-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/hk-latin.woff2" as="font" type="font/woff2" crossorigin>
{headjs}
<style>
/* Fonts are self-hosted (SIL Open Font License). This page sets no cookies and loads no analytics or trackers. */
{head}
{css}</style>
</head>
<body>
{body}
<script>
{js}</script>
</body>
</html>
'''
open('index.html','w').write(html)
print(len(html))
