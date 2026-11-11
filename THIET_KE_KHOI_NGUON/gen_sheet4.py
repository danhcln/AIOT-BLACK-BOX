# -*- coding: utf-8 -*-
"""
Generator for Sheet 4: 04_SIM_POWER_OUTPUTS.kicad_sch
Implements:
1. Dedicated Cellular Supply Stage for A7682S:
   - Option A: 5V Pass-through with P-MOSFET Switch (AO3401A)
   - Option B: TPS62130RGTR 3.8V/3A Synchronous Buck Converter
   - JP1 Hardware Selection Jumper (5V vs 3.8V) with mandatory warning note
   - 1000uF Polymer + 100uF Ceramic + 100nF Decoupling + SMAJ5.0A TVS Protection
2. System Power Distribution Headers:
   - J4: 10-pin Power Distribution Header (5V_SYS, 3V3_SYS, VBAT, GND)
   - J5: 5-pin Cellular Module Interface Header (SIM_PWR, PWRKEY, GND)

Strict 1.27mm Grid - 100% Planar - Full compliance with SCHEMATIC_DRAWING_RULES.md.
"""

import sys
import os

sys.path.append(r"D:\ĐỒ ÁN 2\THIET_KE_KHOI_NGUON")
import build_complete_power_project as bp
import custom_symbols_def as cust_syms
import generate_symbols as base_syms

