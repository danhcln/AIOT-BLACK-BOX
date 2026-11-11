import re
with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

from inspect_ui import extract_sexprs
polys = extract_sexprs(text, "(polyline")
print(f"Total polylines: {len(polys)}")
for i, (st, en, p) in enumerate(polys):
    pts = re.findall(r'\(xy\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)', p)
    print(f"Poly #{i}: {pts}")
