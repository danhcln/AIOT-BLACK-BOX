import subprocess

with open('AIOT_BLACKBOX_PRESENTATION_A3_backup.kicad_sch', 'r', encoding='utf-8') as f:
    a3_text = f.read()

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    a4_text = f.read()

s3_idx = a3_text.find('\t(lib_symbols')
depth = 0
for i in range(s3_idx, len(a3_text)):
    if a3_text[i] == '(': depth += 1
    elif a3_text[i] == ')':
        depth -= 1
        if depth == 0:
            e3_idx = i + 1
            break

s4_idx = a4_text.find('\t(lib_symbols')
depth = 0
for i in range(s4_idx, len(a4_text)):
    if a4_text[i] == '(': depth += 1
    elif a4_text[i] == ')':
        depth -= 1
        if depth == 0:
            e4_idx = i + 1
            break

prefix = a4_text[:e4_idx]
a4_rest = a4_text[e4_idx:].strip()
if a4_rest.endswith(')'):
    a4_rest = a4_rest[:-1].strip()

# Now split a4_rest into individual top-level s-expressions
elements = []
i = 0
while i < len(a4_rest):
    if a4_rest[i] == '(':
        start = i
        depth = 0
        while i < len(a4_rest):
            if a4_rest[i] == '(': depth += 1
            elif a4_rest[i] == ')':
                depth -= 1
                if depth == 0:
                    elements.append(a4_rest[start:i+1])
                    break
            i += 1
    i += 1

print(f"Total elements in a4_rest: {len(elements)}")

def test_elems(elem_list):
    content = prefix + "\n" + "\n".join(elem_list) + "\n)"
    with open("temp_test.kicad_sch", "w", encoding="utf-8") as f:
        f.write(content)
    res = subprocess.run([r"D:\Kicad\bin\kicad-cli.exe", "sch", "export", "svg", "-o", ".", "temp_test.kicad_sch"],
                         capture_output=True, encoding='utf-8', errors='ignore')
    return res.returncode == 0

# Binary search for the bad element
low = 0
high = len(elements)
while low < high:
    mid = (low + high) // 2
    ok = test_elems(elements[:mid])
    print(f"Elements 0 to {mid}: {ok}")
    if ok:
        low = mid + 1
    else:
        high = mid

bad_idx = low - 1
print(f"Bad element at index {bad_idx}:")
print(elements[bad_idx][:200])
