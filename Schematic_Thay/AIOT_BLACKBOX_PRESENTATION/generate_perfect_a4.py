import os
import shutil
import uuid
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

proj_dir = r"D:\ĐỒ ÁN 2\Schematic_Thay\AIOT_BLACKBOX_PRESENTATION"
sch_file = os.path.join(proj_dir, "AIOT_BLACKBOX_PRESENTATION.kicad_sch")

def gen_uuid():
    return str(uuid.uuid4())

# -------------------------------------------------------------
# EXTRACT SYMBOLS FROM KICAD LIBRARIES
# -------------------------------------------------------------
kicad_sym_dir = r"D:\Kicad\share\kicad\symbols"

def extract_sym(file_content, sym_name, new_lib_id):
    pattern = rf'\(symbol\s+"{sym_name}"'
    m = re.search(pattern, file_content)
    if not m:
        return ""
    start = m.start()
    depth = 0
    end = start
    for i in range(start, len(file_content)):
        if file_content[i] == '(':
            depth += 1
        elif file_content[i] == ')':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    content = file_content[start:end]
    content = re.sub(rf'\(symbol\s+"{sym_name}"', f'(symbol "{new_lib_id}"', content)
    content = re.sub(rf'\(symbol\s+"{sym_name}_', f'(symbol "{new_lib_id.split(":")[-1]}_', content)
    return content

with open(os.path.join(kicad_sym_dir, "power.kicad_sym"), 'r', encoding='utf-8') as f:
    pwr_text = f.read()

sym_3v3 = extract_sym(pwr_text, "\\+3V3", "power:+3V3")
sym_gnd = extract_sym(pwr_text, "GND", "power:GND")
sym_pwr_flag = extract_sym(pwr_text, "PWR_FLAG", "power:PWR_FLAG")

def make_pwr_sym(src_sym, old_name, new_name):
    res = re.sub(rf'\(symbol\s+"power:{old_name}"', f'(symbol "power:{new_name}"', src_sym)
    res = re.sub(rf'\(symbol\s+"{old_name}_', f'(symbol "{new_name}_', res)
    res = re.sub(rf'\(property\s+"Value"\s+"{old_name}"', f'(property "Value" "{new_name}"', res)
    return res

sym_5v_raw = extract_sym(pwr_text, "\\+5V", "power:+5V")
sym_5v_sys = make_pwr_sym(sym_5v_raw, "\\+5V", "5V_SYS")
sym_5v_usb = make_pwr_sym(sym_5v_raw, "\\+5V", "5V_USB")
sym_vbat = make_pwr_sym(sym_5v_raw, "\\+5V", "VBAT")

with open(os.path.join(kicad_sym_dir, "Device.kicad_sym"), 'r', encoding='utf-8') as f:
    dev_text = f.read()

sym_r = extract_sym(dev_text, "R", "Device:R")
sym_c = extract_sym(dev_text, "C", "Device:C")
sym_led = extract_sym(dev_text, "LED", "Device:LED")
sym_buzzer = extract_sym(dev_text, "Buzzer", "Device:Buzzer")
sym_bat = extract_sym(dev_text, "Battery_Cell", "Device:Battery_Cell")
sym_antenna = extract_sym(dev_text, "Antenna", "Device:Antenna").replace('(pin input line', '(pin passive line')

with open(os.path.join(kicad_sym_dir, "Switch.kicad_sym"), 'r', encoding='utf-8') as f:
    sw_text = f.read()
sym_sw = extract_sym(sw_text, "SW_Push", "Switch:SW_Push")

sym_npn_standalone = """		(symbol "Presentation:2SC1815"
			(pin_names (offset 0) (hide yes))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "Q" (at 5.08 1.27 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "2SC1815" (at 5.08 -1.27 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "Package_TO_SOT_THT:TO-92_Inline" (at 5.08 2.54 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Datasheet" "https://media.digikey.com/pdf/Data%20Sheets/Toshiba%20PDFs/2SC1815.pdf" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Description" "NPN Transistor, 50V, 0.15A" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "2SC1815_0_1"
				(polyline (pts (xy -2.54 0) (xy 0.635 0)) (stroke (width 0) (type default)) (fill (type none)))
				(polyline (pts (xy 0.635 1.905) (xy 0.635 -1.905)) (stroke (width 0.508) (type default)) (fill (type none)))
				(circle (center 1.27 0) (radius 2.8194) (stroke (width 0.254) (type default)) (fill (type none)))
			)
			(symbol "2SC1815_1_1"
				(polyline (pts (xy 0.635 0.635) (xy 2.54 2.54)) (stroke (width 0) (type default)) (fill (type none)))
				(polyline (pts (xy 0.635 -0.635) (xy 2.54 -2.54)) (stroke (width 0) (type default)) (fill (type none)))
				(polyline (pts (xy 1.27 -1.778) (xy 1.778 -1.27) (xy 2.286 -2.286) (xy 1.27 -1.778)) (stroke (width 0) (type default)) (fill (type outline)))
				(pin passive line (at 2.54 -5.08 90) (length 2.54) (name "E" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 2.54 5.08 270) (length 2.54) (name "C" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin input line (at -5.08 0 0) (length 2.54) (name "B" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
			)
		)"""

