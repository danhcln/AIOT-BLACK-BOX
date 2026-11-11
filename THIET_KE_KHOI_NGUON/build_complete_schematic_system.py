# -*- coding: utf-8 -*-
"""
AIOT BLACK BOX POWER SUPPLY - COMPLETE SCHEMATIC GENERATOR
Generates 5 KiCad 10 schematic files with full hierarchical architecture:
- AIOT_BLACKBOX_POWER_SUPPLY.kicad_sch (Root Sheet)
- 01_INPUT_SELECTION.kicad_sch (Sheet 1)
- 02_CHARGER_BATTERY.kicad_sch (Sheet 2)
- 03_BOOST_BUCK_RAILS.kicad_sch (Sheet 3)
- 04_SIM_POWER_OUTPUTS.kicad_sch (Sheet 4)
"""

import os
import sys
import uuid
import re

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"D:\ĐỒ ÁN 2\THIET_KE_KHOI_NGUON"

def uid():
    return str(uuid.uuid4())

# Load symbols from generate_symbols and custom_symbols_def
import generate_symbols as base_syms
import custom_symbols_def as cust_syms

ALL_LIB_SYMBOLS = f"""\t(lib_symbols
{base_syms.SYM_GND}
{base_syms.SYM_PWR_FLAG}
{base_syms.SYM_R}
{base_syms.SYM_C}
{base_syms.SYM_CP}
{base_syms.SYM_L}
{base_syms.SYM_D_SCHOTTKY}
{base_syms.SYM_D_TVS}
{base_syms.SYM_FUSE}
{base_syms.SYM_LED}
{base_syms.SYM_JUMPER3}
{base_syms.SYM_CONN_02}
{base_syms.SYM_CONN_03}
{base_syms.SYM_CONN_05}
{base_syms.SYM_CONN_10}
{base_syms.SYM_TESTPOINT}
{cust_syms.SYM_TPS2121}
{cust_syms.SYM_BQ25895}
{cust_syms.SYM_DW01A}
{cust_syms.SYM_FS8205A}
{cust_syms.SYM_TPS61088}
{cust_syms.SYM_TPS62162}
{cust_syms.SYM_TPS62130}
{cust_syms.SYM_USB_C_16P}
\t)"""

def make_title_block(title, sheet_num, total_sheets=5):
    return f"""\t(title_block
\t\t(title "{title}")
\t\t(date "2026-10-18")
\t\t(rev "REV 1.0")
\t\t(company "AIOT SMART BLACK BOX - ELECTRIC MOTORCYCLE")
\t\t(comment 1 "ĐỀ TÀI: THIẾT KẾ HỘP ĐEN AIOT THÔNG MINH - PHÂN TÍCH VÀ GHI LẠI SỰ CỐ XE MÁY ĐIỆN")
\t\t(comment 2 "SVTH: NGUYỄN LÊ CÔNG DANH (23161240) - PHẠM TRẦN HUY (21161131)")
\t\t(comment 3 "GVHD: THS. NGUYỄN NGÔ LÂM")
\t\t(comment 4 "SHEET {sheet_num} OF {total_sheets} - BUILDABLE POWER SUPPLY ARCHITECTURE")
\t)"""

print("Schematic builder module loaded.")
