import re, os, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
from sexpr_util import extract_sexprs

SCH_PATH = os.path.join('scratch_rev5', 'AIOT_BLACKBOX_PRESENTATION.kicad_sch')
with open(SCH_PATH, 'r', encoding='utf-8') as f:
    text = f.read()

# Let's define the new coordinates:
# Row 1: CANCEL at y = 124.46
# Row 2: STATUS LED at y = 142.24
# Row 3: BUZZER at y = 154.94

# Symbols to update:
# 1. R3: at (200.66, 118.11, rot=0)
#    Pin 1 (top): (200.66, 114.30) -> wire to +3V3 at (200.66, 111.76)
#    Pin 2 (bottom): (200.66, 121.92) -> wire to node at (200.66, 124.46)
#    Ref at (203.20, 116.84), Val at (203.20, 119.38)
# 2. +3V3_UI: at (200.66, 111.76, rot=0) (power:+3V3)
#    Ref hide, Val at (200.66, 107.95)
# 3. C2: at (200.66, 130.81, rot=0)
#    Pin 1 (top): (200.66, 127.00) -> wire from node at (200.66, 124.46)
#    Pin 2 (bottom): (200.66, 134.62) -> wire to GND at (200.66, 137.16)
#    Ref at (203.20, 129.54), Val at (203.20, 132.08)
# 4. GND_C2: at (200.66, 137.16, rot=0) (power:GND)
#    Ref hide, Val at (200.66, 140.97)
# 5. SW1: at (210.82, 124.46, rot=0)
#    Pin 1: (205.74, 124.46) -> wire from node at (200.66, 124.46)
#    Pin 2: (215.90, 124.46) -> wire to (218.44, 124.46) -> (218.44, 129.54)
#    Ref at (210.82, 120.65), Val at (210.82, 128.27)
# 6. GND_SW1: at (218.44, 129.54, rot=0) (power:GND)
#    Ref hide, Val at (218.44, 133.35)

# Row 2 (STATUS LED):
# 7. R4: at (227.33, 142.24, rot=90)
#    Pin 1 (left): (223.52, 142.24)
#    Pin 2 (right): (231.14, 142.24)
#    Ref at (227.33, 138.43, rot=90), Val at (227.33, 146.05, rot=90)
# 8. D1: at (237.49, 142.24, rot=180)
#    Pin 2 (Anode, left): (233.68, 142.24) -> wire from R4 (231.14, 142.24)
#    Pin 1 (Cathode, right): (241.30, 142.24) -> wire to (243.84, 142.24) -> (243.84, 147.32)
#    Ref at (237.49, 138.43, rot=0), Val at (237.49, 146.05, rot=0)
# 9. GND_D1: at (243.84, 147.32, rot=0) (power:GND)
#    Ref hide, Val at (243.84, 151.13)

# Row 3 (BUZZER):
# 10. R5: at (255.27, 154.94, rot=90)
#     Pin 1 (left): (251.46, 154.94)
#     Pin 2 (right): (259.08, 154.94)
#     Ref at (255.27, 151.13, rot=90), Val at (255.27, 158.75, rot=90)
# 11. Q1: at (266.70, 154.94, rot=0)
#     Base (Pin 3): (261.62, 154.94) -> wire from R5 (259.08, 154.94)
#     Collector (Pin 2): (269.24, 149.86)
#     Emitter (Pin 1): (269.24, 160.02) -> wire to (269.24, 162.56)
#     Ref at (272.50, 152.40), Val at (272.50, 156.50)
# 12. GND_Q1: at (269.24, 162.56, rot=0) (power:GND)
#     Ref hide, Val at (269.24, 166.37)
# 13. BZ1: at (271.78, 147.32, rot=0)
#     Pin 2 (-): (269.24, 149.86) -> connects to Collector
#     Pin 1 (+): (269.24, 144.78) -> wire to (269.24, 139.70)
#     Ref at (278.00, 144.78), Val at (278.00, 149.86)
# 14. 5V_SYS_UI: at (269.24, 139.70, rot=0) (power:5V_SYS)
#     Ref hide, Val at (269.24, 135.89)

# 15. UI Block Title text:
#     text "KHỐI CẢNH BÁO & NÚT BẤM (UI)" at (240 118 0) or (230 164 0)

print("Coordinate mapping prepared.")
