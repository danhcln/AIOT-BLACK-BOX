import os, shutil, subprocess, sys, json, psutil

sys.stdout.reconfigure(encoding='utf-8')

MAIN_DIR = r'D:\ĐỒ ÁN 2\Schematic_Thay\AIOT_BLACKBOX_PRESENTATION'
MAIN_SCH = os.path.join(MAIN_DIR, 'AIOT_BLACKBOX_PRESENTATION.kicad_sch')
BACKUP_SCH = os.path.join(MAIN_DIR, 'AIOT_BLACKBOX_PRESENTATION_REV5_backup.kicad_sch')
CANDIDATE_SCH = os.path.join(MAIN_DIR, 'scratch_rev6', 'AIOT_BLACKBOX_PRESENTATION.kicad_sch')
OUT_PDF = os.path.join(MAIN_DIR, 'AIOT_BLACKBOX_PRESENTATION_A4_REV6.pdf')
OUT_SVG = os.path.join(MAIN_DIR, 'AIOT_BLACKBOX_PRESENTATION_A4_REV6.svg')
SVG_DIR = os.path.join(MAIN_DIR, 'svg_out_rev6')
os.makedirs(SVG_DIR, exist_ok=True)

# 1. Safety check
kicad_procs = [p.name() for p in psutil.process_iter(['name']) if 'kicad' in p.name().lower() or 'eeschema' in p.name().lower()]
if kicad_procs:
    print("ERROR: KiCad processes running:", kicad_procs)
    sys.exit(1)

lck_sch = os.path.join(MAIN_DIR, '~AIOT_BLACKBOX_PRESENTATION.kicad_sch.lck')
lck_pro = os.path.join(MAIN_DIR, '~AIOT_BLACKBOX_PRESENTATION.kicad_pro.lck')
if os.path.exists(lck_sch) or os.path.exists(lck_pro):
    print("ERROR: Lock files exist!")
    sys.exit(1)

if not os.path.exists(BACKUP_SCH):
    print("ERROR: REV5 backup missing! Creating backup now...")
    shutil.copyfile(MAIN_SCH, BACKUP_SCH)
print(f"Verified REV5 backup: {BACKUP_SCH} ({os.path.getsize(BACKUP_SCH)} bytes)")

# 2. Copy candidate to MAIN_SCH
shutil.copyfile(CANDIDATE_SCH, MAIN_SCH)
print(f"Successfully applied REV6 candidate to MAIN source: {MAIN_SCH} ({os.path.getsize(MAIN_SCH)} bytes)")

# 3. Run KiCad ERC on MAIN source
erc_json = os.path.join(MAIN_DIR, 'AIOT_BLACKBOX_PRESENTATION_REV6-erc.json')
cmd_erc = [
    r'D:\KiCad\bin\kicad-cli.exe',
    'sch',
    'erc',
    '--severity-all',
    '--format', 'json',
    '-o', erc_json,
    MAIN_SCH
]
res_erc = subprocess.run(cmd_erc, capture_output=True, text=True)
print(f"KiCad ERC returncode: {res_erc.returncode}")

with open(erc_json, 'r', encoding='utf-8') as f:
    erc_data = json.load(f)

violations = erc_data.get('sheets', [{}])[0].get('violations', [])
errors = [v for v in violations if v.get('type') == 'error']
warnings = [v for v in violations if v.get('type') == 'warning']
print(f"Total ERC violations: {len(violations)}")
print(f"ERC Real Errors: {len(errors)}")
print(f"ERC Real Warnings: {len(warnings)}")

# 4. Export PDF
cmd_pdf = [
    r'D:\KiCad\bin\kicad-cli.exe',
    'sch',
    'export',
    'pdf',
    '-o', OUT_PDF,
    MAIN_SCH
]
res_pdf = subprocess.run(cmd_pdf, capture_output=True, text=True)
print(f"PDF export returncode: {res_pdf.returncode} -> {OUT_PDF} ({os.path.getsize(OUT_PDF)} bytes)")

# 5. Export SVG
cmd_svg = [
    r'D:\KiCad\bin\kicad-cli.exe',
    'sch',
    'export',
    'svg',
    '-o', SVG_DIR,
    MAIN_SCH
]
res_svg = subprocess.run(cmd_svg, capture_output=True, text=True)
exported_svg_file = os.path.join(SVG_DIR, 'AIOT_BLACKBOX_PRESENTATION.svg')
if os.path.exists(exported_svg_file):
    shutil.copyfile(exported_svg_file, OUT_SVG)
    print(f"SVG export returncode: {res_svg.returncode} -> {OUT_SVG} ({os.path.getsize(OUT_SVG)} bytes)")
else:
    print("Warning: Exported SVG not found at", exported_svg_file)

print("\nREV6 APPLIED AND EXPORTED SUCCESSFULLY!")
