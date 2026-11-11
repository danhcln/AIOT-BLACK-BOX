# -*- coding: utf-8 -*-
"""
SYMBOL DEFINITIONS FOR AIOT BLACK BOX POWER SUPPLY
Contains verified, standard KiCad 10 symbols:
- Extracted basic passives: R, C, CP, L, D_Schottky, D_TVS, Fuse, LED, TestPoint, Conn_01x02, Conn_01x03, Conn_01x05, Conn_01x10, Jumper_3_Open
- Power symbols: GND, PWR_FLAG
"""

import os
import re

kicad_sym_dir = r"D:\KiCad\share\kicad\symbols"

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

with open(os.path.join(kicad_sym_dir, "power.kicad_sym"), 'r', encoding='utf-8') as f:
    pwr_text = f.read()

SYM_GND = extract_sym(pwr_text, "GND", "power:GND")
SYM_PWR_FLAG = extract_sym(pwr_text, "PWR_FLAG", "power:PWR_FLAG")

with open(os.path.join(kicad_sym_dir, "Device.kicad_sym"), 'r', encoding='utf-8') as f:
    dev_text = f.read()

SYM_R = extract_sym(dev_text, "R", "Device:R")
SYM_C = extract_sym(dev_text, "C", "Device:C")
SYM_CP = extract_sym(dev_text, "C_Polarized", "Device:C_Polarized")
SYM_L = extract_sym(dev_text, "L", "Device:L")
SYM_D_SCHOTTKY = extract_sym(dev_text, "D_Schottky", "Device:D_Schottky")
SYM_D_TVS = extract_sym(dev_text, "D_TVS", "Device:D_TVS")
SYM_FUSE = extract_sym(dev_text, "Fuse", "Device:Fuse")
SYM_LED = extract_sym(dev_text, "LED", "Device:LED")

with open(os.path.join(kicad_sym_dir, "Jumper.kicad_sym"), 'r', encoding='utf-8') as f:
    jmp_text = f.read()

SYM_JUMPER3 = extract_sym(jmp_text, "Jumper_3_Open", "Jumper:Jumper_3_Open")

with open(os.path.join(kicad_sym_dir, "Connector.kicad_sym"), 'r', encoding='utf-8') as f:
    conn_text = f.read()

SYM_CONN_02 = extract_sym(conn_text, "Conn_01x02_Pin", "Connector:Conn_01x02_Pin")
SYM_CONN_03 = extract_sym(conn_text, "Conn_01x03_Pin", "Connector:Conn_01x03_Pin")
SYM_CONN_05 = extract_sym(conn_text, "Conn_01x05_Pin", "Connector:Conn_01x05_Pin")
SYM_CONN_10 = extract_sym(conn_text, "Conn_01x10_Pin", "Connector:Conn_01x10_Pin")
SYM_TESTPOINT = extract_sym(conn_text, "TestPoint", "Connector:TestPoint")

print("Base library symbols extracted successfully.")
