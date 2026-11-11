import re, os, subprocess, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from sexpr_util import extract_sexprs

# Re-copy fresh REV4 into scratch_rev5
SRC = 'AIOT_BLACKBOX_PRESENTATION_REV4_backup.kicad_sch'
SCH_PATH = os.path.join('scratch_rev5', 'AIOT_BLACKBOX_PRESENTATION.kicad_sch')
shutil.copy(SRC, SCH_PATH)

with open(SCH_PATH, 'r', encoding='utf-8') as f:
    text = f.read()

assert text.count('(') == text.count(')'), "Unbalanced parens at start"

# 1. Update Symbols using helper function
def replace_sexpr_by_ref(content, ref, new_at_str, new_ref_str=None, new_val_str=None):
    syms = extract_sexprs(content, "(symbol")
    for st, en, s in syms:
        if f'(property "Reference" "{ref}"' in s:
            new_s = re.sub(r'\(at\s+[0-9\.\-]+\s+[0-9\.\-]+(?:\s+[0-9\.\-]+)?\)', new_at_str, s, count=1)
            if new_ref_str:
                new_s = re.sub(r'\(property "Reference" "' + ref + r'"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', new_ref_str, new_s)
            if new_val_str:
                new_s = re.sub(r'\(property "Value" "[^"]+"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', new_val_str, new_s)
            return content[:st] + new_s + content[en:]
    raise ValueError(f"Symbol with Reference {ref} not found")

# R3:
text = replace_sexpr_by_ref(text, "R3", "(at 200.66 118.11 0)",
                            '(property "Reference" "R3" (at 203.20 116.84 0)',
                            '(property "Value" "10k" (at 203.20 119.38 0)')
# C2:
text = replace_sexpr_by_ref(text, "C2", "(at 200.66 130.81 0)",
                            '(property "Reference" "C2" (at 203.20 129.54 0)',
                            '(property "Value" "100nF" (at 203.20 132.08 0)')
# SW1:
text = replace_sexpr_by_ref(text, "SW1", "(at 210.82 124.46 0)",
                            '(property "Reference" "SW1" (at 210.82 118.50 0)',
                            '(property "Value" "CANCEL" (at 210.82 121.50 0)')
# R4:
text = replace_sexpr_by_ref(text, "R4", "(at 227.33 142.24 90)",
                            '(property "Reference" "R4" (at 227.33 138.43 90)',
                            '(property "Value" "330R" (at 227.33 146.05 90)')
# D1:
text = replace_sexpr_by_ref(text, "D1", "(at 237.49 142.24 180)",
                            '(property "Reference" "D1" (at 237.49 138.43 0)',
                            '(property "Value" "LED" (at 237.49 146.05 0)')
# R5:
text = replace_sexpr_by_ref(text, "R5", "(at 255.27 154.94 90)",
                            '(property "Reference" "R5" (at 255.27 151.13 90)',
                            '(property "Value" "1k" (at 255.27 158.75 90)')
# Q1:
text = replace_sexpr_by_ref(text, "Q1", "(at 266.7 154.94 0)",
                            '(property "Reference" "Q1" (at 272.50 152.40 0)',
                            '(property "Value" "2SC1815" (at 272.50 156.50 0)')
# BZ1:
text = replace_sexpr_by_ref(text, "BZ1", "(at 271.78 147.32 0)",
                            '(property "Reference" "BZ1" (at 278.00 144.78 0)',
                            '(property "Value" "BUZZER" (at 278.00 149.86 0)')

# Power symbols replacement by match
def replace_power_sym(content, lib, old_x, old_y, new_at_str, new_val_str):
    syms = extract_sexprs(content, "(symbol")
    for st, en, s in syms:
        if f'(lib_id "{lib}")' in s:
            m_at = re.search(r'\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)', s)
            if m_at:
                x, y = float(m_at.group(1)), float(m_at.group(2))
                if abs(x - old_x) < 0.1 and abs(y - old_y) < 0.1:
                    new_s = re.sub(r'\(at\s+[0-9\.\-]+\s+[0-9\.\-]+(?:\s+[0-9\.\-]+)?\)', new_at_str, s, count=1)
                    new_s = re.sub(r'\(property "Value" "[^"]+"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', new_val_str, new_s)
                    return content[:st] + new_s + content[en:]
    raise ValueError(f"Power symbol {lib} at ({old_x},{old_y}) not found")

