import re, os, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
from sexpr_util import extract_sexprs

SCH_PATH = os.path.join('scratch_rev5', 'AIOT_BLACKBOX_PRESENTATION.kicad_sch')
with open(SCH_PATH, 'r', encoding='utf-8') as f:
    text = f.read()

# Let's verify paren balance at start
assert text.count('(') == text.count(')'), "Unbalanced parens at start"

# 1. Update Symbols
# We will do targeted replacements for each symbol block.

# R3:
old_r3_start = text.find('(property "Reference" "R3"')
old_r3_sym_start = text.rfind('(symbol', 0, old_r3_start)
# find end of symbol
p_cnt = 0
for i in range(old_r3_sym_start, len(text)):
    if text[i] == '(': p_cnt += 1
    elif text[i] == ')':
        p_cnt -= 1
        if p_cnt == 0:
            old_r3_sym_end = i + 1
            break
old_r3_block = text[old_r3_sym_start:old_r3_sym_end]

# New R3 block:
# at (200.66, 118.11, 0)
# Ref at (203.20, 116.84)
# Val at (203.20, 119.38)
new_r3_block = re.sub(r'\(at\s+[0-9\.\-]+\s+[0-9\.\-]+(?:\s+[0-9\.\-]+)?\)', '(at 200.66 118.11 0)', old_r3_block, count=1)
new_r3_block = re.sub(r'\(property "Reference" "R3"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', '(property "Reference" "R3" (at 203.20 116.84 0)', new_r3_block)
new_r3_block = re.sub(r'\(property "Value" "10k"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', '(property "Value" "10k" (at 203.20 119.38 0)', new_r3_block)

# C2:
old_c2_start = text.find('(property "Reference" "C2"')
old_c2_sym_start = text.rfind('(symbol', 0, old_c2_start)
p_cnt = 0
for i in range(old_c2_sym_start, len(text)):
    if text[i] == '(': p_cnt += 1
    elif text[i] == ')':
        p_cnt -= 1
        if p_cnt == 0:
            old_c2_sym_end = i + 1
            break
old_c2_block = text[old_c2_sym_start:old_c2_sym_end]

# New C2 block:
# at (200.66, 130.81, 0)
# Ref at (203.20, 129.54)
# Val at (203.20, 132.08)
new_c2_block = re.sub(r'\(at\s+[0-9\.\-]+\s+[0-9\.\-]+(?:\s+[0-9\.\-]+)?\)', '(at 200.66 130.81 0)', old_c2_block, count=1)
new_c2_block = re.sub(r'\(property "Reference" "C2"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', '(property "Reference" "C2" (at 203.20 129.54 0)', new_c2_block)
new_c2_block = re.sub(r'\(property "Value" "100nF"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', '(property "Value" "100nF" (at 203.20 132.08 0)', new_c2_block)

# SW1:
old_sw1_start = text.find('(property "Reference" "SW1"')
old_sw1_sym_start = text.rfind('(symbol', 0, old_sw1_start)
p_cnt = 0
for i in range(old_sw1_sym_start, len(text)):
    if text[i] == '(': p_cnt += 1
    elif text[i] == ')':
        p_cnt -= 1
        if p_cnt == 0:
            old_sw1_sym_end = i + 1
            break
old_sw1_block = text[old_sw1_sym_start:old_sw1_sym_end]

# New SW1 block:
# at (210.82, 124.46, 0)
# Ref at (210.82, 120.65)
# Val at (210.82, 128.27)
new_sw1_block = re.sub(r'\(at\s+[0-9\.\-]+\s+[0-9\.\-]+(?:\s+[0-9\.\-]+)?\)', '(at 210.82 124.46 0)', old_sw1_block, count=1)
new_sw1_block = re.sub(r'\(property "Reference" "SW1"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', '(property "Reference" "SW1" (at 210.82 120.65 0)', new_sw1_block)
new_sw1_block = re.sub(r'\(property "Value" "CANCEL"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', '(property "Value" "CANCEL" (at 210.82 128.27 0)', new_sw1_block)

# R4:
old_r4_start = text.find('(property "Reference" "R4"')
old_r4_sym_start = text.rfind('(symbol', 0, old_r4_start)
p_cnt = 0
for i in range(old_r4_sym_start, len(text)):
    if text[i] == '(': p_cnt += 1
    elif text[i] == ')':
        p_cnt -= 1
        if p_cnt == 0:
            old_r4_sym_end = i + 1
            break
