import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

# find all polylines
poly_matches = re.finditer(r'\(polyline\s*\(pts([\s\S]+?)\)\s*\(stroke([\s\S]+?)\)\s*\(uuid[^\)]+\)\)', text)
for i, m in enumerate(poly_matches):
    pts = re.findall(r'\(xy\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)', m.group(1))
    pts_f = [(float(x), float(y)) for x, y in pts]
    xs = [p[0] for p in pts_f]
    ys = [p[1] for p in pts_f]
    stroke = m.group(2).replace('\n', ' ')
    print(f"Polyline #{i}: x in [{min(xs):.2f}, {max(xs):.2f}], y in [{min(ys):.2f}, {max(ys):.2f}] | stroke: {stroke.strip()}")
