import os, shutil, subprocess, sys, json
sys.stdout.reconfigure(encoding='utf-8')

for f in ['AIOT_BLACKBOX_PRESENTATION.kicad_pro', 'AIOT_BLACKBOX_PRESENTATION.kicad_prl', 'AIOT_BLACKBOX_PRESENTATION.kicad_wks']:
    if os.path.exists(f):
        shutil.copy(f, os.path.join('scratch_rev6', f))

sch_path = os.path.join('scratch_rev6', 'AIOT_BLACKBOX_PRESENTATION.kicad_sch')
erc_out = os.path.join('scratch_rev6', 'test_erc.json')

cmd = [
    r'D:\KiCad\bin\kicad-cli.exe',
    'sch',
    'erc',
    '--severity-all',
    '--format', 'json',
    '-o', erc_out,
    sch_path
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("ERC returncode:", res.returncode)
print("ERC stdout:\n", res.stdout)
print("ERC stderr:\n", res.stderr)

if os.path.exists(erc_out):
    with open(erc_out, 'r', encoding='utf-8') as f:
        d = json.load(f)
    violations = d.get('sheets', [{}])[0].get('violations', [])
    print(f"Total violations: {len(violations)}")
    errors = [v for v in violations if v.get('type') == 'error']
    warnings = [v for v in violations if v.get('type') == 'warning']
    print(f"ERRORS: {len(errors)}")
    print(f"WARNINGS: {len(warnings)}")
    for e in errors:
        print(f"  [ERROR] {e.get('description')}")
    for w in warnings[:10]:
        print(f"  [WARNING] {w.get('description')}")