# -------------------------------------------------------------
# CUSTOM A4 PRESENTATION SYMBOLS
# -------------------------------------------------------------
custom_mcu_sym = """		(symbol "Presentation:ESP32-S3-DevKitC-1"
			(pin_names (offset 1.016))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U1" (at 0 33.02 0) (effects (font (size 1.778 1.778) (bold yes))))
			(property "Value" "ESP32-S3" (at 0 30.48 0) (hide yes) (effects (font (size 1.524 1.524))))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Datasheet" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Description" "ESP32-S3 N16R8 Central Processing Unit" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "ESP32-S3-DevKitC-1_0_1"
				(rectangle (start -13.97 30.48) (end 13.97 -30.48) (stroke (width 0.381) (type default)) (fill (type background)))
				(text "ESP32-S3" (at 0 7.62 0) (effects (font (size 2.0 2.0) (bold yes))))
				(text "DevKitC-1 N16R8" (at 0 2.54 0) (effects (font (size 1.3 1.3) (bold yes))))
				(text "16MB Flash, 8MB PSRAM" (at 0 -2.54 0) (effects (font (size 1.1 1.1))))
			)
			(symbol "ESP32-S3-DevKitC-1_1_1"
				(pin power_in line (at -17.78 25.40 0) (length 3.81) (name "5V" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.016 1.016)))))
				(pin power_out line (at -17.78 20.32 0) (length 3.81) (name "3V3" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.016 1.016)))))
				(pin input line (at -17.78 15.24 0) (length 3.81) (name "GPIO1" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.016 1.016)))))
				(pin bidirectional line (at -17.78 10.16 0) (length 3.81) (name "GPIO8" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.016 1.016)))))
				(pin bidirectional line (at -17.78 5.08 0) (length 3.81) (name "GPIO9" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.016 1.016)))))
				(pin input line (at -17.78 0.00 0) (length 3.81) (name "GPIO10" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.016 1.016)))))
				(pin output line (at -17.78 -5.08 0) (length 3.81) (name "GPIO14" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.016 1.016)))))
				(pin output line (at -17.78 -10.16 0) (length 3.81) (name "GPIO11" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.016 1.016)))))
				(pin output line (at -17.78 -15.24 0) (length 3.81) (name "GPIO12" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.016 1.016)))))
				(pin input line (at -17.78 -20.32 0) (length 3.81) (name "GPIO13" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.016 1.016)))))
				(pin power_in line (at -17.78 -25.40 0) (length 3.81) (name "GND" (effects (font (size 1.27 1.27)))) (number "11" (effects (font (size 1.016 1.016)))))

				(pin output line (at 17.78 25.40 180) (length 3.81) (name "GPIO43" (effects (font (size 1.27 1.27)))) (number "12" (effects (font (size 1.016 1.016)))))
				(pin input line (at 17.78 20.32 180) (length 3.81) (name "GPIO44" (effects (font (size 1.27 1.27)))) (number "13" (effects (font (size 1.016 1.016)))))
				(pin output line (at 17.78 15.24 180) (length 3.81) (name "GPIO4" (effects (font (size 1.27 1.27)))) (number "14" (effects (font (size 1.016 1.016)))))
				(pin input line (at 17.78 10.16 180) (length 3.81) (name "GPIO5" (effects (font (size 1.27 1.27)))) (number "15" (effects (font (size 1.016 1.016)))))
				(pin output line (at 17.78 5.08 180) (length 3.81) (name "GPIO17" (effects (font (size 1.27 1.27)))) (number "16" (effects (font (size 1.016 1.016)))))
				(pin input line (at 17.78 0.00 180) (length 3.81) (name "GPIO18" (effects (font (size 1.27 1.27)))) (number "17" (effects (font (size 1.016 1.016)))))
				(pin input line (at 17.78 -5.08 180) (length 3.81) (name "GPIO21" (effects (font (size 1.27 1.27)))) (number "18" (effects (font (size 1.016 1.016)))))
				(pin input line (at 17.78 -10.16 180) (length 3.81) (name "GPIO6" (effects (font (size 1.27 1.27)))) (number "19" (effects (font (size 1.016 1.016)))))
				(pin output line (at 17.78 -15.24 180) (length 3.81) (name "GPIO7" (effects (font (size 1.27 1.27)))) (number "20" (effects (font (size 1.016 1.016)))))
				(pin output line (at 17.78 -20.32 180) (length 3.81) (name "GPIO15" (effects (font (size 1.27 1.27)))) (number "21" (effects (font (size 1.016 1.016)))))
				(pin power_in line (at 17.78 -25.40 180) (length 3.81) (name "GND" (effects (font (size 1.27 1.27)))) (number "22" (effects (font (size 1.016 1.016)))))
			)
		)"""

custom_mpu_sym = """		(symbol "Presentation:MPU6050_Module"
			(pin_names (offset 1.016))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U2" (at 0 16.51 0) (effects (font (size 1.524 1.524) (bold yes))))
			(property "Value" "MPU6050" (at 0 14.00 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Datasheet" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Description" "6-Axis IMU Module" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "MPU6050_Module_0_1"
				(rectangle (start -12.70 14.00) (end 12.70 -16.51) (stroke (width 0.381) (type default)) (fill (type background)))
				(text "MPU6050" (at 0 2.54 0) (effects (font (size 1.778 1.778) (bold yes))))
				(text "6-Axis IMU (0x69)" (at 0 -1.27 0) (effects (font (size 1.27 1.27))))
			)
			(symbol "MPU6050_Module_1_1"
				(pin power_in line (at -16.51 10.16 0) (length 3.81) (name "VCC" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.016 1.016)))))
				(pin input line (at -16.51 5.08 0) (length 3.81) (name "AD0" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.016 1.016)))))
				(pin bidirectional line (at 16.51 5.08 180) (length 3.81) (name "SDA" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.016 1.016)))))
				(pin input line (at 16.51 0.00 180) (length 3.81) (name "SCL" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.016 1.016)))))
				(pin output line (at 16.51 -5.08 180) (length 3.81) (name "INT" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.016 1.016)))))
				(pin power_in line (at 16.51 -12.70 180) (length 3.81) (name "GND" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.016 1.016)))))
			)
		)"""

custom_rtc_sym = """		(symbol "Presentation:DS3231_RTC_Module"
			(pin_names (offset 1.016))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U3" (at 0 12.70 0) (effects (font (size 1.524 1.524) (bold yes))))
			(property "Value" "DS3231" (at 0 10.50 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Datasheet" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Description" "High Precision Real Time Clock" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "DS3231_RTC_Module_0_1"
				(rectangle (start -12.70 10.16) (end 12.70 -12.70) (stroke (width 0.381) (type default)) (fill (type background)))
				(text "DS3231" (at 0 2.54 0) (effects (font (size 1.778 1.778) (bold yes))))
				(text "RTC Module (0x68)" (at 0 -1.27 0) (effects (font (size 1.27 1.27))))
			)
			(symbol "DS3231_RTC_Module_1_1"
				(pin power_in line (at -16.51 0.00 0) (length 3.81) (name "VBAT" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.016 1.016)))))
				(pin power_in line (at -16.51 5.08 0) (length 3.81) (name "VCC" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.016 1.016)))))
				(pin bidirectional line (at 16.51 5.08 180) (length 3.81) (name "SDA" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.016 1.016)))))
				(pin input line (at 16.51 0.00 180) (length 3.81) (name "SCL" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.016 1.016)))))
				(pin power_in line (at 16.51 -7.62 180) (length 3.81) (name "GND" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.016 1.016)))))
			)
		)"""

custom_sd_sym = """		(symbol "Presentation:MicroSD_SPI_Module"
			(pin_names (offset 1.016))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "J1" (at 0 15.24 0) (effects (font (size 1.524 1.524) (bold yes))))
			(property "Value" "MICROSD" (at 0 13.00 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Datasheet" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Description" "MicroSD Flash Memory Module" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "MicroSD_SPI_Module_0_1"
				(rectangle (start -12.70 12.70) (end 12.70 -17.78) (stroke (width 0.381) (type default)) (fill (type background)))
				(text "MICROSD" (at 0 2.54 0) (effects (font (size 1.778 1.778) (bold yes))))
				(text "SPI Flash Storage" (at 0 -1.27 0) (effects (font (size 1.27 1.27))))
			)
			(symbol "MicroSD_SPI_Module_1_1"
				(pin power_in line (at -16.51 10.16 0) (length 3.81) (name "3V3" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.016 1.016)))))
				(pin input line (at 16.51 10.16 180) (length 3.81) (name "CS" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.016 1.016)))))
				(pin input line (at 16.51 5.08 180) (length 3.81) (name "MOSI" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.016 1.016)))))
				(pin input line (at 16.51 0.00 180) (length 3.81) (name "SCK" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.016 1.016)))))
				(pin output line (at 16.51 -5.08 180) (length 3.81) (name "MISO" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.016 1.016)))))
				(pin power_in line (at 16.51 -12.70 180) (length 3.81) (name "GND" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.016 1.016)))))
			)
		)"""

