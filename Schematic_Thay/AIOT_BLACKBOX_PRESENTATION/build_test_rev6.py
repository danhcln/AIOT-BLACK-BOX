import os, re, sys, uuid

sys.stdout.reconfigure(encoding='utf-8')

# Ensure scratch_rev6 directory exists
os.makedirs('scratch_rev6', exist_ok=True)

# Read the approved baseline schematic (AIOT_BLACKBOX_PRESENTATION.kicad_sch)
with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    sch_text = f.read()

# -------------------------------------------------------------
# 1. DEFINE NEW COMPLETE ESP32-S3 SYMBOL (44 PINS)
# -------------------------------------------------------------

# Left pins: (name, number, type, y_offset)
left_pins = [
    ('5V',     '21', 'power_in',      25.40),
    ('3V3',    '2',  'power_out',     22.86),
    ('3V3',    '1',  'power_out',     20.32),
    ('RST',    '3',  'input',         17.78),
    ('GPIO1',  '26', 'input',         15.24),
    ('GPIO2',  '27', 'bidirectional', 12.70),
    ('GPIO8',  '12', 'bidirectional', 10.16),
    ('GPIO3',  '13', 'bidirectional',  7.62),
    ('GPIO9',  '15', 'bidirectional',  5.08),
    ('GPIO46', '14', 'bidirectional',  2.54),
    ('GPIO10', '16', 'input',          0.00),
    ('GPIO16', '9',  'bidirectional', -2.54),
    ('GPIO14', '20', 'output',        -5.08),
    ('GPIO35', '35', 'bidirectional', -7.62),
    ('GPIO11', '17', 'output',       -10.16),
    ('GPIO36', '34', 'bidirectional', -12.70),
    ('GPIO12', '18', 'output',       -15.24),
    ('GPIO37', '33', 'bidirectional', -17.78),
    ('GPIO13', '19', 'input',        -20.32),
    ('GPIO38', '32', 'bidirectional', -22.86),
    ('GND',    '22', 'power_in',     -25.40),
    ('GND',    '43', 'power_in',     -27.94),
]

# Right pins: (name, number, type, y_offset)
right_pins = [
    ('GPIO43', '24', 'output',        25.40),
    ('GPIO42', '28', 'bidirectional', 22.86),
    ('GPIO44', '25', 'input',         20.32),
    ('GPIO41', '29', 'bidirectional', 17.78),
    ('GPIO4',  '4',  'output',        15.24),
    ('GPIO40', '30', 'bidirectional', 12.70),
    ('GPIO5',  '5',  'input',         10.16),
    ('GPIO39', '31', 'bidirectional',  7.62),
    ('GPIO17', '10', 'output',         5.08),
    ('GPIO19', '42', 'bidirectional',  2.54),
    ('GPIO18', '11', 'input',          0.00),
    ('GPIO20', '41', 'bidirectional', -2.54),
    ('GPIO21', '40', 'input',         -5.08),
    ('GPIO0',  '36', 'bidirectional', -7.62),
    ('GPIO6',  '6',  'input',        -10.16),
    ('GPIO45', '37', 'bidirectional', -12.70),
    ('GPIO7',  '7',  'output',       -15.24),
    ('GPIO47', '39', 'bidirectional', -17.78),
    ('GPIO15', '8',  'output',       -20.32),
    ('GPIO48', '38', 'bidirectional', -22.86),
    ('GND',    '23', 'power_in',     -25.40),
    ('GND',    '44', 'power_in',     -27.94),
]

esp32_pins_sexpr = []
for name, num, ptype, y in left_pins:
    esp32_pins_sexpr.append(f"""\t\t\t\t(pin {ptype} line
\t\t\t\t\t(at -22.86 {y:.2f} 0)
\t\t\t\t\t(length 5.08)
\t\t\t\t\t(name "{name}"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t\t(number "{num}"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.016 1.016)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t)""")

for name, num, ptype, y in right_pins:
    esp32_pins_sexpr.append(f"""\t\t\t\t(pin {ptype} line
\t\t\t\t\t(at 22.86 {y:.2f} 180)
\t\t\t\t\t(length 5.08)
\t\t\t\t\t(name "{name}"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t\t(number "{num}"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.016 1.016)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t)""")

