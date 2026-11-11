# -*- coding: utf-8 -*-
"""
CUSTOM VERIFIED IC SYMBOLS FOR AIOT BLACK BOX POWER SUPPLY
Follows SCHEMATIC_DRAWING_RULES.md:
- Positive power pins at TOP
- GND pins at BOTTOM
- Horizontal pin exits
- Official manufacturer pin numbers
"""

SYM_TPS2121 = """\t\t(symbol "Power_Management:TPS2121RUXR"
\t\t\t(pin_names (offset 1.016))
\t\t\t(exclude_from_sim no)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
\t\t\t(property "Reference" "U" (at 0 17.78 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "TPS2121RUXR" (at 0 -17.78 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "Package_DFN_QFN:Texas_RUX0012A" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t\t(property "Datasheet" "https://www.ti.com/lit/ds/symlink/tps2121.pdf" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t\t(property "Description" "2.8V-22V, 4A Priority Power MUX with Seamless Switchover, VQFN-12" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t\t(symbol "TPS2121RUXR_0_1"
\t\t\t\t(rectangle (start -10.16 15.24) (end 10.16 -15.24) (stroke (width 0.254) (type solid)) (fill (type background)))
\t\t\t)
\t\t\t(symbol "TPS2121RUXR_1_1"
\t\t\t\t(pin power_in line (at -12.7 10.16 0) (length 2.54) (name "IN1" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin power_in line (at -12.7 7.62 0) (length 2.54) (name "IN2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin input line (at -12.7 2.54 0) (length 2.54) (name "PR1" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin input line (at -12.7 0.0 0) (length 2.54) (name "CP2" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin input line (at -12.7 -2.54 0) (length 2.54) (name "OV1" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin input line (at -12.7 -5.08 0) (length 2.54) (name "OV2" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin power_in line (at -12.7 -12.7 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "12" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin power_out line (at 12.7 10.16 180) (length 2.54) (name "OUT" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at 12.7 7.62 180) (length 2.54) (name "OUT" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at 12.7 2.54 180) (length 2.54) (name "SS" (effects (font (size 1.27 1.27)))) (number "11" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at 12.7 0.0 180) (length 2.54) (name "ILIM" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin open_collector line (at 12.7 -2.54 180) (length 2.54) (name "ST" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
\t\t\t)
\t\t)"""