custom_gnss_sym = """		(symbol "Presentation:ATGM336H_GNSS_Module"
			(pin_names (offset 1.016))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U4" (at 0 17.50 0) (effects (font (size 1.524 1.524) (bold yes))))
			(property "Value" "ATGM336H" (at 0 15.00 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Datasheet" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Description" "Dual-Mode BDS/GPS GNSS Module" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "ATGM336H_GNSS_Module_0_1"
				(rectangle (start -12.70 15.24) (end 12.70 -16.51) (stroke (width 0.381) (type default)) (fill (type background)))
				(text "ATGM336H" (at 0 2.54 0) (effects (font (size 1.778 1.778) (bold yes))))
				(text "BDS / GPS (10Hz)" (at 0 -1.27 0) (effects (font (size 1.27 1.27))))
			)
			(symbol "ATGM336H_GNSS_Module_1_1"
				(pin power_in line (at -16.51 15.24 0) (length 3.81) (name "VCC" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.016 1.016)))))
				(pin input line (at -16.51 10.16 0) (length 3.81) (name "RX" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.016 1.016)))))
				(pin output line (at -16.51 5.08 0) (length 3.81) (name "TX" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.016 1.016)))))
				(pin output line (at -16.51 0.00 0) (length 3.81) (name "PPS" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.016 1.016)))))
				(pin power_in line (at -16.51 -10.16 0) (length 3.81) (name "GND" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.016 1.016)))))
				(pin passive line (at 16.51 5.08 180) (length 3.81) (name "ANT" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.016 1.016)))))
			)
		)"""

custom_4g_sym = """		(symbol "Presentation:MKE-M21_SIM7680C_Module"
			(pin_names (offset 1.016))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U5" (at 0 18.50 0) (effects (font (size 1.524 1.524) (bold yes))))
			(property "Value" "MKE-M21" (at 0 16.00 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Datasheet" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Description" "4G LTE Module" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "MKE-M21_SIM7680C_Module_0_1"
				(rectangle (start -13.97 16.51) (end 13.97 -19.05) (stroke (width 0.381) (type default)) (fill (type background)))
				(text "MKE-M21" (at 0 3.81 0) (effects (font (size 1.778 1.778) (bold yes))))
				(text "SIM7680C 4G LTE" (at 0 0.00 0) (effects (font (size 1.27 1.27))))
				(text "SMS / MQTT / Cloud" (at 0 -3.81 0) (effects (font (size 1.016 1.016))))
			)
			(symbol "MKE-M21_SIM7680C_Module_1_1"
				(pin power_in line (at -17.78 15.24 0) (length 3.81) (name "VCC" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.016 1.016)))))
				(pin input line (at -17.78 10.16 0) (length 3.81) (name "RX" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.016 1.016)))))
				(pin output line (at -17.78 5.08 0) (length 3.81) (name "TX" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.016 1.016)))))
				(pin input line (at -17.78 0.00 0) (length 3.81) (name "PWRKEY" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.016 1.016)))))
				(pin output line (at -17.78 -5.08 0) (length 3.81) (name "STATUS" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.016 1.016)))))
				(pin power_in line (at -17.78 -15.24 0) (length 3.81) (name "GND" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.016 1.016)))))
				(pin passive line (at 17.78 5.08 180) (length 3.81) (name "ANT" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.016 1.016)))))
			)
		)"""

custom_pwr_mgmt_sym = """		(symbol "Presentation:Power_Management_18650"
			(pin_names (offset 1.016))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U6" (at 0 18.50 0) (effects (font (size 1.524 1.524) (bold yes))))
			(property "Value" "18650 POWER" (at 0 16.00 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Datasheet" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Description" "18650 Charger and 5V Boost System" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "Power_Management_18650_0_1"
				(rectangle (start -13.97 16.51) (end 13.97 -16.51) (stroke (width 0.381) (type default)) (fill (type background)))
				(text "QUẢN LÝ NGUỒN" (at 0 4.00 0) (effects (font (size 1.778 1.778) (bold yes))))
				(text "& 5V BOOST" (at 0 0.50 0) (effects (font (size 1.524 1.524) (bold yes))))
				(text "Primary Power System" (at 0 -4.00 0) (effects (font (size 1.143 1.143))))
			)
			(symbol "Power_Management_18650_1_1"
				(pin power_in line (at -17.78 5.08 0) (length 3.81) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.016 1.016)))))
				(pin power_in line (at -17.78 -10.16 0) (length 3.81) (name "GND" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.016 1.016)))))
				(pin power_out line (at 17.78 15.24 180) (length 3.81) (name "5V_OUT" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.016 1.016)))))
				(pin passive line (at 17.78 5.08 180) (length 3.81) (name "BAT+" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.016 1.016)))))
				(pin passive line (at 17.78 -2.54 180) (length 3.81) (name "BAT-" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.016 1.016)))))
				(pin power_in line (at 17.78 -10.16 180) (length 3.81) (name "GND" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.016 1.016)))))
			)
		)"""

custom_usbc_sym = """		(symbol "Presentation:USB_C_Input"
			(pin_names (offset 1.016))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "J2" (at 0 12.00 0) (effects (font (size 1.524 1.524) (bold yes))))
			(property "Value" "USB-C" (at 0 9.80 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Datasheet" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Description" "USB Type-C Power Input" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "USB_C_Input_0_1"
				(rectangle (start -10.16 10.16) (end 10.16 -10.16) (stroke (width 0.381) (type default)) (fill (type background)))
				(text "USB-C" (at 0 2.54 0) (effects (font (size 1.778 1.778) (bold yes))))
				(text "5V SẠC" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
			)
			(symbol "USB_C_Input_1_1"
				(pin power_out line (at 13.97 5.08 180) (length 3.81) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.016 1.016)))))
				(pin power_out line (at 13.97 -5.08 180) (length 3.81) (name "GND" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.016 1.016)))))
			)
		)"""

all_lib_symbols = f"""	(lib_symbols
{sym_3v3}
{sym_gnd}
{sym_5v_sys}
{sym_5v_usb}
{sym_vbat}
{sym_pwr_flag}
{sym_r}
{sym_c}
{sym_led}
{sym_buzzer}
{sym_bat}
{sym_antenna}
{sym_sw}
{sym_npn_standalone}
{custom_mcu_sym}
{custom_mpu_sym}
{custom_rtc_sym}
{custom_sd_sym}
{custom_gnss_sym}
{custom_4g_sym}
{custom_pwr_mgmt_sym}
{custom_usbc_sym}
	)"""

# -------------------------------------------------------------
# HELPER FUNCTIONS FOR ROBUST INSTANCES
# -------------------------------------------------------------
elements = []

def pt(x, y):
    return f"(xy {x:.2f} {y:.2f})"

