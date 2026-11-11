import re, sys

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find wires connected to U1
# U1 position is at (152.4, 99.06)
# Let's find all wire endpoints
wires = re.findall(r'\(wire\s+\(pts\s+\(xy\s+([-\d.]+)\s+([-\d.]+)\)\s+\(xy\s+([-\d.]+)\s+([-\d.]+)\)\s*\)', text)
print(f"Total wires in schematic: {len(wires)}")

# Find all labels
labels = re.findall(r'\(label\s+"([^"]+)"\s+\(at\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\)', text)
print(f"Total labels: {len(labels)}")
for l in labels:
    print(f"  Label '{l[0]}' at ({l[1]}, {l[2]}) rot={l[3]}")

# Let's inspect pins of U1 in the instance
# Find symbol instance U1
m = re.search(r'\(symbol\s+\(lib_id "Presentation:ESP32-S3-DevKitC-1"\)[\s\S]*?\(property "Reference" "U1"[\s\S]*?\n\t\)', text)
if m:
    print("\nU1 instance found!")

# Let's find all pins and their coordinates for U1
# In lib_symbols:
m_lib = re.search(r'\(symbol "Presentation:ESP32-S3-DevKitC-1"[\s\S]*?\n\t\t\)', text)
if m_lib:
    lib_body = m_lib.group(0)
    pins = re.findall(r'\(pin\s+([^\s]+)\s+([^\s]+)\s+\(at\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\)\s+\(length\s+([-\d.]+)\)[\s\S]*?\(name\s+"([^"]*)"[\s\S]*?\(number\s+"([^"]*)"', lib_body)
    print(f"\nU1 lib pins ({len(pins)}):")
    u1_x, u1_y = 152.4, 99.06
    for p in pins:
        px, py = float(p[2]), float(p[3])
        # In KiCad S-expr: pin at (px, py) in symbol def.
        # When instance is at (u1_x, u1_y) with angle 0, absolute pin pos is (u1_x + px, u1_y - py)
        # because KiCad symbol def has Y pointing UP, while schematic has Y pointing DOWN!
        abs_x = round(u1_x + px, 4)
        abs_y = round(u1_y - py, 4)
        # Find wires connecting to (abs_x, abs_y)
        connected_wires = [w for w in wires if (round(float(w[0]), 2) == round(abs_x, 2) and round(float(w[1]), 2) == round(abs_y, 2)) or 
                                               (round(float(w[2]), 2) == round(abs_x, 2) and round(float(w[3]), 2) == round(abs_y, 2))]
        # Find labels at (abs_x, abs_y)
        conn_labels = [l for l in labels if round(float(l[1]), 2) == round(abs_x, 2) and round(float(l[2]), 2) == round(abs_y, 2)]
        print(f"  Pin {p[7]:<3} {p[6]:<12} at abs=({abs_x:6.2f}, {abs_y:6.2f}) -> {len(connected_wires)} wires, labels: {[l[0] for l in conn_labels]}")
