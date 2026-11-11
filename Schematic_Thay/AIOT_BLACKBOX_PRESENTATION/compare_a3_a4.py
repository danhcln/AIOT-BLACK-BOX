with open('AIOT_BLACKBOX_PRESENTATION_A3_backup.kicad_sch', 'r', encoding='utf-8') as f:
    a3_text = f.read()

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    a4_text = f.read()

# Check if A3 loads in kicad-cli
import subprocess
res = subprocess.run([r"D:\Kicad\bin\kicad-cli.exe", "sch", "export", "svg", "-o", ".", "AIOT_BLACKBOX_PRESENTATION_A3_backup.kicad_sch"],
                     capture_output=True, encoding='utf-8', errors='ignore')
print("A3 backup loads:", res.returncode == 0)

# Extract lib_symbols from both
def get_lib_syms(txt):
    s = txt.find('(lib_symbols')
    e = txt.find('\n\t)\n', s) + 3
    return txt[s:e]

a3_syms = get_lib_syms(a3_text)
a4_syms = get_lib_syms(a4_text)

# Test loading header + a3_syms + ) vs header + a4_syms + )
header = "(kicad_sch\n\t(version 20260306)\n\t(generator \"eeschema\")\n\t(generator_version \"10.0\")\n\t(uuid \"11111111-2222-3333-4444-555555555555\")\n\t(paper \"A4\")\n"

with open("test_sym_a3.kicad_sch", "w", encoding="utf-8") as f:
    f.write(header + a3_syms + "\n)")
r_a3 = subprocess.run([r"D:\Kicad\bin\kicad-cli.exe", "sch", "export", "svg", "-o", ".", "test_sym_a3.kicad_sch"], capture_output=True, encoding='utf-8', errors='ignore')
print("A3 syms load:", r_a3.returncode == 0)

with open("test_sym_a4.kicad_sch", "w", encoding="utf-8") as f:
    f.write(header + a4_syms + "\n)")
r_a4 = subprocess.run([r"D:\Kicad\bin\kicad-cli.exe", "sch", "export", "svg", "-o", ".", "test_sym_a4.kicad_sch"], capture_output=True, encoding='utf-8', errors='ignore')
print("A4 syms load:", r_a4.returncode == 0)
if r_a4.returncode != 0:
    print("A4 error:", r_a4.stderr, r_a4.stdout)