def add_wire(x1, y1, x2, y2):
    elements.append(f'\t(wire (pts {pt(x1, y1)} {pt(x2, y2)}) (stroke (width 0) (type default)) (uuid "{gen_uuid()}"))')

def add_junction(x, y):
    elements.append(f'\t(junction (at {x:.2f} {y:.2f}) (diameter 1.016) (color 0 0 0 0) (uuid "{gen_uuid()}"))')

def add_net_label(name, x, y, rot=0):
    elements.append(f'\t(label "{name}" (at {x:.2f} {y:.2f} {rot}) (fields_autoplaced yes) (effects (font (size 1.27 1.27) (bold yes))) (uuid "{gen_uuid()}"))')

def power_sym(name, x, y, rot=0):
    val_y = y - 3.81 if rot == 0 else (y + 3.81 if rot == 180 else y)
    val_x = x if rot in [0, 180] else (x + 3.81 if rot == 90 else x - 3.81)
    return f"""\t(symbol (lib_id "power:{name}") (at {x:.2f} {y:.2f} {rot}) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "#PWR?" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "{name}" (at {val_x:.2f} {val_y:.2f} 0) (effects (font (size 1.27 1.27) (bold yes))))
\t\t(property "Footprint" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t)"""

def pwr_flag(x, y, rot=0):
    val_y = y - 3.81 if rot == 0 else (y + 3.81 if rot == 180 else y)
    val_x = x if rot in [0, 180] else (x + 3.81 if rot == 90 else x - 3.81)
    return f"""\t(symbol (lib_id "power:PWR_FLAG") (at {x:.2f} {y:.2f} {rot}) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "#FLG?" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "PWR_FLAG" (at {val_x:.2f} {val_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t)"""

def res_sym(ref, val, x, y, rot=0, text_side="right"):
    if rot in (90, 270):
        rx, ry = x, y - 2.54
        vx, vy = x, y + 2.54
        just = ""
    else:
        if text_side == "left":
            rx, ry = x - 2.54, y - 1.27
            vx, vy = x - 2.54, y + 1.27
            just = " (justify right)"
        else:
            rx, ry = x + 2.54, y - 1.27
            vx, vy = x + 2.54, y + 1.27
            just = ""
    return f"""\t(symbol (lib_id "Device:R") (at {x:.2f} {y:.2f} {rot}) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "{ref}" (at {rx:.2f} {ry:.2f} 0) (effects (font (size 1.27 1.27) (bold yes)){just}))
\t\t(property "Value" "{val}" (at {vx:.2f} {vy:.2f} 0) (effects (font (size 1.27 1.27) (bold yes)){just}))
\t\t(property "Footprint" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "Resistor" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t\t(pin "2" (uuid "{gen_uuid()}"))
\t)"""

def cap_sym(ref, val, x, y, rot=0):
    if rot in (90, 270):
        rx, ry = x, y - 2.54
        vx, vy = x, y + 2.54
    else:
        rx, ry = x + 2.54, y - 1.27
        vx, vy = x + 2.54, y + 1.27
    return f"""\t(symbol (lib_id "Device:C") (at {x:.2f} {y:.2f} {rot}) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "{ref}" (at {rx:.2f} {ry:.2f} 0) (effects (font (size 1.27 1.27) (bold yes))))
\t\t(property "Value" "{val}" (at {vx:.2f} {vy:.2f} 0) (effects (font (size 1.27 1.27) (bold yes))))
\t\t(property "Footprint" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "Capacitor" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t\t(pin "2" (uuid "{gen_uuid()}"))
\t)"""

def led_sym(ref, val, x, y, rot=0):
    rx, ry = x, y - 3.00
    vx, vy = x, y + 3.00
    return f"""\t(symbol (lib_id "Device:LED") (at {x:.2f} {y:.2f} {rot}) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "{ref}" (at {rx:.2f} {ry:.2f} 0) (effects (font (size 1.27 1.27) (bold yes))))
\t\t(property "Value" "{val}" (at {vx:.2f} {vy:.2f} 0) (effects (font (size 1.27 1.27) (bold yes))))
\t\t(property "Footprint" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "Light emitting diode" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t\t(pin "2" (uuid "{gen_uuid()}"))
\t)"""

def sw_sym(ref, val, x, y, rot=0):
    rx, ry = x, y - 3.81
    vx, vy = x, y + 3.81
    return f"""\t(symbol (lib_id "Switch:SW_Push") (at {x:.2f} {y:.2f} {rot}) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "{ref}" (at {rx:.2f} {ry:.2f} 0) (effects (font (size 1.27 1.27) (bold yes))))
\t\t(property "Value" "{val}" (at {vx:.2f} {vy:.2f} 0) (effects (font (size 1.27 1.27) (bold yes))))
\t\t(property "Footprint" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "Push button switch" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t\t(pin "2" (uuid "{gen_uuid()}"))
\t)"""

def bjt_sym(ref, val, x, y, rot=0):
    rx, ry = x + 5.08, y - 2.54
    vx, vy = x + 5.08, y + 2.54
    return f"""\t(symbol (lib_id "Presentation:2SC1815") (at {x:.2f} {y:.2f} {rot}) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "{ref}" (at {rx:.2f} {ry:.2f} 0) (effects (font (size 1.27 1.27) (bold yes))))
\t\t(property "Value" "{val}" (at {vx:.2f} {vy:.2f} 0) (effects (font (size 1.27 1.27) (bold yes))))
\t\t(property "Footprint" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "NPN Transistor" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t\t(pin "2" (uuid "{gen_uuid()}"))
\t\t(pin "3" (uuid "{gen_uuid()}"))
\t)"""

def buzzer_sym(ref, val, x, y, rot=0):
    rx, ry = x + 5.08, y - 2.54
    vx, vy = x + 5.08, y + 2.54
    return f"""\t(symbol (lib_id "Device:Buzzer") (at {x:.2f} {y:.2f} {rot}) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "{ref}" (at {rx:.2f} {ry:.2f} 0) (effects (font (size 1.27 1.27) (bold yes))))
\t\t(property "Value" "{val}" (at {vx:.2f} {vy:.2f} 0) (effects (font (size 1.27 1.27) (bold yes))))
\t\t(property "Footprint" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "Piezo Buzzer" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t\t(pin "2" (uuid "{gen_uuid()}"))
\t)"""

def bat_sym(ref, val, x, y, rot=0):
    return f"""\t(symbol (lib_id "Device:Battery_Cell") (at {x:.2f} {y:.2f} {rot}) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "{ref}" (at {x+3.81:.2f} {y-1.27:.2f} 0) (effects (font (size 1.27 1.27) (bold yes))))
\t\t(property "Value" "{val}" (at {x+3.81:.2f} {y+1.27:.2f} 0) (effects (font (size 1.27 1.27) (bold yes))))
\t\t(property "Footprint" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "Single-cell battery" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t\t(pin "2" (uuid "{gen_uuid()}"))
\t)"""

