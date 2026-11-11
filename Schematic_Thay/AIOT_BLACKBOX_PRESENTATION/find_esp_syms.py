import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'D:\KiCad\share\kicad\symbols\MCU_Espressif.kicad_sym', 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()

symbols = re.findall(r'\(symbol\s+"([^"]+)"', c)
for s in symbols:
    if 's3' in s.lower() or 'devkit' in s.lower():
        print(s)
