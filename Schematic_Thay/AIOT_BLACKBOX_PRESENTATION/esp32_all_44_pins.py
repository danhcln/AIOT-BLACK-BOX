import re, sys
sys.stdout.reconfigure(encoding='utf-8')

# Let's inspect all 44 pins of ESP32-S3-DevKitC-1 v1.1
# Official Espressif J1:
# Pin 1:  3V3       (Type: P)
# Pin 2:  3V3       (Type: P)
# Pin 3:  RST       (Type: I)
# Pin 4:  GPIO4     (Type: I/O/T) -> USED: 4G_PWRKEY
# Pin 5:  GPIO5     (Type: I/O/T) -> USED: 4G_STATUS
# Pin 6:  GPIO6     (Type: I/O/T) -> USED: CANCEL
# Pin 7:  GPIO7     (Type: I/O/T) -> USED: LED_STATUS
# Pin 8:  GPIO15    (Type: I/O/T) -> USED: BUZZER_CTRL
# Pin 9:  GPIO16    (Type: I/O/T) -> Unused
# Pin 10: GPIO17    (Type: I/O/T) -> USED: GNSS_TXD
# Pin 11: GPIO18    (Type: I/O/T) -> USED: GNSS_RXD
# Pin 12: GPIO8     (Type: I/O/T) -> USED: I2C0_SDA
# Pin 13: GPIO3     (Type: I/O/T) -> Unused
# Pin 14: GPIO46    (Type: I/O/T) -> Unused
# Pin 15: GPIO9     (Type: I/O/T) -> USED: I2C0_SCL
# Pin 16: GPIO10    (Type: I/O/T) -> USED: IMU_INT
# Pin 17: GPIO11    (Type: I/O/T) -> USED: SPI_MOSI
# Pin 18: GPIO12    (Type: I/O/T) -> USED: SPI_SCK
# Pin 19: GPIO13    (Type: I/O/T) -> USED: SPI_MISO
# Pin 20: GPIO14    (Type: I/O/T) -> USED: SD_CS
# Pin 21: 5V        (Type: P)     -> USED: 5V_SYS
# Pin 22: GND       (Type: G)     -> USED: GND

# Official Espressif J3:
# Pin 1:  GND       (Type: G)     -> USED: GND
# Pin 2:  GPIO43/TX (Type: I/O/T) -> USED: 4G_TXD
# Pin 3:  GPIO44/RX (Type: I/O/T) -> USED: 4G_RXD
# Pin 4:  GPIO1     (Type: I/O/T) -> USED: ADC_VBAT_SENSE
# Pin 5:  GPIO2     (Type: I/O/T) -> Unused
# Pin 6:  GPIO42    (Type: I/O/T) -> Unused
# Pin 7:  GPIO41    (Type: I/O/T) -> Unused
# Pin 8:  GPIO40    (Type: I/O/T) -> Unused
# Pin 9:  GPIO39    (Type: I/O/T) -> Unused
# Pin 10: GPIO38    (Type: I/O/T) -> Unused
# Pin 11: GPIO37    (Type: I/O/T) -> Unused
# Pin 12: GPIO36    (Type: I/O/T) -> Unused
# Pin 13: GPIO35    (Type: I/O/T) -> Unused
# Pin 14: GPIO0     (Type: I/O/T) -> Unused
# Pin 15: GPIO45    (Type: I/O/T) -> Unused
# Pin 16: GPIO48    (Type: I/O/T) -> Unused
# Pin 17: GPIO47    (Type: I/O/T) -> Unused
# Pin 18: GPIO21    (Type: I/O/T) -> USED: GNSS_PPS
# Pin 19: GPIO20    (Type: I/O/T) -> Unused
# Pin 20: GPIO19    (Type: I/O/T) -> Unused
# Pin 21: GND       (Type: G)     -> Unused
# Pin 22: GND       (Type: G)     -> Unused

print("Pinout analysis complete.")