new_esp32_lib_symbol = f"""\t\t(symbol "Presentation:ESP32-S3-DevKitC-1"
\t\t\t(pin_names
\t\t\t\t(offset 1.016)
\t\t\t)
\t\t\t(exclude_from_sim no)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
\t\t\t(in_pos_files yes)
\t\t\t(duplicate_pin_numbers_are_jumpers no)
\t\t\t(property "Reference" "U1"
\t\t\t\t(at 0 32.0 0)
\t\t\t\t(show_name no)
\t\t\t\t(do_not_autoplace no)
\t\t\t\t(effects
\t\t\t\t\t(font
\t\t\t\t\t\t(size 1.778 1.778)
\t\t\t\t\t\t(bold yes)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t\t(property "Value" "ESP32-S3"
\t\t\t\t(at 0 29.5 0)
\t\t\t\t(show_name no)
\t\t\t\t(do_not_autoplace no)
\t\t\t\t(hide yes)
\t\t\t\t(effects
\t\t\t\t\t(font
\t\t\t\t\t\t(size 1.524 1.524)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t\t(property "Footprint" ""
\t\t\t\t(at 0 0 0)
\t\t\t\t(show_name no)
\t\t\t\t(do_not_autoplace no)
\t\t\t\t(hide yes)
\t\t\t\t(effects
\t\t\t\t\t(font
\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t\t(property "Datasheet" ""
\t\t\t\t(at 0 0 0)
\t\t\t\t(show_name no)
\t\t\t\t(do_not_autoplace no)
\t\t\t\t(hide yes)
\t\t\t\t(effects
\t\t\t\t\t(font
\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t\t(property "Description" "ESP32-S3 N16R8 Central Processing Unit"
\t\t\t\t(at 0 0 0)
\t\t\t\t(show_name no)
\t\t\t\t(do_not_autoplace no)
\t\t\t\t(hide yes)
\t\t\t\t(effects
\t\t\t\t\t(font
\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t\t(symbol "ESP32-S3-DevKitC-1_0_1"
\t\t\t\t(rectangle
\t\t\t\t\t(start -17.78 28.50)
\t\t\t\t\t(end 17.78 -30.48)
\t\t\t\t\t(stroke
\t\t\t\t\t\t(width 0.381)
\t\t\t\t\t\t(type default)
\t\t\t\t\t)
\t\t\t\t\t(fill
\t\t\t\t\t\t(type background)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t\t(text "ESP32-S3"
\t\t\t\t\t(at 0 3.81 0)
\t\t\t\t\t(effects
\t\t\t\t\t\t(font
\t\t\t\t\t\t\t(size 2.2 2.2)
\t\t\t\t\t\t\t(bold yes)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t\t(text "DevKitC-1 N16R8"
\t\t\t\t\t(at 0 -2.54 0)
\t\t\t\t\t(effects
\t\t\t\t\t\t(font
\t\t\t\t\t\t\t(size 1.4 1.4)
\t\t\t\t\t\t\t(bold yes)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t\t(symbol "ESP32-S3-DevKitC-1_1_1"
{chr(10).join(esp32_pins_sexpr)}
\t\t\t)
\t\t\t(embedded_fonts no)
\t\t)"""

# Replace ESP32 lib_symbol in sch_text
pattern_esp = r'\t\t\(symbol "Presentation:ESP32-S3-DevKitC-1"[\s\S]*?\n\t\t\)'
sch_text, count_esp = re.subn(pattern_esp, new_esp32_lib_symbol, sch_text, count=1)
print(f"Replaced ESP32 lib_symbol: {count_esp} match")

# Update U1 symbol instance pins in sch_text
# In symbol instance U1, we have (pin "X" (uuid "..."))
# Let's replace the pins section of U1 instance
new_u1_pins_instance = []
for i in range(1, 45):
    p_uuid = str(uuid.uuid4())
    new_u1_pins_instance.append(f'\t\t(pin "{i}"\n\t\t\t(uuid "{p_uuid}")\n\t\t)')

