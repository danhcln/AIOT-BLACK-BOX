# -*- coding: utf-8 -*-
import subprocess
import os

sch_path = r"D:\ĐỒ ÁN 2\THIET_KE_KHOI_NGUON\01_INPUT_SELECTION.kicad_sch"
with open(sch_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Check parenthesis balance
opens = text.count('(')
closes = text.count(')')
print(f"Parenthesis count: ( = {opens}, ) = {closes}, diff = {opens - closes}")

# Test minimal prefix
s_idx = text.find('\t(lib_symbols')
depth = 0
for i in range(s_idx, len(text)):
    if text[i] == '(': depth += 1
    elif text[i] == ')':
        depth -= 1
        if depth == 0:
            e_idx = i + 1
            break

prefix = text[:e_idx]
print(f"Prefix length: {len(prefix)}")

# Test prefix only
test_sch = prefix + "\n)"
with open(r"D:\ĐỒ ÁN 2\THIET_KE_KHOI_NGUON\test_min.kicad_sch", 'w', encoding='utf-8') as f:
    f.write(test_sch)

res = subprocess.run([r"D:\KiCad\bin\kicad-cli.exe", "sch", "export", "pdf", "-o", r"D:\ĐỒ ÁN 2\THIET_KE_KHOI_NGUON\test_min.pdf", r"D:\ĐỒ ÁN 2\THIET_KE_KHOI_NGUON\test_min.kicad_sch"], capture_output=True, text=True)
print("Prefix test returncode:", res.returncode)
if res.returncode != 0:
    print("Stderr:", res.stderr)
    print("Stdout:", res.stdout)
