import re, sys
sys.stdout.reconfigure(encoding='utf-8')
from inspect_ui import extract_sexprs

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

# Check everything with y between 100 and 190, and x between 160 and 285
print("=== ALL SYMBOLS IN LOWER-RIGHT (x >= 160, y >= 100) ===")
syms = extract_sexprs(text, "(symbol")
for start, end, s in syms:
    m_ref = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', s)
    m_val = re.search(r'\(property\s+"Value"\s+"([^"]+)"', s)
    m_at = re.search(r'\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)(?:\s+([0-9\.\-]+))?\)', s)
    m_lib = re.search(r'\(lib_id\s+"([^"]+)"\)', s)
    ref = m_ref.group(1) if m_ref else ""
    val = m_val.group(1) if m_val else ""
    at = (float(m_at.group(1)), float(m_at.group(2)), float(m_at.group(3) or 0)) if m_at else (0,0,0)
    lib = m_lib.group(1) if m_lib else ""
    if at[0] >= 160 and at[1] >= 100:
        print(f"Ref={ref:10s} Val={val:15s} Lib={lib:25s} At=({at[0]:.2f}, {at[1]:.2f}, rot={at[2]:.0f})")

# Check all text / graphic boxes / lines in this area
print("\n=== GRAPHIC TEXT / SHAPES IN THIS AREA ===")
texts = extract_sexprs(text, "(text")
for start, end, t in texts:
    m_at = re.search(r'\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)', t)
    m_txt = re.search(r'"([^"]+)"', t)
    if m_at and m_txt:
        tx, ty = float(m_at.group(1)), float(m_at.group(2))
        if tx >= 160 and ty >= 100:
            print(f"Text '{m_txt.group(1)}' at ({tx:.2f}, {ty:.2f})")

rects = extract_sexprs(text, "(polyline")
for start, end, r in rects:
    pts = re.findall(r'\(xy\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)', r)
    pts_f = [(float(x), float(y)) for x, y in pts]
    if any(x >= 160 and y >= 100 for x, y in pts_f):
        xs = [p[0] for p in pts_f]
        ys = [p[1] for p in pts_f]
        print(f"Polyline box/line: x in [{min(xs):.2f}, {max(xs):.2f}], y in [{min(ys):.2f}, {max(ys):.2f}]")