# Find U1 instance
m_inst = re.search(r'\(symbol\s+\(lib_id "Presentation:ESP32-S3-DevKitC-1"\)[\s\S]*?\(property "Reference" "U1"[\s\S]*?\n\t\)', sch_text)
if m_inst:
    old_u1_inst = m_inst.group(0)
    # replace the pins block
    old_pins_match = re.search(r'(\t\t\(pin "1"[\s\S]*?\(pin "22"[\s\S]*?\)\n\t\t\))', old_u1_inst)
    if old_pins_match:
        new_u1_inst = old_u1_inst.replace(old_pins_match.group(1), "\n".join(new_u1_pins_instance))
        sch_text = sch_text.replace(old_u1_inst, new_u1_inst)
        print("Updated U1 symbol instance pins (44 pins)")

# -------------------------------------------------------------
# 2. DEFINE EXPANDED GY-521 MPU6050 SYMBOL (8 PINS)
# -------------------------------------------------------------

new_mpu6050_lib_symbol = """\t\t(symbol "Presentation:MPU6050_Module"
\t\t\t(pin_names
\t\t\t\t(offset 1.016)
\t\t\t)
\t\t\t(exclude_from_sim no)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
\t\t\t(in_pos_files yes)
\t\t\t(duplicate_pin_numbers_are_jumpers no)
\t\t\t(property "Reference" "U2"
\t\t\t\t(at 0 16.51 0)
\t\t\t\t(show_name no)
\t\t\t\t(do_not_autoplace no)
\t\t\t\t(effects
\t\t\t\t\t(font
\t\t\t\t\t\t(size 1.524 1.524)
\t\t\t\t\t\t(bold yes)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t\t(property "Value" "MPU6050"
\t\t\t\t(at 0 14 0)
\t\t\t\t(show_name no)
\t\t\t\t(do_not_autoplace no)
\t\t\t\t(hide yes)
\t\t\t\t(effects
\t\t\t\t\t(font
\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t\t(property "Footprint" ""
\t\t\t\t(at 0 0 0)
\t\t\t\t(show_name no)
\t\t\t\t(do_not_autoplace no)
\t\t\t\t(hide yes)
\t\t\t\t(effects
\t\t\t\t\t(font
\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t\t(property "Datasheet" ""
\t\t\t\t(at 0 0 0)
\t\t\t\t(show_name no)
\t\t\t\t(do_not_autoplace no)
\t\t\t\t(hide yes)
\t\t\t\t(effects
\t\t\t\t\t(font
\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t\t(property "Description" "6-Axis IMU Module"
\t\t\t\t(at 0 0 0)
\t\t\t\t(show_name no)
\t\t\t\t(do_not_autoplace no)
\t\t\t\t(hide yes)
\t\t\t\t(effects
\t\t\t\t\t(font
\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t\t(symbol "MPU6050_Module_0_1"
\t\t\t\t(rectangle
\t\t\t\t\t(start -15.24 14)
\t\t\t\t\t(end 15.24 -16.51)
\t\t\t\t\t(stroke
\t\t\t\t\t\t(width 0.381)
\t\t\t\t\t\t(type default)
\t\t\t\t\t)
\t\t\t\t\t(fill
\t\t\t\t\t\t(type background)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t\t(text "MPU6050"
\t\t\t\t\t(at 0 0 0)
\t\t\t\t\t(effects
\t\t\t\t\t\t(font
\t\t\t\t\t\t\t(size 2 2)
\t\t\t\t\t\t\t(bold yes)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t\t(symbol "MPU6050_Module_1_1"
\t\t\t\t(pin power_in line
\t\t\t\t\t(at -19.05 10.16 0)
\t\t\t\t\t(length 3.81)
\t\t\t\t\t(name "VCC"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t\t(number "1"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.016 1.016)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t\t(pin input line
\t\t\t\t\t(at -19.05 5.08 0)
\t\t\t\t\t(length 3.81)
\t\t\t\t\t(name "AD0"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t\t(number "7"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.016 1.016)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t\t(pin bidirectional line
\t\t\t\t\t(at -19.05 0 0)
\t\t\t\t\t(length 3.81)
\t\t\t\t\t(name "XDA"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t\t(number "5"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.016 1.016)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t\t(pin output line
\t\t\t\t\t(at -19.05 -5.08 0)
\t\t\t\t\t(length 3.81)
\t\t\t\t\t(name "XCL"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t\t(number "6"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.016 1.016)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t\t(pin bidirectional line
\t\t\t\t\t(at 19.05 5.08 180)
\t\t\t\t\t(length 3.81)
\t\t\t\t\t(name "SDA"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t\t(number "4"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.016 1.016)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t\t(pin input line
\t\t\t\t\t(at 19.05 0 180)
\t\t\t\t\t(length 3.81)
\t\t\t\t\t(name "SCL"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t\t(number "3"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.016 1.016)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t\t(pin output line
\t\t\t\t\t(at 19.05 -5.08 180)
\t\t\t\t\t(length 3.81)
\t\t\t\t\t(name "INT"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t\t(number "8"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.016 1.016)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t\t(pin power_in line
\t\t\t\t\t(at 19.05 -12.7 180)
\t\t\t\t\t(length 3.81)
\t\t\t\t\t(name "GND"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t\t(number "2"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.016 1.016)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t\t(embedded_fonts no)
\t\t)"""