old_r4_block = text[old_r4_sym_start:old_r4_sym_end]

# New R4 block:
# at (227.33, 142.24, 90)
# Ref at (227.33, 138.43, 90)
# Val at (227.33, 146.05, 90)
new_r4_block = re.sub(r'\(at\s+[0-9\.\-]+\s+[0-9\.\-]+(?:\s+[0-9\.\-]+)?\)', '(at 227.33 142.24 90)', old_r4_block, count=1)
new_r4_block = re.sub(r'\(property "Reference" "R4"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', '(property "Reference" "R4" (at 227.33 138.43 90)', new_r4_block)
new_r4_block = re.sub(r'\(property "Value" "330R"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', '(property "Value" "330R" (at 227.33 146.05 90)', new_r4_block)

# D1:
old_d1_start = text.find('(property "Reference" "D1"')
old_d1_sym_start = text.rfind('(symbol', 0, old_d1_start)
p_cnt = 0
for i in range(old_d1_sym_start, len(text)):
    if text[i] == '(': p_cnt += 1
    elif text[i] == ')':
        p_cnt -= 1
        if p_cnt == 0:
            old_d1_sym_end = i + 1
            break
old_d1_block = text[old_d1_sym_start:old_d1_sym_end]

# New D1 block:
# at (237.49, 142.24, 180)
# Ref at (237.49, 138.43, 0)
# Val at (237.49, 146.05, 0)
new_d1_block = re.sub(r'\(at\s+[0-9\.\-]+\s+[0-9\.\-]+(?:\s+[0-9\.\-]+)?\)', '(at 237.49 142.24 180)', old_d1_block, count=1)
new_d1_block = re.sub(r'\(property "Reference" "D1"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', '(property "Reference" "D1" (at 237.49 138.43 0)', new_d1_block)
new_d1_block = re.sub(r'\(property "Value" "LED"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', '(property "Value" "LED" (at 237.49 146.05 0)', new_d1_block)

# R5:
old_r5_start = text.find('(property "Reference" "R5"')
old_r5_sym_start = text.rfind('(symbol', 0, old_r5_start)
p_cnt = 0
for i in range(old_r5_sym_start, len(text)):
    if text[i] == '(': p_cnt += 1
    elif text[i] == ')':
        p_cnt -= 1
        if p_cnt == 0:
            old_r5_sym_end = i + 1
            break
old_r5_block = text[old_r5_sym_start:old_r5_sym_end]

# New R5 block:
# at (255.27, 154.94, 90)
# Ref at (255.27, 151.13, 90)
# Val at (255.27, 158.75, 90)
new_r5_block = re.sub(r'\(at\s+[0-9\.\-]+\s+[0-9\.\-]+(?:\s+[0-9\.\-]+)?\)', '(at 255.27 154.94 90)', old_r5_block, count=1)
new_r5_block = re.sub(r'\(property "Reference" "R5"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', '(property "Reference" "R5" (at 255.27 151.13 90)', new_r5_block)
new_r5_block = re.sub(r'\(property "Value" "1k"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', '(property "Value" "1k" (at 255.27 158.75 90)', new_r5_block)

# Q1:
old_q1_start = text.find('(property "Reference" "Q1"')
old_q1_sym_start = text.rfind('(symbol', 0, old_q1_start)
p_cnt = 0
for i in range(old_q1_sym_start, len(text)):
    if text[i] == '(': p_cnt += 1
    elif text[i] == ')':
        p_cnt -= 1
        if p_cnt == 0:
            old_q1_sym_end = i + 1
            break
old_q1_block = text[old_q1_sym_start:old_q1_sym_end]

# New Q1 block:
# at (266.70, 154.94, 0)
# Ref at (272.50, 152.40, 0)
# Val at (272.50, 156.50, 0)
new_q1_block = re.sub(r'\(at\s+[0-9\.\-]+\s+[0-9\.\-]+(?:\s+[0-9\.\-]+)?\)', '(at 266.7 154.94 0)', old_q1_block, count=1)
new_q1_block = re.sub(r'\(property "Reference" "Q1"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', '(property "Reference" "Q1" (at 272.50 152.40 0)', new_q1_block)
new_q1_block = re.sub(r'\(property "Value" "2SC1815"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', '(property "Value" "2SC1815" (at 272.50 156.50 0)', new_q1_block)

