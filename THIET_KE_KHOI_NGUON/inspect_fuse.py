# -*- coding: utf-8 -*-
import os, re
sym_dir = r"D:\KiCad\share\kicad\symbols"
with open(os.path.join(sym_dir, "Device.kicad_sym"), 'r', encoding='utf-8') as f:
    dev = f.read()
print("Fuse matches:", [m for m in re.findall(r'\(symbol\s+"([^"]+)"', dev) if "Fuse" in m])
print("Jumper matches:", [m for m in re.findall(r'\(symbol\s+"([^"]+)"', dev) if "Jumper" in m])
