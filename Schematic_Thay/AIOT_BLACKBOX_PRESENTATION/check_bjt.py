import os
import re

kicad_sym_dir = r"D:\Kicad\share\kicad\symbols"
with open(os.path.join(kicad_sym_dir, "Transistor_BJT.kicad_sym"), 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'\(symbol "2SC1815".*?\n\t\)', text, re.DOTALL)
if m:
    print(m.group(0)[:500])
else:
    print("2SC1815 not directly found, looking for extends...")
    for line in text.splitlines():
        if '2SC1815' in line:
            print(line)