# Replace MPU6050 lib_symbol
pattern_mpu = r'\t\t\(symbol "Presentation:MPU6050_Module"[\s\S]*?\n\t\t\)'
sch_text, count_mpu = re.subn(pattern_mpu, new_mpu6050_lib_symbol, sch_text, count=1)
print(f"Replaced MPU6050 lib_symbol: {count_mpu} match")

# Update U2 symbol instance pins
m_u2 = re.search(r'\(symbol\s+\(lib_id "Presentation:MPU6050_Module"\)[\s\S]*?\(property "Reference" "U2"[\s\S]*?\n\t\)', sch_text)
if m_u2:
    old_u2_inst = m_u2.group(0)
    old_pins_match = re.search(r'(\t\t\(pin "1"[\s\S]*?\(pin "6"[\s\S]*?\)\n\t\t\))', old_u2_inst)
    if old_pins_match:
        new_u2_pins = [f'\t\t(pin "{p}"\n\t\t\t(uuid "{str(uuid.uuid4())}")\n\t\t)' for p in [1, 2, 3, 4, 5, 6, 7, 8]]
        new_u2_inst = old_u2_inst.replace(old_pins_match.group(1), "\n".join(new_u2_pins))
        sch_text = sch_text.replace(old_u2_inst, new_u2_inst)
        print("Updated U2 symbol instance pins (8 pins)")

# -------------------------------------------------------------
# 3. ADD NO-CONNECT MARKERS FOR UNUSED PINS
# -------------------------------------------------------------
# Unused ESP32 Left pins (at x = 129.54):
# y = 76.20, 81.28, 86.36, 91.44, 96.52, 101.60, 106.68, 111.76, 116.84, 121.92, 127.00
# Unused ESP32 Right pins (at x = 175.26):
# y = 76.20, 81.28, 86.36, 91.44, 96.52, 101.60, 106.68, 111.76, 116.84, 121.92, 127.00
# Unused MPU6050 pins:
# XDA at (34.29, 93.98), XCL at (34.29, 99.06)

nc_points = []
for y in [76.20, 81.28, 86.36, 91.44, 96.52, 101.60, 106.68, 111.76, 116.84, 121.92, 127.00]:
    nc_points.append((129.54, y))
    nc_points.append((175.26, y))

# Add MPU6050 XDA and XCL
nc_points.append((34.29, 93.98))
nc_points.append((34.29, 99.06))

nc_sexprs = []
for x, y in nc_points:
    nc_sexprs.append(f'\t(no_connect (at {x:.2f} {y:.2f}) (uuid "{str(uuid.uuid4())}"))')

# Insert no_connect markers before the closing parenthesis of the schematic
# Find last closing parenthesis
idx_end = sch_text.rfind(')')
sch_text = sch_text[:idx_end] + "\n" + "\n".join(nc_sexprs) + "\n)\n"
print(f"Added {len(nc_points)} KiCad no_connect markers")

# Write out test schematic in scratch_rev6
out_sch = os.path.join('scratch_rev6', 'AIOT_BLACKBOX_PRESENTATION.kicad_sch')
with open(out_sch, 'w', encoding='utf-8') as f:
    f.write(sch_text)
print(f"Saved test schematic: {out_sch} ({len(sch_text)} bytes)")
