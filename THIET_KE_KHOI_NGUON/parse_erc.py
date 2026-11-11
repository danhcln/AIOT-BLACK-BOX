# -*- coding: utf-8 -*-
import sys, json

report_file = sys.argv[1] if len(sys.argv) > 1 else "erc_s2.json"
with open(report_file, 'r', encoding='utf-8') as f:
    d = json.load(f)

sheets = d.get('sheets', [])
total_v = 0
for s in sheets:
    sheet_name = s.get('name', 'unknown')
    v = s.get('violations', [])
    total_v += len(v)
    print(f"Sheet: {sheet_name} - Violations: {len(v)}")
    for item in v:
        desc = item.get('description', '')
        sev = item.get('severity', '')
        t = item.get('type', '')
        items = [it.get('description', '') for it in item.get('items', [])]
        print(f"  [{sev.upper()}] {t}: {desc} -> {items}")

if total_v == 0:
    print(f"ALL CLEAR: 0 violations in {report_file}!")