# +3V3_UI at (195.58, 124.46) -> (200.66, 111.76, 0)
text = replace_power_sym(text, "power:+3V3", 195.58, 124.46, '(at 200.66 111.76 0)', '(property "Value" "+3V3" (at 200.66 107.95 0)')
# 5V_SYS_UI at (269.24, 121.92) -> (269.24, 139.70, 0)
text = replace_power_sym(text, "power:5V_SYS", 269.24, 121.92, '(at 269.24 139.70 0)', '(property "Value" "5V_SYS" (at 269.24 135.89 0)')
# GND_C2 at (195.58, 149.86) -> (200.66, 137.16, 0)
text = replace_power_sym(text, "power:GND", 195.58, 149.86, '(at 200.66 137.16 0)', '(property "Value" "GND" (at 200.66 140.97 0)')
# GND_SW1 at (213.36, 149.86) -> (218.44, 129.54, 0)
text = replace_power_sym(text, "power:GND", 213.36, 149.86, '(at 218.44 129.54 0)', '(property "Value" "GND" (at 218.44 133.35 0)')
# GND_D1 at (243.84, 143.51) -> (243.84, 147.32, 0)
text = replace_power_sym(text, "power:GND", 243.84, 143.51, '(at 243.84 147.32 0)', '(property "Value" "GND" (at 243.84 151.13 0)')
# GND_Q1 at (269.24, 147.32) -> (269.24, 162.56, 0)
text = replace_power_sym(text, "power:GND", 269.24, 147.32, '(at 269.24 162.56 0)', '(property "Value" "GND" (at 269.24 166.37 0)')

# UI Title text: move to (252 126 0)
old_ui_title = '(text "KHỐI CẢNH BÁO & NÚT BẤM (UI)"\n\t\t(exclude_from_sim no)\n\t\t(at 248 156 0)'
new_ui_title = '(text "KHỐI CẢNH BÁO & NÚT BẤM (UI)"\n\t\t(exclude_from_sim no)\n\t\t(at 252 126 0)'
assert old_ui_title in text, "Failed to find old UI title"
text = text.replace(old_ui_title, new_ui_title)

# Remove ALL old UI wires:
old_wires_coords = [
    (185.42, 109.22, 185.42, 137.16),
    (243.84, 137.16, 243.84, 143.51),
    (195.58, 137.16, 195.58, 134.62),
    (259.08, 137.16, 261.62, 137.16),
    (241.30, 137.16, 243.84, 137.16),
    (175.26, 109.22, 185.42, 109.22),
    (231.14, 137.16, 233.68, 137.16),
    (195.58, 137.16, 195.58, 139.70),
    (269.24, 127.00, 269.24, 121.92),
    (269.24, 142.24, 269.24, 147.32),
    (195.58, 147.32, 195.58, 149.86),
    (213.36, 137.16, 213.36, 149.86),
    (185.42, 137.16, 195.58, 137.16),
    (195.58, 127.00, 195.58, 124.46),
    (195.58, 137.16, 200.66, 137.16),
    (210.82, 137.16, 213.36, 137.16),
    (175.26, 114.30, 187.96, 114.30),
    (187.96, 114.30, 187.96, 111.76),
    (187.96, 111.76, 220.98, 111.76),
    (220.98, 111.76, 220.98, 137.16),
    (220.98, 137.16, 223.52, 137.16),
    (175.26, 119.38, 248.92, 119.38),
    (248.92, 119.38, 248.92, 137.16),
    (248.92, 137.16, 251.46, 137.16),
]

wire_sexprs = extract_sexprs(text, "(wire")
for st, en, w in wire_sexprs:
    m = re.search(r'\(xy\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)\s+\(xy\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)', w)
    if m:
        x1, y1, x2, y2 = float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4))
        for ox1, oy1, ox2, oy2 in old_wires_coords:
            if (abs(x1 - ox1) < 0.05 and abs(y1 - oy1) < 0.05 and abs(x2 - ox2) < 0.05 and abs(y2 - oy2) < 0.05) or \
               (abs(x1 - ox2) < 0.05 and abs(y1 - oy2) < 0.05 and abs(x2 - ox1) < 0.05 and abs(y2 - oy1) < 0.05):
                text = text.replace(w, "")
                break

# Remove old junction at (195.58, 137.16) using extract_sexprs
juncs = extract_sexprs(text, "(junction")
for st, en, j in juncs:
    m = re.search(r'\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)', j)
    if m:
        jx, jy = float(m.group(1)), float(m.group(2))
        if abs(jx - 195.58) < 0.1 and abs(jy - 137.16) < 0.1:
            text = text.replace(j, "")
            print("Removed old junction at (195.58, 137.16)")
            break

import uuid

def make_wire(x1, y1, x2, y2):
    u = str(uuid.uuid4())
    return f'''  (wire
    (pts
      (xy {x1:.2f} {y1:.2f}) (xy {x2:.2f} {y2:.2f})
    )
    (stroke
      (width 0)
      (type default)
    )
    (uuid "{u}")
  )'''

def make_junction(x, y):
    u = str(uuid.uuid4())
    return f'''  (junction
    (at {x:.2f} {y:.2f})
    (diameter 0)
    (color 0 0 0 0)
    (uuid "{u}")
  )'''