def antenna_sym(ref, val, x, y, rot=0):
    return f"""\t(symbol (lib_id "Device:Antenna") (at {x:.2f} {y:.2f} {rot}) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "{ref}" (at {x:.2f} {y-5.08:.2f} 0) (effects (font (size 1.27 1.27) (bold yes))))
\t\t(property "Value" "{val}" (at {x:.2f} {y+6.35:.2f} 0) (effects (font (size 1.27 1.27) (bold yes))))
\t\t(property "Footprint" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "Antenna" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t)"""

def box_border(title, x1, y1, x2, y2):
    poly = f'\t(polyline (pts (xy {x1:.2f} {y1:.2f}) (xy {x2:.2f} {y1:.2f}) (xy {x2:.2f} {y2:.2f}) (xy {x1:.2f} {y2:.2f}) (xy {x1:.2f} {y1:.2f})) (stroke (width 0.254) (type dash) (color 0 70 180 0.75)) (fill (type none)) (uuid "{gen_uuid()}"))'
    txt = f'\t(text "{title}" (at {x1+3.50:.2f} {y1+3.50:.2f} 0) (effects (font (size 1.5 1.5) (bold yes)) (justify left)) (uuid "{gen_uuid()}"))'
    return poly + '\n' + txt

# -------------------------------------------------------------
# ASSEMBLE CIRCUIT ELEMENTS
# -------------------------------------------------------------

# 1. ESP32-S3 DevKitC-1 (U1) - Central Processing Unit at (147.32, 99.06)
u1_x = 147.32
u1_y = 99.06
elements.append(f"""\t(symbol (lib_id "Presentation:ESP32-S3-DevKitC-1") (at {u1_x:.2f} {u1_y:.2f} 0) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "U1" (at {u1_x:.2f} {u1_y - 33.02:.2f} 0) (effects (font (size 1.778 1.778) (bold yes))))
\t\t(property "Value" "ESP32-S3" (at {u1_x:.2f} {u1_y - 30.50:.2f} 0) (hide yes) (effects (font (size 1.524 1.524))))
\t\t(property "Footprint" "" (at {u1_x:.2f} {u1_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {u1_x:.2f} {u1_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "ESP32-S3 N16R8 Central Processing Unit" (at {u1_x:.2f} {u1_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
""" + "\n".join([f'\t\t(pin "{i}" (uuid "{gen_uuid()}"))' for i in range(1, 23)]) + "\n\t)")

# U1 power connections
# Pin 1 (5V): (129.54, 73.66) -> 5V_SYS
add_wire(129.54, 73.66, 124.46, 73.66)
add_wire(124.46, 73.66, 124.46, 71.12)
elements.append(power_sym("5V_SYS", 124.46, 71.12, 0))

# Pin 2 (3V3): (129.54, 78.74) -> +3V3
add_wire(129.54, 78.74, 124.46, 78.74)
add_wire(124.46, 78.74, 124.46, 76.20)
elements.append(power_sym("+3V3", 124.46, 76.20, 0))

# Pin 3 (GPIO1): (129.54, 83.82) -> ADC_VBAT_SENSE
add_wire(129.54, 83.82, 121.92, 83.82)
add_net_label("ADC_VBAT_SENSE", 121.92, 83.82, 180)

# Pin 11 (GND): (129.54, 124.46) -> GND
add_wire(129.54, 124.46, 124.46, 124.46)
add_wire(124.46, 124.46, 124.46, 127.00)
elements.append(power_sym("GND", 124.46, 127.00, 0))

# Pin 22 (GND): (165.10, 124.46) -> GND
add_wire(165.10, 124.46, 170.18, 124.46)
add_wire(170.18, 124.46, 170.18, 127.00)
elements.append(power_sym("GND", 170.18, 127.00, 0))


# 2. MPU6050 (GY-521) IMU (U2) - Center at (55.88, 93.98)
u2_x = 55.88
u2_y = 93.98
elements.append(f"""\t(symbol (lib_id "Presentation:MPU6050_Module") (at {u2_x:.2f} {u2_y:.2f} 0) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "U2" (at {u2_x:.2f} {u2_y - 16.50:.2f} 0) (effects (font (size 1.524 1.524) (bold yes))))
\t\t(property "Value" "MPU6050" (at {u2_x:.2f} {u2_y - 14.00:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at {u2_x:.2f} {u2_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {u2_x:.2f} {u2_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "6-Axis IMU Module" (at {u2_x:.2f} {u2_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
""" + "\n".join([f'\t\t(pin "{i}" (uuid "{gen_uuid()}"))' for i in range(1, 7)]) + "\n\t)")

# U2 Pin 1 (VCC): (39.37, 83.82) -> +3V3
add_wire(39.37, 83.82, 34.29, 83.82)
add_wire(34.29, 83.82, 34.29, 80.01)
elements.append(power_sym("+3V3", 34.29, 80.01, 0))

# U2 Pin 2 (AD0): (39.37, 88.90) -> tied to +3V3
add_wire(39.37, 88.90, 34.29, 88.90)
add_wire(34.29, 88.90, 34.29, 83.82)
add_junction(34.29, 83.82)

# U2 Pin 6 (GND): (72.39, 106.68) -> GND
add_wire(72.39, 106.68, 76.20, 106.68)
add_wire(76.20, 106.68, 76.20, 109.22)
elements.append(power_sym("GND", 76.20, 109.22, 0))

# U2 Signals: SDA (88.90), SCL (93.98), INT (99.06) -> 100% straight horizontal lines to ESP32!
add_wire(72.39, 88.90, 129.54, 88.90) # SDA
add_wire(72.39, 93.98, 129.54, 93.98) # SCL
add_wire(72.39, 99.06, 129.54, 99.06) # INT

# I2C Pull-ups with 10.16 mm spacing
# SDA pull-up at X = 83.82
add_junction(83.82, 88.90)
elements.append(res_sym("R_PU1", "4.7k", 83.82, 83.82, 0, "right"))
add_wire(83.82, 88.90, 83.82, 87.63)
add_wire(83.82, 80.01, 83.82, 77.47)
elements.append(power_sym("+3V3", 83.82, 77.47, 0))
# Drop to RTC SDA at (83.82, 128.27)
add_wire(83.82, 88.90, 83.82, 128.27)

# SCL pull-up at X = 93.98
add_junction(93.98, 93.98)
elements.append(res_sym("R_PU2", "4.7k", 93.98, 87.63, 0, "right"))
add_wire(93.98, 93.98, 93.98, 91.44)
add_wire(93.98, 83.82, 93.98, 80.01)
elements.append(power_sym("+3V3", 93.98, 80.01, 0))
# Drop to RTC SCL at (93.98, 133.35)
add_wire(93.98, 93.98, 93.98, 133.35)


# 3. DS3231 RTC Module (U3) - Center at (55.88, 133.35)
u3_x = 55.88
u3_y = 133.35
elements.append(f"""\t(symbol (lib_id "Presentation:DS3231_RTC_Module") (at {u3_x:.2f} {u3_y:.2f} 0) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "U3" (at {u3_x:.2f} {u3_y - 12.00:.2f} 0) (effects (font (size 1.524 1.524) (bold yes))))
\t\t(property "Value" "DS3231" (at {u3_x:.2f} {u3_y - 9.80:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at {u3_x:.2f} {u3_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {u3_x:.2f} {u3_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "Real Time Clock" (at {u3_x:.2f} {u3_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
""" + "\n".join([f'\t\t(pin "{i}" (uuid "{gen_uuid()}"))' for i in range(1, 6)]) + "\n\t)")