# BZ1:
old_bz1_start = text.find('(property "Reference" "BZ1"')
old_bz1_sym_start = text.rfind('(symbol', 0, old_bz1_start)
p_cnt = 0
for i in range(old_bz1_sym_start, len(text)):
    if text[i] == '(': p_cnt += 1
    elif text[i] == ')':
        p_cnt -= 1
        if p_cnt == 0:
            old_bz1_sym_end = i + 1
            break
old_bz1_block = text[old_bz1_sym_start:old_bz1_sym_end]

# New BZ1 block:
# at (271.78, 147.32, 0)
# Ref at (278.00, 144.78, 0)
# Val at (278.00, 149.86, 0)
new_bz1_block = re.sub(r'\(at\s+[0-9\.\-]+\s+[0-9\.\-]+(?:\s+[0-9\.\-]+)?\)', '(at 271.78 147.32 0)', old_bz1_block, count=1)
new_bz1_block = re.sub(r'\(property "Reference" "BZ1"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', '(property "Reference" "BZ1" (at 278.00 144.78 0)', new_bz1_block)
new_bz1_block = re.sub(r'\(property "Value" "BUZZER"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', '(property "Value" "BUZZER" (at 278.00 149.86 0)', new_bz1_block)

# Power symbols:
# +3V3_UI: currently at 195.58, 124.46
# move to: (200.66, 111.76, 0)
# Val at (200.66, 107.95, 0)
old_pwr3v3_pos = text.find('(at 195.58 124.46 0)')
old_pwr3v3_start = text.rfind('(symbol', 0, old_pwr3v3_pos)
p_cnt = 0
for i in range(old_pwr3v3_start, len(text)):
    if text[i] == '(': p_cnt += 1
    elif text[i] == ')':
        p_cnt -= 1
        if p_cnt == 0:
            old_pwr3v3_end = i + 1
            break
old_pwr3v3_block = text[old_pwr3v3_start:old_pwr3v3_end]
new_pwr3v3_block = re.sub(r'\(at\s+195\.58\s+124\.46\s+0\)', '(at 200.66 111.76 0)', old_pwr3v3_block)
new_pwr3v3_block = re.sub(r'\(property "Value" "\+3V3"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', '(property "Value" "+3V3" (at 200.66 107.95 0)', new_pwr3v3_block)

# 5V_SYS_UI: currently at 269.24, 121.92
# move to: (269.24, 139.70, 0)
# Val at (269.24, 135.89, 0)
old_pwr5v_pos = text.find('(at 269.24 121.92 0)')
old_pwr5v_start = text.rfind('(symbol', 0, old_pwr5v_pos)
p_cnt = 0
for i in range(old_pwr5v_start, len(text)):
    if text[i] == '(': p_cnt += 1
    elif text[i] == ')':
        p_cnt -= 1
        if p_cnt == 0:
            old_pwr5v_end = i + 1
            break
old_pwr5v_block = text[old_pwr5v_start:old_pwr5v_end]
new_pwr5v_block = re.sub(r'\(at\s+269\.24\s+121\.92\s+0\)', '(at 269.24 139.70 0)', old_pwr5v_block)
new_pwr5v_block = re.sub(r'\(property "Value" "5V_SYS"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', '(property "Value" "5V_SYS" (at 269.24 135.89 0)', new_pwr5v_block)

# GND_C2: currently at (195.58, 149.86)
# move to: (200.66, 137.16, 0)
# Val at (200.66, 140.97, 0)
old_gndc2_pos = text.find('(at 195.58 149.86 0)')
old_gndc2_start = text.rfind('(symbol', 0, old_gndc2_pos)
p_cnt = 0
for i in range(old_gndc2_start, len(text)):
    if text[i] == '(': p_cnt += 1
    elif text[i] == ')':
        p_cnt -= 1
        if p_cnt == 0:
            old_gndc2_end = i + 1
            break