def build_sheet4():
    content = bp.make_header("KHỐI NGUỒN CELLULAR VÀ ĐẦU NỐI PHÂN PHỐI (A7682S + HEADERS)", 5, 5)

    # -------------------------------------------------------------------------
    # PROMINENT HARDWARE VERIFICATION WARNING TEXT
    # -------------------------------------------------------------------------
    content += f"""\t(text "HARDWARE VERIFICATION REQUIRED:\\nDO NOT POPULATE JP1 UNTIL A7682S BREAKOUT INPUT VOLTAGE IS PHYSICALLY VERIFIED.\\nOPTION A: PIN 1-2 (5V PASS-THROUGH)\\nOPTION B: PIN 2-3 (TPS62130 3.8V/3A BUCK)"
\t\t(at 160.02 43.18 0)
\t\t(effects (font (size 1.5 1.5) (bold yes)) (justify left))
\t\t(uuid "{bp.uid()}")
\t)\n"""

    # -------------------------------------------------------------------------
    # 1. OPTION A: 5V PASS-THROUGH VIA P-MOSFET SWITCH (AO3401A)
    # Center Q3 at (76.20, 50.80)
    # -------------------------------------------------------------------------
    q3_x, q3_y = 76.20, 50.80
    content += bp.sym_inst("Transistor_FET:AO3401A", "Q3", "AO3401A (-30V/-4A)", q3_x, q3_y, 0,
                           "Package_TO_SOT_SMD:SOT-23",
                           "http://www.aosmd.com/pdfs/datasheet/AO3401A.pdf",
                           "P-Channel 30V 4.2A Power MOSFET Switch, SOT-23",
                           pins=["1", "2", "3"])

    # Gate Pullup R26 (100k) to 5V_SYS and Pulldown R27 (10k) to GND
    r26_x, r26_y = 66.04, 57.15
    content += bp.sym_inst("Device:R", "R26", "100k (1%)", r26_x, r26_y, 0,
                           "Resistor_SMD:R_0603_1608Metric",
                           "~", "Gate Pullup Resistor, 100k, 1%, 0603",
                           pins=["1", "2"])

    r27_x, r27_y = 76.20, 64.77
    content += bp.sym_inst("Device:R", "R27", "10k (1%)", r27_x, r27_y, 0,
                           "Resistor_SMD:R_0603_1608Metric",
                           "~", "Gate Pulldown Resistor (Default ON), 10k, 1%, 0603",
                           pins=["1", "2"])

    # -------------------------------------------------------------------------
    # 2. OPTION B: TPS62130RGTR 3.8V / 3A SYNCHRONOUS BUCK CONVERTER
    # Center U6 at (88.90, 114.30)
    # -------------------------------------------------------------------------
    u6_x, u6_y = 88.90, 114.30
    content += bp.sym_inst("Power_Management:TPS62130RGTR", "U6", "TPS62130RGTR", u6_x, u6_y, 0,
                           "Package_DFN_QFN:Texas_RGT0016A",
                           "https://www.ti.com/lit/ds/symlink/tps62130.pdf",
                           "3V-17V, 3A Synchronous Step-Down Converter with DCS-Control, VQFN-16",
                           pins=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                                 "11", "12", "13", "14", "15", "16", "17"])

    # Input Capacitors for TPS62130: C38 (10uF), C39 (100nF)
    c38_x, c38_y = 66.04, 102.87
    content += bp.sym_inst("Device:C", "C38", "10uF/10V (X5R)", c38_x, c38_y, 0,
                           "Capacitor_SMD:C_0805_2012Metric",
                           "~", "Buck Input Low-ESR Ceramic Capacitor, 10uF, 10V, X5R, 0805",
                           pins=["1", "2"])

    c39_x, c39_y = 58.42, 102.87
    content += bp.sym_inst("Device:C", "C39", "100nF/16V (X7R)", c39_x, c39_y, 0,
                           "Capacitor_SMD:C_0603_1608Metric",
                           "~", "Buck Input High-Frequency Decoupling, 100nF, 16V, 0603",
                           pins=["1", "2"])

    # EN Pullup Resistor R28 (100k) to 5V_SYS
    r28_x, r28_y = 66.04, 114.30
    content += bp.sym_inst("Device:R", "R28", "100k (1%)", r28_x, r28_y, 0,
                           "Resistor_SMD:R_0603_1608Metric",
                           "~", "Buck Enable Pullup Resistor, 100k, 1%, 0603",
                           pins=["1", "2"])

    # SS Soft-Start Capacitor C40 (3.3nF)
    c40_x, c40_y = 66.04, 123.19
    content += bp.sym_inst("Device:C", "C40", "3.3nF/25V (X7R)", c40_x, c40_y, 90,
                           "Capacitor_SMD:C_0603_1608Metric",
                           "~", "Soft-Start Timing Capacitor, 3.3nF, 25V, X7R, 0603",
                           pins=["1", "2"])

    # Buck Inductor L4 (1.0uH / 4A)
    l4_x, l4_y = 119.38, 104.14
    content += bp.sym_inst("Device:L", "L4", "1.0uH (4A Sat)", l4_x, l4_y, 90,
                           "Inductor_SMD:L_Bourns_SRP6540",
                           "https://www.bourns.com/docs/product-datasheets/srp6540.pdf",
                           "Shielded Power Inductor, 1.0uH, 4A Isat, Low DCR SMD",
                           pins=["1", "2"])

    # Output Capacitors for TPS62130: C41 (22uF), C42 (22uF) along 3.8V rail
    c41_x, c41_y = 134.62, 107.95
    content += bp.sym_inst("Device:C", "C41", "22uF/10V (X5R)", c41_x, c41_y, 0,
                           "Capacitor_SMD:C_0805_2012Metric",
                           "~", "Buck Output Low-ESR Ceramic Capacitor, 22uF, 10V, X5R, 0805",
                           pins=["1", "2"])

    c42_x, c42_y = 142.24, 107.95
    content += bp.sym_inst("Device:C", "C42", "22uF/10V (X5R)", c42_x, c42_y, 0,
                           "Capacitor_SMD:C_0805_2012Metric",
                           "~", "Buck Output Low-ESR Ceramic Capacitor, 22uF, 10V, X5R, 0805",
                           pins=["1", "2"])

    # Feedback divider for 3.8V: R29 (374k 1%), R30 (100k 1%), C43 (22pF)
    r29_x, r29_y = 127.00, 114.30
    content += bp.sym_inst("Device:R", "R29", "374k (1%)", r29_x, r29_y, 0,
                           "Resistor_SMD:R_0603_1608Metric",
                           "~", "Feedback Top Resistor (for 3.8V output), 374k, 1%, 0603",
                           pins=["1", "2"])

    c43_x, c43_y = 121.92, 114.30
    content += bp.sym_inst("Device:C", "C43", "22pF/50V (C0G)", c43_x, c43_y, 0,
                           "Capacitor_SMD:C_0603_1608Metric",
                           "~", "Feedback Feedforward Capacitor, 22pF, 50V, C0G, 0603",
                           pins=["1", "2"])

    r30_x, r30_y = 127.00, 125.73
    content += bp.sym_inst("Device:R", "R30", "100k (1%)", r30_x, r30_y, 0,
                           "Resistor_SMD:R_0603_1608Metric",
                           "~", "Feedback Bottom Resistor, 100k, 1%, 0603",
                           pins=["1", "2"])

    # -------------------------------------------------------------------------
    # 3. HARDWARE SELECTION JUMPER JP1 (3-Pin Header)
    # Center JP1 at (154.94, 73.66)
    # -------------------------------------------------------------------------
    jp1_x, jp1_y = 154.94, 73.66
    content += bp.sym_inst("Connector:Conn_01x03_Pin", "JP1", "SIM_PWR_SEL", jp1_x, jp1_y, 0,
                           "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical",
                           "~", "Cellular Supply Voltage Selection Jumper (1-2: 5V, 2-3: 3.8V)",
                           pins=["1", "2", "3"])

    # -------------------------------------------------------------------------
    # 4. CELLULAR POWER RAIL FILTERING & TRANSIENT STORAGE (SIM_PWR)
    # -------------------------------------------------------------------------
    # C35: 1000uF Polymer Aluminum Capacitor (Low-ESR < 15mOhm for 2A bursts)
    c35_x, c35_y = 177.80, 77.47
    content += bp.sym_inst("Device:C_Polarized", "C35", "1000uF/6.3V (Polymer)", c35_x, c35_y, 0,
                           "Capacitor_SMD:CP_Elec_8x10",
                           "https://industrial.panasonic.com/cdvis/browse/do/product/EEF-HX/EEFHX0J102R",
                           "High-Transient Low-ESR Polymer Aluminum Capacitor, 1000uF, 6.3V, ESR<15mOhm",
                           pins=["1", "2"])

    # C36: 100uF Ceramic Capacitor
    c36_x, c36_y = 185.42, 77.47
    content += bp.sym_inst("Device:C", "C36", "100uF/6.3V (X5R)", c36_x, c36_y, 0,
                           "Capacitor_SMD:C_1206_3216Metric",
                           "~", "High-Density Storage Ceramic Capacitor, 100uF, 6.3V, X5R, 1206",
                           pins=["1", "2"])

    # C37: 100nF High-Frequency Decoupling
    c37_x, c37_y = 193.04, 77.47
    content += bp.sym_inst("Device:C", "C37", "100nF/16V (X7R)", c37_x, c37_y, 0,
                           "Capacitor_SMD:C_0603_1608Metric",
                           "~", "RF Decoupling Ceramic Capacitor, 100nF, 16V, X7R, 0603",
                           pins=["1", "2"])

    # D3: SMAJ5.0A TVS Protection Diode
    d3_x, d3_y = 200.66, 77.47
    content += bp.sym_inst("Device:D_TVS", "D3", "SMAJ5.0A (TVS)", d3_x, d3_y, 0,
                           "Diode_SMD:D_SMA",
                           "https://www.littelfuse.com/media?resourcetype=datasheets&itemid=23340578-8314-4148-8df0-7d3d2dcfe3e2&filename=littelfuse-tvs-diode-smaj-datasheet.pdf",
                           "Unidirectional TVS Diode, 5.0V Standoff, 400W Peak Pulse Power, SMA",
                           pins=["1", "2"])

    # Test Point TP8 for SIM_PWR
    tp8_x, tp8_y = 208.28, 73.66
    content += bp.sym_inst("Connector:TestPoint", "TP8", "TP_SIM_PWR", tp8_x, tp8_y, 0,
                           "TestPoint:TestPoint_Pad_D1.5mm",
                           "~", "Test Point for Dedicated Cellular Power Rail (SIM_PWR)",
                           pins=["1"])

    # -------------------------------------------------------------------------
    # 5. OUTPUT HEADERS: J5 (Cellular Interface) & J4 (System Power Distribution)
    # -------------------------------------------------------------------------
    # J5: 5-pin Cellular Header at (226.06, 76.20)
    j5_x, j5_y = 226.06, 76.20
    content += bp.sym_inst("Connector:Conn_01x05_Pin", "J5", "A7682S_BREAKOUT_PWR", j5_x, j5_y, 0,
                           "Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Vertical",
                           "~", "Cellular Module Power and Control Interface Header (SIM_PWR, PWRKEY, GND)",
                           pins=["1", "2", "3", "4", "5"])

    # Test Point TP9 for PWRKEY
    tp9_x, tp9_y = 218.44, 76.20
    content += bp.sym_inst("Connector:TestPoint", "TP9", "TP_PWRKEY", tp9_x, tp9_y, 0,
                           "TestPoint:TestPoint_Pad_D1.5mm",
                           "~", "Test Point for Cellular Power Key Line (PWRKEY)",
                           pins=["1"])

    # J4: 10-pin System Power Distribution Header at (241.30, 137.16)
    j4_x, j4_y = 241.30, 137.16
    content += bp.sym_inst("Connector:Conn_01x10_Pin", "J4", "SYSTEM_POWER_BUS", j4_x, j4_y, 0,
                           "Connector_PinHeader_2.54mm:PinHeader_1x10_P2.54mm_Vertical",
                           "~", "System Main Power Distribution Header (5V_SYS, 3V3_SYS, VBAT, GND)",
                           pins=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])

    # -------------------------------------------------------------------------
    # PIN COORDINATE EXTRACTION
    # -------------------------------------------------------------------------
    q3_p1 = bp.pin_pos(cust_syms.SYM_AO3401A, q3_x, q3_y, "1", 0) # Gate
    q3_p2 = bp.pin_pos(cust_syms.SYM_AO3401A, q3_x, q3_y, "2", 0) # Source
    q3_p3 = bp.pin_pos(cust_syms.SYM_AO3401A, q3_x, q3_y, "3", 0) # Drain

    r26_p1 = bp.pin_pos(base_syms.SYM_R, r26_x, r26_y, "1", 0)
    r26_p2 = bp.pin_pos(base_syms.SYM_R, r26_x, r26_y, "2", 0)
    r27_p1 = bp.pin_pos(base_syms.SYM_R, r27_x, r27_y, "1", 0)
    r27_p2 = bp.pin_pos(base_syms.SYM_R, r27_x, r27_y, "2", 0)

    u6_p11 = bp.pin_pos(cust_syms.SYM_TPS62130, u6_x, u6_y, "11", 0) # PVIN
    u6_p12 = bp.pin_pos(cust_syms.SYM_TPS62130, u6_x, u6_y, "12", 0) # PVIN
    u6_p10 = bp.pin_pos(cust_syms.SYM_TPS62130, u6_x, u6_y, "10", 0) # AVIN
    u6_p13 = bp.pin_pos(cust_syms.SYM_TPS62130, u6_x, u6_y, "13", 0) # EN
    u6_p7 = bp.pin_pos(cust_syms.SYM_TPS62130, u6_x, u6_y, "7", 0)   # FSW
    u6_p8 = bp.pin_pos(cust_syms.SYM_TPS62130, u6_x, u6_y, "8", 0)   # DEF
    u6_p9 = bp.pin_pos(cust_syms.SYM_TPS62130, u6_x, u6_y, "9", 0)   # SS/TR
    u6_p15 = bp.pin_pos(cust_syms.SYM_TPS62130, u6_x, u6_y, "15", 0) # PGND
    u6_p16 = bp.pin_pos(cust_syms.SYM_TPS62130, u6_x, u6_y, "16", 0) # PGND
    u6_p6 = bp.pin_pos(cust_syms.SYM_TPS62130, u6_x, u6_y, "6", 0)   # AGND

    u6_p14 = bp.pin_pos(cust_syms.SYM_TPS62130, u6_x, u6_y, "14", 0) # VOS
    u6_p1 = bp.pin_pos(cust_syms.SYM_TPS62130, u6_x, u6_y, "1", 0)   # SW
    u6_p2 = bp.pin_pos(cust_syms.SYM_TPS62130, u6_x, u6_y, "2", 0)   # SW
    u6_p3 = bp.pin_pos(cust_syms.SYM_TPS62130, u6_x, u6_y, "3", 0)   # SW
    u6_p5 = bp.pin_pos(cust_syms.SYM_TPS62130, u6_x, u6_y, "5", 0)   # FB
    u6_p4 = bp.pin_pos(cust_syms.SYM_TPS62130, u6_x, u6_y, "4", 0)   # PG
    u6_p17 = bp.pin_pos(cust_syms.SYM_TPS62130, u6_x, u6_y, "17", 0) # EP/GND

    c38_p1 = bp.pin_pos(base_syms.SYM_C, c38_x, c38_y, "1", 0)
    c38_p2 = bp.pin_pos(base_syms.SYM_C, c38_x, c38_y, "2", 0)
    c39_p1 = bp.pin_pos(base_syms.SYM_C, c39_x, c39_y, "1", 0)
    c39_p2 = bp.pin_pos(base_syms.SYM_C, c39_x, c39_y, "2", 0)
    r28_p1 = bp.pin_pos(base_syms.SYM_R, r28_x, r28_y, "1", 0)
    r28_p2 = bp.pin_pos(base_syms.SYM_R, r28_x, r28_y, "2", 0)
    c40_p1 = bp.pin_pos(base_syms.SYM_C, c40_x, c40_y, "1", 90)
    c40_p2 = bp.pin_pos(base_syms.SYM_C, c40_x, c40_y, "2", 90)

    l4_p1 = bp.pin_pos(base_syms.SYM_L, l4_x, l4_y, "1", 90)
    l4_p2 = bp.pin_pos(base_syms.SYM_L, l4_x, l4_y, "2", 90)
    c41_p1 = bp.pin_pos(base_syms.SYM_C, c41_x, c41_y, "1", 0)
    c41_p2 = bp.pin_pos(base_syms.SYM_C, c41_x, c41_y, "2", 0)
    c42_p1 = bp.pin_pos(base_syms.SYM_C, c42_x, c42_y, "1", 0)
    c42_p2 = bp.pin_pos(base_syms.SYM_C, c42_x, c42_y, "2", 0)

    r29_p1 = bp.pin_pos(base_syms.SYM_R, r29_x, r29_y, "1", 0)
    r29_p2 = bp.pin_pos(base_syms.SYM_R, r29_x, r29_y, "2", 0)
    c43_p1 = bp.pin_pos(base_syms.SYM_C, c43_x, c43_y, "1", 0)
    c43_p2 = bp.pin_pos(base_syms.SYM_C, c43_x, c43_y, "2", 0)
    r30_p1 = bp.pin_pos(base_syms.SYM_R, r30_x, r30_y, "1", 0)
    r30_p2 = bp.pin_pos(base_syms.SYM_R, r30_x, r30_y, "2", 0)

    jp1_p1 = bp.pin_pos(base_syms.SYM_CONN_03, jp1_x, jp1_y, "1", 0)
    jp1_p2 = bp.pin_pos(base_syms.SYM_CONN_03, jp1_x, jp1_y, "2", 0)
    jp1_p3 = bp.pin_pos(base_syms.SYM_CONN_03, jp1_x, jp1_y, "3", 0)

    c35_p1 = bp.pin_pos(base_syms.SYM_CP, c35_x, c35_y, "1", 0)
    c35_p2 = bp.pin_pos(base_syms.SYM_CP, c35_x, c35_y, "2", 0)
    c36_p1 = bp.pin_pos(base_syms.SYM_C, c36_x, c36_y, "1", 0)
    c36_p2 = bp.pin_pos(base_syms.SYM_C, c36_x, c36_y, "2", 0)
    c37_p1 = bp.pin_pos(base_syms.SYM_C, c37_x, c37_y, "1", 0)
    c37_p2 = bp.pin_pos(base_syms.SYM_C, c37_x, c37_y, "2", 0)
    d3_p1 = bp.pin_pos(base_syms.SYM_D_TVS, d3_x, d3_y, "1", 0)
    d3_p2 = bp.pin_pos(base_syms.SYM_D_TVS, d3_x, d3_y, "2", 0)
    tp8_p1 = bp.pin_pos(base_syms.SYM_TESTPOINT, tp8_x, tp8_y, "1", 0)

    j5_p1 = bp.pin_pos(base_syms.SYM_CONN_05, j5_x, j5_y, "1", 0)
    j5_p2 = bp.pin_pos(base_syms.SYM_CONN_05, j5_x, j5_y, "2", 0)
    j5_p3 = bp.pin_pos(base_syms.SYM_CONN_05, j5_x, j5_y, "3", 0)
    j5_p4 = bp.pin_pos(base_syms.SYM_CONN_05, j5_x, j5_y, "4", 0)
    j5_p5 = bp.pin_pos(base_syms.SYM_CONN_05, j5_x, j5_y, "5", 0)
    tp9_p1 = bp.pin_pos(base_syms.SYM_TESTPOINT, tp9_x, tp9_y, "1", 0)

    # -------------------------------------------------------------------------
    # WIRING - SECTION 1: 5V_SYS INPUT RAIL & OPTION A (P-MOSFET Q3)
    # -------------------------------------------------------------------------
    # 5V_SYS comes in at (25.40, 50.80)
    content += bp.global_lbl("5V_SYS", 25.40, 50.80, 180, "input")
    content += bp.hier_lbl("5V_SYS", 25.40, 50.80, 180, "input")
    
    # 5V_SYS runs right to Q3 Pin 2 (Source at 68.58, 50.80)
    content += bp.wire(25.40, 50.80, 48.26, 50.80)
    content += bp.junc(48.26, 50.80)
    content += bp.wire(48.26, 50.80, q3_p2[0], q3_p2[1])
    
    # Tap 5V_SYS to R26 (Gate pullup) at (66.04, 50.80)
    content += bp.wire(48.26, 50.80, r26_p1[0], 50.80)
    content += bp.junc(r26_p1[0], 50.80)
    content += bp.wire(r26_p1[0], 50.80, r26_p1[0], r26_p1[1])

    # Q3 Gate (pin 1 at 76.20, 58.42): connects to R26 bottom and R27 top
    content += bp.wire(r26_p2[0], r26_p2[1], q3_p1[0], r26_p2[1])
    content += bp.wire(q3_p1[0], r26_p2[1], q3_p1[0], q3_p1[1])
    content += bp.junc(q3_p1[0], r26_p2[1])
    
    content += bp.wire(q3_p1[0], r26_p2[1], r27_p1[0], r27_p1[1])
    content += bp.gnd_sym(r27_p2[0], r27_p2[1])

    # Q3 Drain (pin 3 at 83.82, 50.80) outputs SIM_PWR_A
    # Runs right along Y = 50.80 to X = 154.94, then drops to JP1 Pin 1 (160.02, 71.12)
    content += bp.wire(q3_p3[0], q3_p3[1], 154.94, q3_p3[1])
    content += bp.wire(154.94, q3_p3[1], 154.94, jp1_p1[1])
    content += bp.wire(154.94, jp1_p1[1], jp1_p1[0], jp1_p1[1])

    # -------------------------------------------------------------------------
    # WIRING - SECTION 2: OPTION B (TPS62130 3.8V BUCK CONVERTER)
    # -------------------------------------------------------------------------
    # 5V_SYS drops down from (48.26, 50.80) to Y = 99.06 to feed TPS62130
    content += bp.wire(48.26, 50.80, 48.26, 99.06)
    content += bp.wire(48.26, 99.06, c39_p1[0], 99.06)
    
    # Input Caps C39 (100nF) and C38 (10uF) tapped at Y = 99.06
    content += bp.junc(c39_p1[0], 99.06)
    content += bp.gnd_sym(c39_p2[0], c39_p2[1])

    content += bp.wire(c39_p1[0], 99.06, c38_p1[0], 99.06)
    content += bp.junc(c38_p1[0], 99.06)
    content += bp.gnd_sym(c38_p2[0], c38_p2[1])

    # Connect to U6 PVIN (pins 11, 12 at 73.66, 99.06 and 101.60) & AVIN (pin 10 at 73.66, 104.14)
    content += bp.wire(c38_p1[0], 99.06, u6_p11[0], 99.06)
    content += bp.wire(u6_p11[0], 99.06, u6_p11[0], u6_p11[1])
    content += bp.wire(u6_p11[0], u6_p11[1], u6_p12[0], u6_p12[1])
    content += bp.wire(u6_p12[0], u6_p12[1], u6_p10[0], u6_p10[1])
    content += bp.junc(u6_p11[0], u6_p11[1])
    content += bp.junc(u6_p12[0], u6_p12[1])

    # EN Pullup R28 from 5V_SYS (Y = 99.06) to EN pin 13 (Y = 109.22)
    content += bp.wire(c38_p1[0], 99.06, r28_p1[0], 99.06)
    content += bp.junc(r28_p1[0], 99.06)
    content += bp.wire(r28_p1[0], 99.06, r28_p1[0], r28_p1[1])
    content += bp.wire(r28_p2[0], r28_p2[1], r28_p2[0], u6_p13[1])
    content += bp.wire(r28_p2[0], u6_p13[1], u6_p13[0], u6_p13[1])

    # FSW (pin 7) & DEF (pin 8) tied to GND locally
    content += bp.wire(u6_p7[0], u6_p7[1], 71.12, u6_p7[1])
    content += bp.gnd_sym(71.12, u6_p7[1])
    content += bp.wire(u6_p8[0], u6_p8[1], 71.12, u6_p8[1])
    content += bp.gnd_sym(71.12, u6_p8[1])

    # SS/TR (pin 9 at 73.66, 119.38) to C40 -> GND
    content += bp.wire(u6_p9[0], u6_p9[1], c40_p2[0], u6_p9[1])
    content += bp.wire(c40_p2[0], u6_p9[1], c40_p2[0], c40_p2[1])
    content += bp.gnd_sym(c40_p1[0], c40_p1[1])

    # U6 Grounds: PGND (pins 15, 16) & AGND (pin 6)
    content += bp.wire(u6_p15[0], u6_p15[1], u6_p16[0], u6_p16[1])
    content += bp.wire(u6_p16[0], u6_p16[1], u6_p6[0], u6_p6[1])
    content += bp.wire(u6_p15[0], u6_p15[1], 71.12, u6_p15[1])
    content += bp.junc(u6_p15[0], u6_p15[1])
    content += bp.junc(u6_p16[0], u6_p16[1])
    content += bp.gnd_sym(71.12, u6_p15[1])

    # U6 EP/GND (pin 17) & PG (pin 4)
    content += bp.wire(u6_p17[0], u6_p17[1], 111.76, u6_p17[1])
    content += bp.gnd_sym(111.76, u6_p17[1])
    content += bp.no_conn(u6_p4[0], u6_p4[1])

    # SW (pins 1, 2, 3 at 104.14, 104.14 .. 109.22) tie together to L4 pin 1 (115.57, 104.14)
    content += bp.wire(u6_p1[0], u6_p1[1], u6_p2[0], u6_p2[1])
    content += bp.wire(u6_p2[0], u6_p2[1], u6_p3[0], u6_p3[1])
    content += bp.junc(u6_p1[0], u6_p1[1])
    content += bp.junc(u6_p2[0], u6_p2[1])
    content += bp.wire(u6_p1[0], u6_p1[1], l4_p1[0], l4_p1[1])

    # L4 pin 2 (123.19, 104.14) outputs SIM_PWR_B (3.8V rail)
    # Connects to VOS (pin 14 at 104.14, 99.06) via top trace
    content += bp.wire(l4_p2[0], 104.14, 127.00, 104.14)
    content += bp.junc(127.00, 104.14)
    content += bp.wire(127.00, 104.14, 127.00, 99.06)
    content += bp.wire(127.00, 99.06, u6_p14[0], u6_p14[1])

    # Output Capacitors C41 (22uF) & C42 (22uF) tapped at Y = 104.14
    content += bp.wire(127.00, 104.14, c41_p1[0], 104.14)
    content += bp.junc(c41_p1[0], 104.14)
    content += bp.gnd_sym(c41_p2[0], c41_p2[1])

    content += bp.wire(c41_p1[0], 104.14, c42_p1[0], 104.14)
    content += bp.junc(c42_p1[0], 104.14)
    content += bp.gnd_sym(c42_p2[0], c42_p2[1])

    # Feedback divider: R29 (374k) || C43 (22pF) from 3.8V rail down to FB pin 5 (104.14, 114.30)
    content += bp.wire(127.00, 104.14, r29_p1[0], 104.14)
    content += bp.wire(r29_p1[0], 104.14, r29_p1[0], r29_p1[1])
    
    # C43 in parallel
    content += bp.wire(r29_p1[0], 104.14, c43_p1[0], 104.14)
    content += bp.junc(c43_p1[0], 104.14)
    content += bp.wire(c43_p1[0], 104.14, c43_p1[0], c43_p1[1])

    # Bottom of R29 and C43 meet at Y = 120.65
    content += bp.wire(c43_p2[0], c43_p2[1], c43_p2[0], 120.65)
    content += bp.wire(r29_p2[0], r29_p2[1], r29_p2[0], 120.65)
    content += bp.wire(c43_p2[0], 120.65, r29_p2[0], 120.65)
    content += bp.junc(r29_p2[0], 120.65)

    # Wire to FB pin 5 (104.14, 114.30)
    content += bp.wire(r29_p2[0], 120.65, 114.30, 120.65)
    content += bp.wire(114.30, 120.65, 114.30, u6_p5[1])
    content += bp.wire(114.30, u6_p5[1], u6_p5[0], u6_p5[1])

    # Continue down into R30 (100k) to GND
    content += bp.wire(r29_p2[0], 120.65, r30_p1[0], r30_p1[1])
    content += bp.gnd_sym(r30_p2[0], r30_p2[1])

    # 3.8V rail continues right from C42 (142.24, 104.14) to JP1 Pin 3 (160.02, 76.20)
    content += bp.wire(c42_p1[0], 104.14, 149.86, 104.14)
    content += bp.wire(149.86, 104.14, 149.86, jp1_p3[1])
    content += bp.wire(149.86, jp1_p3[1], jp1_p3[0], jp1_p3[1])

    # -------------------------------------------------------------------------
    # WIRING - SECTION 3: JP1 OUTPUT & CELLULAR POWER BUS (SIM_PWR)
    # -------------------------------------------------------------------------
    # JP1 Pin 2 (160.02, 73.66) is the common SIM_PWR output!
    content += bp.wire(jp1_p2[0], jp1_p2[1], c35_p1[0], jp1_p2[1])
    
    # C35 (1000uF Polymer Aluminum Capacitor)
    content += bp.junc(c35_p1[0], 73.66)
    content += bp.wire(c35_p1[0], 73.66, c35_p1[0], c35_p1[1])
    content += bp.gnd_sym(c35_p2[0], c35_p2[1])

    # C36 (100uF Ceramic)
    content += bp.wire(c35_p1[0], 73.66, c36_p1[0], 73.66)
    content += bp.junc(c36_p1[0], 73.66)
    content += bp.wire(c36_p1[0], 73.66, c36_p1[0], c36_p1[1])
    content += bp.gnd_sym(c36_p2[0], c36_p2[1])

    # C37 (100nF Ceramic)
    content += bp.wire(c36_p1[0], 73.66, c37_p1[0], 73.66)
    content += bp.junc(c37_p1[0], 73.66)
    content += bp.wire(c37_p1[0], 73.66, c37_p1[0], c37_p1[1])
    content += bp.gnd_sym(c37_p2[0], c37_p2[1])

    # D3 (SMAJ5.0A TVS Diode - cathode pin 2 to SIM_PWR, anode pin 1 to GND)
    content += bp.wire(c37_p1[0], 73.66, d3_p2[0], 73.66)
    content += bp.junc(d3_p2[0], 73.66)
    content += bp.wire(d3_p2[0], 73.66, d3_p2[0], d3_p2[1])
    content += bp.gnd_sym(d3_p1[0], d3_p1[1])

    # Test Point TP8 for SIM_PWR
    content += bp.wire(d3_p2[0], 73.66, tp8_p1[0], 73.66)
    content += bp.junc(tp8_p1[0], 73.66)

    # Global and Hierarchical labels for SIM_PWR at (208.28, 64.77)
    content += bp.global_lbl("SIM_PWR", 208.28, 64.77, 90, "bidirectional")
    content += bp.hier_lbl("SIM_PWR", 208.28, 64.77, 90, "output")
    content += bp.wire(tp8_p1[0], 73.66, tp8_p1[0], 64.77)

    # Continue into J5 (Cellular Header Pins 1, 2)
    content += bp.wire(tp8_p1[0], 73.66, 220.98, 73.66)
    content += bp.junc(220.98, 73.66)
    content += bp.wire(220.98, 73.66, 220.98, j5_p1[1])
    content += bp.wire(220.98, j5_p1[1], j5_p1[0], j5_p1[1])
    content += bp.wire(220.98, 73.66, j5_p2[0], j5_p2[1])

    # J5 Pin 3: PWRKEY signal to TP9
    content += bp.wire(j5_p3[0], j5_p3[1], tp9_p1[0], tp9_p1[1])

    # J5 Pins 4, 5: Ground
    content += bp.wire(j5_p4[0], j5_p4[1], j5_p5[0], j5_p5[1])
    content += bp.wire(j5_p4[0], j5_p4[1], 236.22, j5_p4[1])
    content += bp.junc(j5_p4[0], j5_p4[1])
    content += bp.gnd_sym(236.22, j5_p4[1])

    # -------------------------------------------------------------------------
    # WIRING - SECTION 4: J4 SYSTEM POWER DISTRIBUTION HEADER
    # -------------------------------------------------------------------------
    # J4 Pins:
    # Pin 1, 2: 5V_SYS (Y = 127.00, 129.54)
    # Pin 3, 4: 3V3_SYS (Y = 132.08, 134.62)
    # Pin 5, 6: VBAT (Y = 137.16, 139.70)
    # Pin 7, 8, 9, 10: GND (Y = 142.24, 144.78, 147.32, 149.86)
    
    # 5V_SYS inputs to J4
    content += bp.global_lbl("5V_SYS", 231.14, 127.00, 180, "input")
    content += bp.wire(231.14, 127.00, 246.38, 127.00)
    content += bp.wire(246.38, 127.00, 246.38, 129.54)
    content += bp.junc(246.38, 127.00)

    # 3V3_SYS inputs to J4
    content += bp.global_lbl("3V3_SYS", 231.14, 132.08, 180, "input")
    content += bp.hier_lbl("3V3_SYS", 231.14, 132.08, 180, "input")
    content += bp.wire(231.14, 132.08, 246.38, 132.08)
    content += bp.wire(246.38, 132.08, 246.38, 134.62)
    content += bp.junc(246.38, 132.08)

    # VBAT inputs to J4
    content += bp.global_lbl("VBAT", 231.14, 137.16, 180, "input")
    content += bp.hier_lbl("VBAT", 231.14, 137.16, 180, "input")
    content += bp.wire(231.14, 137.16, 246.38, 137.16)
    content += bp.wire(246.38, 137.16, 246.38, 139.70)
    content += bp.junc(246.38, 137.16)

    # Grounds for J4 (Pins 7, 8, 9, 10)
    content += bp.wire(246.38, 142.24, 246.38, 144.78)
    content += bp.wire(246.38, 144.78, 246.38, 147.32)
    content += bp.wire(246.38, 147.32, 246.38, 149.86)
    content += bp.junc(246.38, 142.24)
    content += bp.junc(246.38, 144.78)
    content += bp.junc(246.38, 147.32)
    content += bp.wire(246.38, 149.86, 246.38, 154.94)
    content += bp.gnd_sym(246.38, 154.94)

    # Sheet ending
    content += ")\n"
    
    with open("04_SIM_POWER_OUTPUTS.kicad_sch", "w", encoding="utf-8") as f:
        f.write(content)
    print("Sheet 4 successfully generated: 04_SIM_POWER_OUTPUTS.kicad_sch")

if __name__ == "__main__":
    build_sheet4()