# U3 Pin 2 (VCC): (39.37, 128.27) -> +3V3
add_wire(39.37, 128.27, 34.29, 128.27)
add_wire(34.29, 128.27, 34.29, 125.73)
elements.append(power_sym("+3V3", 34.29, 125.73, 0))

# U3 Pin 1 (VBAT): (39.37, 133.35) -> BT2 (CR2032)
elements.append(bat_sym("BT2", "CR2032", 27.94, 138.43, 0))
elements.append(pwr_flag(27.94, 133.35, 180))
add_wire(27.94, 133.35, 39.37, 133.35) # BT2 (+) -> U3 VBAT
add_wire(27.94, 140.97, 27.94, 143.51)
elements.append(power_sym("GND", 27.94, 143.51, 0))

# U3 Pin 3 (SDA): (72.39, 128.27) -> (83.82, 128.27)
add_wire(72.39, 128.27, 83.82, 128.27)
add_junction(83.82, 128.27)

# U3 Pin 4 (SCL): (72.39, 133.35) -> (93.98, 133.35)
add_wire(72.39, 133.35, 93.98, 133.35)
add_junction(93.98, 133.35)

# U3 Pin 5 (GND): (72.39, 140.97) -> GND
add_wire(72.39, 140.97, 76.20, 140.97)
add_wire(76.20, 140.97, 76.20, 143.51)
elements.append(power_sym("GND", 76.20, 143.51, 0))


# 4. MicroSD Module (J1) - Center at (55.88, 172.72)
j1_x = 55.88
j1_y = 172.72
elements.append(f"""\t(symbol (lib_id "Presentation:MicroSD_SPI_Module") (at {j1_x:.2f} {j1_y:.2f} 0) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "J1" (at {j1_x:.2f} {j1_y - 15.24:.2f} 0) (effects (font (size 1.524 1.524) (bold yes))))
\t\t(property "Value" "MICROSD" (at {j1_x:.2f} {j1_y - 13.00:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at {j1_x:.2f} {j1_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {j1_x:.2f} {j1_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "MicroSD Flash Storage" (at {j1_x:.2f} {j1_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
""" + "\n".join([f'\t\t(pin "{i}" (uuid "{gen_uuid()}"))' for i in range(1, 7)]) + "\n\t)")

# J1 Pin 1 (3V3): (39.37, 162.56) -> +3V3
add_wire(39.37, 162.56, 34.29, 162.56)
add_wire(34.29, 162.56, 34.29, 160.02)
elements.append(power_sym("+3V3", 34.29, 160.02, 0))

# J1 Pin 6 (GND): (72.39, 185.42) -> GND
add_wire(72.39, 185.42, 76.20, 185.42)
add_wire(76.20, 185.42, 76.20, 187.96)
elements.append(power_sym("GND", 76.20, 187.96, 0))

# 4 SPI Lines: CS (162.56), MOSI (167.64), SCK (172.72), MISO (177.80)
# CS -> ESP32 Pin 7 (129.54, 104.14)
add_wire(72.39, 162.56, 104.14, 162.56)
add_wire(104.14, 162.56, 104.14, 104.14)
add_wire(104.14, 104.14, 129.54, 104.14)

# MOSI -> ESP32 Pin 8 (129.54, 109.22)
add_wire(72.39, 167.64, 109.22, 167.64)
add_wire(109.22, 167.64, 109.22, 109.22)
add_wire(109.22, 109.22, 129.54, 109.22)

# SCK -> ESP32 Pin 9 (129.54, 114.30)
add_wire(72.39, 172.72, 114.30, 172.72)
add_wire(114.30, 172.72, 114.30, 114.30)
add_wire(114.30, 114.30, 129.54, 114.30)

# MISO -> ESP32 Pin 10 (129.54, 119.38)
add_wire(72.39, 177.80, 119.38, 177.80)
add_wire(119.38, 177.80, 119.38, 119.38)
add_wire(119.38, 119.38, 129.54, 119.38)


# 5. ATGM336H GNSS Module (U4) - Center at (238.76, 104.14)
u4_x = 238.76
u4_y = 104.14
elements.append(f"""\t(symbol (lib_id "Presentation:ATGM336H_GNSS_Module") (at {u4_x:.2f} {u4_y:.2f} 0) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "U4" (at {u4_x:.2f} {u4_y - 17.50:.2f} 0) (effects (font (size 1.524 1.524) (bold yes))))
\t\t(property "Value" "ATGM336H" (at {u4_x:.2f} {u4_y - 15.00:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at {u4_x:.2f} {u4_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {u4_x:.2f} {u4_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "GNSS BDS/GPS Module" (at {u4_x:.2f} {u4_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
""" + "\n".join([f'\t\t(pin "{i}" (uuid "{gen_uuid()}"))' for i in range(1, 7)]) + "\n\t)")

# U4 Pin 1 (VCC): (222.25, 88.90) -> +3V3
add_wire(222.25, 88.90, 217.17, 88.90)
add_wire(217.17, 88.90, 217.17, 85.09)
elements.append(power_sym("+3V3", 217.17, 85.09, 0))

# U4 Pin 5 (GND): (222.25, 114.30) -> GND
add_wire(222.25, 114.30, 217.17, 114.30)
add_wire(217.17, 114.30, 217.17, 116.84)
elements.append(power_sym("GND", 217.17, 116.84, 0))

# 3 GNSS Lines: RX (93.98), TX (99.06), PPS (104.14) -> 100% straight horizontal lines to ESP32!
add_wire(165.10, 93.98, 222.25, 93.98) # ESP32 Pin 16 (GPIO17 TX) -> GNSS RX
add_wire(165.10, 99.06, 222.25, 99.06) # GNSS TX -> ESP32 Pin 17 (GPIO18 RX)
add_wire(165.10, 104.14, 222.25, 104.14) # GNSS PPS -> ESP32 Pin 18 (GPIO21 PPS)

# U4 Pin 6 (ANT): (255.27, 99.06) -> AE2
elements.append(antenna_sym("AE2", "GNSS Ant", 265.43, 99.06, 270))
add_wire(255.27, 99.06, 260.35, 99.06)


# 6. MKE-M21 SIM7680C 4G LTE Module (U5) - Center at (238.76, 43.18)
u5_x = 238.76
u5_y = 43.18
elements.append(f"""\t(symbol (lib_id "Presentation:MKE-M21_SIM7680C_Module") (at {u5_x:.2f} {u5_y:.2f} 0) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "U5" (at {u5_x:.2f} {u5_y - 18.50:.2f} 0) (effects (font (size 1.524 1.524) (bold yes))))
\t\t(property "Value" "MKE-M21" (at {u5_x:.2f} {u5_y - 16.00:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at {u5_x:.2f} {u5_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {u5_x:.2f} {u5_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "4G LTE Module" (at {u5_x:.2f} {u5_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
""" + "\n".join([f'\t\t(pin "{i}" (uuid "{gen_uuid()}"))' for i in range(1, 8)]) + "\n\t)")