SYM_BQ25895 = """		(symbol "Battery_Management:BQ25895RTWR"
			(pin_names (offset 1.016))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U" (at 0 25.4 0) (effects (font (size 1.27 1.27))))
			(property "Value" "BQ25895RTWR" (at 0 -25.4 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Package_DFN_QFN:Texas_RTW0024A" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Datasheet" "https://www.ti.com/lit/ds/symlink/bq25895.pdf" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Description" "I2C Controlled Single-Cell 5A Fast Charger with NVDC Power Path Management, WQFN-24" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "BQ25895RTWR_0_1"
				(rectangle (start -15.24 22.86) (end 15.24 -22.86) (stroke (width 0.254) (type solid)) (fill (type background)))
			)
			(symbol "BQ25895RTWR_1_1"
				(pin power_in line (at -17.78 17.78 0) (length 2.54) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin power_out line (at -17.78 15.24 0) (length 2.54) (name "PMID" (effects (font (size 1.27 1.27)))) (number "23" (effects (font (size 1.27 1.27)))))
				(pin power_out line (at -17.78 12.7 0) (length 2.54) (name "REGN" (effects (font (size 1.27 1.27)))) (number "22" (effects (font (size 1.27 1.27)))))
				(pin input line (at -17.78 7.62 0) (length 2.54) (name "~CE" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
				(pin input line (at -17.78 5.08 0) (length 2.54) (name "OTG" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
				(pin input line (at -17.78 2.54 0) (length 2.54) (name "QON" (effects (font (size 1.27 1.27)))) (number "12" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -17.78 0.0 0) (length 2.54) (name "ILIM" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.27 1.27)))))
				(pin input line (at -17.78 -2.54 0) (length 2.54) (name "TS" (effects (font (size 1.27 1.27)))) (number "11" (effects (font (size 1.27 1.27)))))
				(pin input line (at -17.78 -5.08 0) (length 2.54) (name "DSEL" (effects (font (size 1.27 1.27)))) (number "24" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at -17.78 -7.62 0) (length 2.54) (name "D+" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at -17.78 -10.16 0) (length 2.54) (name "D-" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at -17.78 -17.78 0) (length 2.54) (name "PGND" (effects (font (size 1.27 1.27)))) (number "17" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -17.78 -20.32 0) (length 2.54) (name "PGND" (effects (font (size 1.27 1.27)))) (number "18" (effects (font (size 1.27 1.27)))))
				(pin power_out line (at 17.78 17.78 180) (length 2.54) (name "SW" (effects (font (size 1.27 1.27)))) (number "19" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 17.78 15.24 180) (length 2.54) (name "SW" (effects (font (size 1.27 1.27)))) (number "20" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 17.78 12.7 180) (length 2.54) (name "BTST" (effects (font (size 1.27 1.27)))) (number "21" (effects (font (size 1.27 1.27)))))
				(pin power_out line (at 17.78 7.62 180) (length 2.54) (name "SYS" (effects (font (size 1.27 1.27)))) (number "15" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 17.78 5.08 180) (length 2.54) (name "SYS" (effects (font (size 1.27 1.27)))) (number "16" (effects (font (size 1.27 1.27)))))
				(pin power_out line (at 17.78 0.0 180) (length 2.54) (name "BAT" (effects (font (size 1.27 1.27)))) (number "13" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 17.78 -2.54 180) (length 2.54) (name "BAT" (effects (font (size 1.27 1.27)))) (number "14" (effects (font (size 1.27 1.27)))))
				(pin open_collector line (at 17.78 -7.62 180) (length 2.54) (name "STAT" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin open_collector line (at 17.78 -10.16 180) (length 2.54) (name "~INT" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at 17.78 -12.7 180) (length 2.54) (name "SCL" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at 17.78 -15.24 180) (length 2.54) (name "SDA" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 0 -22.86 90) (length 2.54) (name "EP" (effects (font (size 1.27 1.27)))) (number "25" (effects (font (size 1.27 1.27)))))
			)
		)"""

SYM_DW01A = """		(symbol "Battery_Management:DW01A"
			(pin_names (offset 1.016))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U" (at 0 12.7 0) (effects (font (size 1.27 1.27))))
			(property "Value" "DW01A" (at 0 -12.7 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Package_TO_SOT_SMD:SOT-23-6" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Datasheet" "https://datasheet.lcsc.com/lcsc/1811151441_Fortune-Semicon-DW01A-G_C24339.pdf" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Description" "Single Cell Lithium-Ion/Polymer Battery Protection IC, SOT-23-6" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "DW01A_0_1"
				(rectangle (start -10.16 10.16) (end 10.16 -10.16) (stroke (width 0.254) (type solid)) (fill (type background)))
			)
			(symbol "DW01A_1_1"
				(pin passive line (at -12.7 5.08 0) (length 2.54) (name "VCC" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin input line (at -12.7 0.0 0) (length 2.54) (name "CS" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -12.7 -2.54 0) (length 2.54) (name "TD" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -12.7 -5.08 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
				(pin output line (at 12.7 5.08 180) (length 2.54) (name "OD" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin output line (at 12.7 -5.08 180) (length 2.54) (name "OC" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
			)
		)"""

