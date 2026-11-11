import re, sys
sys.stdout.reconfigure(encoding='utf-8')
from inspect_ui import extract_sexprs

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

texts = extract_sexprs(text, "(text")
for start, end, t in texts:
    m_at = re.search(r'\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)', t)
    m_txt = re.search(r'"([^"]+)"', t)
    if m_at and m_txt:
        print(f"Text '{m_txt.group(1)}' at ({float(m_at.group(1)):.2f}, {float(m_at.group(2)):.2f})")
