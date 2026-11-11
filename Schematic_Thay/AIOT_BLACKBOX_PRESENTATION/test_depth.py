import subprocess

with open('AIOT_BLACKBOX_PRESENTATION_A3_backup.kicad_sch', 'r', encoding='utf-8') as f:
    a3_text = f.read()

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    a4_text = f.read()

def test_sch(txt):
    with open("temp_test.kicad_sch", "w", encoding="utf-8") as f:
        f.write(txt)
    res = subprocess.run([r"D:\Kicad\bin\kicad-cli.exe", "sch", "export", "svg", "-o", ".", "temp_test.kicad_sch"],
                         capture_output=True, encoding='utf-8', errors='ignore')
    return res.returncode == 0

# Let's extract the lib_symbols block from a4_text
# In a4_text, lib_symbols starts at `\t(lib_symbols` and ends right before the first `\t(junction` or `\t(wire`
s_idx = a4_text.find('\t(lib_symbols')
# Find where lib_symbols closes
depth = 0
e_idx = s_idx
for i in range(s_idx, len(a4_text)):
    if a4_text[i] == '(':
        depth += 1
    elif a4_text[i] == ')':
        depth -= 1
        if depth == 0:
            e_idx = i + 1
            break

a4_lib_symbols = a4_text[s_idx:e_idx]
print(f"a4_lib_symbols len: {len(a4_lib_symbols)}")

# Now in a3_text, find lib_symbols
s3_idx = a3_text.find('\t(lib_symbols')
depth = 0
e3_idx = s3_idx
for i in range(s3_idx, len(a3_text)):
    if a3_text[i] == '(':
        depth += 1
    elif a3_text[i] == ')':
        depth -= 1
        if depth == 0:
            e3_idx = i + 1
            break

a3_lib_symbols = a3_text[s3_idx:e3_idx]
print(f"a3_lib_symbols len: {len(a3_lib_symbols)}")

# Replace a3_lib_symbols with a4_lib_symbols in a3_text:
test_a3_with_a4_syms = a3_text[:s3_idx] + a4_lib_symbols + a3_text[e3_idx:]
print("A3 with A4 symbols test:", test_sch(test_a3_with_a4_syms))

# Now test replacing the instances in a3_text
a4_rest = a4_text[e_idx:]
test_a4_full = a3_text[:s3_idx] + a4_lib_symbols + a4_rest
print("A4 full test:", test_sch(test_a4_full))