old_gndc2_block = text[old_gndc2_start:old_gndc2_end]
new_gndc2_block = re.sub(r'\(at\s+195\.58\s+149\.86\s+0\)', '(at 200.66 137.16 0)', old_gndc2_block)
new_gndc2_block = re.sub(r'\(property "Value" "GND"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', '(property "Value" "GND" (at 200.66 140.97 0)', new_gndc2_block)

# GND_SW1: currently at (213.36, 149.86)
# move to: (218.44, 129.54, 0)
# Val at (218.44, 133.35, 0)
old_gndsw1_pos = text.find('(at 213.36 149.86 0)')
old_gndsw1_start = text.rfind('(symbol', 0, old_gndsw1_pos)
p_cnt = 0
for i in range(old_gndsw1_start, len(text)):
    if text[i] == '(': p_cnt += 1
    elif text[i] == ')':
        p_cnt -= 1
        if p_cnt == 0:
            old_gndsw1_end = i + 1
            break
old_gndsw1_block = text[old_gndsw1_start:old_gndsw1_end]
new_gndsw1_block = re.sub(r'\(at\s+213\.36\s+149\.86\s+0\)', '(at 218.44 129.54 0)', old_gndsw1_block)
new_gndsw1_block = re.sub(r'\(property "Value" "GND"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', '(property "Value" "GND" (at 218.44 133.35 0)', new_gndsw1_block)

# GND_D1: currently at (243.84, 143.51)
# move to: (243.84, 147.32, 0)
# Val at (243.84, 151.13, 0)
old_gndd1_pos = text.find('(at 243.84 143.51 0)')
old_gndd1_start = text.rfind('(symbol', 0, old_gndd1_pos)
p_cnt = 0
for i in range(old_gndd1_start, len(text)):
    if text[i] == '(': p_cnt += 1
    elif text[i] == ')':
        p_cnt -= 1
        if p_cnt == 0:
            old_gndd1_end = i + 1
            break
old_gndd1_block = text[old_gndd1_start:old_gndd1_end]
new_gndd1_block = re.sub(r'\(at\s+243\.84\s+143\.51\s+0\)', '(at 243.84 147.32 0)', old_gndd1_block)
new_gndd1_block = re.sub(r'\(property "Value" "GND"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', '(property "Value" "GND" (at 243.84 151.13 0)', new_gndd1_block)

# GND_Q1: currently at (269.24, 147.32)
# move to: (269.24, 162.56, 0)
# Val at (269.24, 166.37, 0)
old_gndq1_pos = text.find('(at 269.24 147.32 0)')
old_gndq1_start = text.rfind('(symbol', 0, old_gndq1_pos)
p_cnt = 0
for i in range(old_gndq1_start, len(text)):
    if text[i] == '(': p_cnt += 1
    elif text[i] == ')':
        p_cnt -= 1
        if p_cnt == 0:
            old_gndq1_end = i + 1
            break
old_gndq1_block = text[old_gndq1_start:old_gndq1_end]
new_gndq1_block = re.sub(r'\(at\s+269\.24\s+147\.32\s+0\)', '(at 269.24 162.56 0)', old_gndq1_block)
new_gndq1_block = re.sub(r'\(property "Value" "GND"\s+\(at\s+[0-9\.\-]+\s+[0-9\.\-]+[^\)]*\)', '(property "Value" "GND" (at 269.24 166.37 0)', new_gndq1_block)

# Apply all symbol block replacements:
replacements = [
    (old_r3_block, new_r3_block),
    (old_c2_block, new_c2_block),
    (old_sw1_block, new_sw1_block),
    (old_r4_block, new_r4_block),
    (old_d1_block, new_d1_block),
    (old_r5_block, new_r5_block),
    (old_q1_block, new_q1_block),
    (old_bz1_block, new_bz1_block),
    (old_pwr3v3_block, new_pwr3v3_block),
    (old_pwr5v_block, new_pwr5v_block),
    (old_gndc2_block, new_gndc2_block),
    (old_gndsw1_block, new_gndsw1_block),
    (old_gndd1_block, new_gndd1_block),
    (old_gndq1_block, new_gndq1_block),
]

for old_b, new_b in replacements:
    assert old_b in text, f"Failed to find old block for replacement"
    text = text.replace(old_b, new_b)

