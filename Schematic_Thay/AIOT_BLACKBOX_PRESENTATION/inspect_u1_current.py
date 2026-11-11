import re, sys
sys.stdout.reconfigure(encoding='utf-8')
from sexpr_util import extract_sexprs

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

syms = extract_sexprs(text, "(symbol")
for st, en, s in syms:
    if '(property "Reference" "U1"' in s:
        print("=== U1 SYMBOL INSTANCE ===")
        print(s[:1000])

# Also check U1 definition in lib_symbols
pos_lib = text.find("(lib_symbols")
end_lib = text.find("\n  (junction", pos_lib)
lib_text = text[pos_lib:end_lib]

idx = lib_text.find('(symbol "Presentation:ESP32-S3-DevKitC-1"')
if idx == -1:
    idx = lib_text.find('ESP32-S3')
if idx != -1:
    count = 0
    end = -1
    for i in range(idx, len(lib_text)):
        if lib_text[i] == '(': count += 1
        elif lib_text[i] == ')':
            count -= 1
            if count == 0:
                end = i + 1
                break
    sym_def = lib_text[idx:end]
    pins = re.findall(r'\(pin\s+([a-zA-Z_]+)\s+([a-zA-Z_]+)\s+\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)\s+\(length\s+([0-9\.\-]+)\)[\s\S]+?\(name\s+"([^"]+)"[^\)]*\)[\s\S]+?\(number\s+"([^"]+)"', sym_def)
    print(f"\n=== U1 SYMBOL DEFINITION PINS ({len(pins)} pins) ===")
    for p in pins:
        print(f"  Pin {p[7]:3s} ({p[6]:15s}): at ({float(p[2]):6.2f}, {float(p[3]):6.2f}) rot={float(p[4]):3.0f}")
