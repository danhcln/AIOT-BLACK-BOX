import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

print("--- TEXTS in x:[100, 200], y >= 110 ---")
texts = re.findall(r'\(text\s+"([^"]+)"\s+\(at\s+([-\d.]+)\s+([-\d.]+)', text)
for t, x, y in texts:
    if 100 <= float(x) <= 200 and float(y) >= 110:
        print(f"  Text '{t}' at ({x}, {y})")

print("\n--- WIRES in x:[120, 185], y >= 120 ---")
wires = re.findall(r'\(wire\s+\(pts\s+\(xy\s+([-\d.]+)\s+([-\d.]+)\)\s+\(xy\s+([-\d.]+)\s+([-\d.]+)\)\s*\)', text)
for w in wires:
    x1, y1, x2, y2 = float(w[0]), float(w[1]), float(w[2]), float(w[3])
    if (120 <= x1 <= 185 and y1 >= 120) or (120 <= x2 <= 185 and y2 >= 120):
        print(f"  Wire ({x1:6.2f}, {y1:6.2f}) -> ({x2:6.2f}, {y2:6.2f})")

print("\n--- RECTANGLES / POLYLINES ---")
rects = re.findall(r'\(polyline[\s\S]*?\(pts\s+([^\)]+)\)[\s\S]*?\(stroke[\s\S]*?\(width\s+([-\d.]+)\)[\s\S]*?\(color\s+([-\d\s]+)\)', text)
for pts, w, col in rects:
    print(f"  Polyline width={w} color={col.strip()} pts={pts.strip()}")
