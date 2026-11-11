import uuid

def gen_uuid():
    return str(uuid.uuid4())

# Read official power symbols from power.kicad_sym
with open(r'D:\Kicad\share\kicad\symbols\power.kicad_sym', 'r', encoding='utf-8') as f:
    power_lib_text = f.read()

def get_sym(text, name):
    idx = text.find(f'(symbol "{name}"')
    if idx == -1:
        return None
    depth = 0
    for i in range(idx, len(text)):
        if text[i] == '(':
            depth += 1
        elif text[i] == ')':
            depth -= 1
            if depth == 0:
                return text[idx:i+1]
    return None

sym_3v3 = get_sym(power_lib_text, "+3V3").replace('(symbol "+3V3"', '(symbol "power:+3V3"')
sym_gnd = get_sym(power_lib_text, "GND").replace('(symbol "GND"', '(symbol "power:GND"')
sym_pwr_flag = get_sym(power_lib_text, "PWR_FLAG").replace('(symbol "PWR_FLAG"', '(symbol "power:PWR_FLAG"')

sch_uuid = "2e4b636b-9694-4f13-8d7e-a9635a1099e5"

# Let's place:
# U1 (ESP32-S3-TEST): center at (91.44, 101.60)
# Body: start (-17.78, 22.86), end (17.78, -22.86).
# Right edge is at 91.44 + 17.78 = 109.22.
# Pin length: 5.08 mm.
# Pins point 180 (pin line goes from (17.78, y) outward to (22.86, y)).
# So relative pin origin: (22.86, y, 180), length 5.08.
# Then connection point = (91.44 + 22.86, 101.60 - y) = (114.30, 101.60 - y).
# 114.30 / 2.54 = 45!
# Pin SDA (GPIO8): relative (22.86, 5.08, 180), length 5.08.
#   Connection point: (114.30, 96.52). (96.52 / 2.54 = 38).
# Pin SCL (GPIO9): relative (22.86, -5.08, 180), length 5.08.
#   Connection point: (114.30, 106.68). (106.68 / 2.54 = 42).

# U2 (IMU-TEST): center at (193.04, 101.60)
# (193.04 / 2.54 = 76).
# Body: start (-15.24, 20.32), end (15.24, -20.32).
# Left edge at 193.04 - 15.24 = 177.80.
# Pin length: 5.08.
# Left pins point 0 (pin line goes from (-15.24, y) outward to (-20.32, y)).
# Relative pin origin: (-20.32, y, 0), length 5.08.
# Connection point: (193.04 - 20.32, 101.60 - y) = (172.72, 101.60 - y).
# 172.72 / 2.54 = 68!
# Pin SDA: relative (-20.32, 5.08, 0), length 5.08.
#   Connection point: (172.72, 96.52).
# Pin SCL: relative (-20.32, -5.08, 0), length 5.08.
#   Connection point: (172.72, 106.68).

# IMU Power Pins:
# Top Pin VCC:
# Relative: (0, 25.40, 270), length 5.08.
# (starts at (0, 20.32) on top edge, extends up to (0, 25.40)).
# Connection point: (193.04, 101.60 - 25.40) = (193.04, 76.20). (76.20 / 2.54 = 30).
# Bottom Pin GND:
# Relative: (0, -25.40, 90), length 5.08.
# (starts at (0, -20.32) on bottom edge, extends down to (0, -25.40)).
# Connection point: (193.04, 101.60 - (-25.40)) = (193.04, 127.00). (127.00 / 2.54 = 50).

# Power symbol +3V3:
# Placed at (193.04, 66.04), pin at (0, 0, 90). Connection point: (193.04, 66.04).
# Wire from (193.04, 76.20) to (193.04, 66.04) (vertical, length 10.16 mm).
# PWR_FLAG placed at (205.74, 66.04). (205.74 / 2.54 = 81).
# Wire from (193.04, 66.04) to (205.74, 66.04) (horizontal, length 12.70 mm).
# Junction dot at (193.04, 66.04).

