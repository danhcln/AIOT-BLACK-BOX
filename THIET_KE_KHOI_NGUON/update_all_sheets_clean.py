import re
import subprocess

# 1. Update gen_sheet2.py
with open("gen_sheet2.py", "r", encoding="utf-8") as f:
    s2 = f.read()

s2 = s2.replace('content += bp.hier_lbl("VBAT", 287.02, 96.52 + 5.08, 0, "output")',
                'content += bp.hier_lbl("VBAT", 287.02, 96.52, 0, "output")')
s2 = s2.replace('content += bp.hier_lbl("ADC_VBAT_SENSE", 124.46, tp_adc_p1[1] + 5.08, 0, "output")',
                'content += bp.hier_lbl("ADC_VBAT_SENSE", 124.46, tp_adc_p1[1], 0, "output")')
s2 = s2.replace('content += bp.hier_lbl("VBUS_MUX", 152.40, 71.12 + 5.08, 180, "input")',
                'content += bp.hier_lbl("VBUS_MUX", 152.40, 71.12, 180, "input")')
s2 = s2.replace('content += bp.hier_lbl("SYS", 269.24, 88.90 + 3.81, 0, "output")',
                'content += bp.hier_lbl("SYS", 269.24, 88.90, 0, "output")')
s2 = s2.replace('content += bp.hier_lbl("CHG_STAT", 226.06, u2_p4[1] + 2.54, 180, "output")',
                'content += bp.hier_lbl("CHG_STAT", 226.06, u2_p4[1], 180, "output")')
s2 = s2.replace('content += bp.hier_lbl("CHG_INT", 226.06, 109.22 + 2.54, 180, "output")',
                'content += bp.hier_lbl("CHG_INT", 226.06, 109.22, 180, "output")')

with open("gen_sheet2.py", "w", encoding="utf-8") as f:
    f.write(s2)
print("Updated gen_sheet2.py")

# 2. Update gen_sheet3.py
with open("gen_sheet3.py", "r", encoding="utf-8") as f:
    s3 = f.read()

s3 = s3.replace('content += bp.hier_lbl("SYS", 25.40, 77.47 + 5.08, 180, "input")',
                'content += bp.hier_lbl("SYS", 25.40, 77.47, 180, "input")')
s3 = s3.replace('content += bp.hier_lbl("5V_SYS", 175.26, 62.23, 90, "output")',
                'content += bp.hier_lbl("5V_SYS", 175.26, 69.85, 90, "output")')
s3 = s3.replace('content += bp.hier_lbl("3V3_SYS", 276.86, 92.71 + 5.08, 0, "output")',
                'content += bp.hier_lbl("3V3_SYS", 276.86, 92.71, 0, "output")')

with open("gen_sheet3.py", "w", encoding="utf-8") as f:
    f.write(s3)
print("Updated gen_sheet3.py")

# 3. Update gen_sheet4.py
with open("gen_sheet4.py", "r", encoding="utf-8") as f:
    s4 = f.read()

s4 = s4.replace('content += bp.hier_lbl("5V_SYS", 25.40, 50.80 + 5.08, 180, "input")',
                'content += bp.hier_lbl("5V_SYS", 25.40, 50.80, 180, "input")')
s4 = s4.replace('content += bp.hier_lbl("SIM_PWR", 208.28, 57.15, 90, "output")',
                'content += bp.hier_lbl("SIM_PWR", 208.28, 64.77, 90, "output")')
s4 = s4.replace('content += bp.hier_lbl("3V3_SYS", 231.14, 132.08 + 2.54, 180, "input")',
                'content += bp.hier_lbl("3V3_SYS", 231.14, 132.08, 180, "input")')
s4 = s4.replace('content += bp.hier_lbl("VBAT", 231.14, 137.16 + 2.54, 180, "input")',
                'content += bp.hier_lbl("VBAT", 231.14, 137.16, 180, "input")')

with open("gen_sheet4.py", "w", encoding="utf-8") as f:
    f.write(s4)
print("Updated gen_sheet4.py")

# 4. Update gen_root.py (remove duplicate #FLG01)
with open("gen_root.py", "r", encoding="utf-8") as f:
    root = f.read()

flg_block = '''    # Common System Return & PWR_FLAG
    content += bp.gnd_sym(30.48, 101.60)
    content += bp.wire(30.48, 101.60, 30.48, 96.52)
    content += bp.sym_inst("power:PWR_FLAG", "#FLG01", "PWR_FLAG", 30.48, 96.52, 0,
                           "", "", "Global GND Power Flag", pins=["1"])'''

root = root.replace(flg_block, '    # Common System Return handled by sub-sheets')

with open("gen_root.py", "w", encoding="utf-8") as f:
    f.write(root)
print("Updated gen_root.py")

# Now regenerate all sheets
subprocess.run(["python", "fix_hier_s1.py"], check=True)
subprocess.run(["python", "gen_sheet2.py"], check=True)
subprocess.run(["python", "gen_sheet3.py"], check=True)
subprocess.run(["python", "gen_sheet4.py"], check=True)
subprocess.run(["python", "gen_root.py"], check=True)
print("All sheets successfully regenerated!")
