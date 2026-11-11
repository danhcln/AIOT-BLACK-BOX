import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')

for fname in ['AIOT_BLACKBOX_PRESENTATION_REV3_backup.kicad_sch', 'AIOT_BLACKBOX_PRESENTATION_REV4_backup.kicad_sch']:
    if os.path.exists(fname):
        with open(fname, 'r', encoding='utf-8') as f:
            text = f.read()
        m = re.findall(r'\(text\s+"KHỐI CẢNH BÁO[^\"]*\"[\s\S]+?\n\t\)', text)
        print(f"=== In {fname} ===")
        for t in m:
            print(t)
