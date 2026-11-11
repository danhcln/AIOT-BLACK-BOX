import re, sys
sys.stdout.reconfigure(encoding='utf-8')

# Let's inspect the font size of pin names and pin numbers in the current U1 symbol
with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'\(symbol "Presentation:ESP32-S3-DevKitC-1"[\s\S]*?\n\t\t\)', text)
if m:
    lib_body = m.group(0)
    # Check pin text effects
    pin_effects = re.findall(r'\(effects[\s\S]*?\(font[\s\S]*?\(size\s+([-\d.]+)\s+([-\d.]+)\)', lib_body)
    print("Pin effects fonts in U1:", set(pin_effects))
    # Check pin_names offset
    p_offset = re.findall(r'\(pin_names[\s\S]*?\(offset\s+([-\d.]+)\)', lib_body)
    print("Pin names offset:", p_offset)
