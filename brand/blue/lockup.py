# Lockup: original 2021 fireball mark + KUDOKEN wordmark in Unbounded (outlined), electric blue glow.
import base64,io,sys,os
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','concepts'))
from textpath import text_path
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__))
im=Image.open(D+'/fireball-mark-4x.png'); w=640; im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
buf=io.BytesIO(); im.save(buf,'PNG',optimize=True); b64=base64.b64encode(buf.getvalue()).decode()
d,tw=text_path('KUDOKEN','/workspace/kudoken/fonts/unb-latin.woff2',64,wght=800)
mh=110; mw=mh*im.width/im.height
W=int(20+mw+22+tw+20); H=150
for bg,col,glow in (('dark','#fbf7ef','#2fb8ff'),('light','#0a4fb8',None)):
    f=(f'<filter id="gl" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="5" result="b"/><feFlood flood-color="{glow}" flood-opacity=".55"/><feComposite in2="b" operator="in"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>' if glow else '')
    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><title>Kudoken</title><defs>{f}</defs>'
         f'<image x="20" y="{(H-mh)/2:.1f}" width="{mw:.1f}" height="{mh}" href="data:image/png;base64,{b64}"{" filter=\"url(#gl)\"" if glow else ""}/>'
         f'<g transform="translate({20+mw+22:.1f} {H/2+23:.1f})"><path fill="{col}" d="{d}"/></g></svg>')
    open(f'{D}/kudoken-lockup-on-{bg}.svg','w').write(svg)
print(W,H)
