import subprocess
import os
import re

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    full_text = f.read()

start_syms = full_text.find('(lib_symbols')
end_syms = full_text.find('\n\t)\n', start_syms) + 3

header = full_text[:start_syms]
sym_text = full_text[start_syms+12:end_syms-2]

# Let's find top-level symbols inside lib_symbols (depth 1)
# Each top-level symbol starts with \t\t(symbol "
symbols = []
pos = 0
while True:
    m = re.search(r'\n\t\t\(symbol\s+"([^"]+)"', sym_text[pos:])
    if not m:
        break
    start = pos + m.start() + 3 # skip \n\t\t
    s_name = m.group(1)
    depth = 0
    end = start
    for i in range(start, len(sym_text)):
        if sym_text[i] == '(':
            depth += 1
        elif sym_text[i] == ')':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    symbols.append((s_name, sym_text[start:end]))
    pos = end

print(f"Top level symbols: {len(symbols)}")

def test_sym(sym_str):
    content = f"""{header}\t(lib_symbols\n{sym_str}\n\t)\n)"""
    with open("temp_test.kicad_sch", "w", encoding="utf-8") as f:
        f.write(content)
    res = subprocess.run([r"D:\Kicad\bin\kicad-cli.exe", "sch", "export", "svg", "-o", ".", "temp_test.kicad_sch"],
                         capture_output=True, encoding='utf-8', errors='ignore')
    return res.returncode == 0

for name, s in symbols:
    ok = test_sym(s)
    print(f"Symbol {name}: {ok}")
