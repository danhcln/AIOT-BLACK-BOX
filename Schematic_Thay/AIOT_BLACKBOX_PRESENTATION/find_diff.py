with open("AIOT_BLACKBOX_PRESENTATION.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

import re
# Find each (symbol "..."
matches = list(re.finditer(r'\t\t\(symbol\s+"([^"]+)"', text))
for i, m in enumerate(matches):
    sym_name = m.group(1)
    start = m.start()
    end = matches[i+1].start() if i+1 < len(matches) else text.find('(polyline')
    chunk = text[start:end]
    bal = chunk.count('(') - chunk.count(')')
    if bal != 0:
        print(f"Unbalanced symbol: {sym_name} has balance {bal}")
