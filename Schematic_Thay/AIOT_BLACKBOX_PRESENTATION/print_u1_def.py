import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'\(symbol "Presentation:ESP32-S3-DevKitC-1"[\s\S]*?\n\t\t\)', text)
if m:
    print(m.group(0))
