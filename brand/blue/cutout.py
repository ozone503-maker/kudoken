# Clean transparent cutout of the original 2021 Kudoken fireball mark (album item 65), upscaled 4x.
# Background is flood-filled from the borders (so the pale inside of the fireball stays),
# the edge is smoothed, and edge colours are pulled from just inside to remove the white fringe.
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as nd
src=Image.open('/workspace/gphotos/no/65.jpg').convert('RGB').crop((212,222,552,458))
S=4
big=src.resize((src.width*S,src.height*S),Image.LANCZOS).filter(ImageFilter.MedianFilter(5))
big=big.filter(ImageFilter.UnsharpMask(radius=4,percent=70,threshold=3))
a=np.asarray(big).astype(float)
d=255-a.min(axis=2)
lab,n=nd.label(d<70)
border=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
sil=~np.isin(lab,list(border))
sil=nd.binary_fill_holes(nd.binary_opening(sil,iterations=3))
sm=nd.gaussian_filter(sil.astype(float),2.0)
alpha=np.clip((sm-0.55)/0.25,0,1)          # pulls the edge in about 1px and keeps it soft
inner=sm>0.97
dist,(iy,ix)=nd.distance_transform_edt(~nd.binary_erosion(inner,iterations=6),return_indices=True)
rgb=a[iy,ix]                               # every edge pixel takes the colour from 6px inside
core=nd.binary_erosion(inner,iterations=6)
rgb[core]=a[core]
out=np.dstack([np.clip(rgb,0,255),alpha*255]).astype(np.uint8)
im=Image.fromarray(out,'RGBA'); im=im.crop(im.getbbox())
im.save('/workspace/kudoken/brand/blue/fireball-mark-4x.png',optimize=True)
print(im.size)
from PIL import ImageEnhance
rgb_,al=im.convert('RGB'),im.getchannel('A')
im=ImageEnhance.Color(rgb_).enhance(1.12).convert('RGBA'); im.putalpha(al)
im.save('/workspace/kudoken/brand/blue/fireball-mark-4x.png',optimize=True)
