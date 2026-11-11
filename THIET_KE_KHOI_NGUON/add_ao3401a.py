with open('custom_symbols_def.py', 'r', encoding='utf-8') as f:
    text = f.read()

sym_ao3401a = '''
SYM_AO3401A = """\\t\\t(symbol "Transistor_FET:AO3401A"
\\t\\t\\t(pin_names (offset 1.016))
\\t\\t\\t(exclude_from_sim no)
\\t\\t\\t(in_bom yes)
\\t\\t\\t(on_board yes)
\\t\\t\\t(property "Reference" "Q" (at 0 7.62 0) (effects (font (size 1.27 1.27))))
\\t\\t\\t(property "Value" "AO3401A" (at 0 -7.62 0) (effects (font (size 1.27 1.27))))
\\t\\t\\t(property "Footprint" "Package_TO_SOT_SMD:SOT-23" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\\t\\t\\t(property "Datasheet" "http://www.aosmd.com/pdfs/datasheet/AO3401A.pdf" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\\t\\t\\t(property "Description" "-4.0A Id, -30V Vds, P-Channel MOSFET, SOT-23" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\\t\\t\\t(symbol "AO3401A_0_1"
\\t\\t\\t\\t(rectangle (start -5.08 5.08) (end 5.08 -5.08) (stroke (width 0.254) (type solid)) (fill (type background)))
\\t\\t\\t)
\\t\\t\\t(symbol "AO3401A_1_1"
\\t\\t\\t\\t(pin passive line (at -7.62 0 0) (length 2.54) (name "S" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin passive line (at 7.62 0 180) (length 2.54) (name "D" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\\t\\t\\t\\t(pin input line (at 0 -7.62 90) (length 2.54) (name "G" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\\t\\t\\t)
\\t\\t)"""
'''

if 'SYM_AO3401A' not in text:
    text += sym_ao3401a
    with open('custom_symbols_def.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Appended SYM_AO3401A to custom_symbols_def.py.")
else:
    print("SYM_AO3401A already present.")

# Also update ALL_LIB_SYMBOLS in build_complete_power_project.py
with open('build_complete_power_project.py', 'r', encoding='utf-8') as f:
    bp_text = f.read()

if 'cust_syms.SYM_AO3401A' not in bp_text:
    bp_text = bp_text.replace('{cust_syms.SYM_USB_C_16P}', '{cust_syms.SYM_USB_C_16P}\n{cust_syms.SYM_AO3401A}')
    with open('build_complete_power_project.py', 'w', encoding='utf-8') as f:
        f.write(bp_text)
    print("Added cust_syms.SYM_AO3401A to build_complete_power_project.py.")
else:
    print("cust_syms.SYM_AO3401A already present in build_complete_power_project.py.")
