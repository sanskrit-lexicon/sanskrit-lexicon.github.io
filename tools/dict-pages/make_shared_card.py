import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding="utf-8")
W, H = 1200, 630
BG_TOP=(28,42,58); BG_BOTTOM=(45,78,110); INK=(245,249,252); MUTED=(186,205,222); ACCENT=(120,182,224)
F=Path("C:/Windows/Fonts")
tf=ImageFont.truetype(str(F/"georgiab.ttf"),80); sf=ImageFont.truetype(str(F/"georgia.ttf"),38)
ff=ImageFont.truetype(str(F/"arial.ttf"),27); uf=ImageFont.truetype(str(F/"arial.ttf"),26)
img=Image.new("RGB",(W,H),BG_TOP); d=ImageDraw.Draw(img)
for y in range(H):
    t=y/(H-1); d.line([(0,y),(W,y)],fill=(int(BG_TOP[0]+(BG_BOTTOM[0]-BG_TOP[0])*t),int(BG_TOP[1]+(BG_BOTTOM[1]-BG_TOP[1])*t),int(BG_TOP[2]+(BG_BOTTOM[2]-BG_TOP[2])*t)))
d.rectangle([80,150,84,470],fill=ACCENT)
x=130
d.text((x,150),"Cologne Digital",font=tf,fill=INK)
d.text((x,240),"Sanskrit Lexicon",font=tf,fill=INK)
d.text((x,360),"The open, canonical corpus of Sanskrit",font=sf,fill=MUTED)
d.text((x,408),"dictionaries — digitised, corrected, citable",font=sf,fill=MUTED)
d.text((x,485),"49 dictionaries  ·  open data  ·  freely reusable",font=ff,fill=ACCENT)
d.text((x,H-70),"sanskrit-lexicon.uni-koeln.de  ·  github.com/sanskrit-lexicon",font=uf,fill=MUTED)
out=Path(sys.argv[1]); img.save(out,"PNG",optimize=True); print(f"wrote {out} ({out.stat().st_size} bytes)")
