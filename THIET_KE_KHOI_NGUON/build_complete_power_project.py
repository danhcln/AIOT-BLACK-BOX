# -*- coding: utf-8 -*-
"""
AIOT BLACK BOX - COMPLETE HIERARCHICAL POWER SUPPLY SCHEMATIC GENERATOR
Generates all 5 KiCad 10 schematic files with exact pin tip alignment,
strict Drawing Rule compliance, zero off-grid errors, and clean ERC.
"""

import os
import sys
import uuid
import re
import json
import subprocess
import importlib

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"D:\ĐỒ ÁN 2\THIET_KE_KHOI_NGUON"

def uid():
    return str(uuid.uuid4())

def G(n):
    return round(n * 1.27, 4)

import generate_symbols as base_syms
import custom_symbols_def as cust_syms
importlib.reload(cust_syms)

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
{cust_syms.SYM_AO3401A}
\t)"""

def get_pin_offset(sym_str, pin_num, rot=0):
    pattern = rf'\(pin\s+\S+\s+\S+\s+\(at\s+([-\d\.]+)\s+([-\d\.]+)[^\)]*\)(?:(?!\(pin).)*?\(number\s+"{pin_num}"'
    m = re.search(pattern, sym_str, re.DOTALL)
    if not m:
        raise ValueError(f"Pin {pin_num} not found in symbol")
    px, py = float(m.group(1)), float(m.group(2))
    if rot == 0:
        return round(px, 4), round(-py, 4)
    elif rot == 90:
        return round(-py, 4), round(-px, 4)
    elif rot == 180:
        return round(-px, 4), round(py, 4)
    elif rot == 270:
        return round(py, 4), round(px, 4)
    return round(px, 4), round(-py, 4)

def pin_pos(sym_str, sx, sy, pin_num, rot=0):
    dx, dy = get_pin_offset(sym_str, pin_num, rot)
    return round(sx + dx, 4), round(sy + dy, 4)

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
\t\t(at {round(x,4)} {round(y,4)} {rot})
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
\t\t\t(at {round(x,4)} {round(y,4)} 0)
\t\t\t(hide yes)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Datasheet" "{datasheet}"
\t\t\t(at {round(x,4)} {round(y,4)} 0)
\t\t\t(hide yes)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Description" "{desc}"
\t\t\t(at {round(x,4)} {round(y,4)} 0)
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

print("Generator framework initialized.")

# =============================================================================
# SHEET 1: 01_INPUT_SELECTION.kicad_sch
# =============================================================================
def build_sheet1(out_path):
    content = make_header("KHỐI CHỌN NGUỒN ĐẦU VÀO & POWER MUX (TPS2121)", 2, 5)
    
    # -------------------------------------------------------------------------
    # 1. VEHICLE_5V_IN Block
    # -------------------------------------------------------------------------
    j1_x, j1_y = 30.48, 50.80
    content += sym_inst("Connector:Conn_01x02_Pin", "J1", "VEHICLE_5V_IN", j1_x, j1_y, 0,
                        "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical",
                        "https://www.jst-mfg.com/product/pdf/eng/eXH.pdf",
                        "External Regulated 5V Vehicle Input Connector, 2.50mm, 5A",
                        pins=["1", "2"])
    
    f1_x, f1_y = 50.80, 50.80
    content += sym_inst("Device:Fuse", "F1", "MF-MSMF300/16X (3.0A)", f1_x, f1_y, 90,
                        "Fuse:Fuse_1812_4532Metric",
                        "https://www.bourns.com/docs/product-datasheets/mf-msmf.pdf",
                        "PTC Resettable Fuse, 3.0A Hold, 6.0A Trip, 16V, 1812 SMD",
                        pins=["1", "2"])
    
    d1_x, d1_y = 63.50, 60.96
    content += sym_inst("Device:D_TVS", "D1", "SMAJ5.0A", d1_x, d1_y, 90,
                        "Diode_SMD:D_SMA",
                        "https://www.vishay.com/docs/88390/smaj50a.pdf",
                        "600W Transient Voltage Suppressor, 5.0V Reverse Standoff, SMA",
                        pins=["1", "2"])
    
    d3_x, d3_y = 76.20, 50.80
    content += sym_inst("Device:D_Schottky", "D3", "SS34 (3A/40V)", d3_x, d3_y, 180,
                        "Diode_SMD:D_SMA",
                        "https://www.vishay.com/docs/88746/ss32.pdf",
                        "Schottky Barrier Rectifier Diode, 3A, 40V, Low Vf, SMA",
                        pins=["1", "2"])
    
    c1_x, c1_y = 88.90, 60.96
    content += sym_inst("Device:C", "C1", "10uF/25V (X7R)", c1_x, c1_y, 0,
                        "Capacitor_SMD:C_0805_2012Metric",
                        "~", "Ceramic Capacitor, 10uF, 25V, X7R, 10%, 0805",
                        pins=["1", "2"])
    
    c2_x, c2_y = 101.60, 60.96
    content += sym_inst("Device:C_Polarized", "C2", "100uF/25V (Low ESR)", c2_x, c2_y, 0,
                        "Capacitor_SMD:CP_Elec_6.3x5.4",
                        "~", "Aluminum Electrolytic Capacitor, 100uF, 25V, Low-ESR SMD",
                        pins=["1", "2"])
    
    tp1_x, tp1_y = 114.30, 45.72
    content += sym_inst("Connector:TestPoint", "TP1", "TP_VEHICLE_5V", tp1_x, tp1_y, 0,
                        "TestPoint:TestPoint_Pad_D1.5mm",
                        "~", "Test Point Pad 1.5mm, VEHICLE_5V_IN",
                        pins=["1"])
    
    # Calculate pins for Vehicle 5V block
    j1_p1 = pin_pos(base_syms.SYM_CONN_02, j1_x, j1_y, "1", 0)
    j1_p2 = pin_pos(base_syms.SYM_CONN_02, j1_x, j1_y, "2", 0)
    f1_p1 = pin_pos(base_syms.SYM_FUSE, f1_x, f1_y, "1", 90)
    f1_p2 = pin_pos(base_syms.SYM_FUSE, f1_x, f1_y, "2", 90)
    d1_p1 = pin_pos(base_syms.SYM_D_TVS, d1_x, d1_y, "1", 90)
    d1_p2 = pin_pos(base_syms.SYM_D_TVS, d1_x, d1_y, "2", 90)
    d3_p1 = pin_pos(base_syms.SYM_D_SCHOTTKY, d3_x, d3_y, "1", 180)
    d3_p2 = pin_pos(base_syms.SYM_D_SCHOTTKY, d3_x, d3_y, "2", 180)
    c1_p1 = pin_pos(base_syms.SYM_C, c1_x, c1_y, "1", 0)
    c1_p2 = pin_pos(base_syms.SYM_C, c1_x, c1_y, "2", 0)
    c2_p1 = pin_pos(base_syms.SYM_CP, c2_x, c2_y, "1", 0)
    c2_p2 = pin_pos(base_syms.SYM_CP, c2_x, c2_y, "2", 0)
    tp1_p1 = pin_pos(base_syms.SYM_TESTPOINT, tp1_x, tp1_y, "1", 0)
    
    # Wire VEHICLE_5V_IN
    content += wire(j1_p1[0], j1_p1[1], f1_p1[0], f1_p1[1])
    content += wire(f1_p2[0], f1_p2[1], d1_p1[0], f1_p2[1])
    content += junc(d1_p1[0], f1_p2[1])
    content += wire(d1_p1[0], f1_p2[1], d1_p1[0], d1_p1[1])
    content += wire(d1_p2[0], d1_p2[1], d1_p2[0], 68.58)
    content += gnd_sym(d1_p2[0], 68.58)
    
    # Wire D3 Schottky (current enters Anode d3_p2, exits Cathode d3_p1)
    content += wire(d1_p1[0], f1_p2[1], d3_p2[0], d3_p2[1])
    content += wire(d3_p1[0], d3_p1[1], c1_p1[0], d3_p1[1])
    content += junc(c1_p1[0], d3_p1[1])
    content += wire(c1_p1[0], d3_p1[1], c1_p1[0], c1_p1[1])
    content += wire(c1_p2[0], c1_p2[1], c1_p2[0], 68.58)
    content += gnd_sym(c1_p2[0], 68.58)
    
    content += wire(c1_p1[0], d3_p1[1], c2_p1[0], d3_p1[1])
    content += junc(c2_p1[0], d3_p1[1])
    content += wire(c2_p1[0], d3_p1[1], c2_p1[0], c2_p1[1])
    content += wire(c2_p2[0], c2_p2[1], c2_p2[0], 68.58)
    content += gnd_sym(c2_p2[0], 68.58)
    
    content += wire(c2_p1[0], d3_p1[1], tp1_p1[0], d3_p1[1])
    content += junc(tp1_p1[0], d3_p1[1])
    content += wire(tp1_p1[0], d3_p1[1], tp1_p1[0], tp1_p1[1])
    content += pwr_flag(tp1_p1[0], tp1_p1[1])
    content += wire(tp1_p1[0], d3_p1[1], 127.00, d3_p1[1])
    content += global_lbl("VEHICLE_5V_IN", 127.00, d3_p1[1], 0, "bidirectional")
    
    content += wire(j1_p2[0], j1_p2[1], j1_p2[0], 68.58)
    content += gnd_sym(j1_p2[0], 68.58)
    
    # -------------------------------------------------------------------------
    # 2. USB_5V_IN Block
    # -------------------------------------------------------------------------
    j2_x, j2_y = 30.48, 114.30
    content += sym_inst("Connector:USB_C_16P", "J2", "TYPE-C-16P", j2_x, j2_y, 0,
                        "Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12",
                        "https://www.usb.org/type-c",
                        "USB 2.0 Type-C Receptacle, 16 pins, 5A VBUS, 50V",
                        pins=["A1", "A4", "A5", "A6", "A7", "B5", "B9", "B12", "S1"])
    
    f2_x, f2_y = 55.88, 109.22
    content += sym_inst("Device:Fuse", "F2", "MF-MSMF300/16X (3.0A)", f2_x, f2_y, 90,
                        "Fuse:Fuse_1812_4532Metric",
                        "https://www.bourns.com/docs/product-datasheets/mf-msmf.pdf",
                        "PTC Resettable Fuse, 3.0A Hold, 6.0A Trip, 16V, 1812 SMD",
                        pins=["1", "2"])
    
    d2_x, d2_y = 68.58, 121.92
    content += sym_inst("Device:D_TVS", "D2", "SMAJ5.0A", d2_x, d2_y, 90,
                        "Diode_SMD:D_SMA",
                        "https://www.vishay.com/docs/88390/smaj50a.pdf",
                        "600W Transient Voltage Suppressor, 5.0V Reverse Standoff, SMA",
                        pins=["1", "2"])
    
    c3_x, c3_y = 81.28, 121.92
    content += sym_inst("Device:C", "C3", "10uF/16V (X7R)", c3_x, c3_y, 0,
                        "Capacitor_SMD:C_0805_2012Metric",
                        "~", "Ceramic Capacitor, 10uF, 16V, X7R, 10%, 0805",
                        pins=["1", "2"])
    
    r1_x, r1_y = 50.80, 121.92
    content += sym_inst("Device:R", "R1", "5.1k (1%)", r1_x, r1_y, 0,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Resistor, 5.1k, 1%, 0.1W, 0603",
                        pins=["1", "2"])
    
    r2_x, r2_y = 60.96, 121.92
    content += sym_inst("Device:R", "R2", "5.1k (1%)", r2_x, r2_y, 0,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Resistor, 5.1k, 1%, 0.1W, 0603",
                        pins=["1", "2"])
    
    tp2_x, tp2_y = 93.98, 104.14
    content += sym_inst("Connector:TestPoint", "TP2", "TP_USB_5V", tp2_x, tp2_y, 0,
                        "TestPoint:TestPoint_Pad_D1.5mm",
                        "~", "Test Point Pad 1.5mm, USB_5V_IN",
                        pins=["1"])
    
    j2_pa4 = pin_pos(cust_syms.SYM_USB_C_16P, j2_x, j2_y, "A4", 0)
    j2_pb9 = pin_pos(cust_syms.SYM_USB_C_16P, j2_x, j2_y, "B9", 0)
    j2_pa5 = pin_pos(cust_syms.SYM_USB_C_16P, j2_x, j2_y, "A5", 0)
    j2_pb5 = pin_pos(cust_syms.SYM_USB_C_16P, j2_x, j2_y, "B5", 0)
    j2_pa6 = pin_pos(cust_syms.SYM_USB_C_16P, j2_x, j2_y, "A6", 0)
    j2_pa7 = pin_pos(cust_syms.SYM_USB_C_16P, j2_x, j2_y, "A7", 0)
    j2_pa1 = pin_pos(cust_syms.SYM_USB_C_16P, j2_x, j2_y, "A1", 0)
    j2_ps1 = pin_pos(cust_syms.SYM_USB_C_16P, j2_x, j2_y, "S1", 0)
    
    f2_p1 = pin_pos(base_syms.SYM_FUSE, f2_x, f2_y, "1", 90)
    f2_p2 = pin_pos(base_syms.SYM_FUSE, f2_x, f2_y, "2", 90)
    d2_p1 = pin_pos(base_syms.SYM_D_TVS, d2_x, d2_y, "1", 90)
    d2_p2 = pin_pos(base_syms.SYM_D_TVS, d2_x, d2_y, "2", 90)
    c3_p1 = pin_pos(base_syms.SYM_C, c3_x, c3_y, "1", 0)
    c3_p2 = pin_pos(base_syms.SYM_C, c3_x, c3_y, "2", 0)
    r1_p1 = pin_pos(base_syms.SYM_R, r1_x, r1_y, "1", 0)
    r1_p2 = pin_pos(base_syms.SYM_R, r1_x, r1_y, "2", 0)
    r2_p1 = pin_pos(base_syms.SYM_R, r2_x, r2_y, "1", 0)
    r2_p2 = pin_pos(base_syms.SYM_R, r2_x, r2_y, "2", 0)
    tp2_p1 = pin_pos(base_syms.SYM_TESTPOINT, tp2_x, tp2_y, "1", 0)
    
    # Wire USB VBUS
    content += wire(j2_pa4[0], j2_pa4[1], 46.99, j2_pa4[1])
    content += wire(j2_pb9[0], j2_pb9[1], 46.99, j2_pb9[1])
    content += wire(46.99, j2_pa4[1], 46.99, f2_p1[1])
    content += junc(46.99, j2_pb9[1])
    content += wire(46.99, f2_p1[1], f2_p1[0], f2_p1[1])
    
    content += wire(f2_p2[0], f2_p2[1], d2_p1[0], f2_p2[1])
    content += junc(d2_p1[0], f2_p2[1])
    content += wire(d2_p1[0], f2_p2[1], d2_p1[0], d2_p1[1])
    content += wire(d2_p2[0], d2_p2[1], d2_p2[0], 134.62)
    content += gnd_sym(d2_p2[0], 134.62)
    
    content += wire(d2_p1[0], f2_p2[1], c3_p1[0], f2_p2[1])
    content += junc(c3_p1[0], f2_p2[1])
    content += wire(c3_p1[0], f2_p2[1], c3_p1[0], c3_p1[1])
    content += wire(c3_p2[0], c3_p2[1], c3_p2[0], 134.62)
    content += gnd_sym(c3_p2[0], 134.62)
    
    content += wire(c3_p1[0], f2_p2[1], tp2_p1[0], f2_p2[1])
    content += junc(tp2_p1[0], f2_p2[1])
    content += wire(tp2_p1[0], f2_p2[1], tp2_p1[0], tp2_p1[1])
    content += pwr_flag(tp2_p1[0], tp2_p1[1])
    content += wire(tp2_p1[0], f2_p2[1], 106.68, f2_p2[1])
    content += global_lbl("USB_5V_IN", 106.68, f2_p2[1], 0, "bidirectional")
    
    # CC lines
    content += wire(j2_pa5[0], j2_pa5[1], r1_p1[0], j2_pa5[1])
    content += wire(r1_p1[0], j2_pa5[1], r1_p1[0], r1_p1[1])
    content += wire(r1_p2[0], r1_p2[1], r1_p2[0], 134.62)
    content += gnd_sym(r1_p2[0], 134.62)
    
    content += wire(j2_pb5[0], j2_pb5[1], r2_p1[0], j2_pb5[1])
    content += wire(r2_p1[0], j2_pb5[1], r2_p1[0], r2_p1[1])
    content += wire(r2_p2[0], r2_p2[1], r2_p2[0], 134.62)
    content += gnd_sym(r2_p2[0], 134.62)
    
    content += no_conn(j2_pa6[0], j2_pa6[1])
    content += no_conn(j2_pa7[0], j2_pa7[1])
    content += wire(j2_pa1[0], j2_pa1[1], j2_pa1[0], 134.62)
    content += gnd_sym(j2_pa1[0], 134.62)
    content += wire(j2_ps1[0], j2_ps1[1], j2_ps1[0], 134.62)
    content += gnd_sym(j2_ps1[0], 134.62)
    
    # -------------------------------------------------------------------------
    # 3. TPS2121 Power Mux Block
    # -------------------------------------------------------------------------
    u1_x, u1_y = 165.10, 88.90
    content += sym_inst("Power_Management:TPS2121RUXR", "U1", "TPS2121RUXR", u1_x, u1_y, 0,
                        "Package_DFN_QFN:Texas_RUX0012A",
                        "https://www.ti.com/lit/ds/symlink/tps2121.pdf",
                        "2.8V-22V, 4A Priority Power MUX with Seamless Switchover, VQFN-12",
                        pins=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
    
    r3_x, r3_y = 139.70, 81.28
    content += sym_inst("Device:R", "R3", "30k (1%)", r3_x, r3_y, 0,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Resistor, 30k, 1%, 0.1W, 0603",
                        pins=["1", "2"])
    
    r4_x, r4_y = 139.70, 93.98
    content += sym_inst("Device:R", "R4", "10k (1%)", r4_x, r4_y, 0,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Resistor, 10k, 1%, 0.1W, 0603",
                        pins=["1", "2"])
    
    c6_x, c6_y = 187.96, 86.36
    content += sym_inst("Device:C", "C6", "10nF/25V (X7R)", c6_x, c6_y, 90,
                        "Capacitor_SMD:C_0603_1608Metric",
                        "~", "Ceramic Capacitor, 10nF, 25V, X7R, 0603",
                        pins=["1", "2"])
    
    r5_x, r5_y = 187.96, 93.98
    content += sym_inst("Device:R", "R5", "28.7k (1% / 3.5A)", r5_x, r5_y, 90,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Resistor, 28.7k, 1%, 0.1W, 0603",
                        pins=["1", "2"])
    
    r6_x, r6_y = 203.20, 83.82
    content += sym_inst("Device:R", "R6", "100k (1%)", r6_x, r6_y, 0,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Resistor, 100k, 1%, 0.1W, 0603",
                        pins=["1", "2"])
    
    c4_x, c4_y = 215.90, 88.90
    content += sym_inst("Device:C", "C4", "22uF/16V (X5R)", c4_x, c4_y, 0,
                        "Capacitor_SMD:C_0805_2012Metric",
                        "~", "Ceramic Capacitor, 22uF, 16V, X5R, 0805",
                        pins=["1", "2"])
    
    c5_x, c5_y = 226.06, 88.90
    content += sym_inst("Device:C", "C5", "0.1uF/25V (X7R)", c5_x, c5_y, 0,
                        "Capacitor_SMD:C_0603_1608Metric",
                        "~", "Ceramic Capacitor, 0.1uF, 25V, X7R, 0603",
                        pins=["1", "2"])
    
    tp3_x, tp3_y = 238.76, 73.66
    content += sym_inst("Connector:TestPoint", "TP3", "TP_VBUS_MUX", tp3_x, tp3_y, 0,
                        "TestPoint:TestPoint_Pad_D1.5mm",
                        "~", "Test Point Pad 1.5mm, VBUS_MUX",
                        pins=["1"])
    
    tp_st_x, tp_st_y = 203.20, 96.52
    content += sym_inst("Connector:TestPoint", "TP_MUX_ST", "TP_MUX_ST", tp_st_x, tp_st_y, 0,
                        "TestPoint:TestPoint_Pad_D1.5mm",
                        "~", "Test Point Pad 1.5mm, Status of TPS2121",
                        pins=["1"])
    
    u1_p7 = pin_pos(cust_syms.SYM_TPS2121, u1_x, u1_y, "7", 0)
    u1_p2 = pin_pos(cust_syms.SYM_TPS2121, u1_x, u1_y, "2", 0)
    u1_p6 = pin_pos(cust_syms.SYM_TPS2121, u1_x, u1_y, "6", 0)
    u1_p3 = pin_pos(cust_syms.SYM_TPS2121, u1_x, u1_y, "3", 0)
    u1_p5 = pin_pos(cust_syms.SYM_TPS2121, u1_x, u1_y, "5", 0)
    u1_p4 = pin_pos(cust_syms.SYM_TPS2121, u1_x, u1_y, "4", 0)
    u1_p12 = pin_pos(cust_syms.SYM_TPS2121, u1_x, u1_y, "12", 0)
    u1_p1 = pin_pos(cust_syms.SYM_TPS2121, u1_x, u1_y, "1", 0)
    u1_p8 = pin_pos(cust_syms.SYM_TPS2121, u1_x, u1_y, "8", 0)
    u1_p11 = pin_pos(cust_syms.SYM_TPS2121, u1_x, u1_y, "11", 0)
    u1_p10 = pin_pos(cust_syms.SYM_TPS2121, u1_x, u1_y, "10", 0)
    u1_p9 = pin_pos(cust_syms.SYM_TPS2121, u1_x, u1_y, "9", 0)
    
    r3_p1 = pin_pos(base_syms.SYM_R, r3_x, r3_y, "1", 0)
    r3_p2 = pin_pos(base_syms.SYM_R, r3_x, r3_y, "2", 0)
    r4_p1 = pin_pos(base_syms.SYM_R, r4_x, r4_y, "1", 0)
    r4_p2 = pin_pos(base_syms.SYM_R, r4_x, r4_y, "2", 0)
    c6_p1 = pin_pos(base_syms.SYM_C, c6_x, c6_y, "1", 90)
    c6_p2 = pin_pos(base_syms.SYM_C, c6_x, c6_y, "2", 90)
    r5_p1 = pin_pos(base_syms.SYM_R, r5_x, r5_y, "1", 90)
    r5_p2 = pin_pos(base_syms.SYM_R, r5_x, r5_y, "2", 90)
    r6_p1 = pin_pos(base_syms.SYM_R, r6_x, r6_y, "1", 0)
    r6_p2 = pin_pos(base_syms.SYM_R, r6_x, r6_y, "2", 0)
    c4_p1 = pin_pos(base_syms.SYM_C, c4_x, c4_y, "1", 0)
    c4_p2 = pin_pos(base_syms.SYM_C, c4_x, c4_y, "2", 0)
    c5_p1 = pin_pos(base_syms.SYM_C, c5_x, c5_y, "1", 0)
    c5_p2 = pin_pos(base_syms.SYM_C, c5_x, c5_y, "2", 0)
    tp3_p1 = pin_pos(base_syms.SYM_TESTPOINT, tp3_x, tp3_y, "1", 0)
    tp_st_p1 = pin_pos(base_syms.SYM_TESTPOINT, tp_st_x, tp_st_y, "1", 0)
    
    # IN1 Connection
    content += wire(127.00, 50.80, 134.62, 50.80)
    content += wire(134.62, 50.80, 134.62, u1_p7[1])
    content += wire(134.62, u1_p7[1], r3_p1[0], u1_p7[1])
    content += junc(r3_p1[0], u1_p7[1])
    content += wire(r3_p1[0], u1_p7[1], r3_p1[0], r3_p1[1])
    content += wire(r3_p1[0], u1_p7[1], u1_p7[0], u1_p7[1])
    
    # PR1 Divider Connection
    content += wire(r3_p2[0], r3_p2[1], r3_p2[0], u1_p6[1])
    content += junc(r3_p2[0], u1_p6[1])
    content += wire(r3_p2[0], u1_p6[1], u1_p6[0], u1_p6[1])
    content += wire(r3_p2[0], u1_p6[1], r4_p1[0], r4_p1[1])
    content += wire(r4_p2[0], r4_p2[1], r4_p2[0], 106.68)
    content += gnd_sym(r4_p2[0], 106.68)
    
    # IN2 Connection from USB_5V_IN
    content += wire(106.68, 109.22, 134.62, 109.22)
    content += wire(134.62, 109.22, 134.62, u1_p2[1])
    content += wire(134.62, u1_p2[1], u1_p2[0], u1_p2[1])
    
    # Ground bus for CP2, OV1, OV2, GND pins (3, 5, 4, 12)
    content += wire(u1_p3[0], u1_p3[1], 147.32, u1_p3[1])
    content += junc(147.32, u1_p3[1])
    content += wire(u1_p5[0], u1_p5[1], 147.32, u1_p5[1])
    content += junc(147.32, u1_p5[1])
    content += wire(u1_p4[0], u1_p4[1], 147.32, u1_p4[1])
    content += junc(147.32, u1_p4[1])
    content += wire(u1_p12[0], u1_p12[1], 147.32, u1_p12[1])
    content += junc(147.32, u1_p12[1])
    content += wire(147.32, u1_p3[1], 147.32, 106.68)
    content += gnd_sym(147.32, 106.68)
    content += pwr_flag(147.32, 106.68)
    
    # Connect OUT pins 1 and 8 together
    content += wire(u1_p1[0], u1_p1[1], 182.88, u1_p1[1])
    content += wire(u1_p8[0], u1_p8[1], 182.88, u1_p8[1])
    content += wire(182.88, u1_p1[1], 182.88, u1_p8[1])
    content += junc(182.88, u1_p1[1])
    
    # VBUS_MUX output rail along Y = 78.74
    content += wire(182.88, u1_p1[1], r6_p1[0], u1_p1[1])
    content += junc(r6_p1[0], u1_p1[1])
    content += wire(r6_p1[0], u1_p1[1], r6_p1[0], r6_p1[1])
    
    content += wire(r6_p1[0], u1_p1[1], c4_p1[0], u1_p1[1])
    content += junc(c4_p1[0], u1_p1[1])
    content += wire(c4_p1[0], u1_p1[1], c4_p1[0], c4_p1[1])
    content += wire(c4_p2[0], c4_p2[1], c4_p2[0], 101.60)
    content += gnd_sym(c4_p2[0], 101.60)
    
    content += wire(c4_p1[0], u1_p1[1], c5_p1[0], u1_p1[1])
    content += junc(c5_p1[0], u1_p1[1])
    content += wire(c5_p1[0], u1_p1[1], c5_p1[0], c5_p1[1])
    content += wire(c5_p2[0], c5_p2[1], c5_p2[0], 101.60)
    content += gnd_sym(c5_p2[0], 101.60)
    
    content += wire(c5_p1[0], u1_p1[1], tp3_p1[0], u1_p1[1])
    content += junc(tp3_p1[0], u1_p1[1])
    content += wire(tp3_p1[0], u1_p1[1], tp3_p1[0], tp3_p1[1])
    content += wire(tp3_p1[0], u1_p1[1], 248.92, u1_p1[1])
    content += global_lbl("VBUS_MUX", 248.92, u1_p1[1], 0, "bidirectional")
    content += hier_lbl("VBUS_MUX", 248.92, u1_p1[1] + 5.08, 0, "output")
    
    # SS capacitor C6
    content += wire(u1_p11[0], u1_p11[1], c6_p1[0], c6_p1[1])
    content += wire(c6_p2[0], c6_p2[1], 194.31, c6_p2[1])
    content += gnd_sym(194.31, c6_p2[1])
    
    # ILIM resistor R5
    content += wire(u1_p10[0], u1_p10[1], 180.34, u1_p10[1])
    content += wire(180.34, u1_p10[1], 180.34, r5_p1[1])
    content += wire(180.34, r5_p1[1], r5_p1[0], r5_p1[1])
    content += wire(r5_p2[0], r5_p2[1], 194.31, r5_p2[1])
    content += gnd_sym(194.31, r5_p2[1])
    
    # ST pin 9 pullup to R6 and test point
    content += wire(u1_p9[0], u1_p9[1], r6_p2[0], u1_p9[1])
    content += junc(r6_p2[0], u1_p9[1])
    content += wire(r6_p2[0], u1_p9[1], r6_p2[0], r6_p2[1])
    content += wire(r6_p2[0], u1_p9[1], tp_st_p1[0], tp_st_p1[1])
    content += wire(tp_st_p1[0], tp_st_p1[1], tp_st_p1[0], 104.14)
    content += global_lbl("MUX_ST", tp_st_p1[0], 104.14, 0, "output")
    
    # Annotations & Rules Text
    content += sch_text("KHỐI CHỌN NGUỒN ĐẦU VÀO TỰ ĐỘNG (SEAMLESS POWER MULTIPLEXER)", 25.40, 22.86, 2.0, True)
    content += sch_text("Ưu tiên: VEHICLE_5V_IN (PR1 threshold = 4.24V) | Dự phòng: USB_5V_IN", 25.40, 30.48, 1.3, False)
    content += sch_text("Bảo vệ quá dòng: ILIM = 3.5A (R5 = 28.7k) | Khóa dòng ngược tích hợp", 25.40, 35.56, 1.3, False)
    content += sch_text("CỔNG VÀO NGUỒN XE (5V REGULATED)", 25.40, 43.18, 1.4, True)
    content += sch_text("CỔNG VÀO USB-C (SINK CC1/CC2 5.1k)", 25.40, 99.06, 1.4, True)
    content += sch_text("TPS2121 MUX OUTPUT: VBUS_MUX (CUNG CẤP CHO BQ25895)", 165.10, 48.26, 1.4, True)
    
    content += ")\n"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Sheet 1 generated: {out_path}")


# =============================================================================
# SHEET 2: 02_CHARGER_BATTERY.kicad_sch
# =============================================================================
def build_sheet2(out_path):
    content = make_header("KHỐI SẠC PIN LI-ION 1S & BẢO VỆ PIN (BQ25895 + DW01A/FS8205A)", 3, 5)
    
    # -------------------------------------------------------------------------
    # 1. 1S 18650 Battery Connector & Dual FS8205A Protection Circuit
    # -------------------------------------------------------------------------
    # J3 Battery Connector (JST-VH 3.96mm 10A)
    j3_x, j3_y = 35.56, 50.80
    content += sym_inst("Connector:Conn_01x02_Pin", "J3", "18650_CELL_IN", j3_x, j3_y, 0,
                        "Connector_JST:JST_VH_B2P-VH_1x02_P3.96mm_Vertical",
                        "https://www.jst-mfg.com/product/pdf/eng/eVH.pdf",
                        "1S 18650 Li-ion High-Current Connector, 3.96mm, 10A rating",
                        pins=["1", "2"])
    
    # DW01A-G Protection IC U3
    u3_x, u3_y = 60.96, 81.28
    content += sym_inst("Battery_Management:DW01A", "U3", "DW01A-G", u3_x, u3_y, 0,
                        "Package_TO_SOT_SMD:SOT-23-6",
                        "https://datasheet.lcsc.com/lcsc/1811151441_Fortune-Semicon-DW01A-G_C24339.pdf",
                        "Single Cell Li-ion Battery Protection IC, 4.30V OVP, 2.40V UVP, SOT-23-6",
                        pins=["1", "2", "3", "4", "5", "6"])
    
    # Dual FS8205A MOSFETs Q1 and Q2 in parallel (RDSon = 25mOhm total)
    q1_x, q1_y = 91.44, 81.28
    content += sym_inst("Transistor_FET:FS8205A", "Q1", "FS8205A (Dual N-FET)", q1_x, q1_y, 0,
                        "Package_SO:TSSOP-8_4.4x3mm_P0.65mm",
                        "https://datasheet.lcsc.com/lcsc/1811151441_Fortune-Semicon-FS8205A_C32254.pdf",
                        "Dual N-Channel Power MOSFET, 20V 6A, 25mOhm per pair, TSSOP-8",
                        pins=["1", "2", "3", "4", "5", "6", "7", "8"])
    
    q2_x, q2_y = 119.38, 81.28
    content += sym_inst("Transistor_FET:FS8205A", "Q2", "FS8205A (Dual N-FET)", q2_x, q2_y, 0,
                        "Package_SO:TSSOP-8_4.4x3mm_P0.65mm",
                        "https://datasheet.lcsc.com/lcsc/1811151441_Fortune-Semicon-FS8205A_C32254.pdf",
                        "Dual N-Channel Power MOSFET in parallel for 12A / 6.0A trip threshold, TSSOP-8",
                        pins=["1", "2", "3", "4", "5", "6", "7", "8"])
    
    # DW01A Support Passives: R15 (100R VCC filter), C15 (0.1uF), R16 (1k CS filter)
    r15_x, r15_y = 48.26, 68.58
    content += sym_inst("Device:R", "R15", "100 (1%)", r15_x, r15_y, 90,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Resistor, 100 Ohm, 1%, 0.1W, 0603",
                        pins=["1", "2"])
    
    c15_x, c15_y = 48.26, 76.20
    content += sym_inst("Device:C", "C15", "0.1uF/16V", c15_x, c15_y, 0,
                        "Capacitor_SMD:C_0603_1608Metric",
                        "~", "Ceramic Capacitor, 0.1uF, 16V, X7R, 0603",
                        pins=["1", "2"])
    
    r16_x, r16_y = 48.26, 88.90
    content += sym_inst("Device:R", "R16", "1.0k (1%)", r16_x, r16_y, 90,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Resistor, 1.0k, 1%, 0.1W, 0603",
                        pins=["1", "2"])
    
    # -------------------------------------------------------------------------
    # 2. Battery Voltage Measurement Divider (GPIO1 = ADC_VBAT_SENSE)
    # -------------------------------------------------------------------------
    r17_x, r17_y = 76.20, 40.64
    content += sym_inst("Device:R", "R17", "100k (0.1% / 25ppm)", r17_x, r17_y, 0,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Precision Resistor, 100k, 0.1%, 25ppm/C, 0603",
                        pins=["1", "2"])
    
    r18_x, r18_y = 76.20, 53.34
    content += sym_inst("Device:R", "R18", "100k (0.1% / 25ppm)", r18_x, r18_y, 0,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Precision Resistor, 100k, 0.1%, 25ppm/C, 0603",
                        pins=["1", "2"])
    
    c17_x, c17_y = 86.36, 53.34
    content += sym_inst("Device:C", "C17", "100nF/25V (X7R)", c17_x, c17_y, 0,
                        "Capacitor_SMD:C_0603_1608Metric",
                        "~", "Ceramic Capacitor, 100nF, 25V, X7R, 0603",
                        pins=["1", "2"])
    
    tp_adc_x, tp_adc_y = 96.52, 45.72
    content += sym_inst("Connector:TestPoint", "TP_ADC", "TP_ADC_VBAT", tp_adc_x, tp_adc_y, 0,
                        "TestPoint:TestPoint_Pad_D1.5mm",
                        "~", "Test Point Pad 1.5mm, ADC_VBAT_SENSE tied to GPIO1",
                        pins=["1"])
    
    tp_vbat_x, tp_vbat_y = 48.26, 40.64
    content += sym_inst("Connector:TestPoint", "TP_VBAT", "TP_VBAT", tp_vbat_x, tp_vbat_y, 0,
                        "TestPoint:TestPoint_Pad_D1.5mm",
                        "~", "Test Point Pad 1.5mm, VBAT protected rail",
                        pins=["1"])
    
    # -------------------------------------------------------------------------
    # 3. BQ25895 Fast Charger & NVDC Power-Path Management
    # -------------------------------------------------------------------------
    u2_x, u2_y = 177.80, 88.90
    content += sym_inst("Battery_Management:BQ25895RTWR", "U2", "BQ25895RTWR", u2_x, u2_y, 0,
                        "Package_DFN_QFN:Texas_RTW0024A",
                        "https://www.ti.com/lit/ds/symlink/bq25895.pdf",
                        "I2C Controlled Single-Cell 5A Fast Charger with NVDC Power Path Management, WQFN-24",
                        pins=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                              "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                              "21", "22", "23", "24", "25"])
    
    # Input Decoupling Caps: C7 (VBUS 10uF), C8 (PMID 10uF), C9 (REGN 4.7uF)
    c7_x, c7_y = 149.86, 71.12
    content += sym_inst("Device:C", "C7", "10uF/25V (X7R)", c7_x, c7_y, 0,
                        "Capacitor_SMD:C_0805_2012Metric",
                        "~", "Ceramic Capacitor, 10uF, 25V, X7R, 0805",
                        pins=["1", "2"])
    
    c8_x, c8_y = 149.86, 78.74
    content += sym_inst("Device:C", "C8", "10uF/25V (X7R)", c8_x, c8_y, 0,
                        "Capacitor_SMD:C_0805_2012Metric",
                        "~", "High-Frequency Ceramic Capacitor, 10uF, 25V, X7R, 0805",
                        pins=["1", "2"])
    
    c9_x, c9_y = 149.86, 86.36
    content += sym_inst("Device:C", "C9", "4.7uF/10V (X5R)", c9_x, c9_y, 0,
                        "Capacitor_SMD:C_0603_1608Metric",
                        "~", "Ceramic Capacitor, 4.7uF, 10V, X5R, 0603",
                        pins=["1", "2"])
    
    # ILIM resistor R8 (158 Ohm -> 3.25A limit)
    r8_x, r8_y = 149.86, 96.52
    content += sym_inst("Device:R", "R8", "158 (1% / 3.25A)", r8_x, r8_y, 90,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Current Limit Resistor, 158 Ohm, 1%, 0603",
                        pins=["1", "2"])
    
    # TS NTC Divider: R9 (5.23k), R10 (30.1k)
    r9_x, r9_y = 139.70, 91.44
    content += sym_inst("Device:R", "R9", "5.23k (1%)", r9_x, r9_y, 0,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Resistor, 5.23k, 1%, 0603 (JEITA Upper)",
                        pins=["1", "2"])
    
    r10_x, r10_y = 139.70, 101.60
    content += sym_inst("Device:R", "R10", "30.1k (1%)", r10_x, r10_y, 0,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Resistor, 30.1k, 1%, 0603 (JEITA Lower)",
                        pins=["1", "2"])
    
    # Inductor L1 (1.0uH 7.5A) and Bootstrap Cap C10 (47nF)
    l1_x, l1_y = 210.82, 73.66
    content += sym_inst("Device:L", "L1", "1.0uH (7.5A Sat)", l1_x, l1_y, 90,
                        "Inductor_SMD:L_Bourns_SRP6540",
                        "https://www.bourns.com/docs/product-datasheets/srp6540.pdf",
                        "Shielded Power Inductor, 1.0uH, 7.5A Isat, Low DCR SMD",
                        pins=["1", "2"])
    
    c10_x, c10_y = 203.20, 88.90
    content += sym_inst("Device:C", "C10", "47nF/25V (X7R)", c10_x, c10_y, 90,
                        "Capacitor_SMD:C_0603_1608Metric",
                        "~", "Bootstrap Ceramic Capacitor, 47nF, 25V, X7R, 0603",
                        pins=["1", "2"])
    
    # SYS Output Capacitors: C11 (22uF), C12 (22uF)
    c11_x, c11_y = 226.06, 78.74
    content += sym_inst("Device:C", "C11", "22uF/16V (X5R)", c11_x, c11_y, 0,
                        "Capacitor_SMD:C_0805_2012Metric",
                        "~", "Ceramic Capacitor, 22uF, 16V, X5R, 0805",
                        pins=["1", "2"])
    
    c12_x, c12_y = 236.22, 78.74
    content += sym_inst("Device:C", "C12", "22uF/16V (X5R)", c12_x, c12_y, 0,
                        "Capacitor_SMD:C_0805_2012Metric",
                        "~", "Ceramic Capacitor, 22uF, 16V, X5R, 0805",
                        pins=["1", "2"])
    
    # BAT Filter Cap C13 (10uF)
    c13_x, c13_y = 210.82, 83.82
    content += sym_inst("Device:C", "C13", "10uF/16V (X7R)", c13_x, c13_y, 0,
                        "Capacitor_SMD:C_0805_2012Metric",
                        "~", "Ceramic Capacitor, 10uF, 16V, X7R, 0805",
                        pins=["1", "2"])
    
    tp_sys_x, tp_sys_y = 246.38, 66.04
    content += sym_inst("Connector:TestPoint", "TP_SYS", "TP_SYS", tp_sys_x, tp_sys_y, 0,
                        "TestPoint:TestPoint_Pad_D1.5mm",
                        "~", "Test Point Pad 1.5mm, SYS NVDC Rail",
                        pins=["1"])
    
    # Pullup Resistors for STAT, INT, SCL, SDA to 3V3_SYS
    r11_x, r11_y = 205.74, 99.06
    content += sym_inst("Device:R", "R11", "10k (1%)", r11_x, r11_y, 0,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Pullup Resistor, 10k, 1%, 0603",
                        pins=["1", "2"])
    
    r12_x, r12_y = 215.90, 99.06
    content += sym_inst("Device:R", "R12", "10k (1%)", r12_x, r12_y, 0,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Pullup Resistor, 10k, 1%, 0603",
                        pins=["1", "2"])
    
    r13_x, r13_y = 226.06, 99.06
    content += sym_inst("Device:R", "R13", "4.7k (1%)", r13_x, r13_y, 0,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "I2C Pullup Resistor, 4.7k, 1%, 0603",
                        pins=["1", "2"])
    
    r14_x, r14_y = 236.22, 99.06
    content += sym_inst("Device:R", "R14", "4.7k (1%)", r14_x, r14_y, 0,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "I2C Pullup Resistor, 4.7k, 1%, 0603",
                        pins=["1", "2"])
    
    # -------------------------------------------------------------------------
    # Pin Positions Calculation
    # -------------------------------------------------------------------------
    j3_p1 = pin_pos(base_syms.SYM_CONN_02, j3_x, j3_y, "1", 0)
    j3_p2 = pin_pos(base_syms.SYM_CONN_02, j3_x, j3_y, "2", 0)
    
    u3_p5 = pin_pos(cust_syms.SYM_DW01A, u3_x, u3_y, "5", 0)
    u3_p2 = pin_pos(cust_syms.SYM_DW01A, u3_x, u3_y, "2", 0)
    u3_p4 = pin_pos(cust_syms.SYM_DW01A, u3_x, u3_y, "4", 0)
    u3_p6 = pin_pos(cust_syms.SYM_DW01A, u3_x, u3_y, "6", 0)
    u3_p3 = pin_pos(cust_syms.SYM_DW01A, u3_x, u3_y, "3", 0)
    u3_p1 = pin_pos(cust_syms.SYM_DW01A, u3_x, u3_y, "1", 0)
    
    q1_p4 = pin_pos(cust_syms.SYM_FS8205A, q1_x, q1_y, "4", 0)
    q1_p5 = pin_pos(cust_syms.SYM_FS8205A, q1_x, q1_y, "5", 0)
    q1_p1 = pin_pos(cust_syms.SYM_FS8205A, q1_x, q1_y, "1", 0)
    q1_p8 = pin_pos(cust_syms.SYM_FS8205A, q1_x, q1_y, "8", 0)
    q1_p2 = pin_pos(cust_syms.SYM_FS8205A, q1_x, q1_y, "2", 0)
    q1_p3 = pin_pos(cust_syms.SYM_FS8205A, q1_x, q1_y, "3", 0)
    q1_p6 = pin_pos(cust_syms.SYM_FS8205A, q1_x, q1_y, "6", 0)
    q1_p7 = pin_pos(cust_syms.SYM_FS8205A, q1_x, q1_y, "7", 0)
    
    q2_p4 = pin_pos(cust_syms.SYM_FS8205A, q2_x, q2_y, "4", 0)
    q2_p5 = pin_pos(cust_syms.SYM_FS8205A, q2_x, q2_y, "5", 0)
    q2_p1 = pin_pos(cust_syms.SYM_FS8205A, q2_x, q2_y, "1", 0)
    q2_p8 = pin_pos(cust_syms.SYM_FS8205A, q2_x, q2_y, "8", 0)
    q2_p2 = pin_pos(cust_syms.SYM_FS8205A, q2_x, q2_y, "2", 0)
    q2_p3 = pin_pos(cust_syms.SYM_FS8205A, q2_x, q2_y, "3", 0)
    q2_p6 = pin_pos(cust_syms.SYM_FS8205A, q2_x, q2_y, "6", 0)
    q2_p7 = pin_pos(cust_syms.SYM_FS8205A, q2_x, q2_y, "7", 0)
    
    r15_p1 = pin_pos(base_syms.SYM_R, r15_x, r15_y, "1", 90)
    r15_p2 = pin_pos(base_syms.SYM_R, r15_x, r15_y, "2", 90)
    c15_p1 = pin_pos(base_syms.SYM_C, c15_x, c15_y, "1", 0)
    c15_p2 = pin_pos(base_syms.SYM_C, c15_x, c15_y, "2", 0)
    r16_p1 = pin_pos(base_syms.SYM_R, r16_x, r16_y, "1", 90)
    r16_p2 = pin_pos(base_syms.SYM_R, r16_x, r16_y, "2", 90)
    
    r17_p1 = pin_pos(base_syms.SYM_R, r17_x, r17_y, "1", 0)
    r17_p2 = pin_pos(base_syms.SYM_R, r17_x, r17_y, "2", 0)
    r18_p1 = pin_pos(base_syms.SYM_R, r18_x, r18_y, "1", 0)
    r18_p2 = pin_pos(base_syms.SYM_R, r18_x, r18_y, "2", 0)
    c17_p1 = pin_pos(base_syms.SYM_C, c17_x, c17_y, "1", 0)
    c17_p2 = pin_pos(base_syms.SYM_C, c17_x, c17_y, "2", 0)
    tp_adc_p1 = pin_pos(base_syms.SYM_TESTPOINT, tp_adc_x, tp_adc_y, "1", 0)
    tp_vbat_p1 = pin_pos(base_syms.SYM_TESTPOINT, tp_vbat_x, tp_vbat_y, "1", 0)
    
    u2_p1 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "1", 0)
    u2_p23 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "23", 0)
    u2_p22 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "22", 0)
    u2_p9 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "9", 0)
    u2_p8 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "8", 0)
    u2_p12 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "12", 0)
    u2_p10 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "10", 0)
    u2_p11 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "11", 0)
    u2_p24 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "24", 0)
    u2_p2 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "2", 0)
    u2_p3 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "3", 0)
    u2_p17 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "17", 0)
    u2_p18 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "18", 0)
    
    u2_p15 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "15", 0)
    u2_p16 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "16", 0)
    u2_p13 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "13", 0)
    u2_p14 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "14", 0)
    u2_p19 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "19", 0)
    u2_p20 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "20", 0)
    u2_p21 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "21", 0)
    u2_p4 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "4", 0)
    u2_p7 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "7", 0)
    u2_p5 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "5", 0)
    u2_p6 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "6", 0)
    u2_p25 = pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "25", 0)
    
    c7_p1 = pin_pos(base_syms.SYM_C, c7_x, c7_y, "1", 0)
    c7_p2 = pin_pos(base_syms.SYM_C, c7_x, c7_y, "2", 0)
    c8_p1 = pin_pos(base_syms.SYM_C, c8_x, c8_y, "1", 0)
    c8_p2 = pin_pos(base_syms.SYM_C, c8_x, c8_y, "2", 0)
    c9_p1 = pin_pos(base_syms.SYM_C, c9_x, c9_y, "1", 0)
    c9_p2 = pin_pos(base_syms.SYM_C, c9_x, c9_y, "2", 0)
    r8_p1 = pin_pos(base_syms.SYM_R, r8_x, r8_y, "1", 90)
    r8_p2 = pin_pos(base_syms.SYM_R, r8_x, r8_y, "2", 90)
    r9_p1 = pin_pos(base_syms.SYM_R, r9_x, r9_y, "1", 0)
    r9_p2 = pin_pos(base_syms.SYM_R, r9_x, r9_y, "2", 0)
    r10_p1 = pin_pos(base_syms.SYM_R, r10_x, r10_y, "1", 0)
    r10_p2 = pin_pos(base_syms.SYM_R, r10_x, r10_y, "2", 0)
    
    l1_p1 = pin_pos(base_syms.SYM_L, l1_x, l1_y, "1", 90)
    l1_p2 = pin_pos(base_syms.SYM_L, l1_x, l1_y, "2", 90)
    c10_p1 = pin_pos(base_syms.SYM_C, c10_x, c10_y, "1", 90)
    c10_p2 = pin_pos(base_syms.SYM_C, c10_x, c10_y, "2", 90)
    
    c11_p1 = pin_pos(base_syms.SYM_C, c11_x, c11_y, "1", 0)
    c11_p2 = pin_pos(base_syms.SYM_C, c11_x, c11_y, "2", 0)
    c12_p1 = pin_pos(base_syms.SYM_C, c12_x, c12_y, "1", 0)
    c12_p2 = pin_pos(base_syms.SYM_C, c12_x, c12_y, "2", 0)
    c13_p1 = pin_pos(base_syms.SYM_C, c13_x, c13_y, "1", 0)
    c13_p2 = pin_pos(base_syms.SYM_C, c13_x, c13_y, "2", 0)
    tp_sys_p1 = pin_pos(base_syms.SYM_TESTPOINT, tp_sys_x, tp_sys_y, "1", 0)
    
    r11_p1 = pin_pos(base_syms.SYM_R, r11_x, r11_y, "1", 0)
    r11_p2 = pin_pos(base_syms.SYM_R, r11_x, r11_y, "2", 0)
    r12_p1 = pin_pos(base_syms.SYM_R, r12_x, r12_y, "1", 0)
    r12_p2 = pin_pos(base_syms.SYM_R, r12_x, r12_y, "2", 0)
    r13_p1 = pin_pos(base_syms.SYM_R, r13_x, r13_y, "1", 0)
    r13_p2 = pin_pos(base_syms.SYM_R, r13_x, r13_y, "2", 0)
    r14_p1 = pin_pos(base_syms.SYM_R, r14_x, r14_y, "1", 0)
    r14_p2 = pin_pos(base_syms.SYM_R, r14_x, r14_y, "2", 0)
    
    # -------------------------------------------------------------------------
    # Wiring Section
    # -------------------------------------------------------------------------
    # 1. Battery Connector J3 Positive (CELL_POS) to VBAT Rail
    content += wire(j3_p1[0], j3_p1[1], tp_vbat_p1[0], j3_p1[1])
    content += junc(tp_vbat_p1[0], j3_p1[1])
    content += wire(tp_vbat_p1[0], j3_p1[1], tp_vbat_p1[0], tp_vbat_p1[1])
    content += pwr_flag(tp_vbat_p1[0], tp_vbat_p1[1])
    
    # VBAT connects to R15 (DW01A VCC filter)
    content += wire(tp_vbat_p1[0], j3_p1[1], r15_p1[0], j3_p1[1])
    content += junc(r15_p1[0], j3_p1[1])
    content += wire(r15_p1[0], j3_p1[1], r15_p1[0], r15_p1[1])
    
    # R15 to DW01A VCC (pin 5) and C15
    content += wire(r15_p2[0], r15_p2[1], u3_p5[0], r15_p2[1])
    content += junc(u3_p5[0], r15_p2[1])
    content += wire(u3_p5[0], r15_p2[1], u3_p5[0], u3_p5[1])
    content += wire(u3_p5[0], r15_p2[1], c15_p1[0], r15_p2[1])
    content += wire(c15_p1[0], r15_p2[1], c15_p1[0], c15_p1[1])
    
    # VBAT connects to ADC Divider (R17)
    content += wire(r15_p1[0], j3_p1[1], r17_p1[0], j3_p1[1])
    content += junc(r17_p1[0], j3_p1[1])
    content += wire(r17_p1[0], j3_p1[1], r17_p1[0], r17_p1[1])
    
    # VBAT rail continues to BQ25895 BAT pins (13, 14)
    content += wire(r17_p1[0], j3_p1[1], 195.58, j3_p1[1])
    content += wire(195.58, j3_p1[1], u2_p13[0], u2_p13[1])
    content += junc(u2_p13[0], u2_p13[1])
    content += wire(u2_p13[0], u2_p13[1], u2_p14[0], u2_p14[1])
    content += wire(u2_p13[0], u2_p13[1], c13_p1[0], u2_p13[1])
    content += junc(c13_p1[0], u2_p13[1])
    content += wire(c13_p1[0], u2_p13[1], c13_p1[0], c13_p1[1])
    content += wire(c13_p2[0], c13_p2[1], c13_p2[0], 93.98)
    content += gnd_sym(c13_p2[0], 93.98)
    
    # Global & Hierarchical Labels for VBAT
    content += wire(c13_p1[0], u2_p13[1], 248.92, u2_p13[1])
    content += global_lbl("VBAT", 248.92, u2_p13[1], 0, "bidirectional")
    content += hier_lbl("VBAT", 248.92, u2_p13[1] + 5.08, 0, "output")
    
    # ADC Divider Wires
    content += wire(r17_p2[0], r17_p2[1], r17_p2[0], r18_p1[1])
    content += junc(r17_p2[0], r18_p1[1])
    content += wire(r17_p2[0], r18_p1[1], r18_p1[0], r18_p1[1])
    content += wire(r18_p2[0], r18_p2[1], r18_p2[0], 63.50)
    content += gnd_sym(r18_p2[0], 63.50)
    
    content += wire(r17_p2[0], r18_p1[1], c17_p1[0], r18_p1[1])
    content += junc(c17_p1[0], r18_p1[1])
    content += wire(c17_p1[0], r18_p1[1], c17_p1[0], c17_p1[1])
    content += wire(c17_p2[0], c17_p2[1], c17_p2[0], 63.50)
    content += gnd_sym(c17_p2[0], 63.50)
    
    content += wire(c17_p1[0], r18_p1[1], tp_adc_p1[0], r18_p1[1])
    content += junc(tp_adc_p1[0], r18_p1[1])
    content += wire(tp_adc_p1[0], r18_p1[1], tp_adc_p1[0], tp_adc_p1[1])
    content += wire(tp_adc_p1[0], r18_p1[1], 114.30, r18_p1[1])
    content += global_lbl("ADC_VBAT_SENSE", 114.30, r18_p1[1], 0, "output")
    content += hier_lbl("ADC_VBAT_SENSE", 114.30, r18_p1[1] + 5.08, 0, "output")
    
    # 2. Battery Connector J3 Negative (CELL_NEG) to Protection Circuit
    content += wire(j3_p2[0], j3_p2[1], 40.64, 83.82)
    content += wire(40.64, 83.82, u3_p6[0], 83.82)
    content += junc(u3_p6[0], 83.82)
    content += wire(u3_p6[0], 83.82, u3_p6[0], u3_p6[1])
    content += wire(c15_p2[0], c15_p2[1], c15_p2[0], 83.82)
    content += junc(c15_p2[0], 83.82)
    
    # CELL_NEG connects to Source S1 of Q1 and Q2
    content += wire(u3_p6[0], 83.82, 73.66, 83.82)
    content += wire(73.66, 83.82, 73.66, q1_p2[1])
    content += wire(73.66, q1_p2[1], q1_p2[0], q1_p2[1])
    content += junc(q1_p2[0], q1_p2[1])
    content += wire(q1_p2[0], q1_p2[1], q1_p3[0], q1_p3[1])
    content += wire(q1_p2[0], q1_p2[1], q2_p2[0], q2_p2[1])
    content += junc(q2_p2[0], q2_p2[1])
    content += wire(q2_p2[0], q2_p2[1], q2_p3[0], q2_p3[1])
    
    # DW01A Gate Controls: OD (Pin 1) to G1 (Pin 4), OC (Pin 3) to G2 (Pin 5)
    content += wire(u3_p1[0], u3_p1[1], q1_p4[0], u3_p1[1])
    content += junc(q1_p4[0], u3_p1[1])
    content += wire(q1_p4[0], u3_p1[1], q1_p4[0], q1_p4[1])
    content += wire(q1_p4[0], u3_p1[1], q2_p4[0], u3_p1[1])
    content += wire(q2_p4[0], u3_p1[1], q2_p4[0], q2_p4[1])
    
    content += wire(u3_p3[0], u3_p3[1], q1_p5[0], u3_p3[1])
    content += junc(q1_p5[0], u3_p3[1])
    content += wire(q1_p5[0], u3_p3[1], q1_p5[0], q1_p5[1])
    content += wire(q1_p5[0], u3_p3[1], q2_p5[0], u3_p3[1])
    content += wire(q2_p5[0], u3_p3[1], q2_p5[0], q2_p5[1])
    
    # Connect D1 and D2 internally on Q1 and Q2
    content += wire(q1_p1[0], q1_p1[1], q1_p8[0], q1_p8[1])
    content += wire(q2_p1[0], q2_p1[1], q2_p8[0], q2_p8[1])
    
    # Connect Source S2 of Q1 and Q2 to System GND
    content += wire(q1_p6[0], q1_p6[1], q1_p7[0], q1_p7[1])
    content += wire(q2_p6[0], q2_p6[1], q2_p7[0], q2_p7[1])
    content += wire(q1_p7[0], q1_p7[1], q2_p7[0], q1_p7[1])
    content += junc(q2_p7[0], q1_p7[1])
    content += wire(q2_p7[0], q1_p7[1], q2_p7[0], 93.98)
    content += gnd_sym(q2_p7[0], 93.98)
    
    # DW01A CS (pin 2) to system GND through R16
    content += wire(u3_p2[0], u3_p2[1], r16_p1[0], u3_p2[1])
    content += wire(r16_p1[0], u3_p2[1], r16_p1[0], r16_p1[1])
    content += wire(r16_p2[0], r16_p2[1], r16_p2[0], 93.98)
    content += gnd_sym(r16_p2[0], 93.98)
    
    # DW01A TD (pin 4) no connect
    content += no_conn(u3_p4[0], u3_p4[1])
    
    # -------------------------------------------------------------------------
    # 4. BQ25895 Charger Connections
    # -------------------------------------------------------------------------
    # VBUS Input from VBUS_MUX
    content += wire(127.00, 71.12, c7_p1[0], 71.12)
    content += global_lbl("VBUS_MUX", 127.00, 71.12, 180, "bidirectional")
    content += junc(c7_p1[0], 71.12)
    content += wire(c7_p1[0], 71.12, c7_p1[0], c7_p1[1])
    content += wire(c7_p2[0], c7_p2[1], c7_p2[0], 78.74)
    content += gnd_sym(c7_p2[0], 78.74)
    content += wire(c7_p1[0], 71.12, u2_p1[0], u2_p1[1])
    
    # PMID Capacitor C8
    content += wire(u2_p23[0], u2_p23[1], c8_p1[0], u2_p23[1])
    content += wire(c8_p1[0], u2_p23[1], c8_p1[0], c8_p1[1])
    content += wire(c8_p2[0], c8_p2[1], c8_p2[0], 83.82)
    content += gnd_sym(c8_p2[0], 83.82)
    
    # REGN Capacitor C9
    content += wire(u2_p22[0], u2_p22[1], c9_p1[0], u2_p22[1])
    content += junc(c9_p1[0], u2_p22[1])
    content += wire(c9_p1[0], u2_p22[1], c9_p1[0], c9_p1[1])
    content += wire(c9_p2[0], c9_p2[1], c9_p2[0], 91.44)
    content += gnd_sym(c9_p2[0], 91.44)
    
    # REGN to TS upper divider (R9)
    content += wire(c9_p1[0], u2_p22[1], r9_p1[0], u2_p22[1])
    content += wire(r9_p1[0], u2_p22[1], r9_p1[0], r9_p1[1])
    content += wire(r9_p2[0], r9_p2[1], r9_p2[0], u2_p11[1])
    content += junc(r9_p2[0], u2_p11[1])
    content += wire(r9_p2[0], u2_p11[1], u2_p11[0], u2_p11[1])
    content += wire(r9_p2[0], u2_p11[1], r10_p1[0], r10_p1[1])
    content += wire(r10_p2[0], r10_p2[1], r10_p2[0], 109.22)
    content += gnd_sym(r10_p2[0], 109.22)
    
    # /CE (pin 9), OTG (pin 8), DSEL (pin 24) pulled to GND
    content += wire(u2_p9[0], u2_p9[1], 154.94, u2_p9[1])
    content += junc(154.94, u2_p9[1])
    content += wire(u2_p8[0], u2_p8[1], 154.94, u2_p8[1])
    content += junc(154.94, u2_p8[1])
    content += wire(u2_p24[0], u2_p24[1], 154.94, u2_p24[1])
    content += junc(154.94, u2_p24[1])
    content += wire(154.94, u2_p9[1], 154.94, 109.22)
    content += gnd_sym(154.94, 109.22)
    
    # QON (pin 12) pulled to REGN through test point
    content += wire(u2_p12[0], u2_p12[1], 152.40, u2_p12[1])
    content += no_conn(152.40, u2_p12[1])
    
    # ILIM (pin 10) through R8 to GND
    content += wire(u2_p10[0], u2_p10[1], r8_p1[0], u2_p10[1])
    content += wire(r8_p1[0], u2_p10[1], r8_p1[0], r8_p1[1])
    content += wire(r8_p2[0], r8_p2[1], r8_p2[0], 104.14)
    content += gnd_sym(r8_p2[0], 104.14)
    
    # D+, D- (pins 2, 3) left unconnected
    content += no_conn(u2_p2[0], u2_p2[1])
    content += no_conn(u2_p3[0], u2_p3[1])
    
    # PGND (pins 17, 18) and EP/GND (pin 25) to GND bus
    content += wire(u2_p17[0], u2_p17[1], 160.02, 114.30)
    content += wire(u2_p18[0], u2_p18[1], 160.02, 114.30)
    content += wire(u2_p25[0], u2_p25[1], 195.58, 114.30)
    content += wire(160.02, 114.30, 195.58, 114.30)
    content += gnd_sym(177.80, 114.30)
    
    # -------------------------------------------------------------------------
    # 5. BQ25895 Switching & Output (SW, BTST, SYS)
    # -------------------------------------------------------------------------
    # Tie SW pins 19 and 20 together
    content += wire(u2_p19[0], u2_p19[1], 200.66, u2_p19[1])
    content += wire(u2_p20[0], u2_p20[1], 200.66, u2_p20[1])
    content += wire(200.66, u2_p19[1], 200.66, u2_p20[1])
    content += junc(200.66, u2_p19[1])
    
    # Bootstrap Capacitor C10 between BTST (pin 21) and SW
    content += wire(u2_p21[0], u2_p21[1], c10_p1[0], u2_p21[1])
    content += wire(c10_p1[0], u2_p21[1], c10_p1[0], c10_p1[1])
    content += wire(c10_p2[0], c10_p2[1], 200.66, c10_p2[1])
    content += wire(200.66, c10_p2[1], 200.66, u2_p20[1])
    
    # Inductor L1 from SW to SYS
    content += wire(200.66, u2_p19[1], 200.66, l1_p1[1])
    content += wire(200.66, l1_p1[1], l1_p1[0], l1_p1[1])
    
    # SYS output from L1 pin 2
    content += wire(l1_p2[0], l1_p2[1], 218.44, l1_p2[1])
    content += wire(218.44, l1_p2[1], 218.44, u2_p15[1])
    content += wire(218.44, u2_p15[1], u2_p15[0], u2_p15[1])
    content += junc(u2_p15[0], u2_p15[1])
    content += wire(u2_p15[0], u2_p15[1], u2_p16[0], u2_p16[1])
    
    # SYS Output Capacitors C11, C12
    content += wire(218.44, u2_p15[1], c11_p1[0], u2_p15[1])
    content += junc(c11_p1[0], u2_p15[1])
    content += wire(c11_p1[0], u2_p15[1], c11_p1[0], c11_p1[1])
    content += wire(c11_p2[0], c11_p2[1], c11_p2[0], 88.90)
    content += gnd_sym(c11_p2[0], 88.90)
    
    content += wire(c11_p1[0], u2_p15[1], c12_p1[0], u2_p15[1])
    content += junc(c12_p1[0], u2_p15[1])
    content += wire(c12_p1[0], u2_p15[1], c12_p1[0], c12_p1[1])
    content += wire(c12_p2[0], c12_p2[1], c12_p2[0], 88.90)
    content += gnd_sym(c12_p2[0], 88.90)
    
    # Test point and SYS output labels
    content += wire(c12_p1[0], u2_p15[1], tp_sys_p1[0], u2_p15[1])
    content += junc(tp_sys_p1[0], u2_p15[1])
    content += wire(tp_sys_p1[0], u2_p15[1], tp_sys_p1[0], tp_sys_p1[1])
    content += wire(tp_sys_p1[0], u2_p15[1], 254.00, u2_p15[1])
    content += global_lbl("SYS", 254.00, u2_p15[1], 0, "bidirectional")
    content += hier_lbl("SYS", 254.00, u2_p15[1] + 5.08, 0, "output")
    
    # -------------------------------------------------------------------------
    # 6. Status, Interrupt and I2C Pullups (STAT, INT, SCL, SDA)
    # -------------------------------------------------------------------------
    content += wire(u2_p4[0], u2_p4[1], r11_p2[0], u2_p4[1])
    content += junc(r11_p2[0], u2_p4[1])
    content += wire(r11_p2[0], u2_p4[1], r11_p2[0], r11_p2[1])
    content += wire(r11_p2[0], u2_p4[1], 248.92, u2_p4[1])
    content += global_lbl("CHG_STAT", 248.92, u2_p4[1], 0, "output")
    content += hier_lbl("CHG_STAT", 248.92, u2_p4[1] + 3.81, 0, "output")
    
    content += wire(u2_p7[0], u2_p7[1], r12_p2[0], u2_p7[1])
    content += junc(r12_p2[0], u2_p7[1])
    content += wire(r12_p2[0], u2_p7[1], r12_p2[0], r12_p2[1])
    content += wire(r12_p2[0], u2_p7[1], 248.92, u2_p7[1])
    content += global_lbl("CHG_INT", 248.92, u2_p7[1], 0, "output")
    content += hier_lbl("CHG_INT", 248.92, u2_p7[1] + 3.81, 0, "output")
    
    content += wire(u2_p5[0], u2_p5[1], r13_p2[0], u2_p5[1])
    content += junc(r13_p2[0], u2_p5[1])
    content += wire(r13_p2[0], u2_p5[1], r13_p2[0], r13_p2[1])
    content += wire(r13_p2[0], u2_p5[1], 248.92, u2_p5[1])
    content += global_lbl("I2C_SCL", 248.92, u2_p5[1], 0, "bidirectional")
    
    content += wire(u2_p6[0], u2_p6[1], r14_p2[0], u2_p6[1])
    content += junc(r14_p2[0], u2_p6[1])
    content += wire(r14_p2[0], u2_p6[1], r14_p2[0], r14_p2[1])
    content += wire(r14_p2[0], u2_p6[1], 248.92, u2_p6[1])
    content += global_lbl("I2C_SDA", 248.92, u2_p6[1], 0, "bidirectional")
    
    # Tie pullup tops (R11, R12, R13, R14) to 3V3_SYS
    content += wire(r11_p1[0], r11_p1[1], r12_p1[0], r11_p1[1])
    content += junc(r12_p1[0], r11_p1[1])
    content += wire(r12_p1[0], r11_p1[1], r13_p1[0], r11_p1[1])
    content += junc(r13_p1[0], r11_p1[1])
    content += wire(r13_p1[0], r11_p1[1], r14_p1[0], r11_p1[1])
    content += junc(r14_p1[0], r11_p1[1])
    content += wire(r14_p1[0], r11_p1[1], 248.92, r11_p1[1])
    content += global_lbl("3V3_SYS", 248.92, r11_p1[1], 0, "input")
    
    # Section Headings & Explanatory Texts
    content += sch_text("KHỐI SẠC PIN LI-ION & QUẢN LÝ ĐƯỜNG NGUỒN NVDC (BQ25895)", 25.40, 22.86, 2.0, True)
    content += sch_text("MẠCH BẢO VỆ PIN 1S CHUYÊN DỤNG (DW01A + 2x FS8205A SONG SONG)", 25.40, 30.48, 1.4, True)
    content += sch_text("BẢO VỆ: Quá xả (2.40V) | Quá sạc (4.30V) | Quá dòng cắt: 6.0A (RDSon=25mOhm)", 25.40, 35.56, 1.3, False)
    content += sch_text("ĐO ĐIỆN ÁP PIN: GPIO1 = ADC_VBAT_SENSE (Phân áp 100k/100k + C17 100nF)", 60.96, 60.96, 1.3, False)
    content += sch_text("NVDC CHARGER: Dòng sạc tối đa 5A | Giới hạn đầu vào ILIM = 3.25A | Quản lý nhiệt JEITA TS", 140.00, 30.48, 1.3, False)
    content += sch_text("ĐƯỜNG NGUỒN HỆ THỐNG SYS: Cung cấp trực tiếp cho Boost 5V (2.7V - 4.4V)", 140.00, 35.56, 1.3, False)
    
    content += ")\n"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Sheet 2 generated: {out_path}")