SYM_FS8205A = """		(symbol "Transistor_FET:FS8205A"
			(pin_names (offset 1.016))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "Q" (at 0 12.7 0) (effects (font (size 1.27 1.27))))
			(property "Value" "FS8205A" (at 0 -12.7 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Package_SO:TSSOP-8_4.4x3mm_P0.65mm" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Datasheet" "https://datasheet.lcsc.com/lcsc/1811151441_Fortune-Semicon-FS8205A_C32254.pdf" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Description" "Dual N-Channel Enhancement Mode Power MOSFET, 20V 6A, TSSOP-8" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "FS8205A_0_1"
				(rectangle (start -10.16 10.16) (end 10.16 -10.16) (stroke (width 0.254) (type solid)) (fill (type background)))
			)
			(symbol "FS8205A_1_1"
				(pin input line (at -12.7 5.08 0) (length 2.54) (name "G1" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin input line (at -12.7 -5.08 0) (length 2.54) (name "G2" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 12.7 7.62 180) (length 2.54) (name "S1" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 12.7 5.08 180) (length 2.54) (name "S1" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 12.7 2.54 180) (length 2.54) (name "D1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 12.7 0.0 180) (length 2.54) (name "D2" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 12.7 -5.08 180) (length 2.54) (name "S2" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 12.7 -7.62 180) (length 2.54) (name "S2" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
			)
		)"""

SYM_TPS61088 = """		(symbol "Power_Management:TPS61088RHLR"
			(pin_names (offset 1.016))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U" (at 0 22.86 0) (effects (font (size 1.27 1.27))))
			(property "Value" "TPS61088RHLR" (at 0 -22.86 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "Package_DFN_QFN:Texas_RHL0020A" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Datasheet" "https://www.ti.com/lit/ds/symlink/tps61088.pdf" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Description" "2.7V-12V, 10A Fully Integrated Synchronous Boost Converter, VQFN-20" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "TPS61088RHLR_0_1"
				(rectangle (start -12.7 20.32) (end 12.7 -20.32) (stroke (width 0.254) (type solid)) (fill (type background)))
			)
			(symbol "TPS61088RHLR_1_1"
				(pin power_in line (at -15.24 17.78 0) (length 2.54) (name "VIN" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
				(pin power_out line (at -15.24 12.7 0) (length 2.54) (name "SW" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -15.24 10.16 0) (length 2.54) (name "SW" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -15.24 7.62 0) (length 2.54) (name "SW" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -15.24 5.08 0) (length 2.54) (name "SW" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -15.24 0.0 0) (length 2.54) (name "BOOT" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
				(pin input line (at -15.24 -2.54 0) (length 2.54) (name "EN" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin power_out line (at -15.24 -5.08 0) (length 2.54) (name "VCC" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin input line (at -15.24 -7.62 0) (length 2.54) (name "MODE" (effects (font (size 1.27 1.27)))) (number "13" (effects (font (size 1.27 1.27)))))
				(pin input line (at -15.24 -10.16 0) (length 2.54) (name "FSW" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -15.24 -12.7 0) (length 2.54) (name "SS" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -15.24 -15.24 0) (length 2.54) (name "ILIM" (effects (font (size 1.27 1.27)))) (number "19" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at -15.24 -17.78 0) (length 2.54) (name "PGND" (effects (font (size 1.27 1.27)))) (number "20" (effects (font (size 1.27 1.27)))))
				(pin power_out line (at 15.24 17.78 180) (length 2.54) (name "VOUT" (effects (font (size 1.27 1.27)))) (number "14" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 15.24 15.24 180) (length 2.54) (name "VOUT" (effects (font (size 1.27 1.27)))) (number "15" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 15.24 12.7 180) (length 2.54) (name "VOUT" (effects (font (size 1.27 1.27)))) (number "16" (effects (font (size 1.27 1.27)))))
				(pin input line (at 15.24 2.54 180) (length 2.54) (name "FB" (effects (font (size 1.27 1.27)))) (number "17" (effects (font (size 1.27 1.27)))))
				(pin output line (at 15.24 0.0 180) (length 2.54) (name "COMP" (effects (font (size 1.27 1.27)))) (number "18" (effects (font (size 1.27 1.27)))))
				(pin no_connect line (at 15.24 -7.62 180) (length 2.54) (name "NC" (effects (font (size 1.27 1.27)))) (number "11" (effects (font (size 1.27 1.27)))))
				(pin no_connect line (at 15.24 -10.16 180) (length 2.54) (name "NC" (effects (font (size 1.27 1.27)))) (number "12" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 15.24 -17.78 180) (length 2.54) (name "EP/GND" (effects (font (size 1.27 1.27)))) (number "21" (effects (font (size 1.27 1.27)))))
			)
		)"""

