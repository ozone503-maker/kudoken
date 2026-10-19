"""Kudoken fireball v2: an original vector energy ball with an Unbounded K.
Writes the standalone SVGs in brand/fireball/ and the inline pieces the site build uses (src/fb-*.html)."""
import os,sys
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.abspath(D+'/../..')
sys.path.insert(0,D+'/../concepts')
from textpath import font
from fontTools.pens.recordingPen import RecordingPen
CY,CX=60,172          # coin centre in a 240 x 120 box
CYAN,AZURE,COBALT,KINK,KLEG='#8ff6ff','#2fc2ff','#3d7bff','#0b3aa8','#1f9bff'

# --- K from Unbounded 800, the same letterform as the wordmark ---
f=font(R+'/fonts/unb-latin.woff2',800); gs=f.getGlyphSet(); rp=RecordingPen(); gs[f.getBestCmap()[ord('K')]].draw(rp)
polys=[];cur=[]
for op,pts in rp.value:
    if op in('moveTo','lineTo'): cur.append(pts[0])
    elif op=='closePath': polys.append(cur);cur=[]
def kpaths(h,cx,cy):
    s=h/750; w=(889.6-64.8)*s
    out=[]
    for p in polys:
        out.append('M'+' L'.join(f'{cx-w/2+(x-64.8)*s:.2f} {cy+h/2-y*s:.2f}' for x,y in p)+'Z')
    return out  # [stem+arm, lower leg]

# --- tail: tongues streaming left; inner layers are scaled copies toward the coin ---
TIPS=[(56,24),(16,40),(0,59),(18,79),(58,95)]
VALS=[(98,38),(76,51),(78,67),(100,82)]
def tail(kx,ky,dx=0):
    T=lambda x,y:(CX-(CX-x)*kx+dx, CY+(y-CY)*ky)
    P=lambda p:f'{p[0]:.1f} {p[1]:.1f}'
    top0=T(180,14); bot0=T(180,106)
    d=f'M{P(top0)} C{P(T(140,6))} {P(T(96,10))} {P(T(*TIPS[0]))}'
    for i,v in enumerate(VALS):
        t0=TIPS[i]; t1=TIPS[i+1]
        d+=f' Q{P(T(t0[0]+(v[0]-t0[0])*.55,v[1]-(v[1]-t0[1])*.15))} {P(T(*v))}'
        d+=f' Q{P(T(v[0]-(v[0]-t1[0])*.55,v[1]+(t1[1]-v[1])*.15))} {P(T(*t1))}'
    d+=f' C{P(T(96,110))} {P(T(140,114))} {P(bot0)}Z'
    return d
