with open('custom_symbols_def.py', 'r', encoding='utf-8') as f:
    text = f.read()

new_tps61088 = '''SYM_TPS61088 = """\\t\\t(symbol "Power_Management:TPS61088RHLR"
\\t\\t\\t(pin_names (offset 1.016))
\\t\\t\\t(exclude_from_sim no)
\\t\\t\\t(in_bom yes)
\\t\\t\\t(on_board yes)
\\t\\t\\t(property "Reference" "U" (at 0 22.86 0) (effects (font (size 1.27 1.27))))
\\t\\t\\t(property "Value" "TPS61088RHLR" (at 0 -22.86 0) (effects (font (size 1.27 1.27))))
\\t\\t\\t(property "Footprint" "Package_DFN_QFN:Texas_RHL0020A" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\\t\\t\\t(property "Datasheet" "https://www.ti.com/lit/ds/symlink/tps61088.pdf" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\\t\\t\\t(property "Description" "2.7V-12V, 10A Fully Integrated Synchronous Boost Converter, VQFN-20" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\\t\\t\\t(symbol "TPS61088RHLR_0_1"
\\t\\t\\t\\t(rectangle (start -12.7 20.32) (end 12.7 -20.32) (stroke (width 0.254) (type solid)) (fill (type background)))
\\t\\t\\t)
\\t\\t\\t(symbol "TPS61088RHLR_1_1"
\\t\\t\\t\\t(pin power_in line (at -15.24 17.78 0) (length 2.54) (name "VIN" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin power_out line (at -15.24 12.7 0) (length 2.54) (name "SW" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin passive line (at -15.24 10.16 0) (length 2.54) (name "SW" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin passive line (at -15.24 7.62 0) (length 2.54) (name "SW" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin passive line (at -15.24 5.08 0) (length 2.54) (name "SW" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin passive line (at -15.24 0.0 0) (length 2.54) (name "BOOT" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin input line (at -15.24 -2.54 0) (length 2.54) (name "EN" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin power_out line (at -15.24 -5.08 0) (length 2.54) (name "VCC" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin input line (at -15.24 -7.62 0) (length 2.54) (name "MODE" (effects (font (size 1.27 1.27)))) (number "13" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin input line (at -15.24 -10.16 0) (length 2.54) (name "FSW" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin passive line (at -15.24 -12.7 0) (length 2.54) (name "SS" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin passive line (at -15.24 -15.24 0) (length 2.54) (name "ILIM" (effects (font (size 1.27 1.27)))) (number "19" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin power_in line (at -15.24 -17.78 0) (length 2.54) (name "PGND" (effects (font (size 1.27 1.27)))) (number "20" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin power_out line (at 15.24 17.78 180) (length 2.54) (name "VOUT" (effects (font (size 1.27 1.27)))) (number "14" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin passive line (at 15.24 15.24 180) (length 2.54) (name "VOUT" (effects (font (size 1.27 1.27)))) (number "15" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin passive line (at 15.24 12.7 180) (length 2.54) (name "VOUT" (effects (font (size 1.27 1.27)))) (number "16" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin input line (at 15.24 2.54 180) (length 2.54) (name "FB" (effects (font (size 1.27 1.27)))) (number "17" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin output line (at 15.24 0.0 180) (length 2.54) (name "COMP" (effects (font (size 1.27 1.27)))) (number "18" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin no_connect line (at 15.24 -7.62 180) (length 2.54) (name "NC" (effects (font (size 1.27 1.27)))) (number "11" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin no_connect line (at 15.24 -10.16 180) (length 2.54) (name "NC" (effects (font (size 1.27 1.27)))) (number "12" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin power_in line (at 15.24 -17.78 180) (length 2.54) (name "EP/GND" (effects (font (size 1.27 1.27)))) (number "21" (effects (font (size 1.27 1.27)))))
\\t\\t\\t)
\\t\\t)"""'''

import re
pattern = r'SYM_TPS61088 = """.*?"""'
text = re.sub(pattern, new_tps61088, text, flags=re.DOTALL)

with open('custom_symbols_def.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated SYM_TPS61088 in custom_symbols_def.py successfully.")
