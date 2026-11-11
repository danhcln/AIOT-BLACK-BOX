# -*- coding: utf-8 -*-
import subprocess
import os
import re

import generate_symbols as base_syms
import custom_symbols_def as cust_syms

symbols = [
    ("GND", base_syms.SYM_GND),
    ("PWR_FLAG", base_syms.SYM_PWR_FLAG),
    ("R", base_syms.SYM_R),
    ("C", base_syms.SYM_C),
    ("CP", base_syms.SYM_CP),
    ("L", base_syms.SYM_L),
    ("D_SCHOTTKY", base_syms.SYM_D_SCHOTTKY),
    ("D_TVS", base_syms.SYM_D_TVS),
    ("FUSE", base_syms.SYM_FUSE),
    ("LED", base_syms.SYM_LED),
    ("JUMPER3", base_syms.SYM_JUMPER3),
    ("CONN_02", base_syms.SYM_CONN_02),
    ("CONN_03", base_syms.SYM_CONN_03),
    ("CONN_05", base_syms.SYM_CONN_05),
    ("CONN_10", base_syms.SYM_CONN_10),
    ("TESTPOINT", base_syms.SYM_TESTPOINT),
    ("TPS2121", cust_syms.SYM_TPS2121),
    ("BQ25895", cust_syms.SYM_BQ25895),
    ("DW01A", cust_syms.SYM_DW01A),
    ("FS8205A", cust_syms.SYM_FS8205A),
    ("TPS61088", cust_syms.SYM_TPS61088),
    ("TPS62162", cust_syms.SYM_TPS62162),
    ("TPS62130", cust_syms.SYM_TPS62130),
    ("USB_C_16P", cust_syms.SYM_USB_C_16P)
]

header_base = """(kicad_sch
\t(version 20260306)
\t(generator "eeschema")
\t(generator_version "10.0")
\t(uuid "test-uuid")
\t(paper "A4")
\t(lib_symbols
"""

for name, sym in symbols:
    test_content = header_base + sym + "\n\t)\n)"
    test_file = r"D:\ĐỒ ÁN 2\THIET_KE_KHOI_NGUON\test_sym.kicad_sch"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    res = subprocess.run([r"D:\KiCad\bin\kicad-cli.exe", "sch", "export", "pdf", "-o", r"D:\ĐỒ ÁN 2\THIET_KE_KHOI_NGUON\test_sym.pdf", test_file], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FAILED on symbol: {name}")
    else:
        print(f"PASSED: {name}")
