import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

# U2 is at (53.34, 93.98)
# Find U2 lib symbol definition
m = re.search(r'\(symbol "Presentation:MPU6050_Module"[\s\S]*?\n\t\t\)', text)
if m:
    print(m.group(0))

# Find wires near U2 (x in [30, 80], y in [80, 115])
wires = re.findall(r'\(wire\s+\(pts\s+\(xy\s+([-\d.]+)\s+([-\d.]+)\)\s+\(xy\s+([-\d.]+)\s+([-\d.]+)\)\s*\)', text)
print("\n--- Wires near U2 ---")
for w in wires:
    x1, y1, x2, y2 = float(w[0]), float(w[1]), float(w[2]), float(w[3])
    if (30 <= x1 <= 80 and 80 <= y1 <= 115) or (30 <= x2 <= 80 and 80 <= y2 <= 115):
        print(f"  Wire ({x1:6.2f}, {y1:6.2f}) -> ({x2:6.2f}, {y2:6.2f})")
