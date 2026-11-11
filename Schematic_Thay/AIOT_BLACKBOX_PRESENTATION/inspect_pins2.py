import os
import re

kicad_sym_dir = r"D:\Kicad\share\kicad\symbols"
with open(os.path.join(kicad_sym_dir, "Device.kicad_sym"), 'r', encoding='utf-8') as f:
    text = f.read()

for sym in ["R", "C", "Antenna", "Buzzer"]:
    m = re.search(rf'\(symbol "{sym}".*?\n\t\)', text, re.DOTALL)
    if m:
        print(f"=== {sym} ===")
        in_pin = False
        for line in m.group(0).splitlines():
            if '(pin ' in line:
                in_pin = True
            if in_pin:
                print(line)
                if line.strip().startswith(')'):
                    in_pin = False
