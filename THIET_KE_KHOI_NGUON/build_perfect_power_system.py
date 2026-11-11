# -*- coding: utf-8 -*-
"""
AIOT BLACK BOX - COMPLETE HIERARCHICAL POWER SUPPLY SCHEMATIC GENERATOR
Generates 5 KiCad 10 schematic files with full hierarchical architecture,
automated pin tip coordinate alignment, robust power flags, and inter-sheet net connectivity.
"""

import os
import sys
import uuid
import re
import json
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"D:\ĐỒ ÁN 2\THIET_KE_KHOI_NGUON"

def uid():
    return str(uuid.uuid4())

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

print("Building core initialized.")
# -----------------------------------------------------------------------------
# 1. SHEET 1: 01_INPUT_SELECTION.kicad_sch
# -----------------------------------------------------------------------------
def build_sheet1(out_path):
    content = make_header("KHỐI CHỌN NGUỒN ĐẦU VÀO & POWER MUX (TPS2121)", 2, 5)
    
    # 1. VEHICLE_5V_IN Block
    # J1 at (30.48, 50.80)
    j1_x, j1_y = 30.48, 50.80
    content += sym_inst("Connector:Conn_01x02_Pin", "J1", "VEHICLE_5V_IN", j1_x, j1_y, 0,
                        "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical",
                        "https://www.jst-mfg.com/product/pdf/eng/eXH.pdf",
                        "External Regulated 5V Vehicle Input Connector, 2.50mm, 5A",
                        pins=["1", "2"])
    
    # F1 at (50.80, 50.80, rot=90)
    f1_x, f1_y = 50.80, 50.80
    content += sym_inst("Device:Fuse", "F1", "MF-MSMF300/16X (3.0A)", f1_x, f1_y, 90,
                        "Fuse:Fuse_1812_4532Metric",
                        "https://www.bourns.com/docs/product-datasheets/mf-msmf.pdf",
                        "PTC Resettable Fuse, 3.0A Hold, 6.0A Trip, 16V, 1812 SMD",
                        pins=["1", "2"])
    
    # D1 (TVS) at (63.50, 60.96, rot=90)
    d1_x, d1_y = 63.50, 60.96
    content += sym_inst("Device:D_TVS", "D1", "SMAJ5.0A", d1_x, d1_y, 90,
                        "Diode_SMD:D_SMA",
                        "https://www.vishay.com/docs/88390/smaj50a.pdf",
                        "600W Transient Voltage Suppressor, 5.0V Reverse Standoff, SMA",
                        pins=["1", "2"])
    
    # D3 (Schottky) at (76.20, 50.80, rot=270)
    d3_x, d3_y = 76.20, 50.80
    content += sym_inst("Device:D_Schottky", "D3", "SS34 (3A/40V)", d3_x, d3_y, 270,
                        "Diode_SMD:D_SMA",
                        "https://www.vishay.com/docs/88746/ss32.pdf",
                        "Schottky Barrier Rectifier Diode, 3A, 40V, Low Vf, SMA",
                        pins=["1", "2"])
    
    # C1 (10uF) at (88.90, 60.96, rot=0)
    c1_x, c1_y = 88.90, 60.96
    content += sym_inst("Device:C", "C1", "10uF/25V (X7R)", c1_x, c1_y, 0,
                        "Capacitor_SMD:C_0805_2012Metric",
                        "~", "Ceramic Capacitor, 10uF, 25V, X7R, 10%, 0805",
                        pins=["1", "2"])
    
    # C2 (100uF) at (101.60, 60.96, rot=0)
    c2_x, c2_y = 101.60, 60.96
    content += sym_inst("Device:C_Polarized", "C2", "100uF/25V (Low ESR)", c2_x, c2_y, 0,
                        "Capacitor_SMD:CP_Elec_6.3x5.4",
                        "~", "Aluminum Electrolytic Capacitor, 100uF, 25V, Low-ESR SMD",
                        pins=["1", "2"])
    
    # TP1 at (114.30, 45.72)
    tp1_x, tp1_y = 114.30, 45.72
    content += sym_inst("Connector:TestPoint", "TP1", "TP_VEHICLE_5V", tp1_x, tp1_y, 0,
                        "TestPoint:TestPoint_Pad_D1.5mm",
                        "~", "Test Point Pad 1.5mm, VEHICLE_5V_IN",
                        pins=["1"])
    
    # Calculate exact pin positions for Vehicle 5V block
    j1_p1 = pin_pos(base_syms.SYM_CONN_02, j1_x, j1_y, "1", 0)
    j1_p2 = pin_pos(base_syms.SYM_CONN_02, j1_x, j1_y, "2", 0)
    f1_p1 = pin_pos(base_syms.SYM_FUSE, f1_x, f1_y, "1", 90)
    f1_p2 = pin_pos(base_syms.SYM_FUSE, f1_x, f1_y, "2", 90)
    d1_p1 = pin_pos(base_syms.SYM_D_TVS, d1_x, d1_y, "1", 90)
    d1_p2 = pin_pos(base_syms.SYM_D_TVS, d1_x, d1_y, "2", 90)
    d3_p1 = pin_pos(base_syms.SYM_D_SCHOTTKY, d3_x, d3_y, "1", 270)
    d3_p2 = pin_pos(base_syms.SYM_D_SCHOTTKY, d3_x, d3_y, "2", 270)
    c1_p1 = pin_pos(base_syms.SYM_C, c1_x, c1_y, "1", 0)
    c1_p2 = pin_pos(base_syms.SYM_C, c1_x, c1_y, "2", 0)
    c2_p1 = pin_pos(base_syms.SYM_CP, c2_x, c2_y, "1", 0)
    c2_p2 = pin_pos(base_syms.SYM_CP, c2_x, c2_y, "2", 0)
    tp1_p1 = pin_pos(base_syms.SYM_TESTPOINT, tp1_x, tp1_y, "1", 0)
    
    # Wire VEHICLE_5V_IN rail along Y = 50.80
    content += wire(j1_p1[0], j1_p1[1], f1_p1[0], f1_p1[1])
    content += wire(f1_p2[0], f1_p2[1], d1_p1[0], f1_p2[1])
    content += junc(d1_p1[0], f1_p2[1])
    content += wire(d1_p1[0], f1_p2[1], d1_p1[0], d1_p1[1])
    content += wire(d1_p2[0], d1_p2[1], d1_p2[0], 68.58)
    content += gnd_sym(d1_p2[0], 68.58)
    
    content += wire(d1_p1[0], f1_p2[1], d3_p1[0], d3_p1[1])
    content += wire(d3_p2[0], d3_p2[1], c1_p1[0], d3_p2[1])
    content += junc(c1_p1[0], d3_p2[1])
    content += wire(c1_p1[0], d3_p2[1], c1_p1[0], c1_p1[1])
    content += wire(c1_p2[0], c1_p2[1], c1_p2[0], 68.58)
    content += gnd_sym(c1_p2[0], 68.58)
    
    content += wire(c1_p1[0], d3_p2[1], c2_p1[0], d3_p2[1])
    content += junc(c2_p1[0], d3_p2[1])
    content += wire(c2_p1[0], d3_p2[1], c2_p1[0], c2_p1[1])
    content += wire(c2_p2[0], c2_p2[1], c2_p2[0], 68.58)
    content += gnd_sym(c2_p2[0], 68.58)
    
    content += wire(c2_p1[0], d3_p2[1], tp1_p1[0], d3_p2[1])
    content += junc(tp1_p1[0], d3_p2[1])
    content += wire(tp1_p1[0], d3_p2[1], tp1_p1[0], tp1_p1[1])
    content += pwr_flag(tp1_p1[0], tp1_p1[1])
    content += wire(tp1_p1[0], d3_p2[1], 127.00, d3_p2[1])
    content += global_lbl("VEHICLE_5V_IN", 127.00, d3_p2[1], 0, "bidirectional")
    
    content += wire(j1_p2[0], j1_p2[1], j1_p2[0], 68.58)
    content += gnd_sym(j1_p2[0], 68.58)
    
    # 2. USB_5V_IN Block
    j2_x, j2_y = 30.48, 114.30
    content += sym_inst("Connector:USB_C_16P", "J2", "TYPE-C-16P", j2_x, j2_y, 0,
                        "Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12",
                        "https://www.usb.org/type-c",
                        "USB 2.0 Type-C Receptacle, 16 pins, 5A VBUS, 50V",
                        pins=["A1", "A4", "A5", "A6", "A7", "B5", "B9", "B12", "S1"])
    
    f2_x, f2_y = 55.88, 124.46
    content += sym_inst("Device:Fuse", "F2", "MF-MSMF300/16X (3.0A)", f2_x, f2_y, 90,
                        "Fuse:Fuse_1812_4532Metric",
                        "https://www.bourns.com/docs/product-datasheets/mf-msmf.pdf",
                        "PTC Resettable Fuse, 3.0A Hold, 6.0A Trip, 16V, 1812 SMD",
                        pins=["1", "2"])
    
    d2_x, d2_y = 68.58, 134.62
    content += sym_inst("Device:D_TVS", "D2", "SMAJ5.0A", d2_x, d2_y, 90,
                        "Diode_SMD:D_SMA",
                        "https://www.vishay.com/docs/88390/smaj50a.pdf",
                        "600W Transient Voltage Suppressor, 5.0V Reverse Standoff, SMA",
                        pins=["1", "2"])
    
    c3_x, c3_y = 81.28, 134.62
    content += sym_inst("Device:C", "C3", "10uF/16V (X7R)", c3_x, c3_y, 0,
                        "Capacitor_SMD:C_0805_2012Metric",
                        "~", "Ceramic Capacitor, 10uF, 16V, X7R, 10%, 0805",
                        pins=["1", "2"])
    
    r1_x, r1_y = 50.80, 109.22
    content += sym_inst("Device:R", "R1", "5.1k (1%)", r1_x, r1_y, 0,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Resistor, 5.1k, 1%, 0.1W, 0603",
                        pins=["1", "2"])
    
    r2_x, r2_y = 60.96, 109.22
    content += sym_inst("Device:R", "R2", "5.1k (1%)", r2_x, r2_y, 0,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Resistor, 5.1k, 1%, 0.1W, 0603",
                        pins=["1", "2"])
    
    tp2_x, tp2_y = 93.98, 119.38
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
    content += wire(j2_pa4[0], j2_pa4[1], 45.72, j2_pa4[1])
    content += wire(j2_pb9[0], j2_pb9[1], 45.72, j2_pb9[1])
    content += wire(45.72, j2_pa4[1], 45.72, f2_p1[1])
    content += wire(45.72, j2_pb9[1], 45.72, f2_p1[1])
    content += wire(45.72, f2_p1[1], f2_p1[0], f2_p1[1])
    
    content += wire(f2_p2[0], f2_p2[1], d2_p1[0], f2_p2[1])
    content += junc(d2_p1[0], f2_p2[1])
    content += wire(d2_p1[0], f2_p2[1], d2_p1[0], d2_p1[1])
    content += wire(d2_p2[0], d2_p2[1], d2_p2[0], 142.24)
    content += gnd_sym(d2_p2[0], 142.24)
    
    content += wire(d2_p1[0], f2_p2[1], c3_p1[0], f2_p2[1])
    content += junc(c3_p1[0], f2_p2[1])
    content += wire(c3_p1[0], f2_p2[1], c3_p1[0], c3_p1[1])
    content += wire(c3_p2[0], c3_p2[1], c3_p2[0], 142.24)
    content += gnd_sym(c3_p2[0], 142.24)
    
    content += wire(c3_p1[0], f2_p2[1], tp2_p1[0], f2_p2[1])
    content += junc(tp2_p1[0], f2_p2[1])
    content += wire(tp2_p1[0], f2_p2[1], tp2_p1[0], tp2_p1[1])
    content += pwr_flag(tp2_p1[0], tp2_p1[1])
    content += wire(tp2_p1[0], f2_p2[1], 106.68, f2_p2[1])
    content += global_lbl("USB_5V_IN", 106.68, f2_p2[1], 0, "bidirectional")
    
    # Wire CC1, CC2
    content += wire(j2_pa5[0], j2_pa5[1], r1_p1[0], j2_pa5[1])
    content += wire(r1_p1[0], j2_pa5[1], r1_p1[0], r1_p1[1])
    content += wire(r1_p2[0], r1_p2[1], r1_p2[0], 101.60)
    content += gnd_sym(r1_p2[0], 101.60)
    
    content += wire(j2_pb5[0], j2_pb5[1], r2_p1[0], j2_pb5[1])
    content += wire(r2_p1[0], j2_pb5[1], r2_p1[0], r2_p1[1])
    content += wire(r2_p2[0], r2_p2[1], r2_p2[0], 101.60)
    content += gnd_sym(r2_p2[0], 101.60)
    
    # Unused D+, D-
    content += no_conn(j2_pa6[0], j2_pa6[1])
    content += no_conn(j2_pa7[0], j2_pa7[1])
    
    # GND on USB connector
    content += wire(j2_pa1[0], j2_pa1[1], j2_pa1[0], 101.60)
    content += gnd_sym(j2_pa1[0], 101.60)
    content += wire(j2_ps1[0], j2_ps1[1], j2_ps1[0], 101.60)
    content += gnd_sym(j2_ps1[0], 101.60)
    
    # 3. TPS2121 Power Mux Block
    u1_x, u1_y = 165.10, 88.90
    content += sym_inst("Power_Management:TPS2121RUXR", "U1", "TPS2121RUXR", u1_x, u1_y, 0,
                        "Package_DFN_QFN:Texas_RUX0012A",
                        "https://www.ti.com/lit/ds/symlink/tps2121.pdf",
                        "2.8V-22V, 4A Priority Power MUX with Seamless Switchover, VQFN-12",
                        pins=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
    
    r3_x, r3_y = 144.78, 93.98
    content += sym_inst("Device:R", "R3", "30k (1%)", r3_x, r3_y, 0,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Resistor, 30k, 1%, 0.1W, 0603",
                        pins=["1", "2"])
    
    r4_x, r4_y = 144.78, 81.28
    content += sym_inst("Device:R", "R4", "10k (1%)", r4_x, r4_y, 0,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Resistor, 10k, 1%, 0.1W, 0603",
                        pins=["1", "2"])
    
    c6_x, c6_y = 187.96, 91.44
    content += sym_inst("Device:C", "C6", "10nF/25V (X7R)", c6_x, c6_y, 90,
                        "Capacitor_SMD:C_0603_1608Metric",
                        "~", "Ceramic Capacitor, 10nF, 25V, X7R, 0603",
                        pins=["1", "2"])
    
    r5_x, r5_y = 187.96, 88.90
    content += sym_inst("Device:R", "R5", "28.7k (1% / 3.5A)", r5_x, r5_y, 90,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Resistor, 28.7k, 1%, 0.1W, 0603",
                        pins=["1", "2"])
    
    r6_x, r6_y = 187.96, 76.20
    content += sym_inst("Device:R", "R6", "100k (1%)", r6_x, r6_y, 0,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Resistor, 100k, 1%, 0.1W, 0603",
                        pins=["1", "2"])
    
    c4_x, c4_y = 203.20, 99.06
    content += sym_inst("Device:C", "C4", "22uF/16V (X5R)", c4_x, c4_y, 0,
                        "Capacitor_SMD:C_0805_2012Metric",
                        "~", "Ceramic Capacitor, 22uF, 16V, X5R, 0805",
                        pins=["1", "2"])
    
    c5_x, c5_y = 215.90, 99.06
    content += sym_inst("Device:C", "C5", "0.1uF/25V (X7R)", c5_x, c5_y, 0,
                        "Capacitor_SMD:C_0603_1608Metric",
                        "~", "Ceramic Capacitor, 0.1uF, 25V, X7R, 0603",
                        pins=["1", "2"])
    
    tp3_x, tp3_y = 228.60, 93.98
    content += sym_inst("Connector:TestPoint", "TP3", "TP_VBUS_MUX", tp3_x, tp3_y, 0,
                        "TestPoint:TestPoint_Pad_D1.5mm",
                        "~", "Test Point Pad 1.5mm, VBUS_MUX",
                        pins=["1"])
    
    tp_st_x, tp_st_y = 187.96, 68.58
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
    
    # Connect IN1 from VEHICLE_5V_IN
    content += wire(127.00, 50.80, 137.16, 50.80)
    content += wire(137.16, 50.80, 137.16, u1_p7[1])
    content += wire(137.16, u1_p7[1], r3_p1[0], u1_p7[1])
    content += junc(r3_p1[0], u1_p7[1])
    content += wire(r3_p1[0], u1_p7[1], r3_p1[0], r3_p1[1])
    content += wire(r3_p1[0], u1_p7[1], u1_p7[0], u1_p7[1])
    
    # PR1 divider connection
    content += wire(r3_p2[0], r3_p2[1], u1_p6[0], r3_p2[1])
    content += junc(u1_p6[0], r3_p2[1])
    content += wire(u1_p6[0], r3_p2[1], u1_p6[0], u1_p6[1])
    content += wire(u1_p6[0], r3_p2[1], r4_p1[0], r3_p2[1])
    content += wire(r4_p1[0], r3_p2[1], r4_p1[0], r4_p1[1])
    content += wire(r4_p2[0], r4_p2[1], r4_p2[0], 73.66)
    content += gnd_sym(r4_p2[0], 73.66)
    
    # Connect IN2 from USB_5V_IN
    content += wire(106.68, 124.46, 137.16, 124.46)
    content += wire(137.16, 124.46, 137.16, u1_p2[1])
    content += wire(137.16, u1_p2[1], u1_p2[0], u1_p2[1])
    
    # CP2, OV1, OV2, GND to ground bus
    content += wire(u1_p3[0], u1_p3[1], 148.59, u1_p3[1])
    content += wire(u1_p5[0], u1_p5[1], 148.59, u1_p5[1])
    content += wire(u1_p4[0], u1_p4[1], 148.59, u1_p4[1])
    content += wire(u1_p12[0], u1_p12[1], 148.59, u1_p12[1])
    content += wire(148.59, u1_p3[1], 148.59, 73.66)
    content += gnd_sym(148.59, 73.66)
    
    # Connect OUT pins 1 and 8
    content += wire(u1_p1[0], u1_p1[1], 180.34, u1_p1[1])
    content += wire(u1_p8[0], u1_p8[1], 180.34, u1_p8[1])
    content += wire(180.34, u1_p1[1], 180.34, u1_p8[1])
    
    # VBUS_MUX output bus along Y = 97.79
    content += wire(180.34, 97.79, c4_p1[0], 97.79)
    content += junc(c4_p1[0], 97.79)
    content += wire(c4_p1[0], 97.79, c4_p1[0], c4_p1[1])
    content += wire(c4_p2[0], c4_p2[1], c4_p2[0], 91.44)
    content += gnd_sym(c4_p2[0], 91.44)
    
    content += wire(c4_p1[0], 97.79, c5_p1[0], 97.79)
    content += junc(c5_p1[0], 97.79)
    content += wire(c5_p1[0], 97.79, c5_p1[0], c5_p1[1])
    content += wire(c5_p2[0], c5_p2[1], c5_p2[0], 91.44)
    content += gnd_sym(c5_p2[0], 91.44)
    
    content += wire(c5_p1[0], 97.79, tp3_p1[0], 97.79)
    content += junc(tp3_p1[0], 97.79)
    content += wire(tp3_p1[0], 97.79, tp3_p1[0], tp3_p1[1])
    content += pwr_flag(tp3_p1[0], tp3_p1[1])
    content += wire(tp3_p1[0], 97.79, 238.76, 97.79)
    content += global_lbl("VBUS_MUX", 238.76, 97.79, 0, "bidirectional")
    content += hier_lbl("VBUS_MUX", 238.76, 102.87, 0, "output")
    
    # SS capacitor C6
    content += wire(u1_p11[0], u1_p11[1], c6_p1[0], u1_p11[1])
    content += wire(c6_p1[0], u1_p11[1], c6_p1[0], c6_p1[1])
    content += wire(c6_p2[0], c6_p2[1], 194.31, c6_p2[1])
    content += gnd_sym(194.31, c6_p2[1])
    
    # ILIM resistor R5
    content += wire(u1_p10[0], u1_p10[1], r5_p1[0], u1_p10[1])
    content += wire(r5_p1[0], u1_p10[1], r5_p1[0], r5_p1[1])
    content += wire(r5_p2[0], r5_p2[1], 194.31, r5_p2[1])
    content += gnd_sym(194.31, r5_p2[1])
    
    # ST pin 9
    content += wire(u1_p9[0], u1_p9[1], r6_p2[0], u1_p9[1])
    content += junc(r6_p2[0], u1_p9[1])
    content += wire(r6_p2[0], u1_p9[1], r6_p2[0], r6_p2[1])
    content += wire(r6_p1[0], r6_p1[1], r6_p1[0], 97.79)
    content += junc(r6_p1[0], 97.79)
    content += wire(r6_p1[0], 97.79, c4_p1[0], 97.79)
    
    content += wire(r6_p2[0], u1_p9[1], tp_st_p1[0], u1_p9[1])
    content += wire(tp_st_p1[0], u1_p9[1], tp_st_p1[0], tp_st_p1[1])
    content += wire(tp_st_p1[0], tp_st_p1[1], tp_st_p1[0], 63.50)
    content += global_lbl("MUX_ST", tp_st_p1[0], 63.50, 0, "output")
    
    # Notes & Section Headings
    content += sch_text("KHỐI CHỌN NGUỒN ĐẦU VÀO TỰ ĐỘNG (SEAMLESS POWER MULTIPLEXER)", 25.40, 22.86, 2.0, True)
    content += sch_text("Ưu tiên: VEHICLE_5V_IN (PR1 threshold = 4.24V) | Dự phòng: USB_5V_IN", 25.40, 30.48, 1.3, False)
    content += sch_text("Bảo vệ quá dòng: ILIM = 3.5A (R5 = 28.7k) | Khóa dòng ngược tích hợp", 25.40, 35.56, 1.3, False)
    content += sch_text("CỔNG VÀO NGUỒN XE (5V REGULATED)", 25.40, 43.18, 1.4, True)
    content += sch_text("CỔNG VÀO USB-C (SINK CC1/CC2 5.1k)", 25.40, 104.14, 1.4, True)
    content += sch_text("TPS2121 MUX OUTPUT: VBUS_MUX (CUNG CẤP CHO BQ25895)", 165.10, 48.26, 1.4, True)
    
    content += ")\n"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Sheet 1 generated: {out_path}")

print("Sheet 1 generator function ready.")
