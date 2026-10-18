import re
BUY='https://app.uniswap.org/swap?chain=mainnet&outputCurrency=0x09851dD4760a8ed111f850affb38B10f84e80C8A'
head=open('/tmp/head.css').read() if False else open('src/fonts.css').read()
css=open('src/style.css').read()
body=open('src/body.html').read()
def pic(m):
    name,alt,w,h=m.group(1).split('|')
    return (f'<picture class="bg"><source media="(max-width: 699px)" type="image/webp" srcset="images/v2/{name}-m.webp">'
            f'<source media="(max-width: 699px)" srcset="images/v2/{name}-m.jpg"><source type="image/webp" srcset="images/v2/{name}.webp">'
            f'<img src="images/v2/{name}.jpg" width="{w}" height="{h}" loading="lazy" decoding="async" alt="{alt}"></picture>')
def pc(m):
    n,alt=m.group(1).split('|')
    return f'<figure><picture><source type="image/webp" srcset="images/v2/pc-{n}.webp"><img src="images/v2/pc-{n}.jpg" width="480" height="600" loading="lazy" decoding="async" alt="{alt}"></picture></figure>'
X='<svg viewBox="0 0 26 26" aria-hidden="true"><circle cx="13" cy="13" r="12" fill="#b8381f"/><path d="M8.5 8.5l9 9m0-9-9 9" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/></svg>'
OK='<svg viewBox="0 0 26 26" aria-hidden="true"><circle cx="13" cy="13" r="12" fill="#55703f"/><path d="M7.5 13.5l3.6 3.6 7.4-7.6" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
dots='<i class="cold"></i><i class="pool"></i>'+'<i></i>'*188
body=re.sub(r'\{\{pic ([^}]+)\}\}',pic,body)
body=re.sub(r'\{\{pc ([^}]+)\}\}',pc,body)
body=body.replace('{{x}}',X).replace('{{ok}}',OK).replace('{{dots}}',dots).replace('{{BUY}}',BUY)
assert '{{' not in body, re.findall(r'\{\{[^}]*',body)[:3]
js=open('src/main.js').read()
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
<meta property="og:image" content="https://kudoken.vercel.app/images/hero-honu-1100.jpg">
<meta name="theme-color" content="#10293a">
<link rel="icon" type="image/png" href="favicon.png">
<link rel="preload" href="fonts/bss-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/hk-latin.woff2" as="font" type="font/woff2" crossorigin>
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
