from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.varLib import instancer
_c={}
def font(path,wght=None):
    k=(path,wght)
    if k not in _c:
        f=TTFont(path)
        if wght and 'fvar' in f: f=instancer.instantiateVariableFont(f,{'wght':wght})
        _c[k]=f
    return _c[k]
def text_path(txt,path,size,x=0,y=0,wght=None,track=0):
    f=font(path,wght); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm; s=size/upm
    pen=SVGPathPen(gs); cx=0
    for ch in txt:
        g=cmap[ord(ch)]
        tp=TransformPen(pen,(s,0,0,-s,x+cx,y)); gs[g].draw(tp)
        cx+=gs[g].width*s+track
    return pen.getCommands(), cx-track
