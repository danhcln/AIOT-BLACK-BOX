import re, os, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
from sexpr_util import extract_sexprs

SCH_PATH = os.path.join('scratch_rev5', 'AIOT_BLACKBOX_PRESENTATION.kicad_sch')

with open(SCH_PATH, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. We need to identify all UI symbols, wires, and junctions to be replaced.
# Symbols to replace:
# R3, C2, SW1, R4, D1, R5, Q1, BZ1
# and local power symbols:
# +3V3 at 195.58, 124.46
# 5V_SYS at 269.24, 121.92
# GND at 195.58, 149.86 (for C2)
# GND at 213.36, 149.86 (for SW1)
# GND at 243.84, 143.51 (for D1)
# GND at 269.24, 147.32 (for Q1)

# Notice ESP32 GND at (180.34, 127.00) MUST REMAIN!
# ATGM336H GND at (217.17, 116.84) MUST REMAIN!
# ATGM336H +3V3 at (217.17, 85.09) MUST REMAIN!

# Let's verify which symbols are which:
syms = extract_sexprs(text, "(symbol")
ui_symbols_to_remove = []

for st, en, s in syms:
    m_ref = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', s)
    m_val = re.search(r'\(property\s+"Value"\s+"([^"]+)"', s)
    m_at = re.search(r'\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)', s)
    m_lib = re.search(r'\(lib_id\s+"([^"]+)"\)', s)
    
    ref = m_ref.group(1) if m_ref else ""
    val = m_val.group(1) if m_val else ""
    x = float(m_at.group(1)) if m_at else 0
    y = float(m_at.group(2)) if m_at else 0
    lib = m_lib.group(1) if m_lib else ""
    
    if ref in ['R3', 'C2', 'SW1', 'R4', 'D1', 'R5', 'Q1', 'BZ1']:
        ui_symbols_to_remove.append((st, en, ref))
    elif lib == "power:+3V3" and abs(x - 195.58) < 1:
        ui_symbols_to_remove.append((st, en, "+3V3_UI"))
    elif lib == "power:5V_SYS" and abs(x - 269.24) < 1:
        ui_symbols_to_remove.append((st, en, "5V_SYS_UI"))
    elif lib == "power:GND":
        if abs(x - 195.58) < 1: # C2 GND
            ui_symbols_to_remove.append((st, en, "GND_C2"))
        elif abs(x - 213.36) < 1: # SW1 GND
            ui_symbols_to_remove.append((st, en, "GND_SW1"))
        elif abs(x - 243.84) < 1: # D1 GND
            ui_symbols_to_remove.append((st, en, "GND_D1"))
        elif abs(x - 269.24) < 1 and y > 130: # Q1 GND
            ui_symbols_to_remove.append((st, en, "GND_Q1"))

print(f"Found {len(ui_symbols_to_remove)} UI symbols to update:")
for st, en, name in ui_symbols_to_remove:
    print(f"  - {name} [{st}:{en}]")

# Let's verify wires to remove:
# In REV4, wires connecting Pin 19, 20, 21 and the UI components:
wires = extract_sexprs(text, "(wire")
ui_wires_to_remove = []

for st, en, w in wires:
    m = re.search(r'\(xy\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)\s+\(xy\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)', w)
    if m:
        x1, y1, x2, y2 = float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4))
        # Keep ESP32 GND wire: (175.26, 124.46) -> (180.34, 124.46) and (180.34, 124.46) -> (180.34, 127.00)
        if (abs(y1 - 124.46) < 0.1 and abs(y2 - 124.46) < 0.1) or (abs(x1 - 180.34) < 0.1 and abs(x2 - 180.34) < 0.1):
            continue
        # Keep GNSS wires (pins 16, 17, 18 at y=93.98, 99.06, 104.14, and GNSS GND/VCC)
        if y1 <= 105 and y2 <= 105:
            continue
        if abs(y1 - 114.30) < 0.1 and abs(y2 - 116.84) < 0.1: # GNSS GND
            continue
        if abs(y1 - 91.44) < 0.1 or abs(y2 - 91.44) < 0.1: # GNSS VCC
            continue
        
        # UI area wires:
        if (x1 >= 175 or x2 >= 175) and (y1 >= 108 or y2 >= 108) and (y1 <= 155 and y2 <= 155):
            ui_wires_to_remove.append((st, en, f"({x1},{y1})->({x2},{y2})"))

print(f"\nFound {len(ui_wires_to_remove)} UI wires to replace:")
for st, en, wname in ui_wires_to_remove:
    print(f"  - {wname}")

# Junctions:
juncs = extract_sexprs(text, "(junction")
ui_juncs_to_remove = []
for st, en, j in juncs:
    m = re.search(r'\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)', j)
    if m:
        jx, jy = float(m.group(1)), float(m.group(2))
        if jx >= 180 and jy >= 120 and jy <= 155:
            ui_juncs_to_remove.append((st, en, f"Junction at ({jx},{jy})"))

print(f"\nFound {len(ui_juncs_to_remove)} UI junctions to replace:")
for st, en, jname in ui_juncs_to_remove:
    print(f"  - {jname}")
