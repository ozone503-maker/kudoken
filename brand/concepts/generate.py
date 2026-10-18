import sys,os
sys.path.insert(0,os.path.dirname(__file__));from textpath import text_path
F='/workspace/kudoken/fonts/'
OUT='/workspace/kudoken/brand/concepts/'
PAL={
 'lime':{'bright':['#f2ff6b','#b6ff2e','#3dffa8'],'deep':['#5aa800','#2f8a1c','#0f7a5a']},
 'purple':{'bright':['#f6dcff','#c49bff','#8f6bff'],'deep':['#9a5cf5','#6c3be6','#4628c9']},
}
INK='#0b2131'; SHELL='#fbf7ef'
def grad(id,stops):
    n=len(stops)-1
    return f'<linearGradient id="{id}" x1="0" y1="0" x2="1" y2="1">'+''.join(f'<stop offset="{i/n:.2f}" stop-color="{c}"/>' for i,c in enumerate(stops))+'</linearGradient>'
# marks in 100x100 box; g = gradient url, cut = color of knockout
def mark1(g,cut,favicon=False):  # comet coin
    trails='' if favicon else (f'<g stroke="url(#{g}t)" stroke-linecap="round" fill="none">'
        '<path d="M6 36H22" stroke-width="5"/><path d="M0 50H22" stroke-width="7"/><path d="M10 64H22" stroke-width="5"/></g>')
    cx=62 if not favicon else 50; r=36 if not favicon else 48
    s=r/36
    def P(x,y): return f'{cx+(x-62)*s:.1f} {50+(y-50)*s:.1f}'
    k=(f'<path fill="{cut}" d="M{P(48,30)}H{P(58,30)[:4]} ' if False else '')
    k=(f'<path fill="{cut}" d="M{P(47,31)} L{P(57,31)} L{P(57,47)} L{P(70,31)} L{P(82,31)} L{P(66,50)} L{P(82,69)} L{P(70,69)} L{P(57,53)} L{P(57,69)} L{P(47,69)} Z"/>')
    return trails+f'<circle cx="{cx}" cy="50" r="{r}" fill="url(#{g})"/>'+k
def mark2(g,cut,favicon=False):  # bolt K tile
    return (f'<rect x="6" y="6" width="88" height="88" rx="24" fill="url(#{g})"/>'
            f'<path fill="{cut}" d="M27 22H40V78H27Z"/>'
            f'<path fill="{cut}" d="M64 20H81L57 46H64L82 80H65L50 57H40V47Z"/>')
def mark3(g,cut,favicon=False):  # orbit K
    sw=8 if not favicon else 11
    return (f'<circle cx="50" cy="50" r="40" fill="none" stroke="url(#{g})" stroke-width="{sw-2}" stroke-dasharray="210 41.3" transform="rotate(-62 50 50)" stroke-linecap="round"/>'
            f'<circle cx="80" cy="22" r="{8 if not favicon else 10}" fill="url(#{g})"/>'
            f'<path d="M38 30V70M62 30 40 51 62 70" fill="none" stroke="url(#{g})" stroke-width="{sw+3}" stroke-linecap="round" stroke-linejoin="round"/>')
MARKS={1:mark1,2:mark2,3:mark3}
WORD={1:('KUDOKEN',F+'unb-latin.woff2',700,0),2:('KUDOKEN',F+'cp7-latin.woff2',None,6),3:('kudoken',F+'unb-latin.woff2',500,0)}
NAMES={1:'Comet coin',2:'Bolt K',3:'Orbit K'}
def cut_for(n,bg):
    if n==3: return None
    return INK if bg=='dark' else SHELL
def lockup(n,pal,bg):
    tone='bright' if bg=='dark' else 'deep'
    g=f'g{n}{pal}{bg}'
    mk=MARKS[n](g,cut_for(n,bg))
    txt,fp,w,tr=WORD[n]
    d,tw=text_path(txt,fp,64,x=0,y=0,wght=w,track=tr)
    W=int(130+tw+20)
    word_col=SHELL if bg=='dark' else INK
    bgc='#0b2131' if bg=='dark' else '#f1e8d8'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 120" width="{W}" height="120"><title>Kudoken concept {n}, {NAMES[n]}</title>'
            f'<defs>{grad(g,PAL[pal][tone])}<linearGradient id="{g}t" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="24" y2="0"><stop offset="0" stop-color="{PAL[pal][tone][1]}" stop-opacity="0"/><stop offset="1" stop-color="{PAL[pal][tone][1]}"/></linearGradient></defs><g transform="translate(10 10)">{mk}</g>'
            f'<g transform="translate(128 84)"><path fill="{word_col}" d="{d}"/></g></svg>')
def favicon(n,pal,tone='bright',bg='dark'):
    g=f'f{n}{pal}{tone}'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs>{grad(g,PAL[pal][tone])}</defs>{MARKS[n](g,cut_for(n,bg),favicon=True)}</svg>')
files={}
for n in MARKS:
    for pal in PAL:
        for bg in ('dark','light'):
            files[f'concept-{n}-{pal}-on-{bg}.svg']=lockup(n,pal,bg)
        files[f'concept-{n}-mark-{pal}.svg']=favicon(n,pal)
        files[f'concept-{n}-mark-{pal}-deep.svg']=favicon(n,pal,'deep','light')
os.makedirs(OUT,exist_ok=True)
for k,v in files.items(): open(OUT+k,'w').write(v)
# sheet html per concept
for n in MARKS:
    rows=''
    for bg in ('dark','light'):
        cells=''
        for pal in PAL:
            fv=favicon(n,pal,'bright' if bg=='dark' else 'deep',bg)
            cells+=(f'<div class="cell"><div class="lock">{lockup(n,pal,bg)}</div><div class="fav">'
                    +''.join(f'<span style="width:{s}px;height:{s}px">{fv}</span>' for s in (64,32,16))+f'<em>{pal}, favicon 64 / 32 / 16</em></div></div>')
        rows+=f'<section class="{bg}">{cells}</section>'
    html=f'''<!doctype html><html><head><style>
body{{margin:0;font:600 15px system-ui;width:1600px}}
h1{{margin:0;padding:22px 40px;background:#10293a;color:#fbf7ef;font:700 26px system-ui}}
section{{display:grid;grid-template-columns:1fr 1fr;gap:40px;padding:50px 40px}}
section.dark{{background:radial-gradient(circle at 30% 20%,#1d4a66,#0b2131 70%);color:#c9d6de}}
section.light{{background:#f1e8d8;color:#386b86}}
.lock svg{{height:120px;width:auto;max-width:100%}} .lock svg>rect:first-child{{}}
.fav{{display:flex;align-items:flex-end;gap:18px;margin-top:22px}} .fav span{{display:block}} .fav svg{{width:100%;height:100%;display:block}}
em{{font-style:normal;margin-left:10px}}
</style></head><body><h1>Concept {n}: {NAMES[n]}</h1>{rows}</body></html>'''
    open(f'/tmp/logo-sheet-{n}.html','w').write(html)
print(len(files))
