import os, sys, shutil, subprocess, json, pymupdf

sys.stdout.reconfigure(encoding='utf-8')
proj_dir = r"D:\ĐỒ ÁN 2\Schematic_Thay\AIOT_BLACKBOX_PRESENTATION"
os.chdir(proj_dir)

kicad_cli = r"D:\KiCad\bin\kicad-cli.exe"
main_sch = "AIOT_BLACKBOX_PRESENTATION.kicad_sch"
candidate_sch = os.path.join("scratch_rev8", "candidate_rev8.kicad_sch")

# 1. Verify no locks
import glob
lcks = glob.glob('*.lck') + glob.glob('~*')
if lcks:
    print("ERROR: Active lock files found:", lcks)
    sys.exit(1)

# 2. Copy candidate to main
shutil.copyfile(candidate_sch, main_sch)
print(f"Copied {candidate_sch} to {main_sch} (size: {os.path.getsize(main_sch)} bytes)")

# 3. Run ERC on main
erc_json = "AIOT_BLACKBOX_PRESENTATION_REV8_erc.json"
erc_cmd = [kicad_cli, "sch", "erc", "--severity-all", "--format", "json", "-o", erc_json, main_sch]
erc_res = subprocess.run(erc_cmd, capture_output=True, text=True)
print("ERC Return code:", erc_res.returncode)

with open(erc_json, 'r', encoding='utf-8') as f:
    rpt = json.load(f)

violations = rpt['sheets'][0]['violations']
errors = [v for v in violations if v['severity'] == 'error']
warnings = [v for v in violations if v['severity'] == 'warning']
real_warnings = [w for w in warnings if w['type'] != 'lib_symbol_issues']

print("=== FINAL MAIN ERC REPORT ===")
print(f"Total violations: {len(violations)}")
print(f"REAL ERRORS: {len(errors)}")
print(f"REAL WARNINGS: {len(real_warnings)}")
for e in errors:
    print("  ERROR:", e['type'], e['description'])
for rw in real_warnings:
    print("  REAL WARN:", rw['type'], rw['description'])

# 4. Export PDF
pdf_out = "AIOT_BLACKBOX_PRESENTATION_A4_REV8_FINAL.pdf"
subprocess.run([kicad_cli, "sch", "export", "pdf", "-o", pdf_out, main_sch], check=True)
print(f"Exported PDF: {pdf_out} ({os.path.getsize(pdf_out)} bytes)")

# 5. Export SVG
svg_out = "AIOT_BLACKBOX_PRESENTATION_A4_REV8_FINAL.svg"
subprocess.run([kicad_cli, "sch", "export", "svg", "-o", svg_out, main_sch], check=True)
print(f"Exported SVG: {svg_out}")

# 6. Render PNG (300 DPI)
png_out = "AIOT_BLACKBOX_PRESENTATION_A4_REV8_FINAL.png"
doc = pymupdf.open(pdf_out)
page = doc[0]
pix = page.get_pixmap(dpi=300)
pix.save(png_out)
print(f"Rendered PNG: {png_out} ({pix.width}x{pix.height}, {os.path.getsize(png_out)} bytes)")

print("\nREV8 EXPORT COMPLETED SUCCESSFULLY!")
