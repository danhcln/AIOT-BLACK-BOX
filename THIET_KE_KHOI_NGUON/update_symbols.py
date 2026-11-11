# -*- coding: utf-8 -*-
"""
Update custom_symbols_def.py to ensure 100% planar, non-crossing pin arrangements
for BQ25895, DW01A, and FS8205A.
"""
import re

with open("custom_symbols_def.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update DW01A
new_dw01a = """SYM_DW01A = \"\"\"\\t\\t(symbol "Battery_Management:DW01A"
\\t\\t\\t(pin_names (offset 1.016))
\\t\\t\\t(exclude_from_sim no)
\\t\\t\\t(in_bom yes)
\\t\\t\\t(on_board yes)
\\t\\t\\t(property "Reference" "U" (at 0 12.7 0) (effects (font (size 1.27 1.27))))
\\t\\t\\t(property "Value" "DW01A" (at 0 -12.7 0) (effects (font (size 1.27 1.27))))
\\t\\t\\t(property "Footprint" "Package_TO_SOT_SMD:SOT-23-6" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\\t\\t\\t(property "Datasheet" "https://datasheet.lcsc.com/lcsc/1811151441_Fortune-Semicon-DW01A-G_C24339.pdf" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\\t\\t\\t(property "Description" "Single Cell Lithium-Ion/Polymer Battery Protection IC, SOT-23-6" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\\t\\t\\t(symbol "DW01A_0_1"
\\t\\t\\t\\t(rectangle (start -10.16 10.16) (end 10.16 -10.16) (stroke (width 0.254) (type solid)) (fill (type background)))
\\t\\t\\t)
\\t\\t\\t(symbol "DW01A_1_1"
\\t\\t\\t\\t(pin passive line (at -12.7 5.08 0) (length 2.54) (name "VCC" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin input line (at -12.7 0.0 0) (length 2.54) (name "CS" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin passive line (at -12.7 -2.54 0) (length 2.54) (name "TD" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin passive line (at -12.7 -5.08 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin output line (at 12.7 5.08 180) (length 2.54) (name "OD" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin output line (at 12.7 -5.08 180) (length 2.54) (name "OC" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\\t\\t\\t)
\\t\\t)\"\"\""""

# 2. Update FS8205A
new_fs8205a = """SYM_FS8205A = \"\"\"\\t\\t(symbol "Transistor_FET:FS8205A"
\\t\\t\\t(pin_names (offset 1.016))
\\t\\t\\t(exclude_from_sim no)
\\t\\t\\t(in_bom yes)
\\t\\t\\t(on_board yes)
\\t\\t\\t(property "Reference" "Q" (at 0 12.7 0) (effects (font (size 1.27 1.27))))
\\t\\t\\t(property "Value" "FS8205A" (at 0 -12.7 0) (effects (font (size 1.27 1.27))))
\\t\\t\\t(property "Footprint" "Package_SO:TSSOP-8_4.4x3mm_P0.65mm" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\\t\\t\\t(property "Datasheet" "https://datasheet.lcsc.com/lcsc/1811151441_Fortune-Semicon-FS8205A_C32254.pdf" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\\t\\t\\t(property "Description" "Dual N-Channel Enhancement Mode Power MOSFET, 20V 6A, TSSOP-8" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\\t\\t\\t(symbol "FS8205A_0_1"
\\t\\t\\t\\t(rectangle (start -10.16 10.16) (end 10.16 -10.16) (stroke (width 0.254) (type solid)) (fill (type background)))
\\t\\t\\t)
\\t\\t\\t(symbol "FS8205A_1_1"
\\t\\t\\t\\t(pin input line (at -12.7 5.08 0) (length 2.54) (name "G1" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin input line (at -12.7 -5.08 0) (length 2.54) (name "G2" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin passive line (at 12.7 7.62 180) (length 2.54) (name "S1" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin passive line (at 12.7 5.08 180) (length 2.54) (name "S1" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin passive line (at 12.7 2.54 180) (length 2.54) (name "D1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin passive line (at 12.7 0.0 180) (length 2.54) (name "D2" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin passive line (at 12.7 -5.08 180) (length 2.54) (name "S2" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin passive line (at 12.7 -7.62 180) (length 2.54) (name "S2" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
\\t\\t\\t)
\\t\\t)\"\"\""""

# 3. Update BQ25895 with SW/BTST on top, SYS in middle, BAT below, Logic at bottom
new_bq25895 = """SYM_BQ25895 = \"\"\"\\t\\t(symbol "Battery_Management:BQ25895RTWR"
\\t\\t\\t(pin_names (offset 1.016))
\\t\\t\\t(exclude_from_sim no)
\\t\\t\\t(in_bom yes)
\\t\\t\\t(on_board yes)
\\t\\t\\t(property "Reference" "U" (at 0 25.4 0) (effects (font (size 1.27 1.27))))
\\t\\t\\t(property "Value" "BQ25895RTWR" (at 0 -25.4 0) (effects (font (size 1.27 1.27))))
\\t\\t\\t(property "Footprint" "Package_DFN_QFN:Texas_RTW0024A" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\\t\\t\\t(property "Datasheet" "https://www.ti.com/lit/ds/symlink/bq25895.pdf" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\\t\\t\\t(property "Description" "I2C Controlled Single-Cell 5A Fast Charger with NVDC Power Path Management, WQFN-24" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\\t\\t\\t(symbol "BQ25895RTWR_0_1"
\\t\\t\\t\\t(rectangle (start -15.24 22.86) (end 15.24 -22.86) (stroke (width 0.254) (type solid)) (fill (type background)))
\\t\\t\\t)
\\t\\t\\t(symbol "BQ25895RTWR_1_1"
\\t\\t\\t\\t(pin power_in line (at -17.78 17.78 0) (length 2.54) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin power_out line (at -17.78 15.24 0) (length 2.54) (name "PMID" (effects (font (size 1.27 1.27)))) (number "23" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin power_out line (at -17.78 12.7 0) (length 2.54) (name "REGN" (effects (font (size 1.27 1.27)))) (number "22" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin input line (at -17.78 7.62 0) (length 2.54) (name "~CE" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin input line (at -17.78 5.08 0) (length 2.54) (name "OTG" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin input line (at -17.78 2.54 0) (length 2.54) (name "QON" (effects (font (size 1.27 1.27)))) (number "12" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin passive line (at -17.78 0.0 0) (length 2.54) (name "ILIM" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin input line (at -17.78 -2.54 0) (length 2.54) (name "TS" (effects (font (size 1.27 1.27)))) (number "11" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin input line (at -17.78 -5.08 0) (length 2.54) (name "DSEL" (effects (font (size 1.27 1.27)))) (number "24" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin bidirectional line (at -17.78 -7.62 0) (length 2.54) (name "D+" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin bidirectional line (at -17.78 -10.16 0) (length 2.54) (name "D-" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin power_in line (at -17.78 -17.78 0) (length 2.54) (name "PGND" (effects (font (size 1.27 1.27)))) (number "17" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin passive line (at -17.78 -20.32 0) (length 2.54) (name "PGND" (effects (font (size 1.27 1.27)))) (number "18" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin power_out line (at 17.78 17.78 180) (length 2.54) (name "SW" (effects (font (size 1.27 1.27)))) (number "19" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin passive line (at 17.78 15.24 180) (length 2.54) (name "SW" (effects (font (size 1.27 1.27)))) (number "20" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin passive line (at 17.78 12.7 180) (length 2.54) (name "BTST" (effects (font (size 1.27 1.27)))) (number "21" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin power_out line (at 17.78 7.62 180) (length 2.54) (name "SYS" (effects (font (size 1.27 1.27)))) (number "15" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin passive line (at 17.78 5.08 180) (length 2.54) (name "SYS" (effects (font (size 1.27 1.27)))) (number "16" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin power_out line (at 17.78 0.0 180) (length 2.54) (name "BAT" (effects (font (size 1.27 1.27)))) (number "13" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin passive line (at 17.78 -2.54 180) (length 2.54) (name "BAT" (effects (font (size 1.27 1.27)))) (number "14" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin open_collector line (at 17.78 -7.62 180) (length 2.54) (name "STAT" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin open_collector line (at 17.78 -10.16 180) (length 2.54) (name "~INT" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin bidirectional line (at 17.78 -12.7 180) (length 2.54) (name "SCL" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin bidirectional line (at 17.78 -15.24 180) (length 2.54) (name "SDA" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin passive line (at 0 -22.86 90) (length 2.54) (name "EP" (effects (font (size 1.27 1.27)))) (number "25" (effects (font (size 1.27 1.27)))))
\\t\\t\\t)
\\t\\t)\"\"\""""

text = re.sub(r'SYM_DW01A\s*=\s*""".*?"""', new_dw01a, text, flags=re.DOTALL)
text = re.sub(r'SYM_FS8205A\s*=\s*""".*?"""', new_fs8205a, text, flags=re.DOTALL)
text = re.sub(r'SYM_BQ25895\s*=\s*""".*?"""', new_bq25895, text, flags=re.DOTALL)

with open("custom_symbols_def.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Symbols updated successfully with planar pinouts.")
