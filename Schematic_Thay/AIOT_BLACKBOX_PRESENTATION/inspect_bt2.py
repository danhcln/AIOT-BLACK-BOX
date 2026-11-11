import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'\(symbol\s+\(lib_id "Device:Battery_Cell"\)[\s\S]*?\(property "Reference" "BT2"[\s\S]*?\n\t\)', text)
if m:
    print(m.group(0))
