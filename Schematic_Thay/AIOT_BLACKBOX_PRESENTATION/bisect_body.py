import subprocess

with open('AIOT_BLACKBOX_PRESENTATION_A3_backup.kicad_sch', 'r', encoding='utf-8') as f:
    a3_text = f.read()

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    a4_text = f.read()

def split_sections(txt):
    s_sym = txt.find('(lib_symbols')
    e_sym = txt.find('\n\t)\n', s_sym) + 3
    header = txt[:s_sym]
    lib_syms = txt[s_sym:e_sym]
    body = txt[e_sym:]
    return header, lib_syms, body

h4, s4, b4 = split_sections(a4_text)

def test_body(body_str):
    content = f"{h4}{s4}\n{body_str}\n)"
    with open("temp_test.kicad_sch", "w", encoding="utf-8") as f:
        f.write(content)
    res = subprocess.run([r"D:\Kicad\bin\kicad-cli.exe", "sch", "export", "svg", "-o", ".", "temp_test.kicad_sch"],
                         capture_output=True, encoding='utf-8', errors='ignore')
    return res.returncode == 0

# In generate_a4_sch, body is made of:
# junctions, wires, labels, symbols_list, boxes_list
from generate_a4_sch import junctions, wires, labels, symbols_list, boxes_list

print("Testing only junctions:", test_body('\n'.join(junctions)))
print("Testing junctions + wires:", test_body('\n'.join(junctions + wires)))
print("Testing + labels:", test_body('\n'.join(junctions + wires + labels)))
print("Testing + symbols_list:", test_body('\n'.join(junctions + wires + labels + symbols_list)))
print("Testing + boxes_list:", test_body('\n'.join(junctions + wires + labels + symbols_list + boxes_list)))
