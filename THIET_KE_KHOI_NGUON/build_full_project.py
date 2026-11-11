# -*- coding: utf-8 -*-
"""
AIOT BLACK BOX POWER SUPPLY - MASTER BUILDER SCRIPT
Generates all 5 KiCad 10 schematic files and project settings:
1. AIOT_BLACKBOX_POWER_SUPPLY.kicad_sch (Root Sheet)
2. 01_INPUT_SELECTION.kicad_sch (Sheet 1)
3. 02_CHARGER_BATTERY.kicad_sch (Sheet 2)
4. 03_BOOST_BUCK_RAILS.kicad_sch (Sheet 3)
5. 04_SIM_POWER_OUTPUTS.kicad_sch (Sheet 4)
All coordinates snapped to 1.27mm (50-mil) KiCad standard grid.
"""

import os
import sys
import uuid
import subprocess
import json

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"D:\ĐỒ ÁN 2\THIET_KE_KHOI_NGUON"

def uid():
    return str(uuid.uuid4())

# Grid snapping function (n * 1.27 mm)
def G(n):
    return round(n * 1.27, 4)

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

def make_header(title, sheet_num, total_sheets=5):
    tb = f"""\t(title_block
\t\t(title "{title}")
\t\t(date "2026-10-18")
\t\t(rev "REV 1.0")
\t\t(company "AIOT SMART BLACK BOX - ELECTRIC MOTORCYCLE")
\t\t(comment 1 "ĐỀ TÀI: THIẾT KẾ HỘP ĐEN AIOT THÔNG MINH - PHÂN TÍCH VÀ GHI LẠI SỰ CỐ XE MÁY ĐIỆN")
\t\t(comment 2 "SVTH: NGUYỄN LÊ CÔNG DANH (23161240) - PHẠM TRẦN HUY (21161131)")
\t\t(comment 3 "GVHD: THS. NGUYỄN NGÔ LÂM")
\t\t(comment 4 "SHEET {sheet_num} OF {total_sheets} - BUILDABLE POWER SUPPLY ARCHITECTURE")
\t)"""
    return f"""(kicad_sch
\t(version 20260306)
\t(generator "eeschema")
\t(generator_version "10.0")
\t(uuid "{uid()}")
\t(paper "A4")
{tb}
{ALL_LIB_SYMBOLS}
"""

def sym_inst(lib_id, ref, val, x, y, rot=0, footprint="", datasheet="", desc="", pins=None, ref_offset=(2.54, -2.54), val_offset=(2.54, 2.54)):
    rx = round(x + ref_offset[0], 4)
    ry = round(y + ref_offset[1], 4)
    vx = round(x + val_offset[0], 4)
    vy = round(y + val_offset[1], 4)
    pin_str = ""
    if pins:
        for p in pins:
            pin_str += f"""\t\t(pin "{p}" (uuid "{uid()}"))\n"""
    return f"""\t(symbol
\t\t(lib_id "{lib_id}")
\t\t(at {x} {y} {rot})
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "{ref}"
\t\t\t(at {rx} {ry} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t)
\t\t(property "Value" "{val}"
\t\t\t(at {vx} {vy} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t)
\t\t(property "Footprint" "{footprint}"
\t\t\t(at {x} {y} 0)
\t\t\t(hide yes)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Datasheet" "{datasheet}"
\t\t\t(at {x} {y} 0)
\t\t\t(hide yes)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Description" "{desc}"
\t\t\t(at {x} {y} 0)
\t\t\t(hide yes)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
{pin_str}\t)"""

def wire(x1, y1, x2, y2):
    return f"""\t(wire (pts (xy {round(x1,4)} {round(y1,4)}) (xy {round(x2,4)} {round(y2,4)})) (stroke (width 0) (type default)) (uuid "{uid()}"))\n"""

def junc(x, y):
    return f"""\t(junction (at {round(x,4)} {round(y,4)}) (diameter 1.0) (color 0 0 0 0) (uuid "{uid()}"))\n"""

def no_conn(x, y):
    return f"""\t(no_connect (at {round(x,4)} {round(y,4)}) (uuid "{uid()}"))\n"""

def gnd_sym(x, y):
    return f"""\t(symbol
\t\t(lib_id "power:GND")
\t\t(at {round(x,4)} {round(y,4)} 0)
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "#PWR" (at {round(x,4)} {round(y+2.54,4)} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "GND" (at {round(x,4)} {round(y+2.54,4)} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at {round(x,4)} {round(y,4)} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {round(x,4)} {round(y,4)} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "" (at {round(x,4)} {round(y,4)} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{uid()}"))
\t)\n"""

def pwr_flag(x, y):
    return f"""\t(symbol
\t\t(lib_id "power:PWR_FLAG")
\t\t(at {round(x,4)} {round(y,4)} 0)
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "#FLG" (at {round(x,4)} {round(y-2.54,4)} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "PWR_FLAG" (at {round(x,4)} {round(y-2.54,4)} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at {round(x,4)} {round(y,4)} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {round(x,4)} {round(y,4)} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "" (at {round(x,4)} {round(y,4)} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{uid()}"))
\t)\n"""

def global_lbl(name, x, y, rot=0, shape="bidirectional"):
    return f"""\t(global_label "{name}"
\t\t(shape {shape})
\t\t(at {round(x,4)} {round(y,4)} {rot})
\t\t(effects (font (size 1.27 1.27)))
\t\t(uuid "{uid()}")
\t)\n"""

def hier_lbl(name, x, y, rot=0, shape="output"):
    return f"""\t(hierarchical_label "{name}"
\t\t(shape {shape})
\t\t(at {round(x,4)} {round(y,4)} {rot})
\t\t(effects (font (size 1.27 1.27)))
\t\t(uuid "{uid()}")
\t)\n"""

def sch_text(txt, x, y, size=1.5, bold=True):
    b = "yes" if bold else "no"
    return f"""\t(text "{txt}"
\t\t(at {round(x,4)} {round(y,4)} 0)
\t\t(effects (font (size {size} {size}) (bold {b})))
\t\t(uuid "{uid()}")
\t)\n"""

print("Master builder foundation ready.")
