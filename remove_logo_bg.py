# -*- coding: utf-8 -*-
"""ลบพื้นหลังสีขาวของโลโก้ (เฉพาะพื้นหลังด้านนอกที่ต่อจากขอบภาพ)
   โดยไม่แตะสีขาวด้านในตราสัญลักษณ์ (เช่น เสื้อเชิ้ตของตัวการ์ตูน) ด้วยวิธี flood-fill จากมุมภาพ"""
from PIL import Image, ImageDraw

SRC="assets/logo.jpg"
OUT="assets/logo.png"
SENT=(255,0,255)   # สีหมุด (magenta) ไม่มีในโลโก้ ใช้ทำเครื่องหมายพื้นหลัง
THRESH=95          # ระยะความใกล้สีขาวที่ถือว่าเป็นพื้นหลัง (กว้างพอเก็บขอบฟุ้ง)
MAX=768            # ย่อขนาดเพื่อความเร็วและไฟล์เล็ก (พอสำหรับแสดง ~180px)

im=Image.open(SRC).convert("RGB")
w,h=im.size
scale=min(1.0, MAX/max(w,h))
if scale<1.0:
    im=im.resize((round(w*scale),round(h*scale)), Image.LANCZOS)
w,h=im.size

for seed in [(0,0),(w-1,0),(0,h-1),(w-1,h-1)]:
    ImageDraw.floodfill(im, seed, SENT, thresh=THRESH)

im=im.convert("RGBA")
px=im.load()
trans=0
for y in range(h):
    for x in range(w):
        r,g,b,a=px[x,y]
        if r==255 and g==0 and b==255:
            px[x,y]=(0,0,0,0); trans+=1

im.save(OUT)
# วินิจฉัย: มุมควรโปร่งใส, จุดกลางภาพ (ในตรา) ควรทึบ
c=im.load()
print("size",im.size,"transparent%%=%.1f"%(100*trans/(w*h)))
print("corner alpha (ควร 0):", c[0,0][3])
print("center alpha (ควร 255):", c[w//2,h//2][3])
