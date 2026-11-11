import os, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')

SCH_PATH = os.path.join('scratch_rev5', 'AIOT_BLACKBOX_PRESENTATION.kicad_sch')
OUT_PDF = os.path.join('scratch_rev5', 'AIOT_BLACKBOX_PRESENTATION_test_rev5.pdf')
OUT_SVG = os.path.join('scratch_rev5', 'AIOT_BLACKBOX_PRESENTATION_test_rev5.svg')

# Export PDF
print("Exporting PDF...")
cmd_pdf = ['D:\\Kicad\\bin\\kicad-cli.exe', 'sch', 'export', 'pdf', '-o', OUT_PDF, SCH_PATH]
res = subprocess.run(cmd_pdf, capture_output=True, text=True)
print("PDF returncode:", res.returncode)

# Export SVG
print("Exporting SVG...")
cmd_svg = ['D:\\Kicad\\bin\\kicad-cli.exe', 'sch', 'export', 'svg', '-o', OUT_SVG, SCH_PATH]
res = subprocess.run(cmd_svg, capture_output=True, text=True)
print("SVG returncode:", res.returncode)

# Check if poppler or fitz or pdf2image is available, or convert with pymupdf/pdftoppm
try:
    import fitz # PyMuPDF
    doc = fitz.open(OUT_PDF)
    page = doc[0]
    # Render at 300 DPI (zoom = 300/72 = 4.16666)
    zoom = 300 / 72
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    full_png = os.path.join('scratch_rev5', 'full_page.png')
    pix.save(full_png)
    print("Saved full page PNG:", full_png)
    
    # Let's crop the UI region:
    # A4 is 297mm x 210mm.
    # UI region is x: 170mm to 285mm, y: 100mm to 170mm
    # Normalized: x in [170/297, 285/297], y in [100/210, 170/210]
    rect = fitz.Rect(165 * 72 / 25.4, 95 * 72 / 25.4, 285 * 72 / 25.4, 175 * 72 / 25.4)
    pix_crop = page.get_pixmap(matrix=mat, clip=rect)
    crop_png = os.path.join('scratch_rev5', 'ui_region_crop.png')
    pix_crop.save(crop_png)
    print("Saved UI crop PNG:", crop_png)
except Exception as e:
    print("PyMuPDF rendering error:", e)
