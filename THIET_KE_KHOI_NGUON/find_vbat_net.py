import re

with open('02_CHARGER_BATTERY.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

wires = re.findall(r'\(wire\s+\(pts\s+\(xy\s+([\d\.\-]+)\s+([\d\.\-]+)\)\s+\(xy\s+([\d\.\-]+)\s+([\d\.\-]+)\)\)', text)
wires = [(float(x1), float(y1), float(x2), float(y2)) for x1, y1, x2, y2 in wires]

adj = {}
for x1, y1, x2, y2 in wires:
    p1 = (round(x1, 2), round(y1, 2))
    p2 = (round(x2, 2), round(y2, 2))
    adj.setdefault(p1, []).append(p2)
    adj.setdefault(p2, []).append(p1)

start = (287.02, 96.52)
visited = set([start])
queue = [start]
while queue:
    curr = queue.pop(0)
    for nxt in adj.get(curr, []):
        if nxt not in visited:
            visited.add(nxt)
            queue.append(nxt)

print(f"VBAT net has {len(visited)} wire points.")

# Find all power GND symbols
gnds = re.findall(r'\(symbol\s+\(lib_id\s+"power:GND"\)\s+\(at\s+([\d\.\-]+)\s+([\d\.\-]+)', text)
for gx, gy in gnds:
    gp = (round(float(gx), 2), round(float(gy), 2))
    if gp in visited:
        print("GND symbol at", gp, "is on VBAT net!")

# Also let's print all points in visited that have Y >= 60
print("\nSome points on VBAT net:")
for p in sorted(visited):
    if p[1] > 60:
        print(" ", p)
