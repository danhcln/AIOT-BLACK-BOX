import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

erc_file = 'AIOT_BLACKBOX_PRESENTATION-erc.json'
with open(erc_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

sheets = data.get('sheets', [])
total_errors = 0
total_warnings = 0
print(f"Total sheets: {len(sheets)}")
for sheet in sheets:
    violations = sheet.get('violations', [])
    for v in violations:
        sev = v.get('severity', '')
        desc = v.get('description', '')
        type_str = v.get('type', '')
        print(f"[{sev.upper()}] {type_str}: {desc}")
        if sev.lower() == 'error':
            total_errors += 1
        else:
            total_warnings += 1

print(f"\nSummary: {total_errors} errors, {total_warnings} warnings")
