import subprocess
import os

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    full_text = f.read()

# Let's test what part KiCad dislikes.
# In KiCad 10, let's see what happens if we test loading just the header + lib_symbols + )
# Let's extract lib_symbols
start_syms = full_text.find('(lib_symbols')
end_syms = full_text.find('\n\t)\n', start_syms) + 3

header = full_text[:start_syms]
lib_symbols = full_text[start_syms:end_syms]

def test_sch(content, name="temp_test.kicad_sch"):
    with open(name, 'w', encoding='utf-8') as f:
        f.write(content)
    res = subprocess.run([r"D:\Kicad\bin\kicad-cli.exe", "sch", "export", "svg", "-o", ".", name], capture_output=True, text=True)
    return res.returncode == 0, res.stdout, res.stderr

ok, out, err = test_sch(header + lib_symbols + "\n)")
print(f"Header + lib_symbols test: {ok}")
if not ok:
    print("Err:", err, out)
else:
    print("Lib symbols are OK!")
