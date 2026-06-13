# -*- coding: utf-8 -*-
"""ฝังฟอนต์ TH Sarabun IT9 (Regular + Bold) เป็น base64 ลงใน index.html
   และเพิ่มกฎให้ใบรายงานที่พิมพ์/บันทึก PDF ใช้ฟอนต์นี้ (@media print)"""
import base64, os, sys, io

HTML = "index.html"
FONT_DIR = "fonts"

# จับคู่ไฟล์ฟอนต์ตามชื่อ (ชื่อไฟล์มีเลขไทย ๙)
def find_font(*needles_excludes):
    needle, excludes = needles_excludes[0], needles_excludes[1:]
    for f in os.listdir(FONT_DIR):
        low = f.lower()
        if not low.endswith(".ttf"):
            continue
        if needle and needle not in low:
            continue
        if any(x in low for x in excludes):
            continue
        return os.path.join(FONT_DIR, f)
    return None

# Regular = ไฟล์ที่ไม่มี bold/italic ในชื่อ
regular = None
bold = None
for f in os.listdir(FONT_DIR):
    low = f.lower()
    if not low.endswith(".ttf"):
        continue
    has_bold = "bold" in low
    has_italic = "italic" in low
    if not has_bold and not has_italic:
        regular = os.path.join(FONT_DIR, f)
    elif has_bold and not has_italic:
        bold = os.path.join(FONT_DIR, f)

assert regular, "ไม่พบไฟล์ฟอนต์ Regular"
assert bold, "ไม่พบไฟล์ฟอนต์ Bold"
print("Regular:", os.path.basename(regular))
print("Bold   :", os.path.basename(bold))

def b64(path):
    with open(path, "rb") as fh:
        return base64.b64encode(fh.read()).decode("ascii")

reg64 = b64(regular)
bold64 = b64(bold)

font_css = (
"/* ===== ฟอนต์ TH Sarabun IT9 (ฝังในไฟล์ ใช้สำหรับใบรายงานที่พิมพ์/บันทึก PDF) ===== */\n"
"@font-face{font-family:'TH Sarabun IT9';font-style:normal;font-weight:400;font-display:swap;"
"src:local('TH Sarabun IT๙'),local('TH SarabunIT9'),"
"url(data:font/truetype;charset=utf-8;base64," + reg64 + ") format('truetype');}\n"
"@font-face{font-family:'TH Sarabun IT9';font-style:normal;font-weight:700;font-display:swap;"
"src:local('TH Sarabun IT๙ Bold'),local('TH SarabunIT9 Bold'),"
"url(data:font/truetype;charset=utf-8;base64," + bold64 + ") format('truetype');}\n"
)

# กฎตอนพิมพ์: บังคับใบรายงานทั้งใบให้ใช้ TH Sarabun IT9
print_css = (
"@media print{\n"
"  body,.printhead,.printhead *,table,thead,tbody,tr,th,td,td input.pct{"
"font-family:'TH Sarabun IT9','Sarabun',sans-serif!important}\n"
"}\n"
)

with io.open(HTML, "r", encoding="utf-8") as fh:
    html = fh.read()

if "TH Sarabun IT9" in html:
    print("ไฟล์มีการฝังฟอนต์อยู่แล้ว — ข้าม")
    sys.exit(0)

marker = "<style>\n"
idx = html.find(marker)
assert idx != -1, "ไม่พบแท็ก <style>"
insert_at = idx + len(marker)
html = html[:insert_at] + font_css + print_css + html[insert_at:]

with io.open(HTML, "w", encoding="utf-8", newline="") as fh:
    fh.write(html)

print("เสร็จ — index.html ขนาดใหม่:", os.path.getsize(HTML), "bytes")
