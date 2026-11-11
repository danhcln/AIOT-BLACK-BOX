import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

# Find all symbol instances with their reference, value, position
# Pattern: (symbol (lib_id "...") (at X Y R) ... (property "Reference" "REF")
instances = re.findall(r'\(symbol\s+\(lib_id\s+"([^"]+)"\)\s+\(at\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\)[\s\S]*?\(property\s+"Reference"\s+"([^"]+)"[\s\S]*?\(property\s+"Value"\s+"([^"]+)"', text)

print(f"Total symbol instances: {len(instances)}")
print(f"{'Ref':<8} {'Value':<20} {'At (X, Y)':<18} {'Lib ID':<30}")
print("-" * 80)
for lib, x, y, rot, ref, val in sorted(instances, key=lambda i: (float(i[2]), float(i[1]))):
    print(f"{ref:<8} {val:<20} ({float(x):6.2f}, {float(y):6.2f})   {lib:<30}")