new_wires = [
    # --- ROW 1 (CANCEL, GPIO6) ---
    # Lane 1: (175.26, 109.22) -> (195.58, 109.22) -> (195.58, 124.46) -> (200.66, 124.46)
    make_wire(175.26, 109.22, 195.58, 109.22),
    make_wire(195.58, 109.22, 195.58, 124.46),
    make_wire(195.58, 124.46, 200.66, 124.46),
    # Node to R3: (200.66, 124.46) -> (200.66, 121.92)
    make_wire(200.66, 124.46, 200.66, 121.92),
    # R3 to +3V3: (200.66, 114.30) -> (200.66, 111.76)
    make_wire(200.66, 114.30, 200.66, 111.76),
    # Node to C2: (200.66, 124.46) -> (200.66, 127.00)
    make_wire(200.66, 124.46, 200.66, 127.00),
    # C2 to GND: (200.66, 134.62) -> (200.66, 137.16)
    make_wire(200.66, 134.62, 200.66, 137.16),
    # Node to SW1: (200.66, 124.46) -> (205.74, 124.46)
    make_wire(200.66, 124.46, 205.74, 124.46),
    # SW1 to GND: (215.90, 124.46) -> (218.44, 124.46) -> (218.44, 129.54)
    make_wire(215.90, 124.46, 218.44, 124.46),
    make_wire(218.44, 124.46, 218.44, 129.54),

    # --- ROW 2 (STATUS LED, GPIO7) ---
    # Lane 2: (175.26, 114.30) -> (190.50, 114.30) -> (190.50, 142.24) -> (223.52, 142.24)
    make_wire(175.26, 114.30, 190.50, 114.30),
    make_wire(190.50, 114.30, 190.50, 142.24),
    make_wire(190.50, 142.24, 223.52, 142.24),
    # R4 to D1: (231.14, 142.24) -> (233.68, 142.24)
    make_wire(231.14, 142.24, 233.68, 142.24),
    # D1 to GND: (241.30, 142.24) -> (243.84, 142.24) -> (243.84, 147.32)
    make_wire(241.30, 142.24, 243.84, 142.24),
    make_wire(243.84, 142.24, 243.84, 147.32),

    # --- ROW 3 (BUZZER, GPIO15) ---
    # Lane 3: (175.26, 119.38) -> (185.42, 119.38) -> (185.42, 154.94) -> (251.46, 154.94)
    make_wire(175.26, 119.38, 185.42, 119.38),
    make_wire(185.42, 119.38, 185.42, 154.94),
    make_wire(185.42, 154.94, 251.46, 154.94),
    # R5 to Q1 Base: (259.08, 154.94) -> (261.62, 154.94)
    make_wire(259.08, 154.94, 261.62, 154.94),
    # Q1 Emitter to GND: (269.24, 160.02) -> (269.24, 162.56)
    make_wire(269.24, 160.02, 269.24, 162.56),
    # BZ1 Pin 1 (+) to 5V_SYS: (269.24, 144.78) -> (269.24, 139.70)
    make_wire(269.24, 144.78, 269.24, 139.70),
]

new_junc = make_junction(200.66, 124.46)

# Insert new wires and junction
insert_idx = text.rfind(')')
new_elements_str = "\n" + new_junc + "\n" + "\n".join(new_wires) + "\n"
text = text[:insert_idx] + new_elements_str + text[insert_idx:]

assert text.count('(') == text.count(')'), "Unbalanced parens after modification"

with open(SCH_PATH, 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved scratch_rev5. Running ERC...")
cmd = ['D:\\Kicad\\bin\\kicad-cli.exe', 'sch', 'erc', '--severity-all', '--format', 'json', SCH_PATH]
res = subprocess.run(cmd, capture_output=True, text=True)
print("ERC Return code:", res.returncode)

# Export PDF and SVG and render PNG crop
OUT_PDF = os.path.join('scratch_rev5', 'AIOT_BLACKBOX_PRESENTATION_test_rev5.pdf')
OUT_SVG = os.path.join('scratch_rev5', 'AIOT_BLACKBOX_PRESENTATION_test_rev5.svg')
subprocess.run(['D:\\Kicad\\bin\\kicad-cli.exe', 'sch', 'export', 'pdf', '-o', OUT_PDF, SCH_PATH], capture_output=True)
subprocess.run(['D:\\Kicad\\bin\\kicad-cli.exe', 'sch', 'export', 'svg', '-o', OUT_SVG, SCH_PATH], capture_output=True)

import pymupdf
doc = pymupdf.open(OUT_PDF)
page = doc[0]
zoom = 300 / 72
mat = pymupdf.Matrix(zoom, zoom)
rect = pymupdf.Rect(165 * 72 / 25.4, 95 * 72 / 25.4, 285 * 72 / 25.4, 175 * 72 / 25.4)
pix_crop = page.get_pixmap(matrix=mat, clip=rect)
crop_png = os.path.join('scratch_rev5', 'ui_region_crop.png')
pix_crop.save(crop_png)
print("Saved UI crop PNG:", crop_png)
