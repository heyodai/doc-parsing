import pymupdf, numpy as np, io
from PIL import Image, ImageDraw, ImageFont, ImageFilter
src=pymupdf.open('out/irs_form_1040_2025_sample_filled.pdf')
pix=src[0].get_pixmap(dpi=200, colorspace=pymupdf.csGRAY)
img=Image.frombytes('L',(pix.width,pix.height),pix.samples)
W,H=img.size
# handwriting annotations (font-rendered, Bradley Hand)
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf', 54)
font_s=ImageFont.truetype('/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf', 40)
d=ImageDraw.Draw(img)
ink=40
d.text((int(W*0.63),int(H*0.035)),"RECEIVED 4/14/26 - JS",font=font,fill=ink)
d.multiline_text((int(W*0.035),int(H*0.80)),"verify W-2\nw/ borrower",font=font_s,fill=ink,spacing=2)
# circle around line 11a AGI value
x0,y0,x1,y1=int(W*0.80),int(H*0.938),int(W*0.965),int(H*0.970)
d.ellipse((x0,y0,x1,y1),outline=ink,width=4)
d.text((int(W*0.68),int(H*0.942)),"AGI ok",font=font_s,fill=ink)
# paper tone + photocopy effects
arr=np.asarray(img).astype(np.float32)
rng=np.random.default_rng(1040)
arr=arr*0.94+10  # slightly grey paper / lower contrast
noise=rng.normal(0,9,arr.shape); arr=arr+noise
# speckle
mask=rng.random(arr.shape)<0.0015; arr[mask]=rng.uniform(0,90,mask.sum())
# uneven illumination
yy,xx=np.mgrid[0:H,0:W]; shade=1-0.08*((xx/W-0.3)**2+(yy/H-0.4)**2); arr=arr*shade
arr=np.clip(arr,0,255).astype(np.uint8)
img=Image.fromarray(arr).filter(ImageFilter.GaussianBlur(0.7))
img=img.rotate(1.6, resample=Image.BICUBIC, expand=False, fillcolor=235)
# darkened edge like a scanner lid
d=ImageDraw.Draw(img); d.rectangle((0,0,W-1,H-1),outline=60,width=6)
buf=io.BytesIO(); img.save(buf,'JPEG',quality=55,dpi=(200,200)); jpg=buf.getvalue()
out=pymupdf.open(); page=out.new_page(width=612,height=792)
page.insert_image(page.rect, stream=jpg)
out.set_metadata({'title':'Scanned page (image only) - sample 1040 page 1, fictitious data','author':'synthetic'})
out.save('out/scanned_skewed_1040_p1_no_text_layer.pdf', garbage=3, deflate=True)
chk=pymupdf.open('out/scanned_skewed_1040_p1_no_text_layer.pdf')
print('text chars', len(chk[0].get_text().strip()), 'images', len(chk[0].get_images()), 'size', len(jpg))
chk[0].get_pixmap(dpi=90).save('out/check_scan.png')
