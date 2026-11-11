import re

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

# Find lib_symbols
lib_symbols = re.findall(r'\(symbol "([^"]+)"([\s\S]*?)\n\t\t\)', text)
print(f"Total lib_symbols defined: {len(lib_symbols)}")
for name, body in lib_symbols:
    # find pins
    pins = re.findall(r'\(pin\s+([^\s]+)\s+([^\s]+)\s+\(at\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\)\s+\(length\s+([-\d.]+)\)[\s\S]*?\(name\s+"([^"]*)"[\s\S]*?\(number\s+"([^"]*)"', body)
    print(f"\n--- Symbol: {name} ({len(pins)} pins) ---")
    for p in pins:
        print(f"  Pin {p[7]:<4} name={p[6]:<16} type={p[0]:<12} shape={p[1]:<10} at ({p[2]}, {p[3]}) rot={p[4]}")
