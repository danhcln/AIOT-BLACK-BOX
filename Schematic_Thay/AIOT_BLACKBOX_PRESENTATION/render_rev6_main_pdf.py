import os, sys
sys.stdout.reconfigure(encoding='utf-8')

import fitz # PyMuPDF
doc = fitz.open('AIOT_BLACKBOX_PRESENTATION_A4_REV6.pdf')
page = doc[0]

zoom = 300 / 72
mat = fitz.Matrix(zoom, zoom)
pix = page.get_pixmap(matrix=mat)
out_png = 'AIOT_BLACKBOX_PRESENTATION_A4_REV6.png'
pix.save(out_png)
print(f"Saved {out_png} ({os.path.getsize(out_png)} bytes)")
