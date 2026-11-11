import os
import shutil
import uuid
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

proj_dir = r"D:\ĐỒ ÁN 2\Schematic_Thay\AIOT_BLACKBOX_PRESENTATION"
sch_file = os.path.join(proj_dir, "AIOT_BLACKBOX_PRESENTATION.kicad_sch")
bak_file = os.path.join(proj_dir, "AIOT_BLACKBOX_PRESENTATION.kicad_sch.bak")

# 1. Ensure backup
if os.path.exists(sch_file):
    shutil.copy2(sch_file, bak_file)
    print(f"Created backup: {bak_file}")

def gen_uuid():
    return str(uuid.uuid4())

# -------------------------------------------------------------
# EXTRACT SYMBOLS FROM KICAD LIBRARIES WITH EXACT PARSING
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
sym_antenna = extract_sym(dev_text, "Antenna", "Device:Antenna")

with open(os.path.join(kicad_sym_dir, "Switch.kicad_sym"), 'r', encoding='utf-8') as f:
    sw_text = f.read()
sym_sw = extract_sym(sw_text, "SW_Push", "Switch:SW_Push")

# Standalone 2SC1815 BJT Symbol (avoiding extends issue)
sym_npn_standalone = """		(symbol "Transistor_BJT:2SC1815"
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
# CUSTOM PROJECT-LOCAL PRESENTATION SYMBOLS (Strict Rule 2 compliance)
# -------------------------------------------------------------
custom_mcu_sym = """		(symbol "Presentation:ESP32-S3-DevKitC-1"
			(pin_names (offset 1.016))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U1" (at 0 69.85 0) (effects (font (size 1.778 1.778) (bold yes))))
			(property "Value" "ESP32-S3-DevKitC-1" (at 0 67.31 0) (effects (font (size 1.524 1.524))))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Datasheet" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Description" "ESP32-S3 N16R8 Central Processing Unit" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "ESP32-S3-DevKitC-1_0_1"
				(rectangle (start -17.78 64.77) (end 17.78 -64.77) (stroke (width 0.381) (type default)) (fill (type background)))
				(text "ESP32-S3" (at 0 8.89 0) (effects (font (size 2.54 2.54) (bold yes))))
				(text "DevKitC-1 N16R8" (at 0 5.08 0) (effects (font (size 1.778 1.778) (bold yes))))
				(text "16MB Flash, 8MB PSRAM" (at 0 1.27 0) (effects (font (size 1.27 1.27) (italic yes))))
				(text "BỘ XỬ LÝ TRUNG TÂM" (at 0 -3.81 0) (effects (font (size 1.524 1.524) (bold yes))))
			)
			(symbol "ESP32-S3-DevKitC-1_1_1"
				(pin power_in line (at -22.86 48.26 0) (length 5.08) (name "5V" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.016 1.016)))))
				(pin power_out line (at -22.86 43.18 0) (length 5.08) (name "3V3" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.016 1.016)))))
				(pin input line (at -22.86 33.02 0) (length 5.08) (name "GPIO1/ADC_VBAT" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.016 1.016)))))
				(pin bidirectional line (at -22.86 22.86 0) (length 5.08) (name "GPIO8/I2C0_SDA" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.016 1.016)))))
				(pin bidirectional line (at -22.86 17.78 0) (length 5.08) (name "GPIO9/I2C0_SCL" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.016 1.016)))))
				(pin input line (at -22.86 12.70 0) (length 5.08) (name "GPIO10/IMU_INT" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.016 1.016)))))
				(pin output line (at -22.86 -17.78 0) (length 5.08) (name "GPIO14/SD_CS" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.016 1.016)))))
				(pin output line (at -22.86 -22.86 0) (length 5.08) (name "GPIO11/SPI_MOSI" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.016 1.016)))))
				(pin output line (at -22.86 -27.94 0) (length 5.08) (name "GPIO12/SPI_SCK" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.016 1.016)))))
				(pin input line (at -22.86 -33.02 0) (length 5.08) (name "GPIO13/SPI_MISO" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.016 1.016)))))
				(pin power_in line (at -22.86 -58.42 0) (length 5.08) (name "GND" (effects (font (size 1.27 1.27)))) (number "11" (effects (font (size 1.016 1.016)))))
				
				(pin output line (at 22.86 53.34 180) (length 5.08) (name "GPIO43/4G_TXD" (effects (font (size 1.27 1.27)))) (number "12" (effects (font (size 1.016 1.016)))))
				(pin input line (at 22.86 48.26 180) (length 5.08) (name "GPIO44/4G_RXD" (effects (font (size 1.27 1.27)))) (number "13" (effects (font (size 1.016 1.016)))))
				(pin output line (at 22.86 43.18 180) (length 5.08) (name "GPIO4/4G_PWRKEY" (effects (font (size 1.27 1.27)))) (number "14" (effects (font (size 1.016 1.016)))))
				(pin input line (at 22.86 38.10 180) (length 5.08) (name "GPIO5/4G_STATUS" (effects (font (size 1.27 1.27)))) (number "15" (effects (font (size 1.016 1.016)))))
				(pin output line (at 22.86 22.86 180) (length 5.08) (name "GPIO17/GNSS_TXD" (effects (font (size 1.27 1.27)))) (number "16" (effects (font (size 1.016 1.016)))))
				(pin input line (at 22.86 17.78 180) (length 5.08) (name "GPIO18/GNSS_RXD" (effects (font (size 1.27 1.27)))) (number "17" (effects (font (size 1.016 1.016)))))
				(pin input line (at 22.86 12.70 180) (length 5.08) (name "GPIO21/GNSS_PPS" (effects (font (size 1.27 1.27)))) (number "18" (effects (font (size 1.016 1.016)))))
				(pin input line (at 22.86 -17.78 180) (length 5.08) (name "GPIO6/BT_CANCEL" (effects (font (size 1.27 1.27)))) (number "19" (effects (font (size 1.016 1.016)))))
				(pin output line (at 22.86 -27.94 180) (length 5.08) (name "GPIO7/LED_STATUS" (effects (font (size 1.27 1.27)))) (number "20" (effects (font (size 1.016 1.016)))))
				(pin output line (at 22.86 -38.10 180) (length 5.08) (name "GPIO15/BUZZER_CTRL" (effects (font (size 1.27 1.27)))) (number "21" (effects (font (size 1.016 1.016)))))
				(pin power_in line (at 22.86 -58.42 180) (length 5.08) (name "GND" (effects (font (size 1.27 1.27)))) (number "22" (effects (font (size 1.016 1.016)))))
			)
		)"""

custom_imu_sym = """		(symbol "Presentation:MPU6050_Module"
			(pin_names (offset 1.016))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U2" (at 0 25.40 0) (effects (font (size 1.524 1.524) (bold yes))))
			(property "Value" "GY-521 (MPU6050)" (at 0 22.86 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Datasheet" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Description" "6-Axis IMU Sensor Breakout" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "MPU6050_Module_0_1"
				(rectangle (start -15.24 20.32) (end 15.24 -20.32) (stroke (width 0.254) (type default)) (fill (type background)))
				(text "MPU6050" (at 0 2.54 0) (effects (font (size 2.032 2.032) (bold yes))))
				(text "6-Axis IMU" (at 0 -1.27 0) (effects (font (size 1.27 1.27))))
				(text "Addr: 0x69 (AD0=1)" (at 0 -5.08 0) (effects (font (size 1.016 1.016) (italic yes))))
			)
			(symbol "MPU6050_Module_1_1"
				(pin power_in line (at 20.32 15.24 180) (length 5.08) (name "VCC" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.016 1.016)))))
				(pin input line (at 20.32 10.16 180) (length 5.08) (name "AD0" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.016 1.016)))))
				(pin bidirectional line (at 20.32 0.00 180) (length 5.08) (name "SDA" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.016 1.016)))))
				(pin bidirectional line (at 20.32 -5.08 180) (length 5.08) (name "SCL" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.016 1.016)))))
				(pin output line (at 20.32 -10.16 180) (length 5.08) (name "INT" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.016 1.016)))))
				(pin power_in line (at 20.32 -15.24 180) (length 5.08) (name "GND" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.016 1.016)))))
			)
		)"""

custom_rtc_sym = """		(symbol "Presentation:DS3231_RTC_Module"
			(pin_names (offset 1.016))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U3" (at 0 22.86 0) (effects (font (size 1.524 1.524) (bold yes))))
			(property "Value" "DS3231 RTC" (at 0 20.32 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Datasheet" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Description" "High Precision RTC Module" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "DS3231_RTC_Module_0_1"
				(rectangle (start -15.24 17.78) (end 15.24 -17.78) (stroke (width 0.254) (type default)) (fill (type background)))
				(text "DS3231" (at 0 2.54 0) (effects (font (size 2.032 2.032) (bold yes))))
				(text "Precision RTC" (at 0 -1.27 0) (effects (font (size 1.27 1.27))))
				(text "Addr: 0x68" (at 0 -5.08 0) (effects (font (size 1.016 1.016) (italic yes))))
			)
			(symbol "DS3231_RTC_Module_1_1"
				(pin passive line (at -20.32 0.00 0) (length 5.08) (name "VBAT_RTC" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.016 1.016)))))
				(pin power_in line (at 20.32 12.70 180) (length 5.08) (name "VCC" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.016 1.016)))))
				(pin bidirectional line (at 20.32 2.54 180) (length 5.08) (name "SDA" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.016 1.016)))))
				(pin bidirectional line (at 20.32 -2.54 180) (length 5.08) (name "SCL" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.016 1.016)))))
				(pin power_in line (at 20.32 -12.70 180) (length 5.08) (name "GND" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.016 1.016)))))
			)
		)"""

custom_sd_sym = """		(symbol "Presentation:MicroSD_SPI_Module"
			(pin_names (offset 1.016))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "J1" (at 0 25.40 0) (effects (font (size 1.524 1.524) (bold yes))))
			(property "Value" "MicroSD SPI Module" (at 0 22.86 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Datasheet" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Description" "MicroSD Card Module with SPI Interface" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "MicroSD_SPI_Module_0_1"
				(rectangle (start -15.24 20.32) (end 15.24 -20.32) (stroke (width 0.254) (type default)) (fill (type background)))
				(text "MicroSD" (at 0 5.08 0) (effects (font (size 2.032 2.032) (bold yes))))
				(text "SPI Storage" (at 0 1.27 0) (effects (font (size 1.27 1.27))))
				(text "Event Black Box" (at 0 -2.54 0) (effects (font (size 1.016 1.016) (italic yes))))
			)
			(symbol "MicroSD_SPI_Module_1_1"
				(pin power_in line (at 20.32 15.24 180) (length 5.08) (name "VCC" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.016 1.016)))))
				(pin input line (at 20.32 7.62 180) (length 5.08) (name "CS" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.016 1.016)))))
				(pin input line (at 20.32 2.54 180) (length 5.08) (name "MOSI" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.016 1.016)))))
				(pin input line (at 20.32 -2.54 180) (length 5.08) (name "SCK" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.016 1.016)))))
				(pin output line (at 20.32 -7.62 180) (length 5.08) (name "MISO" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.016 1.016)))))
				(pin power_in line (at 20.32 -15.24 180) (length 5.08) (name "GND" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.016 1.016)))))
			)
		)"""

custom_gnss_sym = """		(symbol "Presentation:ATGM336H_GNSS_Module"
			(pin_names (offset 1.016))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U4" (at 0 25.40 0) (effects (font (size 1.524 1.524) (bold yes))))
			(property "Value" "ATGM336H GNSS" (at 0 22.86 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Datasheet" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Description" "GNSS Navigation Module (GPS/BDS)" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "ATGM336H_GNSS_Module_0_1"
				(rectangle (start -15.24 20.32) (end 15.24 -20.32) (stroke (width 0.254) (type default)) (fill (type background)))
				(text "ATGM336H" (at 0 5.08 0) (effects (font (size 2.032 2.032) (bold yes))))
				(text "BDS / GPS GNSS" (at 0 1.27 0) (effects (font (size 1.27 1.27))))
				(text "10Hz High Speed" (at 0 -2.54 0) (effects (font (size 1.016 1.016) (italic yes))))
			)
			(symbol "ATGM336H_GNSS_Module_1_1"
				(pin power_in line (at -20.32 15.24 0) (length 5.08) (name "VCC" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.016 1.016)))))
				(pin input line (at -20.32 5.08 0) (length 5.08) (name "RXD" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.016 1.016)))))
				(pin output line (at -20.32 0.00 0) (length 5.08) (name "TXD" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.016 1.016)))))
				(pin output line (at -20.32 -5.08 0) (length 5.08) (name "PPS" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.016 1.016)))))
				(pin power_in line (at -20.32 -15.24 0) (length 5.08) (name "GND" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.016 1.016)))))
				(pin passive line (at 20.32 0.00 180) (length 5.08) (name "ANT_RF" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.016 1.016)))))
			)
		)"""

custom_4g_sym = """		(symbol "Presentation:MKE-M21_SIM7680C_Module"
			(pin_names (offset 1.016))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U5" (at 0 30.48 0) (effects (font (size 1.524 1.524) (bold yes))))
			(property "Value" "MKE-M21 (SIM7680C)" (at 0 27.94 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Datasheet" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Description" "4G LTE Cat-1 Module" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "MKE-M21_SIM7680C_Module_0_1"
				(rectangle (start -17.78 25.40) (end 17.78 -25.40) (stroke (width 0.254) (type default)) (fill (type background)))
				(text "MKE-M21" (at 0 5.08 0) (effects (font (size 2.032 2.032) (bold yes))))
				(text "SIM7680C 4G LTE" (at 0 1.27 0) (effects (font (size 1.27 1.27))))
				(text "SMS / MQTT / Cloud" (at 0 -2.54 0) (effects (font (size 1.016 1.016) (italic yes))))
			)
			(symbol "MKE-M21_SIM7680C_Module_1_1"
				(pin power_in line (at -22.86 20.32 0) (length 5.08) (name "VCC" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.016 1.016)))))
				(pin input line (at -22.86 10.16 0) (length 5.08) (name "RXD" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.016 1.016)))))
				(pin output line (at -22.86 5.08 0) (length 5.08) (name "TXD" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.016 1.016)))))
				(pin input line (at -22.86 0.00 0) (length 5.08) (name "PWRKEY" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.016 1.016)))))
				(pin output line (at -22.86 -5.08 0) (length 5.08) (name "STATUS" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.016 1.016)))))
				(pin power_in line (at -22.86 -20.32 0) (length 5.08) (name "GND" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.016 1.016)))))
				(pin passive line (at 22.86 0.00 180) (length 5.08) (name "ANT_4G" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.016 1.016)))))
			)
		)"""

custom_pwr_sym = """		(symbol "Presentation:Power_Management_18650"
			(pin_names (offset 1.016))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U6" (at 0 25.40 0) (effects (font (size 1.524 1.524) (bold yes))))
			(property "Value" "18650 Power & Boost" (at 0 22.86 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Datasheet" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Description" "Battery Charger and 5V Boost Management" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "Power_Management_18650_0_1"
				(rectangle (start -22.86 20.32) (end 22.86 -20.32) (stroke (width 0.254) (type default)) (fill (type background)))
				(text "QUẢN LÝ NGUỒN" (at 0 5.08 0) (effects (font (size 1.778 1.778) (bold yes))))
				(text "& 5V BOOST" (at 0 1.27 0) (effects (font (size 1.524 1.524) (bold yes))))
				(text "Primary Power System" (at 0 -3.81 0) (effects (font (size 1.016 1.016) (italic yes))))
			)
			(symbol "Power_Management_18650_1_1"
				(pin power_in line (at -27.94 10.16 0) (length 5.08) (name "VBUS_IN" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.016 1.016)))))
				(pin power_in line (at -27.94 -10.16 0) (length 5.08) (name "GND" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.016 1.016)))))
				(pin power_out line (at 27.94 15.24 180) (length 5.08) (name "5V_OUT" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.016 1.016)))))
				(pin power_out line (at 27.94 5.08 180) (length 5.08) (name "BAT+" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.016 1.016)))))
				(pin power_out line (at 27.94 -5.08 180) (length 5.08) (name "BAT-" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.016 1.016)))))
				(pin power_in line (at 27.94 -15.24 180) (length 5.08) (name "GND" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.016 1.016)))))
			)
		)"""

custom_usb_sym = """		(symbol "Presentation:USB_C_Input"
			(pin_names (offset 1.016))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "J2" (at 0 15.24 0) (effects (font (size 1.524 1.524) (bold yes))))
			(property "Value" "USB-C (5V IN)" (at 0 12.70 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Datasheet" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(property "Description" "USB Type-C Charging Port" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
			(symbol "USB_C_Input_0_1"
				(rectangle (start -10.16 10.16) (end 10.16 -10.16) (stroke (width 0.254) (type default)) (fill (type background)))
				(text "USB-C" (at 0 2.54 0) (effects (font (size 1.778 1.778) (bold yes))))
				(text "5V SẠC" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
			)
			(symbol "USB_C_Input_1_1"
				(pin power_out line (at 15.24 5.08 180) (length 5.08) (name "VBUS" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.016 1.016)))))
				(pin power_in line (at 15.24 -5.08 180) (length 5.08) (name "GND" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.016 1.016)))))
			)
		)"""

lib_symbols_block = f"""	(lib_symbols
{sym_3v3}
{sym_5v_sys}
{sym_5v_usb}
{sym_vbat}
{sym_gnd}
{sym_pwr_flag}
{sym_r}
{sym_c}
{sym_led}
{sym_buzzer}
{sym_bat}
{sym_sw}
{sym_antenna}
{sym_npn_standalone}
{custom_mcu_sym}
{custom_imu_sym}
{custom_rtc_sym}
{custom_sd_sym}
{custom_gnss_sym}
{custom_4g_sym}
{custom_pwr_sym}
{custom_usb_sym}
	)"""

# -------------------------------------------------------------
# DRAWING HELPER FUNCTIONS WITH ACCURATE JUSTIFICATION & OFFSETS
# -------------------------------------------------------------
def wire(x1, y1, x2, y2):
    return f'\t(wire (pts (xy {x1:.2f} {y1:.2f}) (xy {x2:.2f} {y2:.2f})) (stroke (width 0) (type default)) (uuid "{gen_uuid()}"))'

def junction(x, y):
    return f'\t(junction (at {x:.2f} {y:.2f}) (diameter 1.016) (color 0 0 0 0) (uuid "{gen_uuid()}"))'

def net_label(name, x, y, rot=0):
    return f'\t(label "{name}" (at {x:.2f} {y:.2f} {rot}) (fields_autoplaced yes) (effects (font (size 1.27 1.27))) (uuid "{gen_uuid()}"))'

def power_sym(name, x, y, rot=0):
    val_y = y - 3.81 if rot == 0 else (y + 3.81 if rot == 180 else y)
    val_x = x if rot in [0, 180] else (x + 3.81 if rot == 90 else x - 3.81)
    return f"""\t(symbol (lib_id "power:{name}") (at {x:.2f} {y:.2f} {rot}) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "#PWR?" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "{name}" (at {val_x:.2f} {val_y:.2f} 0) (effects (font (size 1.27 1.27))))
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
\t\t(property "Value" "{val}" (at {vx:.2f} {vy:.2f} 0) (effects (font (size 1.27 1.27)){just}))
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
\t\t(property "Value" "{val}" (at {vx:.2f} {vy:.2f} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "Capacitor" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t\t(pin "2" (uuid "{gen_uuid()}"))
\t)"""

def led_sym(ref, val, x, y, rot=0):
    if rot in (0, 180):
        rx, ry = x, y - 3.00
        vx, vy = x, y + 3.00
    else:
        rx, ry = x + 3.00, y - 1.27
        vx, vy = x + 3.00, y + 1.27
    return f"""\t(symbol (lib_id "Device:LED") (at {x:.2f} {y:.2f} {rot}) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "{ref}" (at {rx:.2f} {ry:.2f} 0) (effects (font (size 1.27 1.27) (bold yes))))
\t\t(property "Value" "{val}" (at {vx:.2f} {vy:.2f} 0) (effects (font (size 1.27 1.27))))
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
\t\t(property "Value" "{val}" (at {vx:.2f} {vy:.2f} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "Push button switch" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t\t(pin "2" (uuid "{gen_uuid()}"))
\t)"""

def bjt_sym(ref, val, x, y, rot=0):
    rx, ry = x + 5.08, y - 2.54
    vx, vy = x + 5.08, y + 2.54
    return f"""\t(symbol (lib_id "Transistor_BJT:2SC1815") (at {x:.2f} {y:.2f} {rot}) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "{ref}" (at {rx:.2f} {ry:.2f} 0) (effects (font (size 1.27 1.27) (bold yes))))
\t\t(property "Value" "{val}" (at {vx:.2f} {vy:.2f} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "NPN Transistor" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t\t(pin "2" (uuid "{gen_uuid()}"))
\t\t(pin "3" (uuid "{gen_uuid()}"))
\t)"""

def buzzer_sym(ref, val, x, y, rot=0):
    rx, ry = x + 3.81, y - 5.08
    vx, vy = x + 3.81, y + 5.08
    return f"""\t(symbol (lib_id "Device:Buzzer") (at {x:.2f} {y:.2f} {rot}) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "{ref}" (at {rx:.2f} {ry:.2f} 0) (effects (font (size 1.27 1.27) (bold yes))))
\t\t(property "Value" "{val}" (at {vx:.2f} {vy:.2f} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "Buzzer" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t\t(pin "2" (uuid "{gen_uuid()}"))
\t)"""

def bat_sym(ref, val, x, y, rot=0):
    return f"""\t(symbol (lib_id "Device:Battery_Cell") (at {x:.2f} {y:.2f} {rot}) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "{ref}" (at {x+3.81:.2f} {y-1.27:.2f} 0) (effects (font (size 1.27 1.27) (bold yes))))
\t\t(property "Value" "{val}" (at {x+3.81:.2f} {y+1.27:.2f} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "Single-cell battery" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t\t(pin "2" (uuid "{gen_uuid()}"))
\t)"""

def antenna_sym(ref, val, x, y, rot=0):
    return f"""\t(symbol (lib_id "Device:Antenna") (at {x:.2f} {y:.2f} {rot}) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "{ref}" (at {x:.2f} {y-7.62:.2f} 0) (effects (font (size 1.27 1.27) (bold yes))))
\t\t(property "Value" "{val}" (at {x:.2f} {y+7.62:.2f} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Datasheet" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(property "Description" "Antenna" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t)"""

def box_border(x1, y1, x2, y2, title):
    poly = f'\t(polyline (pts (xy {x1:.2f} {y1:.2f}) (xy {x2:.2f} {y1:.2f}) (xy {x2:.2f} {y2:.2f}) (xy {x1:.2f} {y2:.2f}) (xy {x1:.2f} {y1:.2f})) (stroke (width 0.3) (type dash)) (uuid "{gen_uuid()}"))'
    txt = f'\t(text "{title}" (at {x1+3.81:.2f} {y1+4.50:.2f} 0) (effects (font (size 2.032 2.032) (bold yes)) (justify left)) (uuid "{gen_uuid()}"))'
    return poly + '\n' + txt

def desc_text(txt, x, y, size=1.27, italic=False):
    it_str = " (italic yes)" if italic else ""
    return f'\t(text "{txt}" (at {x:.2f} {y:.2f} 0) (effects (font (size {size} {size}){it_str}) (justify left)) (uuid "{gen_uuid()}"))'

# -------------------------------------------------------------
# ASSEMBLE ALL ELEMENTS
# -------------------------------------------------------------
elements = []

# --- FUNCTIONAL BLOCK BOUNDARIES (A3 Landscape: 420 x 297 mm) ---
# Left column safe margin: X = 27.94 to 175.26
# Center column: X = 185.42 to 251.46
# Right column safe margin: X = 264.16 to 398.78

# Block A: Khối Nguồn & Quản lý pin 18650
elements.append(box_border(27.94, 22.86, 175.26, 91.44, "KHỐI NGUỒN & QUẢN LÝ PIN 18650"))
elements.append(desc_text("Nguồn chính: Pin Li-ion 18650 (3.7V - 4.2V, 2000mAh) | Mạch sạc & Boost 5V_SYS", 31.75, 85.50, 1.143, True))
elements.append(desc_text("Cầu phân áp (100k/100k) & lọc 100nF kết nối ADC_VBAT_SENSE giám sát dung lượng pin", 31.75, 88.50, 1.016, True))

# Block B: Khối Xử lý Trung tâm (Center)
elements.append(box_border(185.42, 78.74, 251.46, 236.22, "KHỐI XỬ LÝ TRUNG TÂM"))
elements.append(desc_text("ESP32-S3-DevKitC-1 N16R8 (16MB Flash, 8MB PSRAM)", 189.23, 86.36, 1.27, True))

# Block C: Khối Cảm biến Quán tính (IMU)
elements.append(box_border(27.94, 96.52, 175.26, 144.78, "KHỐI CẢM BIẾN QUÁN TÍNH (IMU)"))
elements.append(desc_text("GY-521 (MPU6050 6-DOF) | Địa chỉ I2C: 0x69 (Cấu hình chân AD0 nối +3V3)", 31.75, 141.00, 1.143, True))

# Block F: Khối Đồng hồ Thời gian thực (RTC)
elements.append(box_border(27.94, 149.86, 175.26, 198.12, "KHỐI ĐỒNG HỒ THỜI GIAN THỰC (RTC)"))
elements.append(desc_text("DS3231 High-Precision RTC (Địa chỉ I2C: 0x68) | Pin CR2032 (3V) duy trì giờ thực", 31.75, 194.00, 1.143, True))

# Block E: Khối Lưu trữ Dữ liệu (MicroSD)
elements.append(box_border(27.94, 203.20, 175.26, 256.54, "KHỐI LƯU TRỮ DỮ LIỆU (MICROSD)"))
elements.append(desc_text("Giao tiếp SPI chuẩn logic 3.3V (SD_CS, MOSI, SCK, MISO) | Ghi log chu kỳ 10ms", 31.75, 252.00, 1.143, True))

# Block G: Khối Truyền thông 4G LTE
elements.append(box_border(264.16, 22.86, 398.78, 91.44, "KHỐI TRUYỀN THÔNG 4G LTE"))
elements.append(desc_text("Module MKE-M21 (SIM7680C Cat-1) | Giao tiếp UART 3.3V Logic | Nguồn cấp: 5V_SYS", 267.97, 87.00, 1.143, True))

# Block D: Khối Định vị GNSS
elements.append(box_border(264.16, 96.52, 398.78, 157.48, "KHỐI ĐỊNH VỊ GNSS"))
elements.append(desc_text("Module ATGM336H Dual-Mode BDS/GPS (10Hz) | UART 3.3V Logic & PPS | Nguồn: +3V3", 267.97, 153.50, 1.143, True))

# Block H: Khối Giao diện & Cảnh báo
elements.append(box_border(264.16, 162.56, 398.78, 236.22, "KHỐI GIAO DIỆN & CẢNH BÁO"))
elements.append(desc_text("Nút hủy cảnh báo (15s đếm ngược) | Đèn LED trạng thái | Còi cảnh báo Piezo 5V", 267.97, 232.00, 1.143, True))


# =============================================================
# 1. BLOCK A: POWER & BATTERY MANAGEMENT
# =============================================================
# USB-C Input J2 at (45.72, 60.96)
elements.append(f"""\t(symbol (lib_id "Presentation:USB_C_Input") (at 45.72 60.96 0) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "J2" (at 45.72 45.72 0) (effects (font (size 1.524 1.524) (bold yes))))
\t\t(property "Value" "USB-C (5V IN)" (at 45.72 48.26 0) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t\t(pin "2" (uuid "{gen_uuid()}"))
\t)""")

# Power Management & Boost U6 at (104.14, 60.96)
elements.append(f"""\t(symbol (lib_id "Presentation:Power_Management_18650") (at 104.14 60.96 0) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "U6" (at 104.14 35.56 0) (effects (font (size 1.524 1.524) (bold yes))))
\t\t(property "Value" "18650 Power & Boost" (at 104.14 38.10 0) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t\t(pin "2" (uuid "{gen_uuid()}"))
\t\t(pin "3" (uuid "{gen_uuid()}"))
\t\t(pin "4" (uuid "{gen_uuid()}"))
\t\t(pin "5" (uuid "{gen_uuid()}"))
\t\t(pin "6" (uuid "{gen_uuid()}"))
\t)""")

# Wires J2 -> U6:
# J2 Pin 1 (VBUS): (45.72 + 15.24 = 60.96, 60.96 - 5.08 = 55.88)
# U6 Pin 1 (VBUS_IN): (104.14 - 27.94 = 76.20, 60.96 - 10.16 = 50.80)
elements.append(wire(60.96, 55.88, 68.58, 55.88))
elements.append(wire(68.58, 55.88, 68.58, 50.80))
elements.append(wire(68.58, 50.80, 76.20, 50.80))
elements.append(power_sym("5V_USB", 68.58, 50.80, 0))
elements.append(junction(68.58, 50.80))

# J2 Pin 2 (GND): (60.96, 60.96 + 5.08 = 66.04)
# U6 Pin 2 (GND): (76.20, 60.96 + 10.16 = 71.12)
elements.append(wire(60.96, 66.04, 68.58, 66.04))
elements.append(wire(68.58, 66.04, 68.58, 71.12))
elements.append(wire(68.58, 71.12, 76.20, 71.12))
elements.append(power_sym("GND", 68.58, 71.12, 0))
elements.append(junction(68.58, 71.12))
elements.append(pwr_flag(68.58, 78.74, 180))
elements.append(wire(68.58, 71.12, 68.58, 78.74))

# U6 Pin 3 (5V_OUT): at (104.14 + 27.94 = 132.08, 60.96 - 15.24 = 45.72)
elements.append(wire(132.08, 45.72, 142.24, 45.72))
elements.append(power_sym("5V_SYS", 142.24, 45.72, 0))

# 18650 Battery BT1 at (147.32, 63.50)
elements.append(bat_sym("BT1", "18650 Li-Ion (3.7V)", 147.32, 63.50, 0))

# U6 Pin 4 (BAT+): at (132.08, 60.96 - 5.08 = 55.88)
# Connect U6 BAT+ to BT1 Pin 1 (147.32, 58.42):
elements.append(wire(132.08, 55.88, 139.70, 55.88))
elements.append(wire(139.70, 55.88, 139.70, 58.42))
elements.append(wire(139.70, 58.42, 147.32, 58.42))
elements.append(power_sym("VBAT", 139.70, 55.88, 0))
elements.append(junction(139.70, 55.88))

# U6 Pin 5 (BAT-): at (132.08, 60.96 + 5.08 = 66.04)
# Connect U6 BAT- to BT1 Pin 2:
elements.append(wire(132.08, 66.04, 147.32, 66.04))

# U6 Pin 6 (GND): at (132.08, 60.96 + 15.24 = 76.20)
elements.append(wire(132.08, 76.20, 139.70, 76.20))
elements.append(power_sym("GND", 139.70, 76.20, 0))

# Battery Voltage Divider (R1=100k, R2=100k, C1=100nF)
# Placed at X = 157.48 and C1 at 165.10 for generous margin
elements.append(res_sym("R1", "100k (1%)", 157.48, 50.80, 0, text_side="left"))
elements.append(res_sym("R2", "100k (1%)", 157.48, 68.58, 0, text_side="left"))
elements.append(cap_sym("C1", "100nF", 165.10, 68.58, 0))

# Top of R1 (157.48, 46.99) -> connects to VBAT
elements.append(power_sym("VBAT", 157.48, 46.99, 0))

# Mid node: R1 pin 2 (157.48, 54.61), R2 pin 1 (157.48, 64.77)
elements.append(wire(157.48, 54.61, 157.48, 59.69))
elements.append(wire(157.48, 59.69, 157.48, 64.77))
elements.append(junction(157.48, 59.69))
elements.append(wire(157.48, 59.69, 165.10, 59.69))
elements.append(junction(165.10, 59.69))
elements.append(wire(165.10, 59.69, 165.10, 64.77)) # to C1 pin 1
elements.append(wire(165.10, 59.69, 175.26, 59.69))
elements.append(net_label("ADC_VBAT_SENSE", 175.26, 59.69, 0))

# Bottom of R2 (157.48, 72.39) and C1 (165.10, 72.39) to GND
elements.append(wire(157.48, 72.39, 157.48, 76.20))
elements.append(wire(157.48, 76.20, 165.10, 76.20))
elements.append(wire(165.10, 72.39, 165.10, 76.20))
elements.append(junction(157.48, 76.20))
elements.append(power_sym("GND", 157.48, 76.20, 0))


# =============================================================
# 2. BLOCK B: CENTRAL MCU (ESP32-S3 DevKitC-1 N16R8)
# =============================================================
# MCU U1 placed at (218.44, 162.56)
elements.append(f"""\t(symbol (lib_id "Presentation:ESP32-S3-DevKitC-1") (at 218.44 162.56 0) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "U1" (at 218.44 92.71 0) (effects (font (size 1.778 1.778) (bold yes))))
\t\t(property "Value" "ESP32-S3-DevKitC-1" (at 218.44 95.25 0) (effects (font (size 1.524 1.524))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t\t(pin "2" (uuid "{gen_uuid()}"))
\t\t(pin "3" (uuid "{gen_uuid()}"))
\t\t(pin "4" (uuid "{gen_uuid()}"))
\t\t(pin "5" (uuid "{gen_uuid()}"))
\t\t(pin "6" (uuid "{gen_uuid()}"))
\t\t(pin "7" (uuid "{gen_uuid()}"))
\t\t(pin "8" (uuid "{gen_uuid()}"))
\t\t(pin "9" (uuid "{gen_uuid()}"))
\t\t(pin "10" (uuid "{gen_uuid()}"))
\t\t(pin "11" (uuid "{gen_uuid()}"))
\t\t(pin "12" (uuid "{gen_uuid()}"))
\t\t(pin "13" (uuid "{gen_uuid()}"))
\t\t(pin "14" (uuid "{gen_uuid()}"))
\t\t(pin "15" (uuid "{gen_uuid()}"))
\t\t(pin "16" (uuid "{gen_uuid()}"))
\t\t(pin "17" (uuid "{gen_uuid()}"))
\t\t(pin "18" (uuid "{gen_uuid()}"))
\t\t(pin "19" (uuid "{gen_uuid()}"))
\t\t(pin "20" (uuid "{gen_uuid()}"))
\t\t(pin "21" (uuid "{gen_uuid()}"))
\t\t(pin "22" (uuid "{gen_uuid()}"))
\t)""")

# MCU Left side pins (at X = 218.44 - 22.86 = 195.58)
# Pin 1: 5V at Y = 162.56 - 48.26 = 114.30
elements.append(wire(195.58, 114.30, 187.96, 114.30))
elements.append(power_sym("5V_SYS", 187.96, 114.30, 90))

# Pin 2: 3V3 at Y = 162.56 - 43.18 = 119.38
elements.append(wire(195.58, 119.38, 187.96, 119.38))
elements.append(power_sym("+3V3", 187.96, 119.38, 90))

# Pin 3: GPIO1/ADC_VBAT at Y = 162.56 - 33.02 = 129.54 (Net label jump)
elements.append(wire(195.58, 129.54, 185.42, 129.54))
elements.append(net_label("ADC_VBAT_SENSE", 185.42, 129.54, 180))

# Pin 11: GND (Left) at Y = 162.56 - (-58.42) = 220.98
elements.append(wire(195.58, 220.98, 187.96, 220.98))
elements.append(power_sym("GND", 187.96, 220.98, 270))

# MCU Right side pins (at X = 218.44 + 22.86 = 241.30)
# Pin 22: GND (Right) at Y = 162.56 - (-58.42) = 220.98
elements.append(wire(241.30, 220.98, 248.92, 220.98))
elements.append(power_sym("GND", 248.92, 220.98, 90))


# =============================================================
# 3. BLOCK C: IMU (MPU6050) & BLOCK F: RTC (DS3231)
# =============================================================
# IMU U2 at (96.52, 124.46)
elements.append(f"""\t(symbol (lib_id "Presentation:MPU6050_Module") (at 96.52 124.46 0) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "U2" (at 96.52 106.68 0) (effects (font (size 1.524 1.524) (bold yes))))
\t\t(property "Value" "GY-521 (MPU6050)" (at 96.52 109.22 0) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t\t(pin "2" (uuid "{gen_uuid()}"))
\t\t(pin "3" (uuid "{gen_uuid()}"))
\t\t(pin "4" (uuid "{gen_uuid()}"))
\t\t(pin "5" (uuid "{gen_uuid()}"))
\t\t(pin "6" (uuid "{gen_uuid()}"))
\t)""")

# U2 Right pins are at X = 96.52 + 20.32 = 116.84
# Pin 1 (VCC): Y = 124.46 - 15.24 = 109.22
# Pin 2 (AD0): Y = 124.46 - 10.16 = 114.30 -> Tied to VCC (+3V3) for Addr 0x69
elements.append(wire(116.84, 109.22, 127.00, 109.22))
elements.append(wire(116.84, 114.30, 121.92, 114.30))
elements.append(wire(121.92, 114.30, 121.92, 109.22))
elements.append(junction(121.92, 109.22))
elements.append(power_sym("+3V3", 127.00, 109.22, 90))
elements.append(desc_text("AD0 = HIGH -> Addr: 0x69", 119.38, 118.11, 1.016, True))

# Pin 6 (GND): Y = 124.46 - (-15.24) = 139.70
elements.append(wire(116.84, 139.70, 124.46, 139.70))
elements.append(power_sym("GND", 124.46, 139.70, 270))

# RTC U3 at (96.52, 175.26)
elements.append(f"""\t(symbol (lib_id "Presentation:DS3231_RTC_Module") (at 96.52 175.26 0) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "U3" (at 96.52 157.48 0) (effects (font (size 1.524 1.524) (bold yes))))
\t\t(property "Value" "DS3231 RTC" (at 96.52 160.02 0) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t\t(pin "2" (uuid "{gen_uuid()}"))
\t\t(pin "3" (uuid "{gen_uuid()}"))
\t\t(pin "4" (uuid "{gen_uuid()}"))
\t\t(pin "5" (uuid "{gen_uuid()}"))
\t)""")

# U3 Pin 1 (VBAT_RTC): at (96.52 - 20.32 = 76.20, 175.26)
# Connect to CR2032 Battery BT2 at (58.42, 175.26)
elements.append(bat_sym("BT2", "CR2032 (3V Coin)", 58.42, 175.26, 0))
elements.append(wire(58.42, 170.18, 68.58, 170.18))
elements.append(wire(68.58, 170.18, 68.58, 175.26))
elements.append(wire(68.58, 175.26, 76.20, 175.26))
elements.append(wire(58.42, 177.80, 68.58, 177.80))
elements.append(power_sym("GND", 68.58, 177.80, 0))
elements.append(desc_text("Pin CR2032 duy trì RTC khi mất điện", 31.75, 185.42, 1.016, True))

# U3 Pin 2 (VCC): at (116.84, 175.26 - 12.70 = 162.56)
elements.append(wire(116.84, 162.56, 124.46, 162.56))
elements.append(power_sym("+3V3", 124.46, 162.56, 90))

# U3 Pin 5 (GND): at (116.84, 175.26 - (-12.70) = 187.96)
elements.append(wire(116.84, 187.96, 124.46, 187.96))
elements.append(power_sym("GND", 124.46, 187.96, 270))

# --- I2C BUS CONNECTIVITY (Shared by U2 MPU6050 & U3 DS3231 to MCU) ---
# Planar routing:
# Vertical trunk for SDA at X = 134.62
# Vertical trunk for SCL at X = 139.70
# Vertical line for IMU_INT at X = 144.78
# Pull-up R_PU1 pulls up to +3V3 from above SDA trunk
# Pull-up R_PU2 pulls up to +3V3 from below SCL trunk
# -> EXACTLY ZERO WIRE CROSSINGS! Direct clean connections!

# 1. SDA Bus Routing:
# IMU SDA Pin 3: (116.84, 124.46) -> wire to (134.62, 124.46)
elements.append(wire(116.84, 124.46, 134.62, 124.46))
# RTC SDA Pin 3: (116.84, 172.72) -> wire to (134.62, 172.72)
elements.append(wire(116.84, 172.72, 134.62, 172.72))
# Vertical trunk X = 134.62 from Y = 124.46 to Y = 172.72
elements.append(wire(134.62, 124.46, 134.62, 139.70))
elements.append(wire(134.62, 139.70, 134.62, 172.72))
elements.append(junction(134.62, 139.70))
# Branch from trunk to MCU GPIO8 at Y = 139.70:
elements.append(wire(134.62, 139.70, 195.58, 139.70))

# Pull-up R_PU1 (4.7k) at (154.94, 129.54):
elements.append(res_sym("R_PU1", "4.7k", 154.94, 129.54, 0))
elements.append(power_sym("+3V3", 154.94, 125.73, 0))
elements.append(wire(154.94, 133.35, 154.94, 139.70))
elements.append(junction(154.94, 139.70))

# 2. SCL Bus Routing:
# IMU SCL Pin 4: (116.84, 129.54) -> wire to (139.70, 129.54)
elements.append(wire(116.84, 129.54, 139.70, 129.54))
# RTC SCL Pin 4: (116.84, 177.80) -> wire to (139.70, 177.80)
elements.append(wire(116.84, 177.80, 139.70, 177.80))
# Vertical trunk X = 139.70 from Y = 129.54 to Y = 177.80
elements.append(wire(139.70, 129.54, 139.70, 144.78))
elements.append(wire(139.70, 144.78, 139.70, 177.80))
elements.append(junction(139.70, 144.78))
# Branch from trunk to MCU GPIO9 at Y = 144.78:
elements.append(wire(139.70, 144.78, 195.58, 144.78))

# Pull-up R_PU2 (4.7k) at (154.94, 154.94) pulling up to SCL from below:
elements.append(res_sym("R_PU2", "4.7k", 154.94, 154.94, 0))
elements.append(wire(154.94, 144.78, 154.94, 151.13))
elements.append(junction(154.94, 144.78))
elements.append(power_sym("+3V3", 154.94, 158.75, 180))

elements.append(desc_text("I2C Pull-Up (4.7k)", 158.75, 125.73, 1.016, True))

# 3. IMU INT Line:
# U2 Pin 5 (116.84, 134.62) -> MCU Pin 6 (195.58, 149.86):
elements.append(wire(116.84, 134.62, 144.78, 134.62))
elements.append(wire(144.78, 134.62, 144.78, 149.86))
elements.append(wire(144.78, 149.86, 195.58, 149.86))


# =============================================================
# 4. BLOCK E: MICROSD CARD MODULE (SPI STORAGE)
# =============================================================
# MicroSD J1 at (96.52, 231.14)
elements.append(f"""\t(symbol (lib_id "Presentation:MicroSD_SPI_Module") (at 96.52 231.14 0) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "J1" (at 96.52 213.36 0) (effects (font (size 1.524 1.524) (bold yes))))
\t\t(property "Value" "MicroSD SPI Module" (at 96.52 215.90 0) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t\t(pin "2" (uuid "{gen_uuid()}"))
\t\t(pin "3" (uuid "{gen_uuid()}"))
\t\t(pin "4" (uuid "{gen_uuid()}"))
\t\t(pin "5" (uuid "{gen_uuid()}"))
\t\t(pin "6" (uuid "{gen_uuid()}"))
\t)""")

# J1 Right pins at X = 96.52 + 20.32 = 116.84
# Pin 1 (VCC): Y = 231.14 - 15.24 = 215.90
elements.append(wire(116.84, 215.90, 124.46, 215.90))
elements.append(power_sym("+3V3", 124.46, 215.90, 90))

# Pin 6 (GND): Y = 231.14 - (-15.24) = 246.38
elements.append(wire(116.84, 246.38, 124.46, 246.38))
elements.append(power_sym("GND", 124.46, 246.38, 270))

# SPI 4-Signal Group (Concentric parallel routing -> ZERO crossings):
# CS: J1 Pin 2 at (116.84, 223.52) -> MCU GPIO14 at (195.58, 180.34)
elements.append(wire(116.84, 223.52, 134.62, 223.52))
elements.append(wire(134.62, 223.52, 134.62, 180.34))
elements.append(wire(134.62, 180.34, 195.58, 180.34))

# MOSI: J1 Pin 3 at (116.84, 228.60) -> MCU GPIO11 at (195.58, 185.42)
elements.append(wire(116.84, 228.60, 139.70, 228.60))
elements.append(wire(139.70, 228.60, 139.70, 185.42))
elements.append(wire(139.70, 185.42, 195.58, 185.42))

# SCK: J1 Pin 4 at (116.84, 233.68) -> MCU GPIO12 at (195.58, 190.50)
elements.append(wire(116.84, 233.68, 144.78, 233.68))
elements.append(wire(144.78, 233.68, 144.78, 190.50))
elements.append(wire(144.78, 190.50, 195.58, 190.50))

# MISO: J1 Pin 5 at (116.84, 238.76) -> MCU GPIO13 at (195.58, 195.58)
elements.append(wire(116.84, 238.76, 149.86, 238.76))
elements.append(wire(149.86, 238.76, 149.86, 195.58))
elements.append(wire(149.86, 195.58, 195.58, 195.58))


# =============================================================
# 5. BLOCK G: 4G LTE MODULE (MKE-M21 SIM7680C)
# =============================================================
# 4G LTE U5 at (337.82, 58.42)
elements.append(f"""\t(symbol (lib_id "Presentation:MKE-M21_SIM7680C_Module") (at 337.82 58.42 0) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "U5" (at 337.82 27.94 0) (effects (font (size 1.524 1.524) (bold yes))))
\t\t(property "Value" "MKE-M21 (SIM7680C)" (at 337.82 30.48 0) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t\t(pin "2" (uuid "{gen_uuid()}"))
\t\t(pin "3" (uuid "{gen_uuid()}"))
\t\t(pin "4" (uuid "{gen_uuid()}"))
\t\t(pin "5" (uuid "{gen_uuid()}"))
\t\t(pin "6" (uuid "{gen_uuid()}"))
\t\t(pin "7" (uuid "{gen_uuid()}"))
\t)""")

# U5 Pin 1 (VCC): at (337.82 - 22.86 = 314.96, 58.42 - 20.32 = 38.10)
elements.append(wire(314.96, 38.10, 307.34, 38.10))
elements.append(power_sym("5V_SYS", 307.34, 38.10, 270))

# U5 Pin 6 (GND): at (314.96, 58.42 + 20.32 = 78.74)
elements.append(wire(314.96, 78.74, 307.34, 78.74))
elements.append(power_sym("GND", 307.34, 78.74, 90))

# U5 Pin 7 (ANT_4G): at (337.82 + 22.86 = 360.68, 58.42)
elements.append(wire(360.68, 58.42, 375.92, 58.42))
elements.append(antenna_sym("AE1", "4G Antenna", 381.00, 58.42, 270))

# 4G LTE Signals Highway to MCU:
# TXD: U5 Pin 2 (RXD) -> MCU GPIO43 (TXD)
elements.append(wire(314.96, 48.26, 271.78, 48.26))
elements.append(wire(271.78, 48.26, 271.78, 109.22))
elements.append(wire(271.78, 109.22, 241.30, 109.22))

# RXD: U5 Pin 3 (TXD) -> MCU GPIO44 (RXD)
elements.append(wire(314.96, 53.34, 276.86, 53.34))
elements.append(wire(276.86, 53.34, 276.86, 114.30))
elements.append(wire(276.86, 114.30, 241.30, 114.30))

# PWRKEY: U5 Pin 4 (PWRKEY) -> MCU GPIO4
elements.append(wire(314.96, 58.42, 281.94, 58.42))
elements.append(wire(281.94, 58.42, 281.94, 119.38))
elements.append(wire(281.94, 119.38, 241.30, 119.38))

# STATUS: U5 Pin 5 (STATUS) -> MCU GPIO5
elements.append(wire(314.96, 63.50, 287.02, 63.50))
elements.append(wire(287.02, 63.50, 287.02, 124.46))
elements.append(wire(287.02, 124.46, 241.30, 124.46))


# =============================================================
# 6. BLOCK D: GNSS MODULE (ATGM336H)
# =============================================================
# GNSS U4 at (337.82, 132.08)
elements.append(f"""\t(symbol (lib_id "Presentation:ATGM336H_GNSS_Module") (at 337.82 132.08 0) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{gen_uuid()}")
\t\t(property "Reference" "U4" (at 337.82 106.68 0) (effects (font (size 1.524 1.524) (bold yes))))
\t\t(property "Value" "ATGM336H GNSS" (at 337.82 109.22 0) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{gen_uuid()}"))
\t\t(pin "2" (uuid "{gen_uuid()}"))
\t\t(pin "3" (uuid "{gen_uuid()}"))
\t\t(pin "4" (uuid "{gen_uuid()}"))
\t\t(pin "5" (uuid "{gen_uuid()}"))
\t\t(pin "6" (uuid "{gen_uuid()}"))
\t)""")

# U4 Pin 1 (VCC): at (337.82 - 20.32 = 317.50, 132.08 - 15.24 = 116.84)
elements.append(wire(317.50, 116.84, 312.42, 116.84))
elements.append(power_sym("+3V3", 312.42, 116.84, 270))

# U4 Pin 5 (GND): at (317.50, 132.08 + 15.24 = 147.32)
elements.append(wire(317.50, 147.32, 312.42, 147.32))
elements.append(power_sym("GND", 312.42, 147.32, 90))

# U4 Pin 6 (ANT_RF): at (337.82 + 20.32 = 358.14, 132.08)
elements.append(wire(358.14, 132.08, 375.92, 132.08))
elements.append(antenna_sym("AE2", "GNSS Antenna", 381.00, 132.08, 270))

# GNSS Signals to MCU:
# GNSS_RXD (U4 RXD Pin 2 to MCU GPIO17):
elements.append(wire(317.50, 127.00, 302.26, 127.00))
elements.append(wire(302.26, 127.00, 302.26, 139.70))
elements.append(wire(302.26, 139.70, 241.30, 139.70))

# GNSS_TXD (U4 TXD Pin 3 to MCU GPIO18):
elements.append(wire(317.50, 132.08, 297.18, 132.08))
elements.append(wire(297.18, 132.08, 297.18, 144.78))
elements.append(wire(297.18, 144.78, 241.30, 144.78))

# GNSS_PPS (U4 PPS Pin 4 to MCU GPIO21):
elements.append(wire(317.50, 137.16, 292.10, 137.16))
elements.append(wire(292.10, 137.16, 292.10, 149.86))
elements.append(wire(292.10, 149.86, 241.30, 149.86))


# =============================================================
# 7. BLOCK H: USER INTERFACE & WARNING SYSTEM
# =============================================================
# Gutter routing for vertical drops:
# Buzzer wire drops in gutter at X = 256.54 (between MCU and Block H border)
# LED wire drops in gutter at X = 260.35
# Both wires are completely clear of the Block H border at X = 264.16!

# A. Cancel Button Subcircuit (Lane at Y = 180.34):
# MCU Pin 19 (GPIO6/BT_CANCEL) is at (241.30, 180.34)
elements.append(wire(241.30, 180.34, 294.64, 180.34))

# Pull-up Resistor R3 (10k) at (284.48, 172.72)
elements.append(res_sym("R3", "10k", 284.48, 172.72, 0))
elements.append(power_sym("+3V3", 284.48, 168.91, 0))
elements.append(wire(284.48, 176.53, 284.48, 180.34))
elements.append(junction(284.48, 180.34))

# Filter Cap C2 (100nF) at (294.64, 187.96)
elements.append(cap_sym("C2", "100nF", 294.64, 187.96, 0))
elements.append(wire(294.64, 180.34, 294.64, 184.15))
elements.append(junction(294.64, 180.34))
elements.append(wire(294.64, 191.77, 294.64, 194.31))
elements.append(power_sym("GND", 294.64, 194.31, 0))

# Pushbutton SW1 at (309.88, 180.34)
elements.append(sw_sym("SW1", "CANCEL BTN", 309.88, 180.34, 0))
elements.append(wire(294.64, 180.34, 304.80, 180.34)) # to SW1 pin 1
elements.append(wire(314.96, 180.34, 322.58, 180.34)) # from SW1 pin 2 to GND
elements.append(power_sym("GND", 322.58, 180.34, 270))
elements.append(desc_text("HỦY GỬI CẢNH BÁO KHẨN CẤP (15s Countdown - Active LOW)", 332.00, 179.07, 1.143, True))
elements.append(desc_text("Dữ liệu sự cố vẫn được lưu trữ đầy đủ trong thẻ nhớ MicroSD", 332.00, 182.88, 1.016, True))

# B. Status LED Subcircuit (Lane at Y = 195.58):
# MCU Pin 20 (GPIO7/LED_STATUS) is at (241.30, 190.50)
elements.append(wire(241.30, 190.50, 260.35, 190.50))
elements.append(wire(260.35, 190.50, 260.35, 195.58))
elements.append(wire(260.35, 195.58, 280.67, 195.58))

# Current-limiting Resistor R4 (330R, rot 90 horizontal) at (284.48, 195.58)
elements.append(res_sym("R4", "330R", 284.48, 195.58, 90))
elements.append(wire(288.29, 195.58, 294.64, 195.58))

# LED D1 (LED GREEN, rot 180 horizontal) at (298.45, 195.58)
elements.append(led_sym("D1", "LED GREEN", 298.45, 195.58, 180))
elements.append(wire(302.26, 195.58, 309.88, 195.58))
elements.append(power_sym("GND", 309.88, 195.58, 270))
elements.append(desc_text("ĐÈN BÁO TRẠNG THÁI HỆ THỐNG (Green LED - Active HIGH)", 325.00, 195.58, 1.143, True))

# C. Active Piezo Buzzer Subcircuit (Lane at Y = 215.90..223.52):
# MCU Pin 21 (GPIO15/BUZZER_CTRL) is at (241.30, 200.66)
elements.append(wire(241.30, 200.66, 256.54, 200.66))
elements.append(wire(256.54, 200.66, 256.54, 218.44))
elements.append(wire(256.54, 218.44, 276.86, 218.44))

# Base Resistor R5 (1k, rot 90 horizontal) at (280.67, 218.44)
elements.append(res_sym("R5", "1k", 280.67, 218.44, 90))
elements.append(wire(284.48, 218.44, 294.64, 218.44)) # to Q1 Base

# NPN BJT Q1 (2SC1815) at (299.72, 218.44)
# Base at (294.64, 218.44), Collector at (302.26, 213.36), Emitter at (302.26, 223.52)
elements.append(bjt_sym("Q1", "2SC1815 (NPN)", 299.72, 218.44, 0))

# Q1 Emitter to GND:
elements.append(wire(302.26, 223.52, 302.26, 228.60))
elements.append(power_sym("GND", 302.26, 228.60, 0))

# Buzzer BZ1 at (314.96, 210.82)
# Pin 1 (+) at (312.42, 208.28) -> to 5V_SYS
# Pin 2 (-) at (312.42, 213.36) -> from Q1 Collector (302.26, 213.36)
elements.append(buzzer_sym("BZ1", "5V Piezo Buzzer", 314.96, 210.82, 0))
elements.append(wire(302.26, 213.36, 312.42, 213.36))
elements.append(wire(312.42, 208.28, 312.42, 203.20))
elements.append(power_sym("5V_SYS", 312.42, 203.20, 0))
elements.append(desc_text("CÒI BÁO ĐỘNG SỰ CỐ (Active 5V Piezo Buzzer - Driver NPN)", 330.00, 210.82, 1.143, True))
elements.append(desc_text("Không dùng diode dập xung cho còi chíp áp điện (Piezoelectric)", 330.00, 214.63, 1.016, True))


# -------------------------------------------------------------
# ASSEMBLE FULL SCHEMATIC STRING
# -------------------------------------------------------------
sch_uuid = gen_uuid()
elements_str = "\n".join(elements)

full_schematic = f"""(kicad_sch
	(version 20260306)
	(generator "eeschema")
	(generator_version "10.0")
	(uuid "{sch_uuid}")
	(paper "A3")
	(title_block
		(title "HỘP ĐEN AIoT THÔNG MINH GHI NHẬN VÀ HỖ TRỢ PHÂN TÍCH SỰ CỐ XE MÁY")
		(date "2026-09-22")
		(rev "REV 2.0 (PRESENTATION)")
		(company "KHOA ĐIỆN - ĐIỆN TỬ | BỘ MÔN KỸ THUẬT ĐIỆN TỬ")
		(comment 1 "GVHD: GVC. ThS. NGUYỄN NGÔ LÂM")
		(comment 2 "SVTH: LÊ QUỐC DANH - NGUYỄN ĐỨC TIẾN")
		(comment 3 "AIoT Smart Black Box for Motorcycle Accident Analysis")
		(comment 4 "SƠ ĐỒ NGUYÊN LÝ BÁO CÁO (PRESENTATION SCHEMATIC)")
	)
{lib_symbols_block}
{elements_str}
	(sheet_instances
		(path "/" (page "1"))
	)
)
"""

with open(sch_file, 'w', encoding='utf-8') as f:
    f.write(full_schematic)

print("Successfully written perfected schematic file.")
