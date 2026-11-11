import re, sys
sys.stdout.reconfigure(encoding='utf-8')

# Official Espressif ESP32-S3-DevKitC-1 v1.1 Header Pinout
# Let's map each pin with:
# (Header, HeaderPinNo, PinName, PinType, UsedInProject, FunctionInProject)

devkit_pins = [
    # Header J1 (22 pins)
    ('J1', 1,  '3V3',    'power_out',     True,  '+3V3 System Power'),
    ('J1', 2,  '3V3',    'power_out',     False, 'Unused 3.3V Output'),
    ('J1', 3,  'RST',    'input',         False, 'EN / Chip Reset'),
    ('J1', 4,  'GPIO4',  'output',        True,  '4G_PWRKEY'),
    ('J1', 5,  'GPIO5',  'input',         True,  '4G_STATUS'),
    ('J1', 6,  'GPIO6',  'input',         True,  'CANCEL Button Input'),
    ('J1', 7,  'GPIO7',  'output',        True,  'LED_STATUS Output'),
    ('J1', 8,  'GPIO15', 'output',        True,  'BUZZER_CTRL Output'),
    ('J1', 9,  'GPIO16', 'bidirectional', False, 'Unused GPIO16 / UART0 CTS'),
    ('J1', 10, 'GPIO17', 'output',        True,  'GNSS_TXD Output'),
    ('J1', 11, 'GPIO18', 'input',         True,  'GNSS_RXD Input'),
    ('J1', 12, 'GPIO8',  'bidirectional', True,  'I2C0_SDA'),
    ('J1', 13, 'GPIO3',  'bidirectional', False, 'Unused GPIO3 / ADC1_CH2'),
    ('J1', 14, 'GPIO46', 'bidirectional', False, 'Unused GPIO46 / Strapping'),
    ('J1', 15, 'GPIO9',  'bidirectional', True,  'I2C0_SCL'),
    ('J1', 16, 'GPIO10', 'input',         True,  'IMU_INT Input'),
    ('J1', 17, 'GPIO11', 'output',        True,  'SPI_MOSI Output'),
    ('J1', 18, 'GPIO12', 'output',        True,  'SPI_SCK Output'),
    ('J1', 19, 'GPIO13', 'input',         True,  'SPI_MISO Input'),
    ('J1', 20, 'GPIO14', 'output',        True,  'SD_CS Output'),
    ('J1', 21, '5V',     'power_in',      True,  '5V_SYS Main Power Input'),
    ('J1', 22, 'GND',    'power_in',      True,  'Ground'),

    # Header J3 (22 pins)
    ('J3', 1,  'GND',    'power_in',      True,  'Ground'),
    ('J3', 2,  'GPIO43', 'output',        True,  '4G_TXD Output (U0TXD)'),
    ('J3', 3,  'GPIO44', 'input',         True,  '4G_RXD Input (U0RXD)'),
    ('J3', 4,  'GPIO1',  'input',         True,  'ADC_VBAT_SENSE Input'),
    ('J3', 5,  'GPIO2',  'bidirectional', False, 'Unused GPIO2 / ADC1_CH1'),
    ('J3', 6,  'GPIO42', 'bidirectional', False, 'Unused GPIO42 / MTMS'),
    ('J3', 7,  'GPIO41', 'bidirectional', False, 'Unused GPIO41 / MTDI'),
    ('J3', 8,  'GPIO40', 'bidirectional', False, 'Unused GPIO40 / MTDO'),
    ('J3', 9,  'GPIO39', 'bidirectional', False, 'Unused GPIO39 / MTCK'),
    ('J3', 10, 'GPIO38', 'bidirectional', False, 'Unused GPIO38 / RGB LED'),
    ('J3', 11, 'GPIO37', 'bidirectional', False, 'Unused GPIO37 / FSPIQ'),
    ('J3', 12, 'GPIO36', 'bidirectional', False, 'Unused GPIO36 / FSPICLK'),
    ('J3', 13, 'GPIO35', 'bidirectional', False, 'Unused GPIO35 / FSPID'),
    ('J3', 14, 'GPIO0',  'bidirectional', False, 'Unused GPIO0 / Boot Button'),
    ('J3', 15, 'GPIO45', 'bidirectional', False, 'Unused GPIO45 / Strapping'),
    ('J3', 16, 'GPIO48', 'bidirectional', False, 'Unused GPIO48 / SPICLK_N'),
    ('J3', 17, 'GPIO47', 'bidirectional', False, 'Unused GPIO47 / SPICLK_P'),
    ('J3', 18, 'GPIO21', 'input',         True,  'GNSS_PPS Input'),
    ('J3', 19, 'GPIO20', 'bidirectional', False, 'Unused GPIO20 / USB_D+'),
    ('J3', 20, 'GPIO19', 'bidirectional', False, 'Unused GPIO19 / USB_D-'),
    ('J3', 21, 'GND',    'power_in',      False, 'Unused Ground Header Pin'),
    ('J3', 22, 'GND',    'power_in',      False, 'Unused Ground Header Pin'),
]

print(f"Total DevKit pins verified: {len(devkit_pins)}")
used = [p for p in devkit_pins if p[4]]
unused = [p for p in devkit_pins if not p[4]]
print(f"Used pins: {len(used)}")
print(f"Unused pins: {len(unused)}")
