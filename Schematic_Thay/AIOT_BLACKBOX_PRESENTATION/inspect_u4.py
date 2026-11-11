import re
from inspect_ui import extract_sexprs

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

# Find U4
syms = extract_sexprs(text, "(symbol")
for start, end, s in syms:
    if '"U4"' in s:
        print("=== U4 SYMBOL ===")
        print(s[:1000])

# Find all wires connecting to U4 area (x around 210..270, y around 80..120)
print("\n=== WIRES AROUND U4 ===")
wires = extract_sexprs(text, "(wire")
for start, end, w in wires:
    m = re.search(r'\(xy\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)\s+\(xy\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)', w)
    if m:
        x1, y1, x2, y2 = float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4))
        if (210 <= x1 <= 275 or 210 <= x2 <= 275) and (80 <= y1 <= 125 or 80 <= y2 <= 125):
            print(f"Wire: ({x1:6.2f}, {y1:6.2f}) -> ({x2:6.2f}, {y2:6.2f})")
