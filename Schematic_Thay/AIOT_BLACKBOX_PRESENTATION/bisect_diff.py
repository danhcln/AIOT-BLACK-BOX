import subprocess

with open('AIOT_BLACKBOX_PRESENTATION_A3_backup.kicad_sch', 'r', encoding='utf-8') as f:
    a3_text = f.read()

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    a4_text = f.read()

def test_sch(content):
    with open("temp_test.kicad_sch", "w", encoding="utf-8") as f:
        f.write(content)
    res = subprocess.run([r"D:\Kicad\bin\kicad-cli.exe", "sch", "export", "svg", "-o", ".", "temp_test.kicad_sch"],
                         capture_output=True, encoding='utf-8', errors='ignore')
    return res.returncode == 0

# 1. Test A3 with paper A4
a3_a4paper = a3_text.replace('(paper "A3")', '(paper "A4")')
print("A3 with A4 paper:", test_sch(a3_a4paper))

# 2. Extract sections from A3 and A4
def split_sections(txt):
    s_sym = txt.find('(lib_symbols')
    e_sym = txt.find('\n\t)\n', s_sym) + 3
    header = txt[:s_sym]
    lib_syms = txt[s_sym:e_sym]
    body = txt[e_sym:]
    return header, lib_syms, body

h3, s3, b3 = split_sections(a3_text)
h4, s4, b4 = split_sections(a4_text)

# Test: header4 + s3 + b3
print("h4 + s3 + b3:", test_sch(h4 + s3 + b3))

# Test: h4 + s4 + b3 (test s4)
print("h4 + s4 + b3 (test symbols):", test_sch(h4 + s4 + b3))

# Test: h4 + s3 + b4 (test body)
print("h4 + s3 + b4 (test body):", test_sch(h4 + s3 + b4))
