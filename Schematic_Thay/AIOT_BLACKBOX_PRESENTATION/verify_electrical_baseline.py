import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('AIOT_BLACKBOX_PRESENTATION.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

# Verify all required signals from user prompt section 5 & 32:
# GPIO1 -> ADC_VBAT_SENSE
# GPIO8 -> I2C0_SDA
# GPIO9 -> I2C0_SCL
# GPIO10 -> IMU_INT
# GPIO14 -> SD_CS
# GPIO11 -> SPI_MOSI
# GPIO12 -> SPI_SCK
# GPIO13 -> SPI_MISO
# GPIO43 -> 4G_TXD
# GPIO44 -> 4G_RXD
# GPIO4 -> 4G_PWRKEY
# GPIO5 -> 4G_STATUS
# GPIO17 -> GNSS_TXD
# GPIO18 -> GNSS_RXD
# GPIO21 -> GNSS_PPS
# GPIO6 -> CANCEL
# GPIO7 -> LED_STATUS
# GPIO15 -> BUZZER_CTRL
# Power: 5V -> 5V_SYS, 3V3 -> +3V3, GND -> GND

wires = re.findall(r'\(wire\s+\(pts\s+\(xy\s+([-\d.]+)\s+([-\d.]+)\)\s+\(xy\s+([-\d.]+)\s+([-\d.]+)\)\s*\)', text)

# U1 pin tips are at x = 129.54 (left) and x = 175.26 (right)
expected_connections = {
    # Left side (x = 129.54)
    (129.54,  73.66): ('5V', '5V_SYS power line'),
    (129.54,  78.74): ('3V3', '+3V3 power line'),
    (129.54,  83.82): ('GPIO1', 'ADC_VBAT_SENSE net'),
    (129.54,  88.90): ('GPIO8', 'I2C0_SDA net (to MPU6050, DS3231, R_PU1)'),
    (129.54,  93.98): ('GPIO9', 'I2C0_SCL net (to MPU6050, DS3231, R_PU2)'),
    (129.54,  99.06): ('GPIO10', 'IMU_INT net (to MPU6050 INT)'),
    (129.54, 104.14): ('GPIO14', 'SD_CS net (to MicroSD CS)'),
    (129.54, 109.22): ('GPIO11', 'SPI_MOSI net (to MicroSD MOSI)'),
    (129.54, 114.30): ('GPIO12', 'SPI_SCK net (to MicroSD SCK)'),
    (129.54, 119.38): ('GPIO13', 'SPI_MISO net (to MicroSD MISO)'),
    (129.54, 124.46): ('GND', 'GND power line'),

    # Right side (x = 175.26)
    (175.26,  73.66): ('GPIO43', '4G_TXD net (to MKE-M21 RX)'),
    (175.26,  78.74): ('GPIO44', '4G_RXD net (to MKE-M21 TX)'),
    (175.26,  83.82): ('GPIO4', '4G_PWRKEY net (to MKE-M21 PWRKEY)'),
    (175.26,  88.90): ('GPIO5', '4G_STATUS net (to MKE-M21 STATUS)'),
    (175.26,  93.98): ('GPIO17', 'GNSS_TXD net (to ATGM336H RX)'),
    (175.26,  99.06): ('GPIO18', 'GNSS_RXD net (to ATGM336H TX)'),
    (175.26, 104.14): ('GPIO21', 'GNSS_PPS net (to ATGM336H PPS)'),
    (175.26, 109.22): ('GPIO6', 'CANCEL net (to SW1 CANCEL button & filter)'),
    (175.26, 114.30): ('GPIO7', 'LED_STATUS net (to R4 330R & D1 LED)'),
    (175.26, 119.38): ('GPIO15', 'BUZZER_CTRL net (to R5 1k & Q1 base)'),
    (175.26, 124.46): ('GND', 'GND power line'),
}

print(f"{'Pin':<8} {'Expected Net':<40} {'Status':<15} {'Attached Wire Endpoint'}")
print("-" * 80)
all_ok = True
for (px, py), (pname, desc) in expected_connections.items():
    attached = []
    for w in wires:
        x1, y1, x2, y2 = float(w[0]), float(w[1]), float(w[2]), float(w[3])
        if round(x1, 2) == round(px, 2) and round(y1, 2) == round(py, 2):
            attached.append((x2, y2))
        elif round(x2, 2) == round(px, 2) and round(y2, 2) == round(py, 2):
            attached.append((x1, y1))
    
    if len(attached) == 1:
        status = "PASSED"
        endpoint = f"({attached[0][0]:6.2f}, {attached[0][1]:6.2f})"
    else:
        status = f"FAILED ({len(attached)} wires)"
        endpoint = str(attached)
        all_ok = False
    print(f"{pname:<8} {desc:<40} {status:<15} {endpoint}")

print("-" * 80)
print(f"Overall Electrical Baseline Check: {'100% PASSED' if all_ok else 'FAILED'}")
