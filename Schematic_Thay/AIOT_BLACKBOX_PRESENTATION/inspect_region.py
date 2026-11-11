import re

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

from inspect_ui import extract_sexprs

# Find symbols in x >= 170, y >= 70, y <= 130
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
    if at[0] >= 170 and at[1] >= 70 and at[1] <= 130:
        print(f"Ref={ref:10s} Val={val:15s} Lib={lib:25s} At=({at[0]:.2f}, {at[1]:.2f})")

# Also labels in x >= 170, y >= 70
labels = extract_sexprs(text, "(label")
for start, end, l in labels:
    m = re.search(r'\(label\s+"([^"]+)"\s+\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)', l)
    if m:
        name, lx, ly = m.group(1), float(m.group(2)), float(m.group(3))
        if lx >= 170 and ly >= 70:
            print(f"Label '{name}' at ({lx:.2f}, {ly:.2f})")

# Also global labels / hierarchical labels
for tag in ["(global_label", "(hierarchical_label"]:
    gls = extract_sexprs(text, tag)
    for start, end, gl in gls:
        m = re.search(r'"([^"]+)"\s+\(shape[^\)]*\)\s+\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)', gl)
        if m:
            name, lx, ly = m.group(1), float(m.group(2)), float(m.group(3))
            if lx >= 170 and ly >= 70:
                print(f"Global/Hier Label '{name}' at ({lx:.2f}, {ly:.2f})")