# Power symbol GND:
# Placed at (193.04, 137.16), pin at (0, 0, 270). Connection point: (193.04, 137.16).
# Wire from (193.04, 127.00) to (193.04, 137.16) (vertical, length 10.16 mm).
# PWR_FLAG placed at (205.74, 137.16).
# Wire from (193.04, 137.16) to (205.74, 137.16) (horizontal, length 12.70 mm).
# Junction dot at (193.04, 137.16).

# Signal Wires:
# SDA wire: (114.30, 96.52) -> (172.72, 96.52) (perfectly horizontal, length 58.42 mm).
# SCL wire: (114.30, 106.68) -> (172.72, 106.68) (perfectly horizontal, length 58.42 mm).

sch_content = f"""(kicad_sch
	(version 20260306)
	(generator "eeschema")
	(generator_version "10.0")
	(uuid "{sch_uuid}")
	(paper "A4")
	(title_block
		(title "AIOT BLACKBOX - SCHEMATIC CAPABILITY TEST")
		(date "2026-09-22")
		(rev "TEST-v0.1")
		(company "Project 2")
		(comment 1 "Simplified ESP32-S3 and 6-Axis IMU I2C Workflow Test")
	)
	(lib_symbols
		(symbol "ESP32-S3-TEST"
			(pin_names
				(offset 1.016)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(duplicate_pin_numbers_are_jumpers no)
			(property "Reference" "U"
				(at 0 26.67 0)
				(effects
					(font
						(size 1.524 1.524)
						(bold yes)
					)
				)
			)
			(property "Value" "ESP32-S3-TEST"
				(at 0 24.13 0)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Footprint" ""
				(at 0 0 0)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Datasheet" ""
				(at 0 0 0)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Description" "Simplified ESP32-S3 test symbol"
				(at 0 0 0)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(symbol "ESP32-S3-TEST_0_1"
				(rectangle
					(start -17.78 22.86)
					(end 17.78 -22.86)
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type background)
					)
				)
				(text "ESP32-S3"
					(at 0 0 0)
					(effects
						(font
							(size 2.54 2.54)
							(bold yes)
						)
					)
				)
				(text "(MCU)"
					(at 0 -3.81 0)
					(effects
						(font
							(size 1.524 1.524)
						)
					)
				)
			)
			(symbol "ESP32-S3-TEST_1_1"
				(pin bidirectional line
					(at 22.86 5.08 180)
					(length 5.08)
					(name "GPIO8 / SDA"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "8"
						(effects
							(font
								(size 1.016 1.016)
							)
						)
					)
				)
				(pin bidirectional line
					(at 22.86 -5.08 180)
					(length 5.08)
					(name "GPIO9 / SCL"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "9"
						(effects
							(font
								(size 1.016 1.016)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)
		(symbol "IMU-TEST"
			(pin_names
				(offset 1.016)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(duplicate_pin_numbers_are_jumpers no)
			(property "Reference" "U"
				(at 0 24.13 0)
				(effects
					(font
						(size 1.524 1.524)
						(bold yes)
					)
				)
			)
			(property "Value" "IMU-TEST"
				(at 0 21.59 0)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Footprint" ""
				(at 0 0 0)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Datasheet" ""
				(at 0 0 0)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Description" "Simplified 6-axis IMU test symbol"
				(at 0 0 0)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(symbol "IMU-TEST_0_1"
				(rectangle
					(start -15.24 20.32)
					(end 15.24 -20.32)
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type background)
					)
				)
				(text "6-AXIS IMU"
					(at 0 0 0)
					(effects
						(font
							(size 2.032 2.032)
							(bold yes)
						)
					)
				)
				(text "(MOTION)"
					(at 0 -3.81 0)
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(symbol "IMU-TEST_1_1"
				(pin power_in line
					(at 0 25.4 270)
					(length 5.08)
					(name "VCC"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.016 1.016)
							)
						)
					)
				)
				(pin power_in line
					(at 0 -25.4 90)
					(length 5.08)
					(name "GND"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "2"
						(effects
							(font
								(size 1.016 1.016)
							)
						)
					)
				)
				(pin bidirectional line
					(at -20.32 5.08 0)
					(length 5.08)
					(name "SDA"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "3"
						(effects
							(font
								(size 1.016 1.016)
							)
						)
					)
				)
				(pin input line
					(at -20.32 -5.08 0)
					(length 5.08)
					(name "SCL"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "4"
						(effects
							(font
								(size 1.016 1.016)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)
		{sym_3v3}
		{sym_gnd}
		{sym_pwr_flag}
	)
	(wire
		(pts
			(xy 114.3 96.52) (xy 172.72 96.52)
		)
		(stroke
			(width 0)
			(type solid)
		)
		(uuid "{gen_uuid()}")
	)
	(wire
		(pts
			(xy 114.3 106.68) (xy 172.72 106.68)
		)
		(stroke
			(width 0)
			(type solid)
		)
		(uuid "{gen_uuid()}")
	)
	(wire
		(pts
			(xy 193.04 76.2) (xy 193.04 66.04)
		)
		(stroke
			(width 0)
			(type solid)
		)
		(uuid "{gen_uuid()}")
	)
	(wire
		(pts
			(xy 193.04 127) (xy 193.04 137.16)
		)
		(stroke
			(width 0)
			(type solid)
		)
		(uuid "{gen_uuid()}")
	)
	(wire
		(pts
			(xy 193.04 66.04) (xy 205.74 66.04)
		)
		(stroke
			(width 0)
			(type solid)
		)
		(uuid "{gen_uuid()}")
	)
	(wire
		(pts
			(xy 193.04 137.16) (xy 205.74 137.16)
		)
		(stroke
			(width 0)
			(type solid)
		)
		(uuid "{gen_uuid()}")
	)
	(junction
		(at 193.04 66.04)
		(diameter 0)
		(color 0 0 0 0)
		(uuid "{gen_uuid()}")
	)
	(junction
		(at 193.04 137.16)
		(diameter 0)
		(color 0 0 0 0)
		(uuid "{gen_uuid()}")
	)
	(symbol
		(lib_id "ESP32-S3-TEST")
		(at 91.44 101.6 0)
		(unit 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(dnp no)
		(uuid "{gen_uuid()}")
		(property "Reference" "U1"
			(at 91.44 74.93 0)
			(effects
				(font
					(size 1.524 1.524)
					(bold yes)
				)
			)
		)
		(property "Value" "ESP32-S3-TEST"
			(at 91.44 77.47 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Footprint" ""
			(at 91.44 101.6 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Datasheet" ""
			(at 91.44 101.6 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Description" "Simplified ESP32-S3 test symbol"
			(at 91.44 101.6 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(pin "8"
			(uuid "{gen_uuid()}")
		)
		(pin "9"
			(uuid "{gen_uuid()}")
		)
		(instances
			(project "AIOT_BLACKBOX"
				(path "/{sch_uuid}"
					(reference "U1")
					(unit 1)
				)
			)
		)
	)
	(symbol
		(lib_id "IMU-TEST")
		(at 193.04 101.6 0)
		(unit 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(dnp no)
		(uuid "{gen_uuid()}")
		(property "Reference" "U2"
			(at 193.04 78.74 0)
			(effects
				(font
					(size 1.524 1.524)
					(bold yes)
				)
			)
		)
		(property "Value" "IMU-TEST"
			(at 193.04 81.28 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Footprint" ""
			(at 193.04 101.6 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Datasheet" ""
			(at 193.04 101.6 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Description" "Simplified 6-axis IMU test symbol"
			(at 193.04 101.6 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(pin "1"
			(uuid "{gen_uuid()}")
		)
		(pin "2"
			(uuid "{gen_uuid()}")
		)
		(pin "3"
			(uuid "{gen_uuid()}")
		)
		(pin "4"
			(uuid "{gen_uuid()}")
		)
		(instances
			(project "AIOT_BLACKBOX"
				(path "/{sch_uuid}"
					(reference "U2")
					(unit 1)
				)
			)
		)
	)
	(symbol
		(lib_id "power:+3V3")
		(at 193.04 66.04 0)
		(unit 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(dnp no)
		(uuid "{gen_uuid()}")
		(property "Reference" "#PWR01"
			(at 193.04 69.85 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Value" "+3V3"
			(at 193.04 62.23 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Footprint" ""
			(at 193.04 66.04 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Datasheet" ""
			(at 193.04 66.04 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Description" "Power symbol creates a global label with name \\"+3V3\\""
			(at 193.04 66.04 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(pin "1"
			(uuid "{gen_uuid()}")
		)
		(instances
			(project "AIOT_BLACKBOX"
				(path "/{sch_uuid}"
					(reference "#PWR01")
					(unit 1)
				)
			)
		)
	)
	(symbol
		(lib_id "power:PWR_FLAG")
		(at 205.74 66.04 0)
		(unit 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(dnp no)
		(uuid "{gen_uuid()}")
		(property "Reference" "#FLG01"
			(at 205.74 67.945 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Value" "PWR_FLAG"
			(at 205.74 60.96 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Footprint" ""
			(at 205.74 66.04 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Datasheet" ""
			(at 205.74 66.04 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Description" "Special symbol for telling ERC where power comes from"
			(at 205.74 66.04 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(pin "1"
			(uuid "{gen_uuid()}")
		)
		(instances
			(project "AIOT_BLACKBOX"
				(path "/{sch_uuid}"
					(reference "#FLG01")
					(unit 1)
				)
			)
		)
	)
	(symbol
		(lib_id "power:GND")
		(at 193.04 137.16 0)
		(unit 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(dnp no)
		(uuid "{gen_uuid()}")
		(property "Reference" "#PWR02"
			(at 193.04 143.51 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Value" "GND"
			(at 193.04 140.97 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Footprint" ""
			(at 193.04 137.16 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Datasheet" ""
			(at 193.04 137.16 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Description" "Power symbol creates a global label with name \\"GND\\" , ground"
			(at 193.04 137.16 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(pin "1"
			(uuid "{gen_uuid()}")
		)
		(instances
			(project "AIOT_BLACKBOX"
				(path "/{sch_uuid}"
					(reference "#PWR02")
					(unit 1)
				)
			)
		)
	)
	(symbol
		(lib_id "power:PWR_FLAG")
		(at 205.74 137.16 0)
		(unit 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(dnp no)
		(uuid "{gen_uuid()}")
		(property "Reference" "#FLG02"
			(at 205.74 139.065 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Value" "PWR_FLAG"
			(at 205.74 132.08 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Footprint" ""
			(at 205.74 137.16 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Datasheet" ""
			(at 205.74 137.16 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Description" "Special symbol for telling ERC where power comes from"
			(at 205.74 137.16 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(pin "1"
			(uuid "{gen_uuid()}")
		)
		(instances
			(project "AIOT_BLACKBOX"
				(path "/{sch_uuid}"
					(reference "#FLG02")
					(unit 1)
				)
			)
		)
	)
	(sheet_instances
		(path "/"
			(page "1")
		)
	)
	(embedded_fonts no)
)
"""

with open(r'D:\ĐỒ ÁN 2\Schematic\AIOT_BLACKBOX\AIOT_BLACKBOX.kicad_sch', 'w', encoding='utf-8') as f:
    f.write(sch_content)

print("Generated refined clean test schematic.")
