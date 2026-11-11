import os, re

p = r"D:\KiCad\share\kicad\symbols\Device.kicad_sym"
with open(p, 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'\(symbol\s+\"(Q_P[^\"]*)\"', text)
print("Device PMOS matches:", matches)

p2 = r"D:\KiCad\share\kicad\symbols\Transistor_FET.kicad_sym"
if os.path.exists(p2):
    with open(p2, 'r', encoding='utf-8') as f:
        text2 = f.read()
    all_fets = re.findall(r'\(symbol\s+\"([^\"]+)\"', text2)
    pmos = [f for f in all_fets if any(k in f for k in ['AO3401', 'SI2301', 'BSS84', 'TP0610', 'DMP'])]
    print("Transistor_FET PMOS matches:", pmos[:15])
