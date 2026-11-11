# -*- coding: utf-8 -*-
import re

with open("02_CHARGER_BATTERY.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

wires = re.findall(r'\(wire\s+\(pts\s+\(xy\s+([\d\.\-]+)\s+([\d\.\-]+)\)\s+\(xy\s+([\d\.\-]+)\s+([\d\.\-]+)\)\)', text)
wires = [(float(x1), float(y1), float(x2), float(y2)) for x1, y1, x2, y2 in wires]

# Build adjacency
adj = {}
for x1, y1, x2, y2 in wires:
    p1 = (round(x1, 2), round(y1, 2))
    p2 = (round(x2, 2), round(y2, 2))
    adj.setdefault(p1, []).append((p2, (x1, y1, x2, y2)))
    adj.setdefault(p2, []).append((p1, (x1, y1, x2, y2)))

# Find path from (213.36, 78.74) [SYS] to (213.36, 83.82) [BAT]
start = (213.36, 78.74)
target = (213.36, 83.82)

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

print("Path from SYS to BAT:")
if path_found:
    for p in path_found:
        print(" ->", p)
else:
    print("No direct graph path! (Maybe through an overlapping vertical/horizontal line?)")
    # Check if any horizontal wire overlaps a vertical wire
    for x1, y1, x2, y2 in wires:
        # if vertical
        if abs(x1 - x2) < 0.001:
            ymin, ymax = min(y1, y2), max(y1, y2)
            xv = x1
            for hx1, hy1, hx2, hy2 in wires:
                if abs(hy1 - hy2) < 0.001:
                    hxmin, hxmax = min(hx1, hx2), max(hx1, hx2)
                    yv = hy1
                    if hxmin < xv < hxmax and ymin < yv < ymax:
                        print(f"Intersection without vertex: Vertical at X={xv} (Y={ymin}..{ymax}) crosses Horizontal at Y={yv} (X={hxmin}..{hxmax})")
