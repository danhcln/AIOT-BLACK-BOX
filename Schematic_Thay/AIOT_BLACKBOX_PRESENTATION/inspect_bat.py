import os
import re

kicad_sym_dir = r"D:\Kicad\share\kicad\symbols"
with open(os.path.join(kicad_sym_dir, "Device.kicad_sym"), 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'\(symbol "Battery_Cell".*?\n\t\)', text, re.DOTALL)
if m:
    print(m.group(0))

with open(os.path.join(kicad_sym_dir, "Device.kicad_sym"), 'r', encoding='utf-8') as f:
    for line in text.splitlines():
        if 'Antenna' in line or 'Buzzer' in line:
            print(line[:80])
