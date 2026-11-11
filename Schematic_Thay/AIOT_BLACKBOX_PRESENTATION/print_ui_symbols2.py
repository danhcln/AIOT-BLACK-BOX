import re, sys
sys.stdout.reconfigure(encoding='utf-8')
from sexpr_util import extract_sexprs

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

syms = extract_sexprs(text, "(symbol")
for ref_target in ['D1', 'R4', 'C2', 'R3', 'Q1']:
    for st, en, s in syms:
        if f'"{ref_target}"' in s:
            m_at = re.search(r'\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)(?:\s+([0-9\.\-]+))?\)', s)
            at = (float(m_at.group(1)), float(m_at.group(2)), float(m_at.group(3) or 0)) if m_at else (0,0,0)
            print(f"=== {ref_target} at {at} ===")
            print(s)
            break
