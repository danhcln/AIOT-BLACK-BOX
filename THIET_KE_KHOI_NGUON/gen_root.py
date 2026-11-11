# -*- coding: utf-8 -*-
"""
Generator for Root Sheet: AIOT_BLACKBOX_POWER_SUPPLY.kicad_sch
Top-level hierarchical schematic sheet integrating all 4 modular functional blocks:
- Sheet 1: 01_INPUT_SELECTION.kicad_sch (TPS2121 Power Mux)
- Sheet 2: 02_CHARGER_BATTERY.kicad_sch (BQ25895 Charger + DW01A/FS8205A)
- Sheet 3: 03_BOOST_BUCK_RAILS.kicad_sch (TPS61088 5V Boost + TPS62162 3.3V Buck)
- Sheet 4: 04_SIM_POWER_OUTPUTS.kicad_sch (Cellular Supply + Output Headers)

Strict 1.27mm Grid - IEC 61082-1 Planar Inter-Sheet Buses - Clean Hierarchy.
"""

import sys
import os
import uuid

sys.path.append(r"D:\ĐỒ ÁN 2\THIET_KE_KHOI_NGUON")
import build_complete_power_project as bp
import custom_symbols_def as cust_syms
import generate_symbols as base_syms

def build_root_sheet():
    content = bp.make_header("HỆ THỐNG NGUỒN HỘP ĐEN AIOT THÔNG MINH - SƠ ĐỒ KHỐI PHÂN CẤP TỔNG THỂ", 1, 5)

    # Architectural Overview Text
    content += f"""\t(text "KIẾN TRÚC HỆ THỐNG NGUỒN HỘP ĐEN AIOT (HIERARCHICAL SYSTEM ARCHITECTURE):\\n1. INPUT MUX: TỰ ĐỘNG CHỌN NGUỒN NGOÀI (VEHICLE 5V / USB-C 5V) QUA TPS2121 VỚI BẢO VỆ OVP, OCP, TVS\\n2. CHARGER & BATTERY: SẠC PIN 18650 QUA BQ25895 (NVDC POWER PATH) + BẢO VỆ PIN DW01A & DUAL FS8205A (6A OCP)\\n3. SYSTEM RAILS: BOOST TPS61088 (5V_SYS, 3.5A / 5A PEAK) & BUCK TPS62162 (3V3_SYS, 1.0A FIXED)\\n4. CELLULAR STAGE: NGUỒN RIÊNG CHO A7682S (OPTION A: 5V P-FET / OPTION B: TPS62130 3.8V BUCK) + 1000uF POLYMER CAP"
\t\t(at 25.40 33.02 0)
\t\t(effects (font (size 1.3 1.3) (bold yes)) (justify left))
\t\t(uuid "{bp.uid()}")
\t)\n"""

    # -------------------------------------------------------------------------
    # HIERARCHICAL SHEET 1: INPUT_SELECTION
    # (at 25.40, 48.26), size (45.72, 35.56)
    # -------------------------------------------------------------------------
    s1_x, s1_y = 25.40, 48.26
    s1_w, s1_h = 45.72, 35.56
    s1_vbus_mux = (s1_x + s1_w, 60.96) # Output pin at (71.12, 60.96)
    
    content += f"""\t(sheet
\t\t(at {s1_x} {s1_y})
\t\t(size {s1_w} {s1_h})
\t\t(fields_autoplaced yes)
\t\t(stroke (width 0.1524) (type solid))
\t\t(fill (color 0 0 0 0.0000))
\t\t(uuid "{bp.uid()}")
\t\t(property "Sheetname" "01_INPUT_SELECTION" (at {s1_x} {round(s1_y-1.27,2)} 0) (effects (font (size 1.27 1.27) (bold yes)) (justify left bottom)))
\t\t(property "Sheetfile" "01_INPUT_SELECTION.kicad_sch" (at {s1_x} {round(s1_y+s1_h+2.54,2)} 0) (effects (font (size 1.27 1.27)) (justify left top)))
\t\t(pin "VBUS_MUX" output (at {s1_vbus_mux[0]} {s1_vbus_mux[1]} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify right))
\t\t\t(uuid "{bp.uid()}")
\t\t)
\t)\n"""

    # -------------------------------------------------------------------------
    # HIERARCHICAL SHEET 2: CHARGER_BATTERY
    # (at 86.36, 48.26), size (55.88, 66.04)
    # -------------------------------------------------------------------------
    s2_x, s2_y = 86.36, 48.26
    s2_w, s2_h = 55.88, 66.04
    s2_vbus_mux = (s2_x, 60.96)        # Input at (86.36, 60.96)
    s2_sys = (s2_x + s2_w, 55.88)       # Output at (142.24, 55.88)
    s2_vbat = (s2_x + s2_w, 66.04)      # Output at (142.24, 66.04)
    s2_adc_vbat = (s2_x + s2_w, 76.20)  # Output at (142.24, 76.20)
    s2_chg_stat = (s2_x + s2_w, 86.36)  # Output at (142.24, 86.36)
    s2_chg_int = (s2_x + s2_w, 96.52)   # Output at (142.24, 96.52)

    content += f"""\t(sheet
\t\t(at {s2_x} {s2_y})
\t\t(size {s2_w} {s2_h})
\t\t(fields_autoplaced yes)
\t\t(stroke (width 0.1524) (type solid))
\t\t(fill (color 0 0 0 0.0000))
\t\t(uuid "{bp.uid()}")
\t\t(property "Sheetname" "02_CHARGER_BATTERY" (at {s2_x} {round(s2_y-1.27,2)} 0) (effects (font (size 1.27 1.27) (bold yes)) (justify left bottom)))
\t\t(property "Sheetfile" "02_CHARGER_BATTERY.kicad_sch" (at {s2_x} {round(s2_y+s2_h+2.54,2)} 0) (effects (font (size 1.27 1.27)) (justify left top)))
\t\t(pin "VBUS_MUX" input (at {s2_vbus_mux[0]} {s2_vbus_mux[1]} 180)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t\t(uuid "{bp.uid()}")
\t\t)
\t\t(pin "SYS" output (at {s2_sys[0]} {s2_sys[1]} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify right))
\t\t\t(uuid "{bp.uid()}")
\t\t)
\t\t(pin "VBAT" output (at {s2_vbat[0]} {s2_vbat[1]} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify right))
\t\t\t(uuid "{bp.uid()}")
\t\t)
\t\t(pin "ADC_VBAT_SENSE" output (at {s2_adc_vbat[0]} {s2_adc_vbat[1]} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify right))
\t\t\t(uuid "{bp.uid()}")
\t\t)
\t\t(pin "CHG_STAT" output (at {s2_chg_stat[0]} {s2_chg_stat[1]} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify right))
\t\t\t(uuid "{bp.uid()}")
\t\t)
\t\t(pin "CHG_INT" output (at {s2_chg_int[0]} {s2_chg_int[1]} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify right))
\t\t\t(uuid "{bp.uid()}")
\t\t)
\t)\n"""

    # -------------------------------------------------------------------------
    # HIERARCHICAL SHEET 3: BOOST_BUCK_RAILS
    # (at 162.56, 48.26), size (55.88, 50.80)
    # -------------------------------------------------------------------------
    s3_x, s3_y = 162.56, 48.26
    s3_w, s3_h = 55.88, 50.80
    s3_sys = (s3_x, 55.88)               # Input at (162.56, 55.88)
    s3_5v_sys = (s3_x + s3_w, 55.88)     # Output at (218.44, 55.88)
    s3_3v3_sys = (s3_x + s3_w, 66.04)    # Output at (218.44, 66.04)

    content += f"""\t(sheet
\t\t(at {s3_x} {s3_y})
\t\t(size {s3_w} {s3_h})
\t\t(fields_autoplaced yes)
\t\t(stroke (width 0.1524) (type solid))
\t\t(fill (color 0 0 0 0.0000))
\t\t(uuid "{bp.uid()}")
\t\t(property "Sheetname" "03_BOOST_BUCK_RAILS" (at {s3_x} {round(s3_y-1.27,2)} 0) (effects (font (size 1.27 1.27) (bold yes)) (justify left bottom)))
\t\t(property "Sheetfile" "03_BOOST_BUCK_RAILS.kicad_sch" (at {s3_x} {round(s3_y+s3_h+2.54,2)} 0) (effects (font (size 1.27 1.27)) (justify left top)))
\t\t(pin "SYS" input (at {s3_sys[0]} {s3_sys[1]} 180)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t\t(uuid "{bp.uid()}")
\t\t)
\t\t(pin "5V_SYS" output (at {s3_5v_sys[0]} {s3_5v_sys[1]} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify right))
\t\t\t(uuid "{bp.uid()}")
\t\t)
\t\t(pin "3V3_SYS" output (at {s3_3v3_sys[0]} {s3_3v3_sys[1]} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify right))
\t\t\t(uuid "{bp.uid()}")
\t\t)
\t)\n"""

    # -------------------------------------------------------------------------
    # HIERARCHICAL SHEET 4: SIM_POWER_OUTPUTS
    # (at 101.60, 127.00), size (66.04, 50.80)
    # -------------------------------------------------------------------------
    s4_x, s4_y = 101.60, 127.00
    s4_w, s4_h = 66.04, 50.80
    s4_5v_sys = (s4_x, 137.16)           # Input at (101.60, 137.16)
    s4_3v3_sys = (s4_x, 147.32)          # Input at (101.60, 147.32)
    s4_vbat = (s4_x, 157.48)             # Input at (101.60, 157.48)
    s4_sim_pwr = (s4_x + s4_w, 137.16)   # Output at (167.64, 137.16)

    content += f"""\t(sheet
\t\t(at {s4_x} {s4_y})
\t\t(size {s4_w} {s4_h})
\t\t(fields_autoplaced yes)
\t\t(stroke (width 0.1524) (type solid))
\t\t(fill (color 0 0 0 0.0000))
\t\t(uuid "{bp.uid()}")
\t\t(property "Sheetname" "04_SIM_POWER_OUTPUTS" (at {s4_x} {round(s4_y-1.27,2)} 0) (effects (font (size 1.27 1.27) (bold yes)) (justify left bottom)))
\t\t(property "Sheetfile" "04_SIM_POWER_OUTPUTS.kicad_sch" (at {s4_x} {round(s4_y+s4_h+2.54,2)} 0) (effects (font (size 1.27 1.27)) (justify left top)))
\t\t(pin "5V_SYS" input (at {s4_5v_sys[0]} {s4_5v_sys[1]} 180)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t\t(uuid "{bp.uid()}")
\t\t)
\t\t(pin "3V3_SYS" input (at {s4_3v3_sys[0]} {s4_3v3_sys[1]} 180)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t\t(uuid "{bp.uid()}")
\t\t)
\t\t(pin "VBAT" input (at {s4_vbat[0]} {s4_vbat[1]} 180)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t\t(uuid "{bp.uid()}")
\t\t)
\t\t(pin "SIM_PWR" output (at {s4_sim_pwr[0]} {s4_sim_pwr[1]} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify right))
\t\t\t(uuid "{bp.uid()}")
\t\t)
\t)\n"""

    # -------------------------------------------------------------------------
    # INTER-SHEET WIRING & EXTERNAL INTERFACE LABELS
    # -------------------------------------------------------------------------
    # 1. VBUS_MUX: Sheet 1 Pin -> Sheet 2 Pin
    content += bp.wire(s1_vbus_mux[0], s1_vbus_mux[1], s2_vbus_mux[0], s2_vbus_mux[1])
    content += bp.global_lbl("VBUS_MUX", 78.74, 60.96, 0, "bidirectional")

    # 2. SYS: Sheet 2 Pin -> Sheet 3 Pin
    content += bp.wire(s2_sys[0], s2_sys[1], s3_sys[0], s3_sys[1])
    content += bp.global_lbl("SYS", 152.40, 55.88, 0, "bidirectional")

    # 3. 5V_SYS: Sheet 3 Pin -> drops down to Sheet 4 Pin
    content += bp.wire(s3_5v_sys[0], s3_5v_sys[1], 233.68, s3_5v_sys[1])
    content += bp.wire(233.68, s3_5v_sys[1], 233.68, 121.92)
    content += bp.wire(233.68, 121.92, 88.90, 121.92)
    content += bp.wire(88.90, 121.92, 88.90, s4_5v_sys[1])
    content += bp.wire(88.90, s4_5v_sys[1], s4_5v_sys[0], s4_5v_sys[1])
    content += bp.global_lbl("5V_SYS", 233.68, 55.88, 0, "bidirectional")

    # 4. 3V3_SYS: Sheet 3 Pin -> drops down to Sheet 4 Pin
    content += bp.wire(s3_3v3_sys[0], s3_3v3_sys[1], 228.60, s3_3v3_sys[1])
    content += bp.wire(228.60, s3_3v3_sys[1], 228.60, 124.46)
    content += bp.wire(228.60, 124.46, 91.44, 124.46)
    content += bp.wire(91.44, 124.46, 91.44, s4_3v3_sys[1])
    content += bp.wire(91.44, s4_3v3_sys[1], s4_3v3_sys[0], s4_3v3_sys[1])
    content += bp.global_lbl("3V3_SYS", 228.60, 66.04, 0, "bidirectional")

    # 5. VBAT: Sheet 2 Pin -> drops down to Sheet 4 Pin
    content += bp.wire(s2_vbat[0], s2_vbat[1], 149.86, s2_vbat[1])
    content += bp.wire(149.86, s2_vbat[1], 149.86, 116.84)
    content += bp.wire(149.86, 116.84, 93.98, 116.84)
    content += bp.wire(93.98, 116.84, 93.98, s4_vbat[1])
    content += bp.wire(93.98, s4_vbat[1], s4_vbat[0], s4_vbat[1])
    content += bp.global_lbl("VBAT", 149.86, 66.04, 0, "bidirectional")

    # 6. ADC_VBAT_SENSE: Sheet 2 Pin -> Interface Label (GPIO1)
    content += bp.wire(s2_adc_vbat[0], s2_adc_vbat[1], 157.48, s2_adc_vbat[1])
    content += bp.global_lbl("ADC_VBAT_SENSE", 157.48, s2_adc_vbat[1], 0, "output")

    # 7. CHG_STAT: Sheet 2 Pin -> Interface Label
    content += bp.wire(s2_chg_stat[0], s2_chg_stat[1], 157.48, s2_chg_stat[1])
    content += bp.global_lbl("CHG_STAT", 157.48, s2_chg_stat[1], 0, "output")

    # 8. CHG_INT: Sheet 2 Pin -> Interface Label
    content += bp.wire(s2_chg_int[0], s2_chg_int[1], 157.48, s2_chg_int[1])
    content += bp.global_lbl("CHG_INT", 157.48, s2_chg_int[1], 0, "output")

    # 9. SIM_PWR: Sheet 4 Pin -> Interface Label (A7682S)
    content += bp.wire(s4_sim_pwr[0], s4_sim_pwr[1], 177.80, s4_sim_pwr[1])
    content += bp.global_lbl("SIM_PWR", 177.80, s4_sim_pwr[1], 0, "output")

    # Common System Return handled by sub-sheets

    # Sheet ending
    content += ")\n"
    
    with open("AIOT_BLACKBOX_POWER_SUPPLY.kicad_sch", "w", encoding="utf-8") as f:
        f.write(content)
    print("Root Sheet successfully generated: AIOT_BLACKBOX_POWER_SUPPLY.kicad_sch")

if __name__ == "__main__":
    build_root_sheet()