# UI Title text: move to (245 118 0)
old_ui_title = '(text "KHỐI CẢNH BÁO & NÚT BẤM (UI)"\n\t\t(exclude_from_sim no)\n\t\t(at 248 156 0)'
new_ui_title = '(text "KHỐI CẢNH BÁO & NÚT BẤM (UI)"\n\t\t(exclude_from_sim no)\n\t\t(at 245 118 0)'
assert old_ui_title in text, "Failed to find old UI title"
text = text.replace(old_ui_title, new_ui_title)

# Now remove the 24 old UI wires:
# We will find each wire by its coordinates
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
removed_wires = 0
for st, en, w in wire_sexprs:
    m = re.search(r'\(xy\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)\s+\(xy\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)', w)
    if m:
        x1, y1, x2, y2 = float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4))
        for ox1, oy1, ox2, oy2 in old_wires_coords:
            if (abs(x1 - ox1) < 0.05 and abs(y1 - oy1) < 0.05 and abs(x2 - ox2) < 0.05 and abs(y2 - oy2) < 0.05) or \
               (abs(x1 - ox2) < 0.05 and abs(y1 - oy2) < 0.05 and abs(x2 - ox1) < 0.05 and abs(y2 - oy1) < 0.05):
                text = text.replace(w, "")
                removed_wires += 1
                break

print(f"Removed {removed_wires} old wires.")

# Remove old junction at (195.58, 137.16)
old_junc_pattern = r'\(junction\s+\(at\s+195\.58\s+137\.16\)\s+\(diameter\s+0\)\s+\(color\s+0\s+0\s+0\s+0\)\s+\(uuid\s+"[^"]+"\)\)'
m_junc = re.search(old_junc_pattern, text)
if m_junc:
    text = text.replace(m_junc.group(0), "")
    print("Removed old junction at (195.58, 137.16)")

# Now generate UUIDs for new wires and junction
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
    # Lane 2: (175.26, 114.30) -> (187.96, 114.30) -> (187.96, 142.24) -> (223.52, 142.24)
    make_wire(175.26, 114.30, 187.96, 114.30),
    make_wire(187.96, 114.30, 187.96, 142.24),
    make_wire(187.96, 142.24, 223.52, 142.24),
    # R4 to D1: (231.14, 142.24) -> (233.68, 142.24)
    make_wire(231.14, 142.24, 233.68, 142.24),
    # D1 to GND: (241.30, 142.24) -> (243.84, 142.24) -> (243.84, 147.32)
    make_wire(241.30, 142.24, 243.84, 142.24),
    make_wire(243.84, 142.24, 243.84, 147.32),

    # --- ROW 3 (BUZZER, GPIO15) ---
    # Lane 3: (175.26, 119.38) -> (182.88, 119.38) -> (182.88, 154.94) -> (251.46, 154.94)
    make_wire(175.26, 119.38, 182.88, 119.38),
    make_wire(182.88, 119.38, 182.88, 154.94),
    make_wire(182.88, 154.94, 251.46, 154.94),
    # R5 to Q1 Base: (259.08, 154.94) -> (261.62, 154.94)
    make_wire(259.08, 154.94, 261.62, 154.94),
    # Q1 Emitter to GND: (269.24, 160.02) -> (269.24, 162.56)
    make_wire(269.24, 160.02, 269.24, 162.56),
    # BZ1 Pin 1 (+) to 5V_SYS: (269.24, 144.78) -> (269.24, 139.70)
    make_wire(269.24, 144.78, 269.24, 139.70),
]

new_junc = make_junction(200.66, 124.46)

# Insert new wires and junction before the closing paren of schematic
insert_idx = text.rfind(')')
new_elements_str = "\n" + new_junc + "\n" + "\n".join(new_wires) + "\n"
text = text[:insert_idx] + new_elements_str + text[insert_idx:]

assert text.count('(') == text.count(')'), "Unbalanced parens after modification"

with open(SCH_PATH, 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved candidate schematic in scratch_rev5. Running ERC...")
cmd = ['D:\\Kicad\\bin\\kicad-cli.exe', 'sch', 'erc', '--severity-all', '--format', 'json', SCH_PATH]
res = subprocess.run(cmd, capture_output=True, text=True)
print("ERC Return code:", res.returncode)
print("ERC Stdout:\n", res.stdout)
if res.stderr:
    print("ERC Stderr:\n", res.stderr)
