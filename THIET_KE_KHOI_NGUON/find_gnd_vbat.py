# -*- coding: utf-8 -*-
import re

with open("02_CHARGER_BATTERY.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

# Find all wires
wires = re.findall(r'\(wire\s+\(pts\s+\(xy\s+([\d\.\-]+)\s+([\d\.\-]+)\)\s+\(xy\s+([\d\.\-]+)\s+([\d\.\-]+)\)\)', text)
wires = [(float(x1), float(y1), float(x2), float(y2)) for x1, y1, x2, y2 in wires]

# Build graph
adj = {}
for x1, y1, x2, y2 in wires:
    p1 = (round(x1, 2), round(y1, 2))
    p2 = (round(x2, 2), round(y2, 2))
    adj.setdefault(p1, []).append((p2, (x1, y1, x2, y2)))
    adj.setdefault(p2, []).append((p1, (x1, y1, x2, y2)))

# Find path from (81.28, 66.04) [GND at R18] to (279.40, 96.52) [VBAT label]
start = (81.28, 66.04)
target = (279.40, 96.52)

queue = [[start]]
visited = set([start])
path_found = None
while queue:
    path = queue.pop(0)
    curr = path[-1]
    if curr == target:
        path_found = path
        break
    for nxt, seg in adj.get(curr, []):
        if nxt not in visited:
            visited.add(nxt)
            queue.append(path + [nxt])

print("Path from GND(81.28, 66.04) to VBAT(279.40, 96.52):")
if path_found:
    for p in path_found:
        print(" ->", p)
else:
    print("NO DIRECT PATH via wire vertices! Checking overlap...")
    for x1, y1, x2, y2 in wires:
        # vertical
        if abs(x1 - x2) < 0.001:
            ymin, ymax = min(y1, y2), max(y1, y2)
            for hx1, hy1, hx2, hy2 in wires:
                if abs(hy1 - hy2) < 0.001:
                    hxmin, hxmax = min(hx1, hx2), max(hx1, hx2)
                    if hxmin <= x1 <= hxmax and ymin <= hy1 <= ymax:
                        # check if endpoints match
                        if not ((round(x1,2), round(hy1,2)) in [(round(hx1,2), round(hy1,2)), (round(hx2,2), round(hy2,2)), (round(x1,2), round(y1,2)), (round(x1,2), round(y2,2))]):
                            print(f"OVERLAP: Vertical X={x1} (Y={ymin}..{ymax}) intersects Horizontal Y={hy1} (X={hxmin}..{hxmax}) at ({x1}, {hy1})")
