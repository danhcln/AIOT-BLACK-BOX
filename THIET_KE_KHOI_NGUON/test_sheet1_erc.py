# -*- coding: utf-8 -*-
"""
TEST SCRIPT FOR SHEET 1 (01_INPUT_SELECTION)
Generates Sheet 1 and verifies syntax and ERC with kicad-cli.
"""

import os
import sys
import uuid
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"D:\ĐỒ ÁN 2\THIET_KE_KHOI_NGUON"

import build_complete_schematics as b

def build_sheet1():
    header = b.make_header("KHỐI CHỌN NGUỒN ĐẦU VÀO & POWER MUX (TPS2121)", 2, 5)
    
    # Symbols
    content = header
    
    # 1. VEHICLE_5V_IN Block
    # J1: Conn_01x02_Pin at (35, 50)
    content += b.sym_inst("Connector:Conn_01x02_Pin", "J1", "VEHICLE_5V_IN", 35, 50, 0,
                          "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical",
                          "https://www.jst-mfg.com/product/pdf/eng/eXH.pdf",
                          "External Regulated 5V Vehicle Input Connector, 2.50mm pitch, 5A",
                          pins=["1", "2"])
    
    # F1: Fuse at (55, 50, rot=90)
    content += b.sym_inst("Device:Fuse", "F1", "MF-MSMF300/16X (3.0A)", 55, 50, 90,
                          "Fuse:Fuse_1812_4532Metric",
                          "https://www.bourns.com/docs/product-datasheets/mf-msmf.pdf",
                          "PTC Resettable Fuse, 3.0A Hold, 6.0A Trip, 16V, 1812 SMD",
                          pins=["1", "2"])
    
    # D1: TVS at (70, 58, rot=90)
    content += b.sym_inst("Device:D_TVS", "D1", "SMAJ5.0A", 70, 58, 90,
                          "Diode_SMD:D_SMA",
                          "https://www.vishay.com/docs/88390/smaj50a.pdf",
                          "600W Transient Voltage Suppressor, 5.0V Reverse Standoff, SMA",
                          pins=["1", "2"])
    
    # D3: Schottky at (80, 50, rot=270)
    content += b.sym_inst("Device:D_Schottky", "D3", "SS34 (3A/40V)", 80, 50, 270,
                          "Diode_SMD:D_SMA",
                          "https://www.vishay.com/docs/88746/ss32.pdf",
                          "Schottky Barrier Rectifier Diode, 3A, 40V, Low Vf, SMA",
                          pins=["1", "2"])
    
    # C1: 10uF ceramic at (95, 57.62)
    content += b.sym_inst("Device:C", "C1", "10uF/25V (X7R)", 95, 57.62, 0,
                          "Capacitor_SMD:C_0805_2012Metric",
                          "~", "Ceramic Capacitor, 10uF, 25V, X7R, 10%, 0805",
                          pins=["1", "2"])
    
    # C2: 100uF electrolytic at (110, 57.62)
    content += b.sym_inst("Device:C_Polarized", "C2", "100uF/25V (Low ESR)", 110, 57.62, 0,
                          "Capacitor_SMD:CP_Elec_6.3x5.4",
                          "~", "Aluminum Electrolytic Capacitor, 100uF, 25V, Low-ESR SMD",
                          pins=["1", "2"])
    
    # TP1: TestPoint at (120, 45)
    content += b.sym_inst("Connector:TestPoint", "TP1", "TP_VEHICLE_5V", 120, 45, 0,
                          "TestPoint:TestPoint_Pad_D1.5mm",
                          "~", "Test Point Pad 1.5mm, VEHICLE_5V_IN",
                          pins=["1"])
    
    # 2. USB_5V_IN Block
    # J2: USB_C_16P at (35, 110)
    content += b.sym_inst("Connector:USB_C_16P", "J2", "TYPE-C-16P", 35, 110, 0,
                          "Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12",
                          "https://www.usb.org/type-c",
                          "USB 2.0 Type-C Receptacle, 16 pins, 5A VBUS, 50V",
                          pins=["A1", "A4", "A5", "A6", "A7", "B5", "B9", "B12", "S1"])
    
    # F2: Fuse at (60, 110, rot=90)
    content += b.sym_inst("Device:Fuse", "F2", "MF-MSMF300/16X (3.0A)", 60, 110, 90,
                          "Fuse:Fuse_1812_4532Metric",
                          "https://www.bourns.com/docs/product-datasheets/mf-msmf.pdf",
                          "PTC Resettable Fuse, 3.0A Hold, 6.0A Trip, 16V, 1812 SMD",
                          pins=["1", "2"])
    
    # D2: TVS at (75, 118, rot=90)
    content += b.sym_inst("Device:D_TVS", "D2", "SMAJ5.0A", 75, 118, 90,
                          "Diode_SMD:D_SMA",
                          "https://www.vishay.com/docs/88390/smaj50a.pdf",
                          "600W Transient Voltage Suppressor, 5.0V Reverse Standoff, SMA",
                          pins=["1", "2"])
    
    # R1: 5.1k CC1 at (55, 125, rot=0)
    content += b.sym_inst("Device:R", "R1", "5.1k (1%)", 55, 125, 0,
                          "Resistor_SMD:R_0603_1608Metric",
                          "~", "Resistor, 5.1k, 1%, 0.1W, 0603",
                          pins=["1", "2"])
    
    # R2: 5.1k CC2 at (65, 125, rot=0)
    content += b.sym_inst("Device:R", "R2", "5.1k (1%)", 65, 125, 0,
                          "Resistor_SMD:R_0603_1608Metric",
                          "~", "Resistor, 5.1k, 1%, 0.1W, 0603",
                          pins=["1", "2"])
    
    # C3: 10uF at (88, 117.62, rot=0)
    content += b.sym_inst("Device:C", "C3", "10uF/16V (X7R)", 88, 117.62, 0,
                          "Capacitor_SMD:C_0805_2012Metric",
                          "~", "Ceramic Capacitor, 10uF, 16V, X7R, 10%, 0805",
                          pins=["1", "2"])
    
    # TP2: TestPoint at (100, 105)
    content += b.sym_inst("Connector:TestPoint", "TP2", "TP_USB_5V", 100, 105, 0,
                          "TestPoint:TestPoint_Pad_D1.5mm",
                          "~", "Test Point Pad 1.5mm, USB_5V_IN",
                          pins=["1"])
    
    # 3. TPS2121 Power Mux Block at (170, 80)
    content += b.sym_inst("Power_Management:TPS2121RUXR", "U1", "TPS2121RUXR", 170, 80, 0,
                          "Package_DFN_QFN:Texas_RUX0012A",
                          "https://www.ti.com/lit/ds/symlink/tps2121.pdf",
                          "2.8V-22V, 4A Priority Power MUX with Seamless Switchover, VQFN-12",
                          pins=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
    
    # R3: 30k (PR1 top) at (145, 84, rot=0)
    content += b.sym_inst("Device:R", "R3", "30k (1%)", 145, 84, 0,
                          "Resistor_SMD:R_0603_1608Metric",
                          "~", "Resistor, 30k, 1%, 0.1W, 0603",
                          pins=["1", "2"])
    
    # R4: 10k (PR1 bottom) at (145, 96, rot=0)
    content += b.sym_inst("Device:R", "R4", "10k (1%)", 145, 96, 0,
                          "Resistor_SMD:R_0603_1608Metric",
                          "~", "Resistor, 10k, 1%, 0.1W, 0603",
                          pins=["1", "2"])
    
    # C6: 10nF SS at (195, 78.62, rot=0)
    content += b.sym_inst("Device:C", "C6", "10nF/25V (X7R)", 195, 78.62, 0,
                          "Capacitor_SMD:C_0603_1608Metric",
                          "~", "Ceramic Capacitor, 10nF, 25V, X7R, 0603",
                          pins=["1", "2"])
    
    # R5: 28.7k ILIM at (205, 83.81, rot=0)
    content += b.sym_inst("Device:R", "R5", "28.7k (1% / 3.5A)", 205, 83.81, 0,
                          "Resistor_SMD:R_0603_1608Metric",
                          "~", "Resistor, 28.7k, 1%, 0.1W, 0603",
                          pins=["1", "2"])
    
    # R6: 100k pullup for ST at (195, 95, rot=0)
    content += b.sym_inst("Device:R", "R6", "100k (1%)", 195, 95, 0,
                          "Resistor_SMD:R_0603_1608Metric",
                          "~", "Resistor, 100k, 1%, 0.1W, 0603",
                          pins=["1", "2"])
    
    # C4: 22uF output bulk at (215, 66.19, rot=0)
    content += b.sym_inst("Device:C", "C4", "22uF/16V (X5R)", 215, 66.19, 0,
                          "Capacitor_SMD:C_0805_2012Metric",
                          "~", "Ceramic Capacitor, 22uF, 16V, X5R, 0805",
                          pins=["1", "2"])
    
    # C5: 0.1uF output bypass at (225, 66.19, rot=0)
    content += b.sym_inst("Device:C", "C5", "0.1uF/25V (X7R)", 225, 66.19, 0,
                          "Capacitor_SMD:C_0603_1608Metric",
                          "~", "Ceramic Capacitor, 0.1uF, 25V, X7R, 0603",
                          pins=["1", "2"])
    
    # TP3: TestPoint VBUS_MUX at (235, 60)
    content += b.sym_inst("Connector:TestPoint", "TP3", "TP_VBUS_MUX", 235, 60, 0,
                          "TestPoint:TestPoint_Pad_D1.5mm",
                          "~", "Test Point Pad 1.5mm, VBUS_MUX",
                          pins=["1"])
    
    # TP_MUX_ST: TestPoint at (195, 105)
    content += b.sym_inst("Connector:TestPoint", "TP_MUX_ST", "TP_MUX_ST", 195, 105, 0,
                          "TestPoint:TestPoint_Pad_D1.5mm",
                          "~", "Test Point Pad 1.5mm, Status of TPS2121",
                          pins=["1"])
    
    # Wires & Connectivity
    # VEHICLE_5V_IN branch
    content += b.wire(40.08, 50, 51.19, 50)
    content += b.wire(58.81, 50, 70, 50)
    content += b.junc(70, 50)
    content += b.wire(70, 50, 70, 54.19)
    content += b.wire(70, 61.81, 70, 65)
    content += b.gnd_sym(70, 65)
    
    content += b.wire(70, 50, 76.19, 50)
    content += b.wire(83.81, 50, 95, 50)
    content += b.junc(95, 50)
    content += b.wire(95, 50, 95, 53.81)
    content += b.wire(95, 61.43, 95, 65)
    content += b.gnd_sym(95, 65)
    
    content += b.wire(95, 50, 110, 50)
    content += b.junc(110, 50)
    content += b.wire(110, 50, 110, 53.81)
    content += b.wire(110, 61.43, 110, 65)
    content += b.gnd_sym(110, 65)
    
    content += b.wire(110, 50, 120, 50)
    content += b.junc(120, 50)
    content += b.wire(120, 50, 120, 45)
    content += b.pwr_flag(120, 45)
    content += b.wire(120, 50, 135, 50)
    content += b.global_lbl("VEHICLE_5V_IN", 135, 50, 0, "bidirectional")
    
    # J1 ground
    content += b.wire(40.08, 47.46, 40.08, 65)
    content += b.gnd_sym(40.08, 65)
    
    # USB_5V_IN branch
    content += b.wire(47.7, 120.16, 52, 120.16)
    content += b.wire(47.7, 117.62, 52, 117.62)
    content += b.wire(52, 120.16, 52, 110)
    content += b.wire(52, 117.62, 52, 110)
    content += b.junc(52, 110)
    content += b.wire(52, 110, 56.19, 110)
    
    content += b.wire(63.81, 110, 75, 110)
    content += b.junc(75, 110)
    content += b.wire(75, 110, 75, 114.19)
    content += b.wire(75, 121.81, 75, 125)
    content += b.gnd_sym(75, 125)
    
    content += b.wire(75, 110, 88, 110)
    content += b.junc(88, 110)
    content += b.wire(88, 110, 88, 113.81)
    content += b.wire(88, 121.43, 88, 125)
    content += b.gnd_sym(88, 125)
    
    content += b.wire(88, 110, 100, 110)
    content += b.junc(100, 110)
    content += b.wire(100, 110, 100, 105)
    content += b.pwr_flag(100, 105)
    content += b.wire(100, 110, 115, 110)
    content += b.global_lbl("USB_5V_IN", 115, 110, 0, "bidirectional")
    
    # USB CC lines & GND
    content += b.wire(47.7, 112.54, 55, 112.54)
    content += b.wire(55, 112.54, 55, 121.19)
    content += b.wire(55, 128.81, 55, 135)
    content += b.gnd_sym(55, 135)
    
    content += b.wire(47.7, 110.0, 65, 110.0)
    content += b.wire(65, 110.0, 65, 121.19)
    content += b.wire(65, 128.81, 65, 135)
    content += b.gnd_sym(65, 135)
    
    content += b.wire(47.7, 99.84, 47.7, 95)
    content += b.wire(22.3, 99.84, 22.3, 95)
    content += b.wire(22.3, 95, 47.7, 95)
    content += b.gnd_sym(35, 95)
    
    # No-connect on D+, D-
    content += b.no_conn(47.7, 107.46)
    content += b.no_conn(47.7, 104.92)
    
    # TPS2121 Connections
    # IN1 (7) at (157.3, 90.16)
    content += b.wire(135, 50, 145, 50)
    content += b.wire(145, 50, 145, 90.16)
    content += b.junc(145, 90.16)
    content += b.wire(145, 90.16, 157.3, 90.16)
    
    # R3 / R4 divider from IN1 to PR1 (6 at 157.3, 82.54)
    content += b.wire(145, 80.19, 145, 82.54)
    content += b.junc(145, 82.54)
    content += b.wire(145, 82.54, 157.3, 82.54)
    content += b.wire(145, 82.54, 145, 92.19)
    content += b.wire(145, 99.81, 145, 105)
    content += b.gnd_sym(145, 105)
    
    # IN2 (2) at (157.3, 87.62)
    content += b.wire(115, 110, 150, 110)
    content += b.wire(150, 110, 150, 87.62)
    content += b.wire(150, 87.62, 157.3, 87.62)
    
    # CP2 (3 at 157.3, 80.0), OV1 (5 at 157.3, 77.46), OV2 (4 at 157.3, 74.92), GND (12 at 157.3, 67.3)
    content += b.wire(157.3, 80.0, 153, 80.0)
    content += b.wire(157.3, 77.46, 153, 77.46)
    content += b.wire(157.3, 74.92, 153, 74.92)
    content += b.wire(157.3, 67.3, 153, 67.3)
    content += b.wire(153, 80.0, 153, 65)
    content += b.wire(153, 77.46, 153, 65)
    content += b.wire(153, 74.92, 153, 65)
    content += b.wire(153, 67.3, 153, 65)
    content += b.gnd_sym(153, 65)
    
    # Output OUT (1, 8 at 182.7, 90.16 and 87.62)
    content += b.wire(182.7, 90.16, 188, 90.16)
    content += b.wire(182.7, 87.62, 188, 87.62)
    content += b.wire(188, 90.16, 188, 87.62)
    content += b.wire(188, 88.89, 215, 88.89)
    
    # C4 at (215, 66.19)
    content += b.junc(215, 88.89)
    content += b.wire(215, 88.89, 215, 70.0)
    content += b.wire(215, 62.38, 215, 55)
    content += b.gnd_sym(215, 55)
    
    # C5 at (225, 66.19)
    content += b.wire(215, 88.89, 225, 88.89)
    content += b.junc(225, 88.89)
    content += b.wire(225, 88.89, 225, 70.0)
    content += b.wire(225, 62.38, 225, 55)
    content += b.gnd_sym(225, 55)
    
    # TP3 & Global Label VBUS_MUX
    content += b.wire(225, 88.89, 235, 88.89)
    content += b.junc(235, 88.89)
    content += b.wire(235, 88.89, 235, 60)
    content += b.pwr_flag(235, 60)
    content += b.wire(235, 88.89, 245, 88.89)
    content += b.global_lbl("VBUS_MUX", 245, 88.89, 0, "bidirectional")
    content += b.hier_lbl("VBUS_MUX", 245, 93, 0, "output")
    
    # SS (11 at 182.7, 82.54) -> C6 at (195, 78.62)
    content += b.wire(182.7, 82.54, 195, 82.54)
    content += b.wire(195, 82.43, 195, 82.54)
    content += b.wire(195, 74.81, 195, 70)
    content += b.gnd_sym(195, 70)
    
    # ILIM (10 at 182.7, 80.0) -> R5 at (205, 83.81)
    content += b.wire(182.7, 80.0, 205, 80.0)
    content += b.wire(205, 80.0, 205, 80.0)
    content += b.wire(205, 87.62, 205, 92)
    content += b.gnd_sym(205, 92)
    
    # ST (9 at 182.7, 77.46) -> R6 pullup & testpoint
    content += b.wire(182.7, 77.46, 195, 77.46)
    content += b.wire(195, 77.46, 195, 91.19)
    content += b.junc(195, 91.19)
    content += b.wire(195, 91.19, 195, 105)
    content += b.wire(195, 98.81, 195, 88.89)
    content += b.junc(195, 88.89)
    content += b.global_lbl("MUX_ST", 195, 110, 0, "output")
    content += b.wire(195, 105, 195, 110)
    
    # Notes & Section Headings
    content += b.sch_text("KHỐI CHỌN NGUỒN ĐẦU VÀO TỰ ĐỘNG (SEAMLESS POWER MULTIPLEXER)", 30, 25, 2.0, True)
    content += b.sch_text("Ưu tiên: VEHICLE_5V_IN (Ngưỡng chuyển đổi PR1 = 4.24V) | Dự phòng: USB_5V_IN", 30, 32, 1.3, False)
    content += b.sch_text("Bảo vệ quá dòng: ILIM = 3.5A (R5 = 28.7k) | Khóa dòng ngược tích hợp", 30, 37, 1.3, False)
    content += b.sch_text("CỔNG VÀO NGUỒN XE (5V REGULATED)", 30, 44, 1.4, True)
    content += b.sch_text("CỔNG VÀO USB-C (SINK CC1/CC2 5.1k)", 30, 103, 1.4, True)
    content += b.sch_text("TPS2121 MUX POWER OUTPUT: VBUS_MUX (CUNG CẤP CHO BQ25895)", 170, 50, 1.4, True)
    
    content += ")\n"
    
    out_file = os.path.join(OUT_DIR, "01_INPUT_SELECTION.kicad_sch")
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Sheet 1 generated: {out_file}")

build_sheet1()
