# -*- coding: utf-8 -*-
"""
AIOT BLACK BOX POWER SUPPLY - COMPREHENSIVE SCHEMATIC BUILDER
Generates all 5 KiCad 10 schematic files with exact 1.27mm grid alignment,
valid hierarchical sheets, symbols, power flags, and inter-sheet net labels.
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
\t\t(property "Value" "PWR_FLAG" (at {round(x,4)} {round(y-2.54,4)} 0) (effects (font (size 1.27 1.27))))
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

print("Generator primitives compiled.")
# -----------------------------------------------------------------------------
# SHEET 1: 01_INPUT_SELECTION.kicad_sch
# -----------------------------------------------------------------------------
def build_sheet1():
    header = make_header("KHỐI CHỌN NGUỒN ĐẦU VÀO & POWER MUX (TPS2121)", 2, 5)
    content = header
    
    # 1. VEHICLE_5V_IN Block
    # J1 at (G(25), G(40)) -> Pin 1 at (G(25)+5.08, G(40)) = (G(25)+G(4), G(40)) = (G(29), G(40))
    # Pin 2 at (G(29), G(40)-2.54) = (G(29), G(38))
    content += sym_inst("Connector:Conn_01x02_Pin", "J1", "VEHICLE_5V_IN", G(25), G(40), 0,
                        "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical",
                        "https://www.jst-mfg.com/product/pdf/eng/eXH.pdf",
                        "External Regulated 5V Vehicle Input Connector, 2.50mm, 5A",
                        pins=["1", "2"])
    
    # F1 (Fuse) at (G(40), G(40), rot=90) -> Pin 1 at (G(40)-3.81, G(40)) = (G(37), G(40)), Pin 2 at (G(43), G(40))
    content += sym_inst("Device:Fuse", "F1", "MF-MSMF300/16X (3.0A)", G(40), G(40), 90,
                        "Fuse:Fuse_1812_4532Metric",
                        "https://www.bourns.com/docs/product-datasheets/mf-msmf.pdf",
                        "PTC Resettable Fuse, 3.0A Hold, 6.0A Trip, 16V, 1812 SMD",
                        pins=["1", "2"])
    
    # D1 (TVS) at (G(50), G(46), rot=90) -> Pin 1 at (G(50), G(46)-3.81) = (G(50), G(43)), Pin 2 at (G(50), G(49))
    content += sym_inst("Device:D_TVS", "D1", "SMAJ5.0A", G(50), G(46), 90,
                        "Diode_SMD:D_SMA",
                        "https://www.vishay.com/docs/88390/smaj50a.pdf",
                        "600W Transient Voltage Suppressor, 5.0V Reverse Standoff, SMA",
                        pins=["1", "2"])
    
    # D3 (Schottky) at (G(60), G(40), rot=270) -> Pin 1 at (G(60)-3.81, G(40)) = (G(57), G(40)), Pin 2 at (G(63), G(40))
    content += sym_inst("Device:D_Schottky", "D3", "SS34 (3A/40V)", G(60), G(40), 270,
                        "Diode_SMD:D_SMA",
                        "https://www.vishay.com/docs/88746/ss32.pdf",
                        "Schottky Barrier Rectifier Diode, 3A, 40V, Low Vf, SMA",
                        pins=["1", "2"])
    
    # C1 (10uF) at (G(70), G(46), rot=0) -> Pin 1 at (G(70), G(46)+3.81) = (G(70), G(49)), Pin 2 at (G(70), G(43))
    content += sym_inst("Device:C", "C1", "10uF/25V (X7R)", G(70), G(46), 0,
                        "Capacitor_SMD:C_0805_2012Metric",
                        "~", "Ceramic Capacitor, 10uF, 25V, X7R, 10%, 0805",
                        pins=["1", "2"])
    
    # C2 (100uF) at (G(80), G(46), rot=0) -> Pin 1 at (G(80), G(46)+3.81) = (G(80), G(49)), Pin 2 at (G(80), G(43))
    content += sym_inst("Device:C_Polarized", "C2", "100uF/25V (Low ESR)", G(80), G(46), 0,
                        "Capacitor_SMD:CP_Elec_6.3x5.4",
                        "~", "Aluminum Electrolytic Capacitor, 100uF, 25V, Low-ESR SMD",
                        pins=["1", "2"])
    
    # TP1 at (G(90), G(36)) -> Pin 1 at (G(90), G(36))
    content += sym_inst("Connector:TestPoint", "TP1", "TP_VEHICLE_5V", G(90), G(36), 0,
                        "TestPoint:TestPoint_Pad_D1.5mm",
                        "~", "Test Point Pad 1.5mm, VEHICLE_5V_IN",
                        pins=["1"])
    
    # Wires for VEHICLE_5V_IN
    # J1 pin 1 to F1 pin 1
    content += wire(G(29), G(40), G(37), G(40))
    # F1 pin 2 to D1 tap
    content += wire(G(43), G(40), G(50), G(40))
    content += junc(G(50), G(40))
    content += wire(G(50), G(40), G(50), G(42.19) if False else G(43))
    content += wire(G(50), G(49), G(50), G(52))
    content += gnd_sym(G(50), G(52))
    
    # D1 tap to D3 pin 1
    content += wire(G(50), G(40), G(57), G(40))
    # D3 pin 2 to C1 tap
    content += wire(G(63), G(40), G(70), G(40))
    content += junc(G(70), G(40))
    content += wire(G(70), G(40), G(70), G(43))
    content += wire(G(70), G(49), G(70), G(52))
    content += gnd_sym(G(70), G(52))
    
    # C1 tap to C2 tap
    content += wire(G(70), G(40), G(80), G(40))
    content += junc(G(80), G(40))
    content += wire(G(80), G(40), G(80), G(43))
    content += wire(G(80), G(49), G(80), G(52))
    content += gnd_sym(G(80), G(52))
    
    # C2 tap to TP1 & Label
    content += wire(G(80), G(40), G(90), G(40))
    content += junc(G(90), G(40))
    content += wire(G(90), G(40), G(90), G(36))
    content += pwr_flag(G(90), G(36))
    content += wire(G(90), G(40), G(100), G(40))
    content += global_lbl("VEHICLE_5V_IN", G(100), G(40), 0, "bidirectional")
    
    # J1 GND
    content += wire(G(29), G(38), G(29), G(52))
    content += gnd_sym(G(29), G(52))
    
    # 2. USB_5V_IN Block at Y = G(90)
    # J2 at (G(25), G(90))
    # Pin A4 at (G(25)+12.7, G(90)+10.16) = (G(35), G(98))
    # Pin B9 at (G(35), G(96))
    # Pin A5 (CC1) at (G(35), G(92))
    # Pin B5 (CC2) at (G(35), G(90))
    # Pin A6 (D+) at (G(35), G(88))
    # Pin A7 (D-) at (G(35), G(86))
    # Pin A1 (GND) at (G(35), G(82))
    # Pin S1 (SHIELD) at (G(25)-12.7, G(90)-10.16) = (G(15), G(82))
    content += sym_inst("Connector:USB_C_16P", "J2", "TYPE-C-16P", G(25), G(90), 0,
                        "Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12",
                        "https://www.usb.org/type-c",
                        "USB 2.0 Type-C Receptacle, 16 pins, 5A VBUS, 50V",
                        pins=["A1", "A4", "A5", "A6", "A7", "B5", "B9", "B12", "S1"])
    
    # VBUS bus at Y = G(97)
    content += wire(G(35), G(98), G(38), G(98))
    content += wire(G(35), G(96), G(38), G(96))
    content += wire(G(38), G(98), G(38), G(96))
    content += wire(G(38), G(97), G(42), G(97))
    
    # F2 (Fuse) at (G(45), G(97), rot=90) -> Pin 1 at (G(42), G(97)), Pin 2 at (G(48), G(97))
    content += sym_inst("Device:Fuse", "F2", "MF-MSMF300/16X (3.0A)", G(45), G(97), 90,
                        "Fuse:Fuse_1812_4532Metric",
                        "https://www.bourns.com/docs/product-datasheets/mf-msmf.pdf",
                        "PTC Resettable Fuse, 3.0A Hold, 6.0A Trip, 16V, 1812 SMD",
                        pins=["1", "2"])
    
    # D2 (TVS) at (G(55), G(103), rot=90) -> Pin 1 at (G(55), G(100)), Pin 2 at (G(55), G(106))
    content += sym_inst("Device:D_TVS", "D2", "SMAJ5.0A", G(55), G(103), 90,
                        "Diode_SMD:D_SMA",
                        "https://www.vishay.com/docs/88390/smaj50a.pdf",
                        "600W Transient Voltage Suppressor, 5.0V Reverse Standoff, SMA",
                        pins=["1", "2"])
    
    # C3 (10uF) at (G(65), G(103), rot=0) -> Pin 1 at (G(65), G(106)), Pin 2 at (G(65), G(100))
    content += sym_inst("Device:C", "C3", "10uF/16V (X7R)", G(65), G(103), 0,
                        "Capacitor_SMD:C_0805_2012Metric",
                        "~", "Ceramic Capacitor, 10uF, 16V, X7R, 10%, 0805",
                        pins=["1", "2"])
    
    # R1 (5.1k CC1) at (G(42), G(88), rot=0) -> Pin 1 at (G(42), G(91)), Pin 2 at (G(42), G(85))
    content += sym_inst("Device:R", "R1", "5.1k (1%)", G(42), G(88), 0,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Resistor, 5.1k, 1%, 0.1W, 0603",
                        pins=["1", "2"])
    
    # R2 (5.1k CC2) at (G(50), G(88), rot=0) -> Pin 1 at (G(50), G(91)), Pin 2 at (G(50), G(85))
    content += sym_inst("Device:R", "R2", "5.1k (1%)", G(50), G(88), 0,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Resistor, 5.1k, 1%, 0.1W, 0603",
                        pins=["1", "2"])
    
    # TP2 at (G(75), G(93))
    content += sym_inst("Connector:TestPoint", "TP2", "TP_USB_5V", G(75), G(93), 0,
                        "TestPoint:TestPoint_Pad_D1.5mm",
                        "~", "Test Point Pad 1.5mm, USB_5V_IN",
                        pins=["1"])
    
    # Wires for USB_5V_IN
    content += wire(G(48), G(97), G(55), G(97))
    content += junc(G(55), G(97))
    content += wire(G(55), G(97), G(55), G(100))
    content += wire(G(55), G(106), G(55), G(109))
    content += gnd_sym(G(55), G(109))
    
    content += wire(G(55), G(97), G(65), G(97))
    content += junc(G(65), G(97))
    content += wire(G(65), G(97), G(65), G(100))
    content += wire(G(65), G(106), G(65), G(109))
    content += gnd_sym(G(65), G(109))
    
    content += wire(G(65), G(97), G(75), G(97))
    content += junc(G(75), G(97))
    content += wire(G(75), G(97), G(75), G(93))
    content += pwr_flag(G(75), G(93))
    content += wire(G(75), G(97), G(85), G(97))
    content += global_lbl("USB_5V_IN", G(85), G(97), 0, "bidirectional")
    
    # CC lines
    content += wire(G(35), G(92), G(42), G(92))
    content += wire(G(42), G(92), G(42), G(91))
    content += wire(G(42), G(85), G(42), G(81))
    content += gnd_sym(G(42), G(81))
    
    content += wire(G(35), G(90), G(50), G(90))
    content += wire(G(50), G(90), G(50), G(91))
    content += wire(G(50), G(85), G(50), G(81))
    content += gnd_sym(G(50), G(81))
    
    # D+, D- no connect
    content += no_conn(G(35), G(88))
    content += no_conn(G(35), G(86))
    
    # GND pins on J2
    content += wire(G(35), G(82), G(35), G(78))
    content += gnd_sym(G(35), G(78))
    content += wire(G(15), G(82), G(15), G(78))
    content += gnd_sym(G(15), G(78))
    
    # 3. TPS2121 Power Mux Block at (G(135), G(65))
    # Box from (-10.16, 15.24) to (10.16, -15.24) = (-G(8), G(12)) to (G(8), -G(12))
    # Left Pins at X = G(135)-G(10) = G(125):
    # Pin 7 (IN1): Y = G(65)+G(8) = G(73)
    # Pin 2 (IN2): Y = G(65)+G(6) = G(71)
    # Pin 6 (PR1): Y = G(65)+G(2) = G(67)
    # Pin 3 (CP2): Y = G(65)
    # Pin 5 (OV1): Y = G(65)-G(2) = G(63)
    # Pin 4 (OV2): Y = G(65)-G(4) = G(61)
    # Pin 12 (GND): Y = G(65)-G(10) = G(55)
    # Right Pins at X = G(135)+G(10) = G(145):
    # Pin 1 (OUT): Y = G(65)+G(8) = G(73)
    # Pin 8 (OUT): Y = G(65)+G(6) = G(71)
    # Pin 11 (SS): Y = G(65)+G(2) = G(67)
    # Pin 10 (ILIM): Y = G(65)
    # Pin 9 (ST): Y = G(65)-G(2) = G(63)
    content += sym_inst("Power_Management:TPS2121RUXR", "U1", "TPS2121RUXR", G(135), G(65), 0,
                        "Package_DFN_QFN:Texas_RUX0012A",
                        "https://www.ti.com/lit/ds/symlink/tps2121.pdf",
                        "2.8V-22V, 4A Priority Power MUX with Seamless Switchover, VQFN-12",
                        pins=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
    
    # R3 (30k PR1 top) at (G(118), G(70), rot=0) -> Pin 1 at (G(118), G(73)), Pin 2 at (G(118), G(67))
    content += sym_inst("Device:R", "R3", "30k (1%)", G(118), G(70), 0,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Resistor, 30k, 1%, 0.1W, 0603",
                        pins=["1", "2"])
    
    # R4 (10k PR1 bottom) at (G(118), G(61), rot=0) -> Pin 1 at (G(118), G(64)), Pin 2 at (G(118), G(58))
    content += sym_inst("Device:R", "R4", "10k (1%)", G(118), G(61), 0,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Resistor, 10k, 1%, 0.1W, 0603",
                        pins=["1", "2"])
    
    # C6 (10nF SS) at (G(155), G(67), rot=90) -> Pin 1 at (G(152), G(67)), Pin 2 at (G(158), G(67))
    content += sym_inst("Device:C", "C6", "10nF/25V (X7R)", G(155), G(67), 90,
                        "Capacitor_SMD:C_0603_1608Metric",
                        "~", "Ceramic Capacitor, 10nF, 25V, X7R, 0603",
                        pins=["1", "2"])
    
    # R5 (28.7k ILIM) at (G(155), G(60), rot=90) -> Pin 1 at (G(152), G(60)), Pin 2 at (G(158), G(60))
    content += sym_inst("Device:R", "R5", "28.7k (1% / 3.5A)", G(155), G(60), 90,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Resistor, 28.7k, 1%, 0.1W, 0603",
                        pins=["1", "2"])
    
    # R6 (100k pullup for ST) at (G(155), G(74), rot=0) -> Pin 1 at (G(155), G(77)), Pin 2 at (G(155), G(71))
    content += sym_inst("Device:R", "R6", "100k (1%)", G(155), G(74), 0,
                        "Resistor_SMD:R_0603_1608Metric",
                        "~", "Resistor, 100k, 1%, 0.1W, 0603",
                        pins=["1", "2"])
    
    # C4 (22uF output) at (G(170), G(66), rot=0) -> Pin 1 at (G(170), G(69)), Pin 2 at (G(170), G(63))
    content += sym_inst("Device:C", "C4", "22uF/16V (X5R)", G(170), G(66), 0,
                        "Capacitor_SMD:C_0805_2012Metric",
                        "~", "Ceramic Capacitor, 22uF, 16V, X5R, 0805",
                        pins=["1", "2"])
    
    # C5 (0.1uF output) at (G(180), G(66), rot=0) -> Pin 1 at (G(180), G(69)), Pin 2 at (G(180), G(63))
    content += sym_inst("Device:C", "C5", "0.1uF/25V (X7R)", G(180), G(66), 0,
                        "Capacitor_SMD:C_0603_1608Metric",
                        "~", "Ceramic Capacitor, 0.1uF, 25V, X7R, 0603",
                        pins=["1", "2"])
    
    # TP3 at (G(190), G(66))
    content += sym_inst("Connector:TestPoint", "TP3", "TP_VBUS_MUX", G(190), G(66), 0,
                        "TestPoint:TestPoint_Pad_D1.5mm",
                        "~", "Test Point Pad 1.5mm, VBUS_MUX",
                        pins=["1"])
    
    # TP_MUX_ST at (G(150), G(55))
    content += sym_inst("Connector:TestPoint", "TP_MUX_ST", "TP_MUX_ST", G(150), G(55), 0,
                        "TestPoint:TestPoint_Pad_D1.5mm",
                        "~", "Test Point Pad 1.5mm, Status of TPS2121",
                        pins=["1"])
    
    # Wires for TPS2121
    # IN1 from VEHICLE_5V_IN
    content += wire(G(100), G(40), G(110), G(40))
    content += wire(G(110), G(40), G(110), G(73))
    content += wire(G(110), G(73), G(118), G(73))
    content += junc(G(118), G(73))
    content += wire(G(118), G(73), G(125), G(73))
    
    # PR1 divider R3 & R4
    content += wire(G(118), G(67), G(125), G(67))
    content += junc(G(118), G(67))
    content += wire(G(118), G(67), G(118), G(64))
    content += wire(G(118), G(58), G(118), G(53))
    content += gnd_sym(G(118), G(53))
    
    # IN2 from USB_5V_IN
    content += wire(G(85), G(97), G(112), G(97))
    content += wire(G(112), G(97), G(112), G(71))
    content += wire(G(112), G(71), G(125), G(71))
    
    # CP2, OV1, OV2, GND to system ground
    content += wire(G(125), G(65), G(122), G(65))
    content += wire(G(125), G(63), G(122), G(63))
    content += wire(G(125), G(61), G(122), G(61))
    content += wire(G(125), G(55), G(122), G(55))
    content += wire(G(122), G(65), G(122), G(52))
    content += gnd_sym(G(122), G(52))
    
    # OUT pins (1 and 8) tied together at Y = G(72)
    content += wire(G(145), G(73), G(148), G(73))
    content += wire(G(145), G(71), G(148), G(71))
    content += wire(G(148), G(73), G(148), G(71))
    content += wire(G(148), G(72), G(170), G(72))
    
    # C4
    content += junc(G(170), G(72))
    content += wire(G(170), G(72), G(170), G(69))
    content += wire(G(170), G(63), G(170), G(58))
    content += gnd_sym(G(170), G(58))
    
    # C5
    content += wire(G(170), G(72), G(180), G(72))
    content += junc(G(180), G(72))
    content += wire(G(180), G(72), G(180), G(69))
    content += wire(G(180), G(63), G(180), G(58))
    content += gnd_sym(G(180), G(58))
    
    # TP3 & Global/Hierarchical label VBUS_MUX
    content += wire(G(180), G(72), G(190), G(72))
    content += junc(G(190), G(72))
    content += wire(G(190), G(72), G(190), G(66))
    content += pwr_flag(G(190), G(66))
    content += wire(G(190), G(72), G(200), G(72))
    content += global_lbl("VBUS_MUX", G(200), G(72), 0, "bidirectional")
    content += hier_lbl("VBUS_MUX", G(200), G(76), 0, "output")
    
    # SS capacitor C6
    content += wire(G(145), G(67), G(152), G(67))
    content += wire(G(158), G(67), G(162), G(67))
    content += gnd_sym(G(162), G(67))
    
    # ILIM resistor R5
    content += wire(G(145), G(65), G(148), G(65))
    content += wire(G(148), G(65), G(148), G(60))
    content += wire(G(148), G(60), G(152), G(60))
    content += wire(G(158), G(60), G(162), G(60))
    content += gnd_sym(G(162), G(60))
    
    # ST pin 9
    content += wire(G(145), G(63), G(150), G(63))
    content += junc(G(150), G(63))
    content += wire(G(150), G(63), G(155), G(63))
    content += wire(G(155), G(63), G(155), G(71))
    content += wire(G(155), G(77), G(155), G(80))
    content += wire(G(155), G(80), G(170), G(80))
    content += wire(G(170), G(80), G(170), G(72))
    
    content += wire(G(150), G(63), G(150), G(55))
    content += wire(G(150), G(55), G(150), G(48))
    content += global_lbl("MUX_ST", G(150), G(48), 0, "output")
    
    # Annotations & Section Headings
    content += sch_text("KHỐI CHỌN NGUỒN ĐẦU VÀO TỰ ĐỘNG (SEAMLESS POWER MULTIPLEXER)", G(20), G(18), 2.0, True)
    content += sch_text("Ưu tiên: VEHICLE_5V_IN (PR1 threshold = 4.24V) | Dự phòng: USB_5V_IN", G(20), G(24), 1.3, False)
    content += sch_text("Bảo vệ quá dòng: ILIM = 3.5A (R5 = 28.7k) | Khóa dòng ngược tích hợp", G(20), G(28), 1.3, False)
    content += sch_text("CỔNG VÀO NGUỒN XE (5V REGULATED)", G(20), G(34), 1.4, True)
    content += sch_text("CỔNG VÀO USB-C (SINK CC1/CC2 5.1k)", G(20), G(85), 1.4, True)
    content += sch_text("TPS2121 MUX OUTPUT: VBUS_MUX (CUNG CẤP CHO BQ25895)", G(130), G(38), 1.4, True)
    
    content += ")\n"
    
    out_file = os.path.join(OUT_DIR, "01_INPUT_SELECTION.kicad_sch")
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Sheet 1 built: {out_file}")

build_sheet1()
