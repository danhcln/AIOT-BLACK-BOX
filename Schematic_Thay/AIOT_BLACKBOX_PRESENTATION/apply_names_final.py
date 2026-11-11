import os, sys, shutil, subprocess, json, pymupdf

sys.stdout.reconfigure(encoding='utf-8')
proj_dir = r"D:\ĐỒ ÁN 2\Schematic_Thay\AIOT_BLACKBOX_PRESENTATION"
os.chdir(proj_dir)

kicad_cli = r"D:\KiCad\bin\kicad-cli.exe"
main_sch = "AIOT_BLACKBOX_PRESENTATION.kicad_sch"
source_sch = os.path.join("scratch_rev8", "test_all_names.kicad_sch")

# 1. Copy to main
shutil.copyfile(source_sch, main_sch)
print(f"Updated {main_sch} ({os.path.getsize(main_sch)} bytes)")

# 2. Run ERC
erc_json = "AIOT_BLACKBOX_PRESENTATION_REV8_erc.json"
subprocess.run([kicad_cli, "sch", "erc", "--severity-all", "--format", "json", "-o", erc_json, main_sch], check=True)

with open(erc_json, 'r', encoding='utf-8') as f:
    rpt = json.load(f)

violations = rpt['sheets'][0]['violations']
errors = [v for v in violations if v['severity'] == 'error']
raw_warnings = [v for v in violations if v['severity'] == 'warning']
warnings = [w for w in raw_warnings if w['type'] != 'lib_symbol_issues']

print("=== FINAL MAIN ERC REPORT ===")
print(f"Total violations: {len(violations)}")
print(f"REAL ERRORS: {len(errors)}")
print(f"REAL WARNINGS: {len(warnings)}")

# 3. Export PDF
pdf_out = "AIOT_BLACKBOX_PRESENTATION_A4_REV8_FINAL.pdf"
subprocess.run([kicad_cli, "sch", "export", "pdf", "-o", pdf_out, main_sch], check=True)
print(f"Exported PDF: {pdf_out} ({os.path.getsize(pdf_out)} bytes)")

# 4. Export SVG
svg_out = "AIOT_BLACKBOX_PRESENTATION_A4_REV8_FINAL.svg"
subprocess.run([kicad_cli, "sch", "export", "svg", "-o", svg_out, main_sch], check=True)
print(f"Exported SVG: {svg_out}")

# Copy standalone SVG if folder created
if os.path.isdir(svg_out):
    inner_svg = os.path.join(svg_out, "AIOT_BLACKBOX_PRESENTATION.svg")
    if os.path.exists(inner_svg):
        shutil.copy(inner_svg, "AIOT_BLACKBOX_PRESENTATION_A4_REV8_FINAL_standalone.svg")

# 5. Render PNG (300 DPI)
png_out = "AIOT_BLACKBOX_PRESENTATION_A4_REV8_FINAL.png"
doc = pymupdf.open(pdf_out)
page = doc[0]
pix = page.get_pixmap(dpi=300)
pix.save(png_out)
print(f"Rendered PNG: {png_out} ({pix.width}x{pix.height}, {os.path.getsize(png_out)} bytes)")

print("\nSYNCHRONIZATION COMPLETED AND EXPORTED SUCCESSFULLY!")