# U5 Pin 1 (VCC): (220.98, 27.94) -> 5V_SYS
add_wire(220.98, 27.94, 215.90, 27.94)
add_wire(215.90, 27.94, 215.90, 25.40)
elements.append(power_sym("5V_SYS", 215.90, 25.40, 0))

# U5 Pin 6 (GND): (220.98, 58.42) -> GND
add_wire(220.98, 58.42, 215.90, 58.42)
add_wire(215.90, 58.42, 215.90, 60.96)
elements.append(power_sym("GND", 215.90, 60.96, 0))

# U5 Pin 7 (ANT): (256.54, 38.10) -> AE1
elements.append(antenna_sym("AE1", "4G Ant", 265.43, 38.10, 270))
add_wire(256.54, 38.10, 260.35, 38.10)

# 4 4G Lines to ESP32: RX (33.02), TX (38.10), PWRKEY (43.18), STATUS (48.26)
# RX -> ESP32 Pin 12 (165.10, 73.66)
add_wire(220.98, 33.02, 175.26, 33.02)
add_wire(175.26, 33.02, 175.26, 73.66)
add_wire(175.26, 73.66, 165.10, 73.66)

# TX -> ESP32 Pin 13 (165.10, 78.74)
add_wire(220.98, 38.10, 180.34, 38.10)
add_wire(180.34, 38.10, 180.34, 78.74)
add_wire(180.34, 78.74, 165.10, 78.74)

# PWRKEY -> ESP32 Pin 14 (165.10, 83.82)
add_wire(220.98, 43.18, 185.42, 43.18)
add_wire(185.42, 43.18, 185.42, 83.82)
add_wire(185.42, 83.82, 165.10, 83.82)

# STATUS -> ESP32 Pin 15 (165.10, 88.90)
add_wire(220.98, 48.26, 190.50, 48.26)
add_wire(190.50, 48.26, 190.50, 88.90)
add_wire(190.50, 88.90, 165.10, 88.90)


# 7. KHỐI GIAO DIỆN & CẢNH BÁO (UI & Warning) - Corridor Drops (No Box Overlaps)
# SW1 CANCEL BUTTON from ESP32 Pin 19 (165.10, 109.22)
add_wire(165.10, 109.22, 186.69, 109.22)
add_wire(186.69, 109.22, 186.69, 137.16)
add_wire(186.69, 137.16, 195.58, 137.16)
add_junction(195.58, 137.16)

# R3 Pull-up 10k to +3V3
elements.append(res_sym("R3", "10k", 195.58, 130.81, 0, "right"))
add_wire(195.58, 137.16, 195.58, 134.62)
add_wire(195.58, 127.00, 195.58, 124.46)
elements.append(power_sym("+3V3", 195.58, 124.46, 0))

# C2 Filter 100nF to GND
elements.append(cap_sym("C2", "100nF", 195.58, 143.51, 0))
add_wire(195.58, 137.16, 195.58, 139.70)
add_wire(195.58, 147.32, 195.58, 149.86)
elements.append(power_sym("GND", 195.58, 149.86, 0))

# SW1 Push button to GND
elements.append(sw_sym("SW1", "CANCEL", 205.74, 137.16, 0))
add_wire(195.58, 137.16, 200.66, 137.16)
add_wire(210.82, 137.16, 213.36, 137.16)
add_wire(213.36, 137.16, 213.36, 149.86)
elements.append(power_sym("GND", 213.36, 149.86, 0))

# STATUS LED from ESP32 Pin 20 (165.10, 114.30)
add_wire(165.10, 114.30, 191.77, 114.30)
add_wire(191.77, 114.30, 191.77, 137.16)
add_wire(191.77, 137.16, 223.52, 137.16)

# R4 330R (horizontal)
elements.append(res_sym("R4", "330R", 227.33, 137.16, 90))
add_wire(223.52, 137.16, 223.52, 137.16)
add_wire(231.14, 137.16, 233.68, 137.16)

# D1 LED Green (rot 180 horizontal: Anode at 233.68, Cathode at 241.30)
elements.append(led_sym("D1", "LED", 237.49, 137.16, 180))
add_wire(241.30, 137.16, 243.84, 137.16)
add_wire(243.84, 137.16, 243.84, 143.51)
elements.append(power_sym("GND", 243.84, 143.51, 0))

# ACTIVE PIEZO BUZZER from ESP32 Pin 21 (165.10, 119.38)
add_wire(165.10, 119.38, 196.85, 119.38)
add_wire(196.85, 119.38, 196.85, 129.54)
add_wire(196.85, 129.54, 251.46, 129.54)
add_wire(251.46, 129.54, 251.46, 137.16)

# R5 1k (horizontal)
elements.append(res_sym("R5", "1k", 255.27, 137.16, 90))
add_wire(251.46, 137.16, 251.46, 137.16)
add_wire(259.08, 137.16, 261.62, 137.16)

# Q1 2SC1815 NPN (at 266.70, 137.16): Base at (261.62, 137.16), Emitter at (269.24, 142.24), Collector at (269.24, 132.08)
elements.append(bjt_sym("Q1", "2SC1815", 266.70, 137.16, 0))
add_wire(269.24, 142.24, 269.24, 147.32)
elements.append(power_sym("GND", 269.24, 147.32, 0))

# Buzzer BZ1 at (271.78, 129.54, 0): Pin 1 (+) at (269.24, 127.00), Pin 2 (-) at (269.24, 132.08)
elements.append(buzzer_sym("BZ1", "BUZZER", 271.78, 129.54, 0))
# Connect Collector to Pin 2 (-):
add_wire(269.24, 132.08, 269.24, 132.08)
# Connect Pin 1 (+) to 5V_SYS:
add_wire(269.24, 127.00, 269.24, 121.92)
elements.append(power_sym("5V_SYS", 269.24, 121.92, 0))


# 8. KHỐI NGUỒN & QUẢN LÝ PIN 18650 (Power Block)
# J2 USB-C Input - Center at (35.56, 43.18)
j2_x = 35.56
j2_y = 43.18
elements.append(f"""\t(symbol (lib_id "Presentation:USB_C_Input") (at {j2_x:.2f} {j2_y:.2f} 0) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "J2" (at {j2_x:.2f} {j2_y - 12.00:.2f} 0) (effects (font (size 1.524 1.524) (bold yes))))
\t\t(property "Value" "USB-C" (at {j2_x:.2f} {j2_y - 9.80:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at {j2_x:.2f} {j2_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {j2_x:.2f} {j2_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "USB Type-C 5V IN" (at {j2_x:.2f} {j2_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t\t(pin "2" (uuid "{gen_uuid()}"))
\t)""")

