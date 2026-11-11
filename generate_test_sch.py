import uuid

def gen_uuid():
    return str(uuid.uuid4())

# Let's define the schematic text
# Sheet size A4 (297 x 210 mm)
# Let's place ESP32-S3 test symbol at (90, 100)
# Let's place IMU test symbol at (180, 100)

sch_uuid = "2e4b636b-9694-4f13-8d7e-a9635a1099e5" # preserve original uuid

content = f"""(kicad_sch
	(version 20260306)
	(generator "eeschema")
	(generator_version "10.0")
	(uuid "{sch_uuid}")
	(paper "A4")
	(lib_symbols
		(symbol "Test_Symbols:ESP32-S3-TEST"
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(duplicate_pin_numbers_are_jumpers no)
			(property "Reference" "U"
				(at 0 24.13 0)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Value" "ESP32-S3-TEST"
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
					(start -17.78 20.32)
					(end 17.78 -20.32)
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type background)
					)
				)
			)
			(symbol "ESP32-S3-TEST_1_1"
				(pin bidirectional line
					(at 22.86 2.54 180)
					(length 5.08)
					(name "GPIO8/SDA"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "P_SDA"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin bidirectional line
					(at 22.86 -2.54 180)
					(length 5.08)
					(name "GPIO9/SCL"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "P_SCL"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)
		(symbol "Test_Symbols:IMU-TEST"
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(duplicate_pin_numbers_are_jumpers no)
			(property "Reference" "U"
				(at 0 17.78 0)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Value" "IMU-TEST"
				(at 0 15.24 0)
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
					(start -12.7 13.97)
					(end 12.7 -13.97)
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type background)
					)
				)
			)
			(symbol "IMU-TEST_1_1"
				(pin power_in line
					(at 0 19.05 270)
					(length 5.08)
					(name "VCC"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "P_VCC"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin power_in line
					(at 0 -19.05 90)
					(length 5.08)
					(name "GND"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "P_GND"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin bidirectional line
					(at -17.78 2.54 0)
					(length 5.08)
					(name "SDA"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "P_SDA"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin input line
					(at -17.78 -2.54 0)
					(length 5.08)
					(name "SCL"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "P_SCL"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)
		(symbol "power:+3V3"
			(power global)
			(pin_numbers
				(hide yes)
			)
			(pin_names
				(offset 0)
				(hide yes)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(duplicate_pin_numbers_are_jumpers no)
			(property "Reference" "#PWR"
				(at 0 -3.81 0)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Value" "+3V3"
				(at 0 3.556 0)
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
			(property "Description" "Power symbol creates a global label with name \\"+3V3\\""
				(at 0 0 0)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(symbol "+3V3_0_1"
				(polyline
					(pts
						(xy -0.762 1.27) (xy 0 2.54)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy 0 2.54) (xy 0.762 1.27)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy 0 0) (xy 0 2.54)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
			)
			(symbol "+3V3_1_1"
				(pin power_in line
					(at 0 0 90)
					(length 0)
					(name ""
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)
		(symbol "power:GND"
			(power global)
			(pin_numbers
				(hide yes)
			)
			(pin_names
				(offset 0)
				(hide yes)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(duplicate_pin_numbers_are_jumpers no)
			(property "Reference" "#PWR"
				(at 0 -6.35 0)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Value" "GND"
				(at 0 -3.81 0)
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
			(property "Description" "Power symbol creates a global label with name \\"GND\\" , ground"
				(at 0 0 0)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(symbol "GND_0_1"
				(polyline
					(pts
						(xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
			)
			(symbol "GND_1_1"
				(pin power_in line
					(at 0 0 270)
					(length 0)
					(name ""
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)
	)
	(wire
		(pts
			(xy 102.86 97.46) (xy 162.22 97.46)
		)
		(stroke
			(width 0)
			(type solid)
		)
		(uuid "{gen_uuid()}")
	)
	(wire
		(pts
			(xy 102.86 102.54) (xy 162.22 102.54)
		)
		(stroke
			(width 0)
			(type solid)
		)
		(uuid "{gen_uuid()}")
	)
	(wire
		(pts
			(xy 180 80.95) (xy 180 73.66)
		)
		(stroke
			(width 0)
			(type solid)
		)
		(uuid "{gen_uuid()}")
	)
	(wire
		(pts
			(xy 180 119.05) (xy 180 127)
		)
		(stroke
			(width 0)
			(type solid)
		)
		(uuid "{gen_uuid()}")
	)
	(symbol
		(lib_id "Test_Symbols:ESP32-S3-TEST")
		(at 80 100 0)
		(unit 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(dnp no)
		(uuid "{gen_uuid()}")
		(property "Reference" "U1"
			(at 80 74.93 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Value" "ESP32-S3-TEST"
			(at 80 77.47 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Footprint" ""
			(at 80 100 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Datasheet" ""
			(at 80 100 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Description" "Simplified ESP32-S3 test symbol"
			(at 80 100 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(pin "P_SDA"
			(uuid "{gen_uuid()}")
		)
		(pin "P_SCL"
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
		(lib_id "Test_Symbols:IMU-TEST")
		(at 180 100 0)
		(unit 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(dnp no)
		(uuid "{gen_uuid()}")
		(property "Reference" "U2"
			(at 180 81.28 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Value" "IMU-TEST"
			(at 180 83.82 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Footprint" ""
			(at 180 100 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Datasheet" ""
			(at 180 100 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Description" "Simplified 6-axis IMU test symbol"
			(at 180 100 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(pin "P_VCC"
			(uuid "{gen_uuid()}")
		)
		(pin "P_GND"
			(uuid "{gen_uuid()}")
		)
		(pin "P_SDA"
			(uuid "{gen_uuid()}")
		)
		(pin "P_SCL"
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
		(at 180 73.66 0)
		(unit 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(dnp no)
		(uuid "{gen_uuid()}")
		(property "Reference" "#PWR01"
			(at 180 77.47 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Value" "+3V3"
			(at 180 69.85 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Footprint" ""
			(at 180 73.66 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Datasheet" ""
			(at 180 73.66 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Description" "Power symbol creates a global label with name \\"+3V3\\""
			(at 180 73.66 0)
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
		(lib_id "power:GND")
		(at 180 127 0)
		(unit 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(dnp no)
		(uuid "{gen_uuid()}")
		(property "Reference" "#PWR02"
			(at 180 133.35 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Value" "GND"
			(at 180 132.08 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Footprint" ""
			(at 180 127 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Datasheet" ""
			(at 180 127 0)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Description" "Power symbol creates a global label with name \\"GND\\" , ground"
			(at 180 127 0)
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
	(sheet_instances
		(path "/"
			(page "1")
		)
	)
	(embedded_fonts no)
)
"""

with open(r'D:\ĐỒ ÁN 2\Schematic\AIOT_BLACKBOX\AIOT_BLACKBOX.kicad_sch', 'w', encoding='utf-8') as f:
    f.write(content)
print("Schematic written successfully.")
