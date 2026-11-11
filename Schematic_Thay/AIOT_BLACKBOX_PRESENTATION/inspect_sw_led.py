import os
import re

kicad_sym_dir = r"D:\Kicad\share\kicad\symbols"
with open(os.path.join(kicad_sym_dir, "Switch.kicad_sym"), 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'\(symbol "SW_Push".*?\n\t\)', text, re.DOTALL)
if m:
    print("=== SW_Push ===")
    for line in m.group(0).splitlines():
        if '(pin ' in line or '(at ' in line:
            print(line.strip())

with open(os.path.join(kicad_sym_dir, "Device.kicad_sym"), 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'\(symbol "LED".*?\n\t\)', text, re.DOTALL)
if m:
    print("=== LED ===")
    for line in m.group(0).splitlines():
        if '(pin ' in line or '(at ' in line:
            print(line.strip())