DEFS=f'''<linearGradient id="fbT1" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{COBALT}" stop-opacity="0"/><stop offset=".35" stop-color="{COBALT}" stop-opacity=".85"/><stop offset="1" stop-color="{COBALT}"/></linearGradient>
<linearGradient id="fbT2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{AZURE}" stop-opacity="0"/><stop offset=".4" stop-color="{AZURE}" stop-opacity=".9"/><stop offset="1" stop-color="{AZURE}"/></linearGradient>
<linearGradient id="fbT3" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".45" stop-color="{CYAN}"/><stop offset="1" stop-color="#ffffff"/></linearGradient>
<radialGradient id="fbGlow"><stop offset="0" stop-color="{AZURE}" stop-opacity=".75"/><stop offset=".55" stop-color="{AZURE}" stop-opacity=".28"/><stop offset="1" stop-color="{AZURE}" stop-opacity="0"/></radialGradient>
<radialGradient id="fbRing" cx=".42" cy=".4" r=".62"><stop offset="0" stop-color="{CYAN}"/><stop offset=".7" stop-color="{AZURE}"/><stop offset="1" stop-color="{COBALT}"/></radialGradient>
<radialGradient id="fbCore" cx=".45" cy=".42" r=".6"><stop offset="0" stop-color="#ffffff"/><stop offset=".62" stop-color="#f1feff"/><stop offset="1" stop-color="#b9f6ff"/></radialGradient>'''
K1,K2=kpaths(40,CX+1,CY)
def body(anim=True):
    sp=''.join(f'<rect class="sp sp{i}" x="{x}" y="{y}" width="{w}" height="2.6" rx="1.3" fill="#ffffff"/>' for i,(x,y,w) in enumerate([(70,44,34),(52,58,46),(74,72,30),(96,52,22)]))
    return (f'<circle class="glow" cx="{CX}" cy="{CY}" r="62" fill="url(#fbGlow)"/>'
            f'<g class="tail"><path class="t1" d="{tail(1,1)}" fill="url(#fbT1)"/>'
            f'<path class="t2" d="{tail(.74,.78,4)}" fill="url(#fbT2)"/>'
            f'<path class="t3" d="{tail(.5,.56,6)}" fill="url(#fbT3)"/>'+(f'<g class="sps">{sp}</g>' if anim else '')+'</g>'
            f'<g class="coin"><circle cx="{CX}" cy="{CY}" r="46" fill="url(#fbRing)"/>'
            f'<circle cx="{CX}" cy="{CY}" r="38.5" fill="url(#fbCore)"/>'
            f'<path d="M{CX-30} {CY-22} A37 37 0 0 1 {CX+14} {CY-35}" fill="none" stroke="#ffffff" stroke-width="2.4" stroke-linecap="round" opacity=".8"/>'
            f'<path fill="{KINK}" d="{K1}"/><path fill="{KLEG}" d="{K2}"/></g>'
            f'<circle class="burst" cx="{CX}" cy="{CY}" r="46" fill="none" stroke="{CYAN}" stroke-width="5"/>')
VB='0 0 240 120'
CSS=open(R+'/src/fireball.css').read() if os.path.exists(R+'/src/fireball.css') else ''
def standalone(anim):
    st=f'<style>{CSS}</style>' if anim else '<style>.burst{opacity:0}</style>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB}" width="480" height="240" class="fb"><title>Kudoken fireball</title>{st}<defs>{DEFS}</defs>{body(anim)}</svg>')
open(D+'/kudoken-fireball.svg','w').write(standalone(False))
open(D+'/kudoken-fireball-animated.svg','w').write(standalone(True))
# coin-only favicon, simplified flat colours so it holds at 16px
c=50; kf=kpaths(50,c+1.5,c)
coin=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><title>Kudoken</title>'
      f'<circle cx="50" cy="50" r="49" fill="{COBALT}"/><circle cx="50" cy="50" r="42" fill="{AZURE}"/><circle cx="50" cy="50" r="36" fill="#ffffff"/>'
      f'<path fill="{KINK}" d="{kf[0]}"/><path fill="{KINK}" d="{kf[1]}"/></svg>')
open(D+'/kudoken-coin.svg','w').write(coin)
# wordmark lockups (Unbounded 800, outlined)
from textpath import text_path
wd,tw=text_path('KUDOKEN',R+'/fonts/unb-latin.woff2',64,wght=800)
for bg,col in (('dark','#fbf7ef'),('light','#0a4fb8')):
    W=int(24+240*1.1+18+tw+24)
    open(D+f'/kudoken-lockup-on-{bg}.svg','w').write(
      f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 150" width="{W}" height="150"><title>Kudoken</title><defs>{DEFS}</defs><style>.burst{{opacity:0}}</style>'
      f'<g transform="translate(16 9) scale(1.1)">{body(False)}</g><g transform="translate({24+240*1.1+10:.1f} 98)"><path fill="{col}" d="{wd}"/></g></svg>')
# inline pieces for the site
open(R+'/src/fb-defs.html','w').write(f'<svg class="fb-defs" width="0" height="0" aria-hidden="true" focusable="false"><defs>{DEFS}</defs></svg>')
open(R+'/src/fb-inline.html','w').write(f'<svg class="fb" viewBox="{VB}" aria-hidden="true" focusable="false">{body(True)}</svg>')
print('ok',len(body(True)))
