import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')
from sexpr_util import extract_sexprs

SCH_PATH = os.path.join('scratch_rev5', 'AIOT_BLACKBOX_PRESENTATION.kicad_sch')
with open(SCH_PATH, 'r', encoding='utf-8') as f:
    text = f.read()

juncs = extract_sexprs(text, "(junction")
print(f"Total junctions: {len(juncs)}")
for st, en, j in juncs:
    m = re.search(r'\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)', j)
    if m:
        jx, jy = float(m.group(1)), float(m.group(2))
        print(f"Junction at ({jx:.2f}, {jy:.2f})")