# J2 Pin 1 (VBUS): (49.53, 38.10) -> 5V_USB
add_wire(49.53, 38.10, 52.07, 38.10)
add_wire(52.07, 38.10, 52.07, 34.29)
elements.append(power_sym("5V_USB", 52.07, 34.29, 0))

# J2 Pin 2 (GND): (49.53, 48.26) -> GND
add_wire(49.53, 48.26, 52.07, 48.26)
add_wire(52.07, 48.26, 52.07, 52.07)
elements.append(power_sym("GND", 52.07, 52.07, 0))

# U6 Power Management & Boost - Center at (73.66, 43.18)
u6_x = 73.66
u6_y = 43.18
elements.append(f"""\t(symbol (lib_id "Presentation:Power_Management_18650") (at {u6_x:.2f} {u6_y:.2f} 0) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "U6" (at {u6_x:.2f} {u6_y - 20.00:.2f} 0) (effects (font (size 1.524 1.524) (bold yes))))
\t\t(property "Value" "18650 POWER" (at {u6_x:.2f} {u6_y - 17.50:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at {u6_x:.2f} {u6_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {u6_x:.2f} {u6_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "Power Management & 5V Boost" (at {u6_x:.2f} {u6_y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
""" + "\n".join([f'\t\t(pin "{i}" (uuid "{gen_uuid()}"))' for i in range(1, 7)]) + "\n\t)")

# U6 Pin 1 (VBUS): (55.88, 38.10) -> 5V_USB
add_wire(55.88, 38.10, 59.69, 38.10)
add_wire(59.69, 38.10, 59.69, 34.29)
elements.append(power_sym("5V_USB", 59.69, 34.29, 0))

# U6 Pin 2 (GND): (55.88, 53.34) -> GND
add_wire(55.88, 53.34, 59.69, 53.34)
add_wire(59.69, 53.34, 59.69, 55.88)
elements.append(power_sym("GND", 59.69, 55.88, 0))

# U6 Pin 3 (5V_OUT): (91.44, 27.94) -> 5V_SYS
add_wire(91.44, 27.94, 95.25, 27.94)
add_wire(95.25, 27.94, 95.25, 25.40)
elements.append(power_sym("5V_SYS", 95.25, 25.40, 0))

# U6 Pin 6 (GND): (91.44, 53.34) -> GND
add_wire(91.44, 53.34, 95.25, 53.34)
add_wire(95.25, 53.34, 95.25, 55.88)
elements.append(power_sym("GND", 95.25, 55.88, 0))

# BT1 18650 Li-ion Battery - Placed at (101.60, 43.18, 0): Pin 1 (+) at (101.60, 38.10), Pin 2 (-) at (101.60, 45.72)
elements.append(bat_sym("BT1", "18650 Li-ion", 101.60, 43.18, 0))

# U6 Pin 4 (BAT+): (91.44, 38.10) -> BT1 Pin 1 (101.60, 38.10)
add_wire(91.44, 38.10, 101.60, 38.10)
add_junction(101.60, 38.10)

# U6 Pin 5 (BAT-): (91.44, 45.72) -> BT1 Pin 2 (101.60, 45.72)
add_wire(91.44, 45.72, 101.60, 45.72)

# Voltage Divider connected to BAT+ (VBAT)
add_wire(101.60, 38.10, 114.30, 38.10)
add_junction(114.30, 38.10)
add_wire(114.30, 38.10, 114.30, 34.29)
elements.append(power_sym("VBAT", 114.30, 34.29, 0))
elements.append(pwr_flag(114.30, 34.29, 0))

# R1 100k 1% (vertical from 38.10 to 45.72: center at 41.91)
elements.append(res_sym("R1", "100k", 114.30, 41.91, 0, "left"))

# Mid node at (114.30, 45.72)
add_junction(114.30, 45.72)

# R2 100k 1% (vertical from 45.72 to 53.34: center at 49.53)
elements.append(res_sym("R2", "100k", 114.30, 49.53, 0, "left"))
add_wire(114.30, 53.34, 114.30, 55.88)
elements.append(power_sym("GND", 114.30, 55.88, 0))

# C1 100nF filter in parallel with R2 (vertical from 45.72 to 53.34: center at 49.53)
elements.append(cap_sym("C1", "100nF", 120.65, 49.53, 0))
add_wire(114.30, 45.72, 120.65, 45.72)
add_wire(120.65, 45.72, 123.19, 45.72)
add_net_label("ADC_VBAT_SENSE", 123.19, 45.72, 0)
add_wire(120.65, 53.34, 120.65, 55.88)
elements.append(power_sym("GND", 120.65, 55.88, 0))

# -------------------------------------------------------------
# GRAPHICAL FUNCTIONAL BLOCK FRAMES & BOLD TITLES (ACADEMIC MINIMALISM)
# -------------------------------------------------------------
elements.append(box_border("KHỐI NGUỒN & PIN 18650", 16.00, 16.00, 128.00, 64.00))
elements.append(box_border("KHỐI IMU (MPU6050)", 16.00, 70.00, 78.00, 114.00))
elements.append(box_border("KHỐI RTC (DS3231)", 16.00, 115.00, 78.00, 146.00))
elements.append(box_border("KHỐI THẺ NHỚ MICROSD", 16.00, 149.00, 78.00, 194.00))

elements.append(box_border("KHỐI 4G LTE (SIM7680C)", 206.00, 16.00, 282.00, 64.00))
elements.append(box_border("KHỐI ĐỊNH VỊ GNSS (ATGM336H)", 206.00, 70.00, 282.00, 122.00))
elements.append(box_border("KHỐI CẢNH BÁO & NÚT BẤM", 182.00, 125.00, 282.00, 154.00))

# -------------------------------------------------------------
# ASSEMBLE COMPLETE .kicad_sch FILE
# -------------------------------------------------------------
final_sch = f"""(kicad_sch
\t(version 20260306)
\t(generator "eeschema")
\t(generator_version "10.0")
\t(uuid "{gen_uuid()}")
\t(paper "A4")
\t(title_block
\t\t(title "HỘP ĐEN AIoT THÔNG MINH GHI NHẬN VÀ HỖ TRỢ PHÂN TÍCH SỰ CỐ XE MÁY")
\t\t(date "2026-09-22")
\t\t(rev "REV 2.0 (PRESENTATION A4)")
\t\t(company "BỘ MÔN KỸ THUẬT ĐIỆN TỬ - KHOA ĐIỆN - ĐIỆN TỬ")
\t\t(comment 1 "GVHD: GVC. ThS. NGUYỄN NGÔ LÂM")
\t\t(comment 2 "SVTH: LÊ QUỐC DANH - NGUYỄN ĐỨC TIẾN")
\t\t(comment 3 "ĐỀ TÀI: AIoT Smart Black Box for Motorcycle Accident Analysis")
\t\t(comment 4 "SƠ ĐỒ NGUYÊN LÝ BÁO CÁO (PRESENTATION SCHEMATIC)")
\t)
{all_lib_symbols}
{chr(10).join(elements)}
)
"""

with open(sch_file, "w", encoding="utf-8") as f:
    f.write(final_sch)

print("Successfully written perfected A4 schematic file.")
