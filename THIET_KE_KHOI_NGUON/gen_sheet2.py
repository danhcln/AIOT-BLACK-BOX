# -*- coding: utf-8 -*-
"""
Verified 100% planar generator for Sheet 2: BQ25895 + DW01A/FS8205A
Zero vertical wire crossings.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import build_complete_power_project as bp
import custom_symbols_def as cust_syms
import generate_symbols as base_syms

def generate_sheet2(out_path):
    content = bp.make_header("KHỐI SẠC PIN LI-ION 1S & BẢO VỆ PIN (BQ25895 + DW01A/FS8205A)", 3, 5)
    
    # -------------------------------------------------------------------------
    # 1. 1S Battery & Dual FS8205A Protection Circuit
    # -------------------------------------------------------------------------
    j3_x, j3_y = 35.56, 50.80
    content += bp.sym_inst("Connector:Conn_01x02_Pin", "J3", "18650_CELL_IN", j3_x, j3_y, 0,
                           "Connector_JST:JST_VH_B2P-VH_1x02_P3.96mm_Vertical",
                           "https://www.jst-mfg.com/product/pdf/eng/eVH.pdf",
                           "1S 18650 Li-ion High-Current Connector, 3.96mm, 10A rating",
                           pins=["1", "2"])
    
    u3_x, u3_y = 66.04, 86.36
    content += bp.sym_inst("Battery_Management:DW01A", "U3", "DW01A-G", u3_x, u3_y, 0,
                           "Package_TO_SOT_SMD:SOT-23-6",
                           "https://datasheet.lcsc.com/lcsc/1811151441_Fortune-Semicon-DW01A-G_C24339.pdf",
                           "Single Cell Li-ion Battery Protection IC, 4.30V OVP, 2.40V UVP, SOT-23-6",
                           pins=["1", "2", "3", "4", "5", "6"])
    
    q1_x, q1_y = 101.60, 86.36
    content += bp.sym_inst("Transistor_FET:FS8205A", "Q1", "FS8205A (Dual N-FET)", q1_x, q1_y, 0,
                           "Package_SO:TSSOP-8_4.4x3mm_P0.65mm",
                           "https://datasheet.lcsc.com/lcsc/1811151441_Fortune-Semicon-FS8205A_C32254.pdf",
                           "Dual N-Channel Power MOSFET, 20V 6A, 25mOhm per pair, TSSOP-8",
                           pins=["1", "2", "3", "4", "5", "6", "7", "8"])
    
    q2_x, q2_y = 129.54, 86.36
    content += bp.sym_inst("Transistor_FET:FS8205A", "Q2", "FS8205A (Dual N-FET)", q2_x, q2_y, 0,
                           "Package_SO:TSSOP-8_4.4x3mm_P0.65mm",
                           "https://datasheet.lcsc.com/lcsc/1811151441_Fortune-Semicon-FS8205A_C32254.pdf",
                           "Dual N-Channel Power MOSFET in parallel for 12A / 6.0A trip threshold, TSSOP-8",
                           pins=["1", "2", "3", "4", "5", "6", "7", "8"])
    
    r15_x, r15_y = 50.80, 71.12
    content += bp.sym_inst("Device:R", "R15", "100 (1%)", r15_x, r15_y, 0,
                           "Resistor_SMD:R_0603_1608Metric",
                           "~", "VCC RC Filter Resistor, 100 Ohm, 1%, 0603",
                           pins=["1", "2"])
    
    c15_x, c15_y = 50.80, 86.36
    content += bp.sym_inst("Device:C", "C15", "0.1uF/16V (X7R)", c15_x, c15_y, 0,
                           "Capacitor_SMD:C_0603_1608Metric",
                           "~", "VCC Decoupling Capacitor, 0.1uF, 16V, X7R, 0603",
                           pins=["1", "2"])
    
    r16_x, r16_y = 50.80, 101.60
    content += bp.sym_inst("Device:R", "R16", "1k (1%)", r16_x, r16_y, 90,
                           "Resistor_SMD:R_0603_1608Metric",
                           "~", "Current Sense Filter Resistor, 1k, 1%, 0603",
                           pins=["1", "2"])
    
    # Battery Voltage Monitoring Divider (GPIO1 = ADC_VBAT_SENSE)
    r17_x, r17_y = 81.28, 45.72
    content += bp.sym_inst("Device:R", "R17", "100k (0.1%)", r17_x, r17_y, 0,
                           "Resistor_SMD:R_0603_1608Metric",
                           "~", "High-Precision Divider Resistor, 100k, 0.1%, 25ppm, 0603",
                           pins=["1", "2"])
    
    r18_x, r18_y = 81.28, 58.42
    content += bp.sym_inst("Device:R", "R18", "100k (0.1%)", r18_x, r18_y, 0,
                           "Resistor_SMD:R_0603_1608Metric",
                           "~", "High-Precision Divider Resistor, 100k, 0.1%, 25ppm, 0603",
                           pins=["1", "2"])
    
    c17_x, c17_y = 96.52, 58.42
    content += bp.sym_inst("Device:C", "C17", "100nF/16V (C0G)", c17_x, c17_y, 0,
                           "Capacitor_SMD:C_0603_1608Metric",
                           "~", "ADC Anti-Aliasing Ceramic Capacitor, 100nF, 16V, C0G, 0603",
                           pins=["1", "2"])
    
    tp_adc_x, tp_adc_y = 111.76, 52.07
    content += bp.sym_inst("Connector:TestPoint", "TP3", "TP_ADC_VBAT", tp_adc_x, tp_adc_y, 0,
                           "TestPoint:TestPoint_Pad_D1.5mm",
                           "~", "Test Point for Battery ADC Divider Output",
                           pins=["1"])
    
    tp_vbat_x, tp_vbat_y = 111.76, 38.10
    content += bp.sym_inst("Connector:TestPoint", "TP4", "TP_VBAT", tp_vbat_x, tp_vbat_y, 0,
                           "TestPoint:TestPoint_Pad_D1.5mm",
                           "~", "Test Point for Protected Battery Voltage Rail (VBAT)",
                           pins=["1"])

    # -------------------------------------------------------------------------
    # 2. BQ25895 NVDC Charger
    # -------------------------------------------------------------------------
    u2_x, u2_y = 203.20, 96.52
    content += bp.sym_inst("Battery_Management:BQ25895RTWR", "U2", "BQ25895RTWR", u2_x, u2_y, 0,
                           "Package_DFN_QFN:Texas_RTW0024A",
                           "https://www.ti.com/lit/ds/symlink/bq25895.pdf",
                           "I2C Controlled Single-Cell 5A Fast Charger with NVDC Power Path Management, WQFN-24",
                           pins=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                                 "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                                 "21", "22", "23", "24", "25"])
    
    # Left passives: C7, C8, C9, R8, R9, R10
    c7_x, c7_y = 175.26, 78.74
    content += bp.sym_inst("Device:C", "C7", "10uF/25V (X7R)", c7_x, c7_y, 0,
                           "Capacitor_SMD:C_0805_2012Metric",
                           "~", "Ceramic Capacitor, 10uF, 25V, X7R, 0805",
                           pins=["1", "2"])
    
    c8_x, c8_y = 167.64, 81.28
    content += bp.sym_inst("Device:C", "C8", "10uF/25V (X7R)", c8_x, c8_y, 0,
                           "Capacitor_SMD:C_0805_2012Metric",
                           "~", "High-Frequency Ceramic Capacitor, 10uF, 25V, X7R, 0805",
                           pins=["1", "2"])
    
    c9_x, c9_y = 160.02, 83.82
    content += bp.sym_inst("Device:C", "C9", "4.7uF/10V (X5R)", c9_x, c9_y, 0,
                           "Capacitor_SMD:C_0603_1608Metric",
                           "~", "Ceramic Capacitor, 4.7uF, 10V, X5R, 0603",
                           pins=["1", "2"])
    
    r8_x, r8_y = 175.26, 96.52
    content += bp.sym_inst("Device:R", "R8", "158 (1% / 3.25A)", r8_x, r8_y, 90,
                           "Resistor_SMD:R_0603_1608Metric",
                           "~", "Current Limit Resistor, 158 Ohm, 1%, 0603",
                           pins=["1", "2"])
    
    # NTC JEITA divider placed directly opposite Pin 11 (TS at Y = 99.06)
    r9_x, r9_y = 167.64, 93.98
    content += bp.sym_inst("Device:R", "R9", "5.23k (1%)", r9_x, r9_y, 0,
                           "Resistor_SMD:R_0603_1608Metric",
                           "~", "Resistor, 5.23k, 1%, 0603 (JEITA Upper)",
                           pins=["1", "2"])
    
    r10_x, r10_y = 167.64, 104.14
    content += bp.sym_inst("Device:R", "R10", "30.1k (1%)", r10_x, r10_y, 0,
                           "Resistor_SMD:R_0603_1608Metric",
                           "~", "Resistor, 30.1k, 1%, 0603 (JEITA Lower)",
                           pins=["1", "2"])
    
    # Inductor L1 (1.0uH 7.5A) placed at Y = 78.74 (SW Lane)
    l1_x, l1_y = 236.22, 78.74
    content += bp.sym_inst("Device:L", "L1", "1.0uH (7.5A Sat)", l1_x, l1_y, 90,
                           "Inductor_SMD:L_Bourns_SRP6540",
                           "https://www.bourns.com/docs/product-datasheets/srp6540.pdf",
                           "Shielded Power Inductor, 1.0uH, 7.5A Isat, Low DCR SMD",
                           pins=["1", "2"])
    
    c10_x, c10_y = 231.14, 83.82
    content += bp.sym_inst("Device:C", "C10", "47nF/25V (X7R)", c10_x, c10_y, 90,
                           "Capacitor_SMD:C_0603_1608Metric",
                           "~", "Bootstrap Ceramic Capacitor, 47nF, 25V, X7R, 0603",
                           pins=["1", "2"])
    
    # System Output Caps: C11 (22uF), C12 (22uF) & TP_SYS along Y = 88.90 (SYS Lane)
    c11_x, c11_y = 246.38, 88.90
    content += bp.sym_inst("Device:C", "C11", "22uF/10V (X5R)", c11_x, c11_y, 0,
                           "Capacitor_SMD:C_0805_2012Metric",
                           "~", "SYS Output Capacitor, 22uF, 10V, X5R, 0805",
                           pins=["1", "2"])
    
    c12_x, c12_y = 254.00, 88.90
    content += bp.sym_inst("Device:C", "C12", "22uF/10V (X5R)", c12_x, c12_y, 0,
                           "Capacitor_SMD:C_0805_2012Metric",
                           "~", "SYS Output Capacitor, 22uF, 10V, X5R, 0805",
                           pins=["1", "2"])
    
    tp_sys_x, tp_sys_y = 261.62, 88.90
    content += bp.sym_inst("Connector:TestPoint", "TP5", "TP_SYS", tp_sys_x, tp_sys_y, 0,
                           "TestPoint:TestPoint_Pad_D1.5mm",
                           "~", "Test Point for NVDC System Output Rail (SYS)",
                           pins=["1"])
    
    # Battery Output Caps: C13 (10uF), C14 (10uF) along Y = 100.33 (pin 1 at Y = 96.52)
    c13_x, c13_y = 271.78, 100.33
    content += bp.sym_inst("Device:C", "C13", "10uF/10V (X5R)", c13_x, c13_y, 0,
                           "Capacitor_SMD:C_0805_2012Metric",
                           "~", "BAT Filter Capacitor, 10uF, 10V, X5R, 0805",
                           pins=["1", "2"])
    
    c14_x, c14_y = 279.40, 100.33
    content += bp.sym_inst("Device:C", "C14", "10uF/10V (X5R)", c14_x, c14_y, 0,
                           "Capacitor_SMD:C_0805_2012Metric",
                           "~", "BAT Filter Capacitor, 10uF, 10V, X5R, 0805",
                           pins=["1", "2"])
    
    # Pullup Resistors for STAT, INT, SCL, SDA placed HORIZONTALLY
    r11_x, r11_y = 243.84, 104.14
    content += bp.sym_inst("Device:R", "R11", "10k (1%)", r11_x, r11_y, 90,
                           "Resistor_SMD:R_0603_1608Metric",
                           "~", "Pullup Resistor for CHG_STAT, 10k, 1%, 0603",
                           pins=["1", "2"])
    
    r12_x, r12_y = 243.84, 109.22
    content += bp.sym_inst("Device:R", "R12", "10k (1%)", r12_x, r12_y, 90,
                           "Resistor_SMD:R_0603_1608Metric",
                           "~", "Pullup Resistor for CHG_INT, 10k, 1%, 0603",
                           pins=["1", "2"])
    
    r13_x, r13_y = 243.84, 114.30
    content += bp.sym_inst("Device:R", "R13", "4.7k (1%)", r13_x, r13_y, 90,
                           "Resistor_SMD:R_0603_1608Metric",
                           "~", "I2C SCL Pullup Resistor, 4.7k, 1%, 0603",
                           pins=["1", "2"])
    
    r14_x, r14_y = 243.84, 119.38
    content += bp.sym_inst("Device:R", "R14", "4.7k (1%)", r14_x, r14_y, 90,
                           "Resistor_SMD:R_0603_1608Metric",
                           "~", "I2C SDA Pullup Resistor, 4.7k, 1%, 0603",
                           pins=["1", "2"])

    # -------------------------------------------------------------------------
    # CALCULATE PIN POSITIONS
    # -------------------------------------------------------------------------
    j3_p1 = bp.pin_pos(base_syms.SYM_CONN_02, j3_x, j3_y, "1", 0)
    j3_p2 = bp.pin_pos(base_syms.SYM_CONN_02, j3_x, j3_y, "2", 0)
    
    u3_p1 = bp.pin_pos(cust_syms.SYM_DW01A, u3_x, u3_y, "1", 0)
    u3_p2 = bp.pin_pos(cust_syms.SYM_DW01A, u3_x, u3_y, "2", 0)
    u3_p3 = bp.pin_pos(cust_syms.SYM_DW01A, u3_x, u3_y, "3", 0)
    u3_p4 = bp.pin_pos(cust_syms.SYM_DW01A, u3_x, u3_y, "4", 0)
    u3_p5 = bp.pin_pos(cust_syms.SYM_DW01A, u3_x, u3_y, "5", 0)
    u3_p6 = bp.pin_pos(cust_syms.SYM_DW01A, u3_x, u3_y, "6", 0)
    
    q1_p1 = bp.pin_pos(cust_syms.SYM_FS8205A, q1_x, q1_y, "1", 0)
    q1_p2 = bp.pin_pos(cust_syms.SYM_FS8205A, q1_x, q1_y, "2", 0)
    q1_p3 = bp.pin_pos(cust_syms.SYM_FS8205A, q1_x, q1_y, "3", 0)
    q1_p4 = bp.pin_pos(cust_syms.SYM_FS8205A, q1_x, q1_y, "4", 0)
    q1_p5 = bp.pin_pos(cust_syms.SYM_FS8205A, q1_x, q1_y, "5", 0)
    q1_p6 = bp.pin_pos(cust_syms.SYM_FS8205A, q1_x, q1_y, "6", 0)
    q1_p7 = bp.pin_pos(cust_syms.SYM_FS8205A, q1_x, q1_y, "7", 0)
    q1_p8 = bp.pin_pos(cust_syms.SYM_FS8205A, q1_x, q1_y, "8", 0)
    
    q2_p1 = bp.pin_pos(cust_syms.SYM_FS8205A, q2_x, q2_y, "1", 0)
    q2_p2 = bp.pin_pos(cust_syms.SYM_FS8205A, q2_x, q2_y, "2", 0)
    q2_p3 = bp.pin_pos(cust_syms.SYM_FS8205A, q2_x, q2_y, "3", 0)
    q2_p4 = bp.pin_pos(cust_syms.SYM_FS8205A, q2_x, q2_y, "4", 0)
    q2_p5 = bp.pin_pos(cust_syms.SYM_FS8205A, q2_x, q2_y, "5", 0)
    q2_p6 = bp.pin_pos(cust_syms.SYM_FS8205A, q2_x, q2_y, "6", 0)
    q2_p7 = bp.pin_pos(cust_syms.SYM_FS8205A, q2_x, q2_y, "7", 0)
    q2_p8 = bp.pin_pos(cust_syms.SYM_FS8205A, q2_x, q2_y, "8", 0)
    
    r15_p1 = bp.pin_pos(base_syms.SYM_R, r15_x, r15_y, "1", 0)
    r15_p2 = bp.pin_pos(base_syms.SYM_R, r15_x, r15_y, "2", 0)
    c15_p1 = bp.pin_pos(base_syms.SYM_C, c15_x, c15_y, "1", 0)
    c15_p2 = bp.pin_pos(base_syms.SYM_C, c15_x, c15_y, "2", 0)
    r16_p1 = bp.pin_pos(base_syms.SYM_R, r16_x, r16_y, "1", 90)
    r16_p2 = bp.pin_pos(base_syms.SYM_R, r16_x, r16_y, "2", 90)
    
    r17_p1 = bp.pin_pos(base_syms.SYM_R, r17_x, r17_y, "1", 0)
    r17_p2 = bp.pin_pos(base_syms.SYM_R, r17_x, r17_y, "2", 0)
    r18_p1 = bp.pin_pos(base_syms.SYM_R, r18_x, r18_y, "1", 0)
    r18_p2 = bp.pin_pos(base_syms.SYM_R, r18_x, r18_y, "2", 0)
    c17_p1 = bp.pin_pos(base_syms.SYM_C, c17_x, c17_y, "1", 0)
    c17_p2 = bp.pin_pos(base_syms.SYM_C, c17_x, c17_y, "2", 0)
    tp_adc_p1 = bp.pin_pos(base_syms.SYM_TESTPOINT, tp_adc_x, tp_adc_y, "1", 0)
    tp_vbat_p1 = bp.pin_pos(base_syms.SYM_TESTPOINT, tp_vbat_x, tp_vbat_y, "1", 0)
    
    u2_p1 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "1", 0)
    u2_p23 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "23", 0)
    u2_p22 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "22", 0)
    u2_p9 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "9", 0)
    u2_p8 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "8", 0)
    u2_p12 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "12", 0)
    u2_p10 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "10", 0)
    u2_p11 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "11", 0)
    u2_p24 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "24", 0)
    u2_p2 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "2", 0)
    u2_p3 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "3", 0)
    u2_p17 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "17", 0)
    u2_p18 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "18", 0)
    u2_p25 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "25", 0)
    
    u2_p19 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "19", 0)
    u2_p20 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "20", 0)
    u2_p21 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "21", 0)
    u2_p15 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "15", 0)
    u2_p16 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "16", 0)
    u2_p13 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "13", 0)
    u2_p14 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "14", 0)
    u2_p4 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "4", 0)
    u2_p7 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "7", 0)
    u2_p5 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "5", 0)
    u2_p6 = bp.pin_pos(cust_syms.SYM_BQ25895, u2_x, u2_y, "6", 0)
    
    c7_p1 = bp.pin_pos(base_syms.SYM_C, c7_x, c7_y, "1", 0)
    c7_p2 = bp.pin_pos(base_syms.SYM_C, c7_x, c7_y, "2", 0)
    c8_p1 = bp.pin_pos(base_syms.SYM_C, c8_x, c8_y, "1", 0)
    c8_p2 = bp.pin_pos(base_syms.SYM_C, c8_x, c8_y, "2", 0)
    c9_p1 = bp.pin_pos(base_syms.SYM_C, c9_x, c9_y, "1", 0)
    c9_p2 = bp.pin_pos(base_syms.SYM_C, c9_x, c9_y, "2", 0)
    
    r8_p1 = bp.pin_pos(base_syms.SYM_R, r8_x, r8_y, "1", 90)
    r8_p2 = bp.pin_pos(base_syms.SYM_R, r8_x, r8_y, "2", 90)
    
    r9_p1 = bp.pin_pos(base_syms.SYM_R, r9_x, r9_y, "1", 0)
    r9_p2 = bp.pin_pos(base_syms.SYM_R, r9_x, r9_y, "2", 0)
    r10_p1 = bp.pin_pos(base_syms.SYM_R, r10_x, r10_y, "1", 0)
    r10_p2 = bp.pin_pos(base_syms.SYM_R, r10_x, r10_y, "2", 0)
    
    l1_p1 = bp.pin_pos(base_syms.SYM_L, l1_x, l1_y, "1", 90)
    l1_p2 = bp.pin_pos(base_syms.SYM_L, l1_x, l1_y, "2", 90)
    c10_p1 = bp.pin_pos(base_syms.SYM_C, c10_x, c10_y, "1", 90)
    c10_p2 = bp.pin_pos(base_syms.SYM_C, c10_x, c10_y, "2", 90)
    
    c11_p1 = bp.pin_pos(base_syms.SYM_C, c11_x, c11_y, "1", 0)
    c11_p2 = bp.pin_pos(base_syms.SYM_C, c11_x, c11_y, "2", 0)
    c12_p1 = bp.pin_pos(base_syms.SYM_C, c12_x, c12_y, "1", 0)
    c12_p2 = bp.pin_pos(base_syms.SYM_C, c12_x, c12_y, "2", 0)
    tp_sys_p1 = bp.pin_pos(base_syms.SYM_TESTPOINT, tp_sys_x, tp_sys_y, "1", 0)
    
    c13_p1 = bp.pin_pos(base_syms.SYM_C, c13_x, c13_y, "1", 0)
    c13_p2 = bp.pin_pos(base_syms.SYM_C, c13_x, c13_y, "2", 0)
    c14_p1 = bp.pin_pos(base_syms.SYM_C, c14_x, c14_y, "1", 0)
    c14_p2 = bp.pin_pos(base_syms.SYM_C, c14_x, c14_y, "2", 0)
    
    r11_p1 = bp.pin_pos(base_syms.SYM_R, r11_x, r11_y, "1", 90)
    r11_p2 = bp.pin_pos(base_syms.SYM_R, r11_x, r11_y, "2", 90)
    r12_p1 = bp.pin_pos(base_syms.SYM_R, r12_x, r12_y, "1", 90)
    r12_p2 = bp.pin_pos(base_syms.SYM_R, r12_x, r12_y, "2", 90)
    r13_p1 = bp.pin_pos(base_syms.SYM_R, r13_x, r13_y, "1", 90)
    r13_p2 = bp.pin_pos(base_syms.SYM_R, r13_x, r13_y, "2", 90)
    r14_p1 = bp.pin_pos(base_syms.SYM_R, r14_x, r14_y, "1", 90)
    r14_p2 = bp.pin_pos(base_syms.SYM_R, r14_x, r14_y, "2", 90)

    # -------------------------------------------------------------------------
    # WIRING - SECTION 1: BATTERY, DW01A, FS8205A, ADC DIVIDER
    # -------------------------------------------------------------------------
    content += bp.wire(j3_p1[0], j3_p1[1], 30.48, j3_p1[1])
    content += bp.wire(30.48, j3_p1[1], 30.48, 38.10)
    content += bp.wire(30.48, 38.10, r15_p1[0], 38.10)
    
    content += bp.junc(r15_p1[0], 38.10)
    content += bp.wire(r15_p1[0], 38.10, r15_p1[0], r15_p1[1])
    
    content += bp.wire(r15_p1[0], 38.10, r17_p1[0], 38.10)
    content += bp.junc(r17_p1[0], 38.10)
    content += bp.wire(r17_p1[0], 38.10, r17_p1[0], r17_p1[1])
    
    content += bp.wire(r17_p1[0], 38.10, tp_vbat_p1[0], 38.10)
    content += bp.junc(tp_vbat_p1[0], 38.10)
    content += bp.wire(tp_vbat_p1[0], 38.10, tp_vbat_p1[0], tp_vbat_p1[1])
    
    # VBAT rail across top to X = 284.48 and drops to Y = 96.52
    content += bp.wire(tp_vbat_p1[0], 38.10, 284.48, 38.10)
    content += bp.wire(284.48, 38.10, 284.48, 96.52)
    content += bp.junc(284.48, 96.52)
    content += bp.wire(284.48, 96.52, 287.02, 96.52)
    content += bp.global_lbl("VBAT", 287.02, 96.52, 0, "bidirectional")
    content += bp.hier_lbl("VBAT", 287.02, 96.52, 0, "output")
    
    # DW01A Pin 5 (VCC) Filter Node
    content += bp.wire(r15_p2[0], r15_p2[1], r15_p2[0], u3_p5[1])
    content += bp.wire(r15_p2[0], u3_p5[1], u3_p5[0], u3_p5[1])
    content += bp.junc(r15_p2[0], u3_p5[1])
    content += bp.wire(r15_p2[0], u3_p5[1], c15_p1[0], c15_p1[1])
    
    # J3 Pin 2 (CELL_NEG) -> Runs down at X = 25.40
    content += bp.wire(j3_p2[0], j3_p2[1], 25.40, j3_p2[1])
    content += bp.wire(25.40, j3_p2[1], 25.40, 91.44)
    content += bp.wire(25.40, 91.44, c15_p2[0], 91.44)
    content += bp.junc(c15_p2[0], 91.44)
    content += bp.wire(c15_p2[0], 91.44, c15_p2[0], c15_p2[1])
    content += bp.wire(c15_p2[0], 91.44, u3_p6[0], u3_p6[1])
    
    # CELL_NEG connects to Source S1 of Q1 and Q2 along Y = 73.66
    content += bp.wire(25.40, 91.44, 25.40, 73.66)
    content += bp.wire(25.40, 73.66, 114.30, 73.66)
    content += bp.wire(114.30, 73.66, 114.30, q1_p2[1])
    content += bp.wire(114.30, q1_p2[1], q1_p2[0], q1_p2[1])
    content += bp.wire(q1_p3[0], q1_p3[1], 114.30, q1_p3[1])
    content += bp.wire(114.30, q1_p2[1], 114.30, q1_p3[1])
    content += bp.junc(114.30, q1_p2[1])
    content += bp.junc(114.30, q1_p3[1])
    
    content += bp.wire(114.30, 73.66, 142.24, 73.66)
    content += bp.wire(142.24, 73.66, 142.24, q2_p2[1])
    content += bp.wire(142.24, q2_p2[1], q2_p2[0], q2_p2[1])
    content += bp.wire(q2_p3[0], q2_p3[1], 142.24, q2_p3[1])
    content += bp.wire(142.24, q2_p2[1], 142.24, q2_p3[1])
    content += bp.junc(142.24, q2_p2[1])
    content += bp.junc(142.24, q2_p3[1])
    
    # DW01A Pin 4 (TD) -> No connect
    content += bp.no_conn(u3_p4[0], u3_p4[1])
    
    # DW01A Pin 2 (CS) -> R16 to Common System GND
    content += bp.wire(u3_p2[0], u3_p2[1], 60.96, u3_p2[1])
    content += bp.wire(60.96, u3_p2[1], 60.96, r16_p2[1])
    content += bp.wire(60.96, r16_p2[1], r16_p2[0], r16_p2[1])
    content += bp.wire(r16_p1[0], r16_p1[1], 45.72, r16_p1[1])
    content += bp.wire(45.72, r16_p1[1], 45.72, 116.84)
    content += bp.gnd_sym(45.72, 116.84)
    
    # DW01A Gate Controls
    content += bp.wire(u3_p1[0], u3_p1[1], q1_p4[0], q1_p4[1])
    content += bp.junc(q1_p4[0], q1_p4[1])
    content += bp.wire(q1_p4[0], q1_p4[1], q2_p4[0], q2_p4[1])
    
    content += bp.wire(u3_p3[0], u3_p3[1], q1_p5[0], q1_p5[1])
    content += bp.junc(q1_p5[0], q1_p5[1])
    content += bp.wire(q1_p5[0], q1_p5[1], q2_p5[0], q2_p5[1])
    
    # Q1 & Q2 Common System GND side
    content += bp.wire(q1_p6[0], q1_p6[1], 119.38, q1_p6[1])
    content += bp.wire(q1_p7[0], q1_p7[1], 119.38, q1_p7[1])
    content += bp.wire(119.38, q1_p6[1], 119.38, 116.84)
    content += bp.junc(119.38, q1_p6[1])
    content += bp.junc(119.38, q1_p7[1])
    content += bp.gnd_sym(119.38, 116.84)
    
    content += bp.wire(q2_p6[0], q2_p6[1], 147.32, q2_p6[1])
    content += bp.wire(q2_p7[0], q2_p7[1], 147.32, q2_p7[1])
    content += bp.wire(147.32, q2_p6[1], 147.32, 116.84)
    content += bp.junc(147.32, q2_p6[1])
    content += bp.junc(147.32, q2_p7[1])
    content += bp.gnd_sym(147.32, 116.84)
    
    # Q1 & Q2 Drain D1/D2 tie together
    content += bp.wire(q1_p1[0], q1_p1[1], 116.84, q1_p1[1])
    content += bp.wire(q1_p8[0], q1_p8[1], 116.84, q1_p8[1])
    content += bp.wire(116.84, q1_p1[1], 116.84, q1_p8[1])
    content += bp.wire(116.84, q1_p1[1], 144.78, q1_p1[1])
    content += bp.junc(116.84, q1_p1[1])
    
    content += bp.wire(q2_p1[0], q2_p1[1], 144.78, q2_p1[1])
    content += bp.wire(q2_p8[0], q2_p8[1], 144.78, q2_p8[1])
    content += bp.wire(144.78, q2_p1[1], 144.78, q2_p8[1])
    content += bp.junc(144.78, q2_p1[1])
    
    # ADC Divider Wires
    content += bp.wire(r17_p2[0], r17_p2[1], r17_p2[0], 52.07)
    content += bp.wire(r17_p2[0], 52.07, r18_p1[0], r18_p1[1])
    content += bp.junc(r17_p2[0], 52.07)
    
    content += bp.wire(r17_p2[0], 52.07, c17_p1[0], 52.07)
    content += bp.junc(c17_p1[0], 52.07)
    content += bp.wire(c17_p1[0], 52.07, c17_p1[0], c17_p1[1])
    
    content += bp.wire(c17_p1[0], 52.07, tp_adc_p1[0], tp_adc_p1[1])
    content += bp.junc(tp_adc_p1[0], tp_adc_p1[1])
    content += bp.wire(tp_adc_p1[0], tp_adc_p1[1], 124.46, tp_adc_p1[1])
    content += bp.global_lbl("ADC_VBAT_SENSE", 124.46, tp_adc_p1[1], 0, "output")
    content += bp.hier_lbl("ADC_VBAT_SENSE", 124.46, tp_adc_p1[1], 0, "output")
    
    # R18 bottom and C17 bottom to GND
    content += bp.wire(r18_p2[0], r18_p2[1], r18_p2[0], 66.04)
    content += bp.gnd_sym(r18_p2[0], 66.04)
    content += bp.wire(c17_p2[0], c17_p2[1], c17_p2[0], 66.04)
    content += bp.gnd_sym(c17_p2[0], 66.04)

    # -------------------------------------------------------------------------
    # WIRING - SECTION 2: BQ25895 CHARGER & NVDC POWER PATH
    # -------------------------------------------------------------------------
    # Pin 1 (VBUS): C7 and Input Global Label VBUS_MUX
    content += bp.wire(u2_p1[0], u2_p1[1], c7_p1[0], u2_p1[1])
    content += bp.junc(c7_p1[0], u2_p1[1])
    content += bp.wire(c7_p1[0], u2_p1[1], c7_p1[0], c7_p1[1])
    content += bp.gnd_sym(c7_p2[0], c7_p2[1]) # Local GND right at pin 2!
    content += bp.wire(c7_p1[0], u2_p1[1], c7_p1[0], 71.12)
    content += bp.wire(c7_p1[0], 71.12, 152.40, 71.12)
    content += bp.global_lbl("VBUS_MUX", 152.40, 71.12, 180, "input")
    content += bp.hier_lbl("VBUS_MUX", 152.40, 71.12, 180, "input")
    
    # Pin 23 (PMID): High frequency ceramic cap C8 (10uF) to PGND
    content += bp.wire(u2_p23[0], u2_p23[1], c8_p1[0], u2_p23[1])
    content += bp.wire(c8_p1[0], u2_p23[1], c8_p1[0], c8_p1[1])
    content += bp.gnd_sym(c8_p2[0], c8_p2[1]) # Local GND right at pin 2!
    
    # Pin 22 (REGN): LDO output cap C9 (4.7uF) to PGND and TS pullup R9
    content += bp.wire(u2_p22[0], u2_p22[1], c9_p1[0], u2_p22[1])
    content += bp.junc(c9_p1[0], u2_p22[1])
    content += bp.wire(c9_p1[0], u2_p22[1], c9_p1[0], c9_p1[1])
    content += bp.gnd_sym(c9_p2[0], c9_p2[1]) # Local GND right at pin 2!
    content += bp.wire(c9_p1[0], u2_p22[1], r9_p1[0], u2_p22[1])
    content += bp.wire(r9_p1[0], u2_p22[1], r9_p1[0], r9_p1[1])
    
    # Pin 11 (TS): Connected straight to NTC divider (R9 bottom & R10 top at 167.64, 99.06)
    content += bp.wire(r9_p2[0], r9_p2[1], r9_p2[0], 99.06)
    content += bp.wire(r9_p2[0], 99.06, r10_p1[0], r10_p1[1])
    content += bp.junc(r9_p2[0], 99.06)
    content += bp.wire(r9_p2[0], 99.06, u2_p11[0], u2_p11[1])
    content += bp.gnd_sym(r10_p2[0], r10_p2[1]) # Local GND right at pin 2!
    
    # Pin 10 (ILIM): Resistor R8 (158 Ohm) to GND for 3.25A limit
    content += bp.wire(u2_p10[0], u2_p10[1], r8_p2[0], u2_p10[1])
    content += bp.gnd_sym(r8_p1[0], r8_p1[1]) # Local GND right at pin 1!
    
    # Logic pins tied to GND locally: ~CE (pin 9), OTG (pin 8), DSEL (pin 24)
    content += bp.wire(u2_p9[0], u2_p9[1], 180.34, u2_p9[1])
    content += bp.gnd_sym(180.34, u2_p9[1])
    
    content += bp.wire(u2_p8[0], u2_p8[1], 180.34, u2_p8[1])
    content += bp.gnd_sym(180.34, u2_p8[1])
    
    content += bp.wire(u2_p24[0], u2_p24[1], 180.34, u2_p24[1])
    content += bp.gnd_sym(180.34, u2_p24[1])
    
    # Pin 12 (QON) -> No Connect
    content += bp.no_conn(u2_p12[0], u2_p12[1])
    
    # Pins 2, 3 (D+, D-) -> No Connect
    content += bp.no_conn(u2_p2[0], u2_p2[1])
    content += bp.no_conn(u2_p3[0], u2_p3[1])
    
    # Power GND Pins: 17, 18, 25 (PGND & Thermal Pad) - Grouped cleanly at bottom
    content += bp.wire(u2_p17[0], u2_p17[1], 180.34, u2_p17[1])
    content += bp.wire(u2_p18[0], u2_p18[1], 180.34, u2_p18[1])
    content += bp.wire(u2_p25[0], u2_p25[1], 180.34, u2_p25[1])
    content += bp.wire(180.34, u2_p17[1], 180.34, u2_p25[1])
    content += bp.junc(180.34, u2_p17[1])
    content += bp.junc(180.34, u2_p18[1])
    content += bp.junc(180.34, u2_p25[1])
    content += bp.gnd_sym(180.34, u2_p25[1])
    
    # -------------------------------------------------------------------------
    # RIGHT SIDE - LANE 1 (TOP): SW & BTST (Y = 78.74)
    # -------------------------------------------------------------------------
    content += bp.wire(u2_p19[0], u2_p19[1], u2_p20[0], u2_p20[1])
    content += bp.wire(u2_p19[0], u2_p19[1], l1_p1[0], u2_p19[1])
    content += bp.junc(l1_p1[0], u2_p19[1])
    content += bp.wire(l1_p1[0], u2_p19[1], l1_p1[0], l1_p1[1])
    content += bp.wire(l1_p1[0], u2_p19[1], c10_p2[0], u2_p19[1])
    content += bp.wire(c10_p2[0], u2_p19[1], c10_p2[0], c10_p2[1])
    
    content += bp.wire(u2_p21[0], u2_p21[1], c10_p1[0], u2_p21[1])
    content += bp.wire(c10_p1[0], u2_p21[1], c10_p1[0], c10_p1[1])
    
    # -------------------------------------------------------------------------
    # RIGHT SIDE - LANE 2: SYS (Y = 88.90) - Stops at X = 269.24!
    # -------------------------------------------------------------------------
    content += bp.wire(l1_p2[0], l1_p2[1], 241.30, l1_p2[1])
    content += bp.wire(241.30, l1_p2[1], 241.30, 88.90)
    content += bp.wire(u2_p15[0], u2_p15[1], u2_p16[0], u2_p16[1])
    content += bp.wire(u2_p15[0], u2_p15[1], 241.30, 88.90)
    content += bp.junc(241.30, 88.90)
    
    content += bp.wire(241.30, 88.90, c11_p1[0], 88.90)
    content += bp.junc(c11_p1[0], 88.90)
    content += bp.wire(c11_p1[0], 88.90, c11_p1[0], c11_p1[1])
    content += bp.gnd_sym(c11_p2[0], c11_p2[1])
    
    content += bp.wire(c11_p1[0], 88.90, c12_p1[0], 88.90)
    content += bp.junc(c12_p1[0], 88.90)
    content += bp.wire(c12_p1[0], 88.90, c12_p1[0], c12_p1[1])
    content += bp.gnd_sym(c12_p2[0], c12_p2[1])
    
    content += bp.wire(c12_p1[0], 88.90, tp_sys_p1[0], 88.90)
    content += bp.junc(tp_sys_p1[0], 88.90)
    content += bp.wire(tp_sys_p1[0], 88.90, tp_sys_p1[0], tp_sys_p1[1])
    content += bp.wire(tp_sys_p1[0], 88.90, 269.24, 88.90)
    content += bp.global_lbl("SYS", 269.24, 88.90, 0, "output")
    content += bp.hier_lbl("SYS", 269.24, 88.90, 0, "output")
    
    # -------------------------------------------------------------------------
    # RIGHT SIDE - LANE 3: BAT (Y = 96.52) - Runs out to X = 284.48!
    # -------------------------------------------------------------------------
    content += bp.wire(u2_p13[0], u2_p13[1], u2_p14[0], u2_p14[1])
    content += bp.wire(u2_p13[0], u2_p13[1], c13_p1[0], 96.52)
    content += bp.junc(c13_p1[0], 96.52)
    content += bp.wire(c13_p1[0], 96.52, c13_p1[0], c13_p1[1])
    content += bp.gnd_sym(c13_p2[0], c13_p2[1])
    
    content += bp.wire(c13_p1[0], 96.52, c14_p1[0], 96.52)
    content += bp.junc(c14_p1[0], 96.52)
    content += bp.wire(c14_p1[0], 96.52, c14_p1[0], c14_p1[1])
    content += bp.gnd_sym(c14_p2[0], c14_p2[1])
    
    # From C14, BAT continues right to 284.48, meeting the incoming line from top!
    content += bp.wire(c14_p1[0], 96.52, 284.48, 96.52)
    
    # -------------------------------------------------------------------------
    # RIGHT SIDE - LANE 4: OPEN-DRAIN & I2C SIGNALS (Y = 104.14 .. 119.38)
    # -------------------------------------------------------------------------
    content += bp.wire(u2_p4[0], u2_p4[1], 226.06, u2_p4[1])
    content += bp.junc(226.06, u2_p4[1])
    content += bp.global_lbl("CHG_STAT", 226.06, u2_p4[1], 180, "output")
    content += bp.hier_lbl("CHG_STAT", 226.06, u2_p4[1], 180, "output")
    content += bp.wire(226.06, u2_p4[1], r11_p1[0], u2_p4[1])
    
    content += bp.wire(u2_p7[0], u2_p7[1], 223.52, u2_p7[1])
    content += bp.wire(223.52, u2_p7[1], 223.52, 109.22)
    content += bp.wire(223.52, 109.22, 226.06, 109.22)
    content += bp.junc(226.06, 109.22)
    content += bp.global_lbl("CHG_INT", 226.06, 109.22, 180, "output")
    content += bp.hier_lbl("CHG_INT", 226.06, 109.22, 180, "output")
    content += bp.wire(226.06, 109.22, r12_p1[0], 109.22)
    
    content += bp.wire(u2_p5[0], u2_p5[1], 220.98, u2_p5[1])
    content += bp.wire(220.98, u2_p5[1], 220.98, 114.30)
    content += bp.wire(220.98, 114.30, 226.06, 114.30)
    content += bp.junc(226.06, 114.30)
    content += bp.global_lbl("I2C_SCL", 226.06, 114.30, 180, "bidirectional")
    content += bp.wire(226.06, 114.30, r13_p1[0], 114.30)
    
    content += bp.wire(u2_p6[0], u2_p6[1], 218.44, u2_p6[1])
    content += bp.wire(218.44, u2_p6[1], 218.44, 119.38)
    content += bp.wire(218.44, 119.38, 226.06, 119.38)
    content += bp.junc(226.06, 119.38)
    content += bp.global_lbl("I2C_SDA", 226.06, 119.38, 180, "bidirectional")
    content += bp.wire(226.06, 119.38, r14_p1[0], 119.38)
    
    # Pullup Pin 2s tied vertically to 3V3_SYS
    content += bp.wire(r11_p2[0], r11_p2[1], r12_p2[0], r12_p2[1])
    content += bp.wire(r12_p2[0], r12_p2[1], r13_p2[0], r13_p2[1])
    content += bp.wire(r13_p2[0], r13_p2[1], r14_p2[0], r14_p2[1])
    content += bp.junc(r12_p2[0], r12_p2[1])
    content += bp.junc(r13_p2[0], r13_p2[1])
    content += bp.wire(r11_p2[0], r11_p2[1], 259.08, r11_p2[1])
    content += bp.global_lbl("3V3_SYS", 259.08, r11_p2[1], 0, "input")
    
    # Section Headings & Explanatory Texts
    content += bp.sch_text("KHỐI SẠC PIN LI-ION & QUẢN LÝ ĐƯỜNG NGUỒN NVDC (BQ25895)", 25.40, 22.86, 2.0, True)
    content += bp.sch_text("MẠCH BẢO VỆ PIN 1S CHUYÊN DỤNG (DW01A + 2x FS8205A SONG SONG)", 25.40, 30.48, 1.4, True)
    content += bp.sch_text("BẢO VỆ: Quá xả (2.40V) | Quá sạc (4.30V) | Quá dòng cắt: 6.0A (RDSon=25mOhm)", 25.40, 34.29, 1.3, False)
    content += bp.sch_text("ĐO ĐIỆN ÁP PIN: GPIO1 = ADC_VBAT_SENSE (Phân áp 100k/100k + C17 100nF)", 60.96, 45.72, 1.3, False)
    content += bp.sch_text("NVDC CHARGER: Dòng sạc tối đa 5A | Giới hạn đầu vào ILIM = 3.25A | Quản lý nhiệt JEITA TS", 140.00, 30.48, 1.3, False)
    content += bp.sch_text("ĐƯỜNG NGUỒN HỆ THỐNG SYS: Cung cấp trực tiếp cho Boost 5V (2.7V - 4.4V)", 140.00, 34.29, 1.3, False)
    
    content += ")\n"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Sheet 2 successfully generated: {out_path}")

if __name__ == '__main__':
    generate_sheet2("02_CHARGER_BATTERY.kicad_sch")
