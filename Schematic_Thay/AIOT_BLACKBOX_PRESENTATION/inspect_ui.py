import re

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find all instances of (symbol (lib_id ...) ...)
# and extract their Reference property
symbols = []
# split or parse top-level symbols
# KiCad schematic contains (symbol (lib_id ...) ... ) at root level
# We can find them by regex matching "(symbol (lib_id" and then matching balanced parentheses

def extract_sexprs(content, tag):
    idx = 0
    results = []
    pattern = tag
    while True:
        pos = content.find(pattern, idx)
        if pos == -1:
            break
        # verify if it is preceded by newline or space or start of sexpr
        count = 0
        end = -1
        for i in range(pos, len(content)):
            if content[i] == '(':
                count += 1
            elif content[i] == ')':
                count -= 1
                if count == 0:
                    end = i + 1
                    break
        if end != -1:
            results.append((pos, end, content[pos:end]))
            idx = end
        else:
            idx = pos + 1
    return results

if __name__ == '__main__':
    syms = extract_sexprs(text, "(symbol")
    print(f"Total symbols found: {len(syms)}")

    ui_refs = ['R3', 'C2', 'SW1', 'R4', 'D1', 'R5', 'Q1', 'BZ1']

    for start, end, s in syms:
    m_ref = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', s)
    m_val = re.search(r'\(property\s+"Value"\s+"([^"]+)"', s)
    m_at = re.search(r'\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)(?:\s+([0-9\.\-]+))?\)', s)
    m_lib = re.search(r'\(lib_id\s+"([^"]+)"\)', s)
    
    ref = m_ref.group(1) if m_ref else ""
    val = m_val.group(1) if m_val else ""
    at = (float(m_at.group(1)), float(m_at.group(2)), float(m_at.group(3) or 0)) if m_at else (0,0,0)
    lib = m_lib.group(1) if m_lib else ""
    
    if ref in ui_refs or "GND" in lib or "+3V3" in lib or "5V" in lib:
        if ref in ui_refs or (at[0] >= 170 and at[1] >= 100):
            print(f"Symbol: Ref={ref:6s} Val={val:10s} Lib={lib:20s} At=({at[0]:.2f}, {at[1]:.2f}, {at[2]:.0f})")

print("\n=== WIRES IN UI REGION (x >= 170, y >= 100) ===")
wires = extract_sexprs(text, "(wire")
for start, end, w in wires:
    m = re.search(r'\(xy\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)\s+\(xy\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)', w)
    if m:
        x1, y1, x2, y2 = float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4))
        if (x1 >= 170 or x2 >= 170) and (y1 >= 100 or y2 >= 100):
            print(f"Wire: ({x1:6.2f}, {y1:6.2f}) -> ({x2:6.2f}, {y2:6.2f})")

print("\n=== JUNCTIONS IN UI REGION (x >= 170, y >= 100) ===")
juncs = extract_sexprs(text, "(junction")
for start, end, j in juncs:
    m = re.search(r'\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)', j)
    if m:
        jx, jy = float(m.group(1)), float(m.group(2))
        if jx >= 170 and jy >= 100:
            print(f"Junction at ({jx:.2f}, {jy:.2f})")
