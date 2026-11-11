# -*- coding: utf-8 -*-
"""
Generator for Sheet 3: 03_BOOST_BUCK_RAILS.kicad_sch
Implements:
1. TPS61088RHLR Synchronous Boost Converter (SYS -> 5V_SYS, 3.5A / 5A Peak)
2. TPS62162DSGR Synchronous Buck Converter (5V_SYS -> 3V3_SYS, 1.0A Fixed)

100% Planar Topology - Left-to-Right Power Flow - Strict 1.27mm Grid.
"""

import sys
import os

sys.path.append(r"D:\ĐỒ ÁN 2\THIET_KE_KHOI_NGUON")
import build_complete_power_project as bp
import custom_symbols_def as cust_syms
import generate_symbols as base_syms

def build_sheet3():
    content = bp.make_header("KHỐI NGUỒN 5V VÀ 3.3V HỆ THỐNG (TPS61088 BOOST & TPS62162 BUCK)", 4, 5)

    # -------------------------------------------------------------------------
    # 1. TPS61088 Boost Converter (SYS -> 5V_SYS)
    # Center U4 at (110.49, 95.25)
    # -------------------------------------------------------------------------
    u4_x, u4_y = 110.49, 95.25
    content += bp.sym_inst("Power_Management:TPS61088RHLR", "U4", "TPS61088RHLR", u4_x, u4_y, 0,
                           "Package_DFN_QFN:Texas_RHL0020A",
                           "https://www.ti.com/lit/ds/symlink/tps61088.pdf",
                           "2.7V-12V, 10A Fully Integrated Synchronous Boost Converter, VQFN-20",
                           pins=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                                 "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21"])

    # Input Capacitors: C18, C19, C20 along SYS rail at Y = 77.47
    c18_x, c18_y = 40.64, 81.28
    content += bp.sym_inst("Device:C", "C18", "22uF/10V (X5R)", c18_x, c18_y, 0,
                           "Capacitor_SMD:C_0805_2012Metric",
                           "~", "Input Low-ESR Ceramic Capacitor, 22uF, 10V, X5R, 0805",
                           pins=["1", "2"])

    c19_x, c19_y = 48.26, 81.28
    content += bp.sym_inst("Device:C", "C19", "22uF/10V (X5R)", c19_x, c19_y, 0,
                           "Capacitor_SMD:C_0805_2012Metric",
                           "~", "Input Low-ESR Ceramic Capacitor, 22uF, 10V, X5R, 0805",
                           pins=["1", "2"])

    c20_x, c20_y = 55.88, 81.28
    content += bp.sym_inst("Device:C", "C20", "100nF/16V (X7R)", c20_x, c20_y, 0,
                           "Capacitor_SMD:C_0603_1608Metric",
                           "~", "High-Frequency Decoupling Capacitor, 100nF, 16V, X7R, 0603",
                           pins=["1", "2"])

    # Inductor L2 (1.0uH / 10A Saturation) placed horizontally at (76.20, 82.55)
    l2_x, l2_y = 76.20, 82.55
    content += bp.sym_inst("Device:L", "L2", "1.0uH (10A Sat)", l2_x, l2_y, 90,
                           "Inductor_SMD:L_Bourns_SRP6540",
                           "https://www.bourns.com/docs/product-datasheets/srp6540.pdf",
                           "Shielded Power Inductor, 1.0uH, 10A Isat, Low DCR SMD",
                           pins=["1", "2"])

    # Bootstrap capacitor C23 (100nF) between BOOT (Y = 95.25) and SW (Y = 90.17)
    c23_x, c23_y = 80.01, 92.71
    content += bp.sym_inst("Device:C", "C23", "100nF/16V (X7R)", c23_x, c23_y, 90,
                           "Capacitor_SMD:C_0603_1608Metric",
                           "~", "High-Side Bootstrap Ceramic Capacitor, 100nF, 16V, 0603",
                           pins=["1", "2"])

    # Left-side Bias & Configuration Passives (X = 80.01)
    c21_x, c21_y = 80.01, 100.33 # VCC cap
    content += bp.sym_inst("Device:C", "C21", "4.7uF/10V (X5R)", c21_x, c21_y, 90,
                           "Capacitor_SMD:C_0603_1608Metric",
                           "~", "VCC LDO Bias Ceramic Capacitor, 4.7uF, 10V, X5R, 0603",
                           pins=["1", "2"])

    r19_x, r19_y = 80.01, 102.87 # MODE (PWM)
    content += bp.sym_inst("Device:R", "R19", "0 (PWM)", r19_x, r19_y, 90,
                           "Resistor_SMD:R_0603_1608Metric",
                           "~", "MODE Selection (0 Ohm to GND for Forced PWM), 0603",
                           pins=["1", "2"])

    r20_x, r20_y = 80.01, 105.41 # FSW
    content += bp.sym_inst("Device:R", "R20", "200k (1%)", r20_x, r20_y, 90,
                           "Resistor_SMD:R_0603_1608Metric",
                           "~", "Switching Frequency Set Resistor (600kHz), 200k, 1%, 0603",
                           pins=["1", "2"])

    c22_x, c22_y = 80.01, 107.95 # SS
    content += bp.sym_inst("Device:C", "C22", "47nF/16V (X7R)", c22_x, c22_y, 90,
                           "Capacitor_SMD:C_0603_1608Metric",
                           "~", "Soft-Start Ceramic Capacitor, 47nF, 16V, X7R, 0603",
                           pins=["1", "2"])

    r21_x, r21_y = 80.01, 110.49 # ILIM
    content += bp.sym_inst("Device:R", "R21", "12k (1%)", r21_x, r21_y, 90,
                           "Resistor_SMD:R_0603_1608Metric",
                           "~", "Peak Inductor Current Limit (10A), 12k, 1%, 0603",
                           pins=["1", "2"])

    # Output Capacitors: C24, C25, C26, C27 (4x 22uF) directly on 5V_SYS rail at Y = 77.47
    c24_x, c24_y = 144.78, 81.28
    content += bp.sym_inst("Device:C", "C24", "22uF/10V (X5R)", c24_x, c24_y, 0,
                           "Capacitor_SMD:C_0805_2012Metric",
                           "~", "Output Ceramic Capacitor, 22uF, 10V, X5R, 0805",
                           pins=["1", "2"])

    c25_x, c25_y = 152.40, 81.28
    content += bp.sym_inst("Device:C", "C25", "22uF/10V (X5R)", c25_x, c25_y, 0,
                           "Capacitor_SMD:C_0805_2012Metric",
                           "~", "Output Ceramic Capacitor, 22uF, 10V, X5R, 0805",
                           pins=["1", "2"])

    c26_x, c26_y = 160.02, 81.28
    content += bp.sym_inst("Device:C", "C26", "22uF/10V (X5R)", c26_x, c26_y, 0,
                           "Capacitor_SMD:C_0805_2012Metric",
                           "~", "Output Ceramic Capacitor, 22uF, 10V, X5R, 0805",
                           pins=["1", "2"])

    c27_x, c27_y = 167.64, 81.28
    content += bp.sym_inst("Device:C", "C27", "22uF/10V (X5R)", c27_x, c27_y, 0,
                           "Capacitor_SMD:C_0805_2012Metric",
                           "~", "Output Ceramic Capacitor, 22uF, 10V, X5R, 0805",
                           pins=["1", "2"])

    # Feedback divider: R22 (316k 1%), R23 (100k 1%), C28 (10pF Cff)
    r22_x, r22_y = 137.16, 85.09
    content += bp.sym_inst("Device:R", "R22", "316k (1%)", r22_x, r22_y, 0,
                           "Resistor_SMD:R_0603_1608Metric",
                           "~", "Feedback Divider Top Resistor, 316k, 1%, 0603",
                           pins=["1", "2"])

    c28_x, c28_y = 137.16, 85.09 # Parallel with R22 at same Y or offset
    # Let's offset C28 to X = 132.08, Y = 85.09
    c28_x = 132.08
    content += bp.sym_inst("Device:C", "C28", "10pF/50V (C0G)", c28_x, c28_y, 0,
                           "Capacitor_SMD:C_0603_1608Metric",
                           "~", "Feedback Feedforward Capacitor, 10pF, 50V, C0G, 0603",
                           pins=["1", "2"])

    r23_x, r23_y = 137.16, 96.52
    content += bp.sym_inst("Device:R", "R23", "100k (1%)", r23_x, r23_y, 0,
                           "Resistor_SMD:R_0603_1608Metric",
                           "~", "Feedback Divider Bottom Resistor, 100k, 1%, 0603",
                           pins=["1", "2"])

    # Compensation network: R24 (20k), C29 (2.2nF), C30 (47pF)
    r24_x, r24_y = 134.62, 95.25
    content += bp.sym_inst("Device:R", "R24", "20k (1%)", r24_x, r24_y, 90,
                           "Resistor_SMD:R_0603_1608Metric",
                           "~", "Loop Compensation Resistor, 20k, 1%, 0603",
                           pins=["1", "2"])

    c29_x, c29_y = 142.24, 99.06
    content += bp.sym_inst("Device:C", "C29", "2.2nF/25V (X7R)", c29_x, c29_y, 0,
                           "Capacitor_SMD:C_0603_1608Metric",
                           "~", "Loop Compensation Series Capacitor, 2.2nF, 25V, 0603",
                           pins=["1", "2"])

    c30_x, c30_y = 149.86, 99.06
    content += bp.sym_inst("Device:C", "C30", "47pF/50V (C0G)", c30_x, c30_y, 0,
                           "Capacitor_SMD:C_0603_1608Metric",
                           "~", "Loop High-Frequency Roll-Off Capacitor, 47pF, 50V, 0603",
                           pins=["1", "2"])

    # Test point TP6 for 5V_SYS
    tp6_x, tp6_y = 175.26, 77.47
    content += bp.sym_inst("Connector:TestPoint", "TP6", "TP_5V_SYS", tp6_x, tp6_y, 0,
                           "TestPoint:TestPoint_Pad_D1.5mm",
                           "~", "Test Point for Regulated 5V System Power Rail (5V_SYS)",
                           pins=["1"])

    # -------------------------------------------------------------------------
    # 2. TPS62162 Buck Converter (5V_SYS -> 3V3_SYS)
    # Center U5 at (215.90, 95.25)
    # -------------------------------------------------------------------------
    u5_x, u5_y = 215.90, 95.25
    content += bp.sym_inst("Power_Management:TPS62162DSGR", "U5", "TPS62162DSGR", u5_x, u5_y, 0,
                           "Package_SON:WSON-8-1EP_2x2mm_P0.5mm_EP0.9x1.6mm",
                           "https://www.ti.com/lit/ds/symlink/tps62162.pdf",
                           "3V-17V, 1A Step-Down Converter with DCS-Control, Fixed 3.3V, WSON-8",
                           pins=["1", "2", "3", "4", "5", "6", "7", "8", "9"])

    # Input Capacitors for TPS62162: C31 (10uF), C32 (100nF) along 5V_SYS input line (Y = 87.63)
    c31_x, c31_y = 193.04, 91.44
    content += bp.sym_inst("Device:C", "C31", "10uF/10V (X5R)", c31_x, c31_y, 0,
                           "Capacitor_SMD:C_0805_2012Metric",
                           "~", "Buck Input Low-ESR Ceramic Capacitor, 10uF, 10V, X5R, 0805",
                           pins=["1", "2"])

    c32_x, c32_y = 185.42, 91.44
    content += bp.sym_inst("Device:C", "C32", "100nF/16V (X7R)", c32_x, c32_y, 0,
                           "Capacitor_SMD:C_0603_1608Metric",
                           "~", "Buck Input Decoupling Capacitor, 100nF, 16V, X7R, 0603",
                           pins=["1", "2"])

    # EN Pullup Resistor R25 (100k) to 5V_SYS
    r25_x, r25_y = 198.12, 91.44
    content += bp.sym_inst("Device:R", "R25", "100k (1%)", r25_x, r25_y, 0,
                           "Resistor_SMD:R_0603_1608Metric",
                           "~", "Buck Enable Pullup Resistor, 100k, 1%, 0603",
                           pins=["1", "2"])

    # Buck Inductor L3 (2.2uH / 2.5A)
    l3_x, l3_y = 238.76, 92.71
    content += bp.sym_inst("Device:L", "L3", "2.2uH (2.5A Sat)", l3_x, l3_y, 90,
                           "Inductor_SMD:L_Bourns_SRP4020TA",
                           "https://www.bourns.com/docs/product-datasheets/srp4020ta.pdf",
                           "Shielded Power Inductor, 2.2uH, 2.5A Isat, Low DCR SMD",
                           pins=["1", "2"])

    # Output Capacitors for TPS62162: C33 (22uF), C34 (100nF) along Y = 92.71
    c33_x, c33_y = 254.00, 96.52
    content += bp.sym_inst("Device:C", "C33", "22uF/10V (X5R)", c33_x, c33_y, 0,
                           "Capacitor_SMD:C_0805_2012Metric",
                           "~", "Buck Output Low-ESR Ceramic Capacitor, 22uF, 10V, X5R, 0805",
                           pins=["1", "2"])

    c34_x, c34_y = 261.62, 96.52
    content += bp.sym_inst("Device:C", "C34", "100nF/16V (X7R)", c34_x, c34_y, 0,
                           "Capacitor_SMD:C_0603_1608Metric",
                           "~", "Buck Output High-Frequency Capacitor, 100nF, 16V, X7R, 0603",
                           pins=["1", "2"])

    # Test point TP7 for 3V3_SYS
    tp7_x, tp7_y = 269.24, 92.71
    content += bp.sym_inst("Connector:TestPoint", "TP7", "TP_3V3_SYS", tp7_x, tp7_y, 0,
                           "TestPoint:TestPoint_Pad_D1.5mm",
                           "~", "Test Point for Regulated 3.3V Peripheral Rail (3V3_SYS)",
                           pins=["1"])

    # -------------------------------------------------------------------------
    # PIN COORDINATE EXTRACTION
    # -------------------------------------------------------------------------
    u4_p9 = bp.pin_pos(cust_syms.SYM_TPS61088, u4_x, u4_y, "9", 0)    # VIN
    u4_p4 = bp.pin_pos(cust_syms.SYM_TPS61088, u4_x, u4_y, "4", 0)    # SW
    u4_p5 = bp.pin_pos(cust_syms.SYM_TPS61088, u4_x, u4_y, "5", 0)    # SW
    u4_p6 = bp.pin_pos(cust_syms.SYM_TPS61088, u4_x, u4_y, "6", 0)    # SW
    u4_p7 = bp.pin_pos(cust_syms.SYM_TPS61088, u4_x, u4_y, "7", 0)    # SW
    u4_p8 = bp.pin_pos(cust_syms.SYM_TPS61088, u4_x, u4_y, "8", 0)    # BOOT
    u4_p2 = bp.pin_pos(cust_syms.SYM_TPS61088, u4_x, u4_y, "2", 0)    # EN
    u4_p1 = bp.pin_pos(cust_syms.SYM_TPS61088, u4_x, u4_y, "1", 0)    # VCC
    u4_p13 = bp.pin_pos(cust_syms.SYM_TPS61088, u4_x, u4_y, "13", 0)  # MODE
    u4_p3 = bp.pin_pos(cust_syms.SYM_TPS61088, u4_x, u4_y, "3", 0)    # FSW
    u4_p10 = bp.pin_pos(cust_syms.SYM_TPS61088, u4_x, u4_y, "10", 0)  # SS
    u4_p19 = bp.pin_pos(cust_syms.SYM_TPS61088, u4_x, u4_y, "19", 0)  # ILIM
    u4_p20 = bp.pin_pos(cust_syms.SYM_TPS61088, u4_x, u4_y, "20", 0)  # PGND
    
    u4_p14 = bp.pin_pos(cust_syms.SYM_TPS61088, u4_x, u4_y, "14", 0)  # VOUT
    u4_p15 = bp.pin_pos(cust_syms.SYM_TPS61088, u4_x, u4_y, "15", 0)  # VOUT
    u4_p16 = bp.pin_pos(cust_syms.SYM_TPS61088, u4_x, u4_y, "16", 0)  # VOUT
    u4_p17 = bp.pin_pos(cust_syms.SYM_TPS61088, u4_x, u4_y, "17", 0)  # FB
    u4_p18 = bp.pin_pos(cust_syms.SYM_TPS61088, u4_x, u4_y, "18", 0)  # COMP
    u4_p11 = bp.pin_pos(cust_syms.SYM_TPS61088, u4_x, u4_y, "11", 0)  # NC
    u4_p12 = bp.pin_pos(cust_syms.SYM_TPS61088, u4_x, u4_y, "12", 0)  # NC
    u4_p21 = bp.pin_pos(cust_syms.SYM_TPS61088, u4_x, u4_y, "21", 0)  # EP/GND

    u5_p1 = bp.pin_pos(cust_syms.SYM_TPS62162, u5_x, u5_y, "1", 0)    # PGND
    u5_p2 = bp.pin_pos(cust_syms.SYM_TPS62162, u5_x, u5_y, "2", 0)    # VIN
    u5_p3 = bp.pin_pos(cust_syms.SYM_TPS62162, u5_x, u5_y, "3", 0)    # EN
    u5_p4 = bp.pin_pos(cust_syms.SYM_TPS62162, u5_x, u5_y, "4", 0)    # AGND
    u5_p5 = bp.pin_pos(cust_syms.SYM_TPS62162, u5_x, u5_y, "5", 0)    # FB
    u5_p6 = bp.pin_pos(cust_syms.SYM_TPS62162, u5_x, u5_y, "6", 0)    # VOS
    u5_p7 = bp.pin_pos(cust_syms.SYM_TPS62162, u5_x, u5_y, "7", 0)    # SW
    u5_p8 = bp.pin_pos(cust_syms.SYM_TPS62162, u5_x, u5_y, "8", 0)    # PG
    u5_p9 = bp.pin_pos(cust_syms.SYM_TPS62162, u5_x, u5_y, "9", 0)    # EP/GND

    c18_p1 = bp.pin_pos(base_syms.SYM_C, c18_x, c18_y, "1", 0)
    c18_p2 = bp.pin_pos(base_syms.SYM_C, c18_x, c18_y, "2", 0)
    c19_p1 = bp.pin_pos(base_syms.SYM_C, c19_x, c19_y, "1", 0)
    c19_p2 = bp.pin_pos(base_syms.SYM_C, c19_x, c19_y, "2", 0)
    c20_p1 = bp.pin_pos(base_syms.SYM_C, c20_x, c20_y, "1", 0)
    c20_p2 = bp.pin_pos(base_syms.SYM_C, c20_x, c20_y, "2", 0)
    
    l2_p1 = bp.pin_pos(base_syms.SYM_L, l2_x, l2_y, "1", 90)
    l2_p2 = bp.pin_pos(base_syms.SYM_L, l2_x, l2_y, "2", 90)

    c23_p1 = bp.pin_pos(base_syms.SYM_C, c23_x, c23_y, "1", 90)
    c23_p2 = bp.pin_pos(base_syms.SYM_C, c23_x, c23_y, "2", 90)

    c21_p1 = bp.pin_pos(base_syms.SYM_C, c21_x, c21_y, "1", 90)
    c21_p2 = bp.pin_pos(base_syms.SYM_C, c21_x, c21_y, "2", 90)
    
    r19_p1 = bp.pin_pos(base_syms.SYM_R, r19_x, r19_y, "1", 90)
    r19_p2 = bp.pin_pos(base_syms.SYM_R, r19_x, r19_y, "2", 90)
    r20_p1 = bp.pin_pos(base_syms.SYM_R, r20_x, r20_y, "1", 90)
    r20_p2 = bp.pin_pos(base_syms.SYM_R, r20_x, r20_y, "2", 90)
    c22_p1 = bp.pin_pos(base_syms.SYM_C, c22_x, c22_y, "1", 90)
    c22_p2 = bp.pin_pos(base_syms.SYM_C, c22_x, c22_y, "2", 90)
    r21_p1 = bp.pin_pos(base_syms.SYM_R, r21_x, r21_y, "1", 90)
    r21_p2 = bp.pin_pos(base_syms.SYM_R, r21_x, r21_y, "2", 90)

    c24_p1 = bp.pin_pos(base_syms.SYM_C, c24_x, c24_y, "1", 0)
    c24_p2 = bp.pin_pos(base_syms.SYM_C, c24_x, c24_y, "2", 0)
    c25_p1 = bp.pin_pos(base_syms.SYM_C, c25_x, c25_y, "1", 0)
    c25_p2 = bp.pin_pos(base_syms.SYM_C, c25_x, c25_y, "2", 0)
    c26_p1 = bp.pin_pos(base_syms.SYM_C, c26_x, c26_y, "1", 0)
    c26_p2 = bp.pin_pos(base_syms.SYM_C, c26_x, c26_y, "2", 0)
    c27_p1 = bp.pin_pos(base_syms.SYM_C, c27_x, c27_y, "1", 0)
    c27_p2 = bp.pin_pos(base_syms.SYM_C, c27_x, c27_y, "2", 0)

    r22_p1 = bp.pin_pos(base_syms.SYM_R, r22_x, r22_y, "1", 0)
    r22_p2 = bp.pin_pos(base_syms.SYM_R, r22_x, r22_y, "2", 0)
    c28_p1 = bp.pin_pos(base_syms.SYM_C, c28_x, c28_y, "1", 0)
    c28_p2 = bp.pin_pos(base_syms.SYM_C, c28_x, c28_y, "2", 0)
    r23_p1 = bp.pin_pos(base_syms.SYM_R, r23_x, r23_y, "1", 0)
    r23_p2 = bp.pin_pos(base_syms.SYM_R, r23_x, r23_y, "2", 0)

    r24_p1 = bp.pin_pos(base_syms.SYM_R, r24_x, r24_y, "1", 90)
    r24_p2 = bp.pin_pos(base_syms.SYM_R, r24_x, r24_y, "2", 90)
    c29_p1 = bp.pin_pos(base_syms.SYM_C, c29_x, c29_y, "1", 0)
    c29_p2 = bp.pin_pos(base_syms.SYM_C, c29_x, c29_y, "2", 0)
    c30_p1 = bp.pin_pos(base_syms.SYM_C, c30_x, c30_y, "1", 0)
    c30_p2 = bp.pin_pos(base_syms.SYM_C, c30_x, c30_y, "2", 0)
    tp6_p1 = bp.pin_pos(base_syms.SYM_TESTPOINT, tp6_x, tp6_y, "1", 0)

    c31_p1 = bp.pin_pos(base_syms.SYM_C, c31_x, c31_y, "1", 0)
    c31_p2 = bp.pin_pos(base_syms.SYM_C, c31_x, c31_y, "2", 0)
    c32_p1 = bp.pin_pos(base_syms.SYM_C, c32_x, c32_y, "1", 0)
    c32_p2 = bp.pin_pos(base_syms.SYM_C, c32_x, c32_y, "2", 0)
    r25_p1 = bp.pin_pos(base_syms.SYM_R, r25_x, r25_y, "1", 0)
    r25_p2 = bp.pin_pos(base_syms.SYM_R, r25_x, r25_y, "2", 0)

    l3_p1 = bp.pin_pos(base_syms.SYM_L, l3_x, l3_y, "1", 90)
    l3_p2 = bp.pin_pos(base_syms.SYM_L, l3_x, l3_y, "2", 90)
    c33_p1 = bp.pin_pos(base_syms.SYM_C, c33_x, c33_y, "1", 0)
    c33_p2 = bp.pin_pos(base_syms.SYM_C, c33_x, c33_y, "2", 0)
    c34_p1 = bp.pin_pos(base_syms.SYM_C, c34_x, c34_y, "1", 0)
    c34_p2 = bp.pin_pos(base_syms.SYM_C, c34_x, c34_y, "2", 0)
    tp7_p1 = bp.pin_pos(base_syms.SYM_TESTPOINT, tp7_x, tp7_y, "1", 0)

    # -------------------------------------------------------------------------
    # WIRING - SECTION 1: TPS61088 BOOST CONVERTER
    # -------------------------------------------------------------------------
    # Input Rail SYS comes in at (25.40, 77.47)
    content += bp.global_lbl("SYS", 25.40, 77.47, 180, "input")
    content += bp.hier_lbl("SYS", 25.40, 77.47, 180, "input")
    content += bp.wire(25.40, 77.47, c18_p1[0], 77.47)
    
    # Input Capacitors C18, C19, C20 tapped to SYS line at Y = 77.47
    content += bp.junc(c18_p1[0], 77.47)
    content += bp.gnd_sym(c18_p2[0], c18_p2[1])

    content += bp.wire(c18_p1[0], 77.47, c19_p1[0], 77.47)
    content += bp.junc(c19_p1[0], 77.47)
    content += bp.gnd_sym(c19_p2[0], c19_p2[1])

    content += bp.wire(c19_p1[0], 77.47, c20_p1[0], 77.47)
    content += bp.junc(c20_p1[0], 77.47)
    content += bp.gnd_sym(c20_p2[0], c20_p2[1])

    # Connect to L2 Pin 1 and down to U4 Pin 9 (VIN at 95.25, 77.47)
    content += bp.wire(c20_p1[0], 77.47, 68.58, 77.47)
    content += bp.junc(68.58, 77.47)
    content += bp.wire(68.58, 77.47, u4_p9[0], u4_p9[1])
    
    # Tap to Inductor L2 Pin 1 (72.39, 82.55)
    content += bp.wire(68.58, 77.47, 68.58, 82.55)
    content += bp.wire(68.58, 82.55, l2_p1[0], l2_p1[1])

    # L2 Pin 2 (79.91, 82.55) connects straight to SW Pin 4 (95.25, 82.55)
    content += bp.wire(l2_p2[0], l2_p2[1], u4_p4[0], u4_p4[1])
    content += bp.wire(u4_p4[0], u4_p4[1], u4_p5[0], u4_p5[1])
    content += bp.wire(u4_p5[0], u4_p5[1], u4_p6[0], u4_p6[1])
    content += bp.wire(u4_p6[0], u4_p6[1], u4_p7[0], u4_p7[1])
    content += bp.junc(u4_p4[0], u4_p4[1])
    content += bp.junc(u4_p5[0], u4_p5[1])
    content += bp.junc(u4_p6[0], u4_p6[1])
    content += bp.junc(u4_p7[0], u4_p7[1])

    # Connect SW node to C23 pin 2 (BOOT capacitor at 83.82, 92.71)
    content += bp.wire(u4_p7[0], u4_p7[1], 87.63, u4_p7[1])
    content += bp.wire(87.63, u4_p7[1], 87.63, 92.71)
    content += bp.wire(87.63, 92.71, c23_p2[0], c23_p2[1])

    # BOOT pin 8 (95.25, 95.25) to C23 pin 1 (76.20, 92.71)
    content += bp.wire(u4_p8[0], u4_p8[1], 76.20, u4_p8[1])
    content += bp.wire(76.20, u4_p8[1], c23_p1[0], c23_p1[1])

    # EN (Pin 2 at 95.25, 97.79) pull up to VIN (68.58, 77.47)
    content += bp.wire(u4_p2[0], u4_p2[1], 64.77, u4_p2[1])
    content += bp.wire(64.77, u4_p2[1], 64.77, 77.47)
    content += bp.wire(64.77, 77.47, 68.58, 77.47)

    # VCC (Pin 1 at 95.25, 100.33) to C21
    content += bp.wire(u4_p1[0], u4_p1[1], c21_p2[0], u4_p1[1])
    content += bp.gnd_sym(c21_p1[0], c21_p1[1])

    # MODE (Pin 13 at 95.25, 102.87) to R19
    content += bp.wire(u4_p13[0], u4_p13[1], r19_p2[0], u4_p13[1])
    content += bp.gnd_sym(r19_p1[0], r19_p1[1])

    # FSW (Pin 3 at 95.25, 105.41) to R20
    content += bp.wire(u4_p3[0], u4_p3[1], r20_p2[0], u4_p3[1])
    content += bp.gnd_sym(r20_p1[0], r20_p1[1])

    # SS (Pin 10 at 95.25, 107.95) to C22
    content += bp.wire(u4_p10[0], u4_p10[1], c22_p2[0], u4_p10[1])
    content += bp.gnd_sym(c22_p1[0], c22_p1[1])

    # ILIM (Pin 19 at 95.25, 110.49) to R21
    content += bp.wire(u4_p19[0], u4_p19[1], r21_p2[0], u4_p19[1])
    content += bp.gnd_sym(r21_p1[0], r21_p1[1])

    # PGND (Pin 20 at 95.25, 113.03) to GND
    content += bp.wire(u4_p20[0], u4_p20[1], 83.82, u4_p20[1])
    content += bp.gnd_sym(83.82, u4_p20[1])

    # -------------------------------------------------------------------------
    # RIGHT SIDE: VOUT, FB, COMP, NC, EP/GND
    # -------------------------------------------------------------------------
    # Pins 14, 15, 16 tie together at X = 125.73
    content += bp.wire(u4_p14[0], u4_p14[1], u4_p15[0], u4_p15[1])
    content += bp.wire(u4_p15[0], u4_p15[1], u4_p16[0], u4_p16[1])
    content += bp.junc(u4_p14[0], u4_p14[1])
    content += bp.junc(u4_p15[0], u4_p15[1])

    # Main 5V_SYS Rail runs from (125.73, 77.47) right across to X = 185.42
    content += bp.wire(u4_p14[0], 77.47, c24_p1[0], 77.47)
    content += bp.junc(c24_p1[0], 77.47)
    content += bp.gnd_sym(c24_p2[0], c24_p2[1])

    content += bp.wire(c24_p1[0], 77.47, c25_p1[0], 77.47)
    content += bp.junc(c25_p1[0], 77.47)
    content += bp.gnd_sym(c25_p2[0], c25_p2[1])

    content += bp.wire(c25_p1[0], 77.47, c26_p1[0], 77.47)
    content += bp.junc(c26_p1[0], 77.47)
    content += bp.gnd_sym(c26_p2[0], c26_p2[1])

    content += bp.wire(c26_p1[0], 77.47, c27_p1[0], 77.47)
    content += bp.junc(c27_p1[0], 77.47)
    content += bp.gnd_sym(c27_p2[0], c27_p2[1])

    # Connect to TP6 (Test Point 5V_SYS at 175.26, 77.47)
    content += bp.wire(c27_p1[0], 77.47, tp6_p1[0], 77.47)
    content += bp.junc(tp6_p1[0], 77.47)

    # Global and Hierarchical labels for 5V_SYS at (175.26, 69.85)
    content += bp.global_lbl("5V_SYS", 175.26, 69.85, 90, "bidirectional")
    content += bp.hier_lbl("5V_SYS", 175.26, 69.85, 90, "output")
    content += bp.wire(175.26, 77.47, 175.26, 69.85)

    # Feedback Network: R22 || C28 from 5V_SYS rail down to FB pin 17 (125.73, 92.71)
    content += bp.wire(125.73, 77.47, r22_p1[0], 77.47)
    content += bp.junc(r22_p1[0], 77.47)
    content += bp.wire(r22_p1[0], 77.47, r22_p1[0], r22_p1[1])
    
    # C28 tapped in parallel
    content += bp.wire(r22_p1[0], 77.47, c28_p1[0], 77.47)
    content += bp.junc(c28_p1[0], 77.47)
    content += bp.wire(c28_p1[0], 77.47, c28_p1[0], c28_p1[1])

    # Bottom of R22 and C28 tie together at Y = 92.71 (FB pin level)
    content += bp.wire(c28_p2[0], c28_p2[1], c28_p2[0], 92.71)
    content += bp.wire(r22_p2[0], r22_p2[1], r22_p2[0], 92.71)
    content += bp.wire(c28_p2[0], 92.71, r22_p2[0], 92.71)
    content += bp.junc(r22_p2[0], 92.71)
    
    # Wire straight to FB pin 17 (125.73, 92.71)
    content += bp.wire(u4_p17[0], u4_p17[1], r22_p2[0], 92.71)
    
    # Continue down into R23 (137.16, 96.52)
    content += bp.wire(r22_p2[0], 92.71, r23_p1[0], r23_p1[1])
    content += bp.gnd_sym(r23_p2[0], r23_p2[1])

    # COMP pin 18 (125.73, 95.25) to R24 -> C29 || C30 -> GND
    content += bp.wire(u4_p18[0], u4_p18[1], r24_p1[0], u4_p18[1])
    
    content += bp.wire(r24_p2[0], r24_p2[1], c29_p1[0], r24_p2[1])
    content += bp.junc(c29_p1[0], r24_p2[1])
    content += bp.gnd_sym(c29_p2[0], c29_p2[1])

    content += bp.wire(c29_p1[0], r24_p2[1], c30_p1[0], r24_p2[1])
    content += bp.gnd_sym(c30_p2[0], c30_p2[1])

    # NC pins (11, 12)
    content += bp.no_conn(u4_p11[0], u4_p11[1])
    content += bp.no_conn(u4_p12[0], u4_p12[1])

    # EP/GND (Pin 21 at 125.73, 113.03) to GND
    content += bp.wire(u4_p21[0], u4_p21[1], 134.62, u4_p21[1])
    content += bp.gnd_sym(134.62, u4_p21[1])

    # -------------------------------------------------------------------------
    # WIRING - SECTION 2: TPS62162 BUCK CONVERTER (5V_SYS -> 3V3_SYS)
    # -------------------------------------------------------------------------
    # 5V_SYS continues right from (175.26, 77.47) to (185.42, 77.47), then drops to (185.42, 87.63)
    content += bp.wire(175.26, 77.47, 185.42, 77.47)
    content += bp.wire(185.42, 77.47, 185.42, 87.63)
    
    # Input Caps C32 (100nF) and C31 (10uF) tapped at Y = 87.63
    content += bp.junc(185.42, 87.63)
    content += bp.gnd_sym(c32_p2[0], c32_p2[1])

    content += bp.wire(185.42, 87.63, c31_p1[0], 87.63)
    content += bp.junc(c31_p1[0], 87.63)
    content += bp.gnd_sym(c31_p2[0], c31_p2[1])

    # Continue into U5 VIN (pin 2 at 203.20, 87.63) and EN pullup R25
    content += bp.wire(c31_p1[0], 87.63, r25_p1[0], 87.63)
    content += bp.junc(r25_p1[0], 87.63)
    content += bp.wire(r25_p1[0], 87.63, u5_p2[0], u5_p2[1])
    
    # EN pullup R25 from 5V_SYS (Y = 87.63) to EN (Y = 92.71)
    content += bp.wire(r25_p2[0], r25_p2[1], r25_p2[0], u5_p3[1])
    content += bp.wire(r25_p2[0], u5_p3[1], u5_p3[0], u5_p3[1])

    # U5 Grounds: PGND (pin 1 at 203.20, 102.87), AGND (pin 4 at 203.20, 105.41), EP/GND (pin 9 at 228.60, 105.41)
    content += bp.wire(u5_p1[0], u5_p1[1], 195.58, u5_p1[1])
    content += bp.gnd_sym(195.58, u5_p1[1])
    content += bp.wire(u5_p4[0], u5_p4[1], 195.58, u5_p4[1])
    content += bp.gnd_sym(195.58, u5_p4[1])
    content += bp.wire(u5_p9[0], u5_p9[1], 233.68, u5_p9[1])
    content += bp.gnd_sym(233.68, u5_p9[1])

    # U5 FB (pin 5 at 228.60, 97.79) tied to AGND for fixed 3.3V version
    content += bp.wire(u5_p5[0], u5_p5[1], 233.68, u5_p5[1])
    content += bp.gnd_sym(233.68, u5_p5[1])

    # U5 PG (pin 8) - Power Good, uncommitted / NC
    content += bp.no_conn(u5_p8[0], u5_p8[1])

    # SW (pin 7 at 228.60, 92.71) straight to Inductor L3 pin 1 (234.95, 92.71)
    content += bp.wire(u5_p7[0], u5_p7[1], l3_p1[0], l3_p1[1])

    # L3 pin 2 (242.57, 92.71) connects to 3V3_SYS output rail along Y = 92.71
    # VOS sense (pin 6 at 228.60, 87.63) connects directly to output rail at Y = 92.71
    content += bp.wire(u5_p6[0], u5_p6[1], 246.38, u5_p6[1])
    content += bp.wire(246.38, u5_p6[1], 246.38, 92.71)
    content += bp.wire(l3_p2[0], 92.71, 246.38, 92.71)
    content += bp.junc(246.38, 92.71)

    # Output Capacitors C33 (22uF) and C34 (100nF)
    content += bp.wire(246.38, 92.71, c33_p1[0], 92.71)
    content += bp.junc(c33_p1[0], 92.71)
    content += bp.gnd_sym(c33_p2[0], c33_p2[1])

    content += bp.wire(c33_p1[0], 92.71, c34_p1[0], 92.71)
    content += bp.junc(c34_p1[0], 92.71)
    content += bp.gnd_sym(c34_p2[0], c34_p2[1])

    # Connect to TP7 (Test Point 3V3_SYS at 269.24, 92.71)
    content += bp.wire(c34_p1[0], 92.71, tp7_p1[0], 92.71)
    content += bp.junc(tp7_p1[0], 92.71)

    # Output Labels for 3V3_SYS
    content += bp.wire(tp7_p1[0], 92.71, 276.86, 92.71)
    content += bp.global_lbl("3V3_SYS", 276.86, 92.71, 0, "bidirectional")
    content += bp.hier_lbl("3V3_SYS", 276.86, 92.71, 0, "output")

    # Sheet ending
    content += ")\n"
    
    with open("03_BOOST_BUCK_RAILS.kicad_sch", "w", encoding="utf-8") as f:
        f.write(content)
    print("Sheet 3 successfully generated: 03_BOOST_BUCK_RAILS.kicad_sch")

if __name__ == "__main__":
    build_sheet3()