SYM_TPS62162 = """\t\t(symbol "Power_Management:TPS62162DSGR"
\t\t\t(pin_names (offset 1.016))
\t\t\t(exclude_from_sim no)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
\t\t\t(property "Reference" "U" (at 0 15.24 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "TPS62162DSGR" (at 0 -15.24 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "Package_SON:WSON-8-1EP_2x2mm_P0.5mm_EP0.9x1.6mm" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t\t(property "Datasheet" "https://www.ti.com/lit/ds/symlink/tps62162.pdf" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t\t(property "Description" "3V-17V, 1A Step-Down Converter with DCS-Control, Fixed 3.3V, WSON-8" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t\t(symbol "TPS62162DSGR_0_1"
\t\t\t\t(rectangle (start -10.16 12.7) (end 10.16 -12.7) (stroke (width 0.254) (type solid)) (fill (type background)))
\t\t\t)
\t\t\t(symbol "TPS62162DSGR_1_1"
\t\t\t\t(pin power_in line (at -12.7 7.62 0) (length 2.54) (name "VIN" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin input line (at -12.7 2.54 0) (length 2.54) (name "EN" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin power_in line (at -12.7 -7.62 0) (length 2.54) (name "PGND" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin power_in line (at -12.7 -10.16 0) (length 2.54) (name "AGND" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin input line (at 12.7 7.62 180) (length 2.54) (name "VOS" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin power_out line (at 12.7 2.54 180) (length 2.54) (name "SW" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin input line (at 12.7 -2.54 180) (length 2.54) (name "FB" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin open_collector line (at 12.7 -5.08 180) (length 2.54) (name "PG" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin power_in line (at 12.7 -10.16 180) (length 2.54) (name "EP/GND" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
\t\t\t)
\t\t)"""

SYM_TPS62130 = """\t\t(symbol "Power_Management:TPS62130RGTR"
\t\t\t(pin_names (offset 1.016))
\t\t\t(exclude_from_sim no)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
\t\t\t(property "Reference" "U" (at 0 20.32 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "TPS62130RGTR" (at 0 -20.32 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "Package_DFN_QFN:Texas_RGT0016A" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t\t(property "Datasheet" "https://www.ti.com/lit/ds/symlink/tps62130.pdf" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t\t(property "Description" "3V-17V, 3A Synchronous Step-Down Converter with DCS-Control, VQFN-16" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t\t(symbol "TPS62130RGTR_0_1"
\t\t\t\t(rectangle (start -12.7 17.78) (end 12.7 -17.78) (stroke (width 0.254) (type solid)) (fill (type background)))
\t\t\t)
\t\t\t(symbol "TPS62130RGTR_1_1"
\t\t\t\t(pin power_in line (at -15.24 15.24 0) (length 2.54) (name "PVIN" (effects (font (size 1.27 1.27)))) (number "11" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at -15.24 12.7 0) (length 2.54) (name "PVIN" (effects (font (size 1.27 1.27)))) (number "12" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin power_in line (at -15.24 10.16 0) (length 2.54) (name "AVIN" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin input line (at -15.24 5.08 0) (length 2.54) (name "EN" (effects (font (size 1.27 1.27)))) (number "13" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin input line (at -15.24 0.0 0) (length 2.54) (name "FSW" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin input line (at -15.24 -2.54 0) (length 2.54) (name "DEF" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at -15.24 -5.08 0) (length 2.54) (name "SS/TR" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin power_in line (at -15.24 -12.7 0) (length 2.54) (name "PGND" (effects (font (size 1.27 1.27)))) (number "15" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at -15.24 -15.24 0) (length 2.54) (name "PGND" (effects (font (size 1.27 1.27)))) (number "16" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin power_in line (at -15.24 -17.78 0) (length 2.54) (name "AGND" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin input line (at 15.24 15.24 180) (length 2.54) (name "VOS" (effects (font (size 1.27 1.27)))) (number "14" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin power_out line (at 15.24 10.16 180) (length 2.54) (name "SW" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at 15.24 7.62 180) (length 2.54) (name "SW" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at 15.24 5.08 180) (length 2.54) (name "SW" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin input line (at 15.24 0.0 180) (length 2.54) (name "FB" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin open_collector line (at 15.24 -5.08 180) (length 2.54) (name "PG" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin power_in line (at 15.24 -17.78 180) (length 2.54) (name "EP/GND" (effects (font (size 1.27 1.27)))) (number "17" (effects (font (size 1.27 1.27)))))
\t\t\t)
\t\t)"""

