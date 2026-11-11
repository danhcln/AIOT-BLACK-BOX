import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

from inspect_ui import extract_sexprs

# Find symbol definitions in lib_symbols
lib_syms = extract_sexprs(text, "(symbol")
# In kicad_sch, lib_symbols is under (lib_symbols ...)
pos_lib = text.find("(lib_symbols")
end_lib = text.find("\n  (junction", pos_lib)
lib_text = text[pos_lib:end_lib]

print("Length of lib_symbols:", len(lib_text))

# Let's inspect the pins of each symbol used in UI:
# Device:R, Device:C, Switch:SW_Push, Device:LED, Presentation:2SC1815, Device:Buzzer
# Let's search pin positions for each:
for name in ["Device:R", "Device:C", "Switch:SW_Push", "Device:LED", "Presentation:2SC1815", "Device:Buzzer", "Presentation:ATGM336H_GNSS_Module"]:
    idx = lib_text.find(f'(symbol "{name}"')
    if idx != -1:
        # find end of symbol
        count = 0
        end = -1
        for i in range(idx, len(lib_text)):
            if lib_text[i] == '(':
                count += 1
            elif lib_text[i] == ')':
                count -= 1
                if count == 0:
                    end = i + 1
                    break
        sym_def = lib_text[idx:end]
        pins = re.findall(r'\(pin\s+([a-zA-Z_]+)\s+([a-zA-Z_]+)\s+\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)\s+\(length\s+([0-9\.\-]+)\)[\s\S]+?\(name\s+"([^"]+)"[^\)]*\)[\s\S]+?\(number\s+"([^"]+)"', sym_def)
        print(f"\n--- Symbol {name} ---")
        for p in pins:
            print(f"  Pin {p[7]:3s} ({p[6]:10s}): at ({float(p[2]):6.2f}, {float(p[3]):6.2f}) rot={float(p[4]):3.0f} len={float(p[5]):.2f} type={p[0]}/{p[1]}")
