import re
with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

from inspect_ui import extract_sexprs
texts = extract_sexprs(text, "(text")
for st, en, t in texts:
    if "CẢNH BÁO" in t:
        print("UI Block Text definition:")
        print(t)