SYM_USB_C_16P = """\t\t(symbol "Connector:USB_C_16P"
\t\t\t(pin_names (offset 1.016))
\t\t\t(exclude_from_sim no)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
\t\t\t(property "Reference" "J" (at 0 15.24 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "USB_C_16P" (at 0 -15.24 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t\t(property "Datasheet" "https://www.usb.org/type-c" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t\t(property "Description" "USB 2.0 Type-C Receptacle connector, 16 pins" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t\t(symbol "USB_C_16P_0_1"
\t\t\t\t(rectangle (start -10.16 12.7) (end 10.16 -12.7) (stroke (width 0.254) (type solid)) (fill (type background)))
\t\t\t)
\t\t\t(symbol "USB_C_16P_1_1"
\t\t\t\t(pin passive line (at 12.7 10.16 180) (length 2.54) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "A4" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at 12.7 7.62 180) (length 2.54) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "B9" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin bidirectional line (at 12.7 2.54 180) (length 2.54) (name "CC1" (effects (font (size 1.27 1.27)))) (number "A5" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin bidirectional line (at 12.7 0.0 180) (length 2.54) (name "CC2" (effects (font (size 1.27 1.27)))) (number "B5" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin bidirectional line (at 12.7 -2.54 180) (length 2.54) (name "D+" (effects (font (size 1.27 1.27)))) (number "A6" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin bidirectional line (at 12.7 -5.08 180) (length 2.54) (name "D-" (effects (font (size 1.27 1.27)))) (number "A7" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin power_in line (at 12.7 -10.16 180) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "A1" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at -12.7 -10.16 0) (length 2.54) (name "SHIELD" (effects (font (size 1.27 1.27)))) (number "S1" (effects (font (size 1.27 1.27)))))
\t\t\t)
\t\t)"""

print("Custom symbols ready.")

SYM_AO3401A = """\t\t(symbol "Transistor_FET:AO3401A"
\t\t\t(pin_names (offset 1.016))
\t\t\t(exclude_from_sim no)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
\t\t\t(property "Reference" "Q" (at 0 7.62 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "AO3401A" (at 0 -7.62 0) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "Package_TO_SOT_SMD:SOT-23" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t\t(property "Datasheet" "http://www.aosmd.com/pdfs/datasheet/AO3401A.pdf" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t\t(property "Description" "-4.0A Id, -30V Vds, P-Channel MOSFET, SOT-23" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t\t(symbol "AO3401A_0_1"
\t\t\t\t(rectangle (start -5.08 5.08) (end 5.08 -5.08) (stroke (width 0.254) (type solid)) (fill (type background)))
\t\t\t)
\t\t\t(symbol "AO3401A_1_1"
\t\t\t\t(pin passive line (at -7.62 0 0) (length 2.54) (name "S" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin passive line (at 7.62 0 180) (length 2.54) (name "D" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
\t\t\t\t(pin input line (at 0 -7.62 90) (length 2.54) (name "G" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t\t)
\t\t)"""
