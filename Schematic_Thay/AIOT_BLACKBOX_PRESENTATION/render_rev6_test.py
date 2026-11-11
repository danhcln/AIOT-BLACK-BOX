import os, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')

SCH_PATH = os.path.join('scratch_rev6', 'AIOT_BLACKBOX_PRESENTATION.kicad_sch')
OUT_PDF = os.path.join('scratch_rev6', 'test_rev6.pdf')
OUT_SVG_DIR = os.path.join('scratch_rev6', 'svg_out')
os.makedirs(OUT_SVG_DIR, exist_ok=True)

# Export PDF
print("Exporting PDF...")
res_pdf = subprocess.run([r'D:\KiCad\bin\kicad-cli.exe', 'sch', 'export', 'pdf', '-o', OUT_PDF, SCH_PATH], capture_output=True, text=True)
print("PDF returncode:", res_pdf.returncode)

# Export SVG
print("Exporting SVG...")
res_svg = subprocess.run([r'D:\KiCad\bin\kicad-cli.exe', 'sch', 'export', 'svg', '-o', OUT_SVG_DIR, SCH_PATH], capture_output=True, text=True)
print("SVG returncode:", res_svg.returncode)

# Render high-resolution PNGs with PyMuPDF
import fitz # PyMuPDF
doc = fitz.open(OUT_PDF)
page = doc[0]

# 300 DPI
zoom = 300 / 72
mat = fitz.Matrix(zoom, zoom)

# 1. Full page
pix_full = page.get_pixmap(matrix=mat)
full_png = os.path.join('scratch_rev6', 'full_page_rev6.png')
pix_full.save(full_png)
print("Saved full page PNG:", full_png)

# 2. Crop around ESP32-S3 (U1)
# Center is at x: 152.4, y: 99.06. Rect: x in [110, 195], y in [60, 140] mm
# mm to pt: mm * 72 / 25.4
r_esp = fitz.Rect(110 * 72 / 25.4, 60 * 72 / 25.4, 195 * 72 / 25.4, 140 * 72 / 25.4)
pix_esp = page.get_pixmap(matrix=mat, clip=r_esp)
esp_png = os.path.join('scratch_rev6', 'crop_esp32_rev6.png')
pix_esp.save(esp_png)
print("Saved ESP32 crop PNG:", esp_png)

# 3. Crop around MPU6050 (U2)
# U2 is at x: 53.34, y: 93.98. Rect: x in [25, 85], y in [75, 115] mm
r_mpu = fitz.Rect(25 * 72 / 25.4, 75 * 72 / 25.4, 85 * 72 / 25.4, 115 * 72 / 25.4)
pix_mpu = page.get_pixmap(matrix=mat, clip=r_mpu)
mpu_png = os.path.join('scratch_rev6', 'crop_mpu_rev6.png')
pix_mpu.save(mpu_png)
print("Saved MPU6050 crop PNG:", mpu_png)

# 4. Crop around UI area
r_ui = fitz.Rect(170 * 72 / 25.4, 100 * 72 / 25.4, 285 * 72 / 25.4, 170 * 72 / 25.4)
pix_ui = page.get_pixmap(matrix=mat, clip=r_ui)
ui_png = os.path.join('scratch_rev6', 'crop_ui_rev6.png')
pix_ui.save(ui_png)
print("Saved UI crop PNG:", ui_png)
