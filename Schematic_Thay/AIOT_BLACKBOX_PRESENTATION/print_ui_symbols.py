import re, sys
sys.stdout.reconfigure(encoding='utf-8')
from sexpr_util import extract_sexprs

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

syms = extract_sexprs(text, "(symbol")
ui_refs = ['R3', 'C2', 'SW1', 'R4', 'D1', 'R5', 'Q1', 'BZ1']

for st, en, s in syms:
    m_ref = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', s)
    m_val = re.search(r'\(property\s+"Value"\s+"([^"]+)"', s)
    m_at = re.search(r'\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)(?:\s+([0-9\.\-]+))?\)', s)
    m_lib = re.search(r'\(lib_id\s+"([^"]+)"\)', s)
    ref = m_ref.group(1) if m_ref else ""
    val = m_val.group(1) if m_val else ""
    at = (float(m_at.group(1)), float(m_at.group(2)), float(m_at.group(3) or 0)) if m_at else (0,0,0)
    lib = m_lib.group(1) if m_lib else ""
    
    if ref in ui_refs or (at[0] >= 185 and at[1] >= 120 and at[1] <= 165):
        print(f"=== {ref or lib} ({val}) at {at} ===")
        print(s)
