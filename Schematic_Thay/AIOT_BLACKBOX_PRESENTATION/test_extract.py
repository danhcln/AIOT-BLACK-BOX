import os, re

kicad_sym_dir = r"D:\Kicad\share\kicad\symbols"

def extract_sym(file_content, sym_name, new_lib_id):
    pattern = rf'\(symbol\s+"{sym_name}"'
    m = re.search(pattern, file_content)
    if not m:
        return ""
    start = m.start()
    depth = 0
    end = start
    for i in range(start, len(file_content)):
        if file_content[i] == '(':
            depth += 1
        elif file_content[i] == ')':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    content = file_content[start:end]
    content = re.sub(rf'\(symbol\s+"{sym_name}"', f'(symbol "{new_lib_id}"', content)
    content = re.sub(rf'\(symbol\s+"{sym_name}_', f'(symbol "{new_lib_id.split(":")[-1]}_', content)
    return content

with open(os.path.join(kicad_sym_dir, "Device.kicad_sym"), 'r', encoding='utf-8') as f:
    dev_text = f.read()

with open(os.path.join(kicad_sym_dir, "power.kicad_sym"), 'r', encoding='utf-8') as f:
    pwr_text = f.read()

sym_r = extract_sym(dev_text, "R", "Device:R")
sym_3v3 = extract_sym(pwr_text, "\\+3V3", "power:+3V3")

print("sym_r balance:", sym_r.count('(') - sym_r.count(')'))
print("sym_r length:", len(sym_r))
print("sym_3v3 balance:", sym_3v3.count('(') - sym_3v3.count(')'))
print("sym_3v3 length:", len(sym_3v3))
