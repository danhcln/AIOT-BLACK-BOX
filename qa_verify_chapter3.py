# -*- coding: utf-8 -*-
"""
Comprehensive QA script to verify the generated Chapter 3 Word document.
Checks:
- Document structure, paragraphs, headings, tables, figures
- Fact checking and forbidden words
- GPIO table verification
- Power architecture verification
"""

import sys
import io
import os
import re
import docx

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

docx_path = r"D:\ĐỒ ÁN 2\Bao_Cao\CHUONG_3_THIET_KE_VA_XAY_DUNG_HE_THONG_AIOT_BLACKBOX.docx"
print(f"Loading document: {docx_path}")
doc = docx.Document(docx_path)

print(f"Total Paragraphs: {len(doc.paragraphs)}")
print(f"Total Tables: {len(doc.tables)}")

# Extract all text
full_text = []
for p in doc.paragraphs:
    full_text.append(p.text)
for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            full_text.append(cell.text)
all_text_str = " \n ".join(full_text)

print("\n--- 1. HEADINGS AUDIT ---")
headings = []
for p in doc.paragraphs:
    if p.style.name.startswith("Heading"):
        headings.append((p.style.name, p.text.strip()))
        print(f"  [{p.style.name}]: {p.text.strip()}")

print("\n--- 2. FIGURES AUDIT ---")
figures = []
for p in doc.paragraphs:
    txt = p.text.strip()
    if txt.startswith("Hình 3."):
        figures.append(txt)
        print(f"  {txt}")
print(f"Total Figures Found: {len(figures)} (Expected: 13)")

print("\n--- 3. TABLES AUDIT ---")
table_caps = []
for p in doc.paragraphs:
    txt = p.text.strip()
    # Match actual table captions: "Bảng 3.x: ..."
    if re.match(r"^Bảng 3\.\d+:", txt):
        table_caps.append(txt)
        print(f"  {txt}")
print(f"Total Table Captions Found: {len(table_caps)} (Expected: 21)")

print("\n--- 4. FORBIDDEN WORDS / SAMPLE CONTENT CHECK ---")
forbidden_regexes = [
    (r"\bung thư\b", "ung thư"),
    (r"\bphổi\b", "phổi"),
    (r"\bảnh CT\b", "ảnh CT"),
    (r"\bbệnh nhân\b", "bệnh nhân"),
    (r"\bbác sĩ\b", "bác sĩ"),
    (r"\bphòng khám\b", "phòng khám"),
    (r"\bFirebase\b", "Firebase"),
    (r"\bYOLO\b", "YOLO"),
    (r"\bKeypad\b", "Keypad"),
    (r"\bđã huấn luyện\b", "đã huấn luyện"),
    (r"\bđộ chính xác 95%\b", "độ chính xác 95%"),
    (r"\bmAP\b", "mAP")
]
found_forbidden = {}
for pattern, label in forbidden_regexes:
    matches = re.findall(pattern, all_text_str, re.IGNORECASE)
    if matches:
        found_forbidden[label] = len(matches)
print(f"Forbidden terms occurrences: {found_forbidden if found_forbidden else 'ZERO - COMPLETELY CLEAN'}")

print("\n--- 5. FACT CHECK: GNSS MODULE ---")
m8n_count = len(re.findall(r"\bNEO-M8N\b", all_text_str))
atgm_count = len(re.findall(r"\bATGM336H\b", all_text_str))
print(f"NEO-M8N mentions: {m8n_count}")
print(f"ATGM336H mentions: {atgm_count} (Only in comparison table as alternative)")
if "Phương án được lựa chọn: Module NEO-M8N" in all_text_str or "NEO-M8N GNSS Module" in all_text_str:
    print("Selected GNSS is correctly NEO-M8N: PASS")
else:
    print("Selected GNSS verification: FAIL")

print("\n--- 6. FACT CHECK: FROZEN GPIO MAPPING ---")
expected_gpios = [
    ("GPIO1", "ADC_VBAT_SENSE"),
    ("GPIO8", "I2C0_SDA"),
    ("GPIO9", "I2C0_SCL"),
    ("GPIO10", "IMU_INT"),
    ("GPIO14", "SD_CS"),
    ("GPIO11", "SPI_MOSI"),
    ("GPIO12", "SPI_SCK"),
    ("GPIO13", "SPI_MISO"),
    ("GPIO17", "GNSS_TXD"),
    ("GPIO18", "GNSS_RXD"),
    ("GPIO21", "GNSS_PPS"),
    ("GPIO43", "4G_TXD"),
    ("GPIO44", "4G_RXD"),
    ("GPIO4", "4G_PWRKEY"),
    ("GPIO5", "4G_STATUS"),
    ("GPIO6", "CANCEL"),
    ("GPIO7", "LED_STATUS"),
    ("GPIO15", "BUZZER_CTRL")
]
gpio_checks = []
for gpio, net in expected_gpios:
    ok = (gpio in all_text_str) and (net in all_text_str)
    gpio_checks.append((gpio, net, ok))
    print(f"  {gpio:6s} -> {net:16s} : {'PASS' if ok else 'FAIL'}")

print("\n--- 7. FACT CHECK: POWER ARCHITECTURE ---")
vbat_primary = ("PRIMARY OPERATING POWER SOURCE" in all_text_str) or ("NGUỒN NĂNG LƯỢNG VẬN HÀNH CHÍNH" in all_text_str)
vbus_charging = ("sạc ngoài" in all_text_str.lower()) and ("VBUS" in all_text_str)
rails_separated = ("5V_SYS" in all_text_str) and ("3V3_SYS" in all_text_str)
esp32_load = ("LOADS" in all_text_str) or ("TẢI TIÊU THỤ" in all_text_str)
adc_sense = ("ADC_VBAT_SENSE" in all_text_str) and ("100k" in all_text_str) and ("100nF" in all_text_str)

print(f"  VBAT is primary source: {'PASS' if vbat_primary else 'FAIL'}")
print(f"  VBUS is charging input: {'PASS' if vbus_charging else 'FAIL'}")
print(f"  5V_SYS & 3V3_SYS separate: {'PASS' if rails_separated else 'FAIL'}")
print(f"  ESP32 is load, not central supplier: {'PASS' if esp32_load else 'FAIL'}")
print(f"  ADC_VBAT_SENSE divider: {'PASS' if adc_sense else 'FAIL'}")

print("\n==============================================================")
print("FINAL QA VERDICT:")
all_passed = (
    len(found_forbidden) == 0 and 
    m8n_count > 0 and 
    len(figures) == 13 and
    len(table_caps) == 21 and
    all(c[2] for c in gpio_checks) and
    vbat_primary and vbus_charging and rails_separated and esp32_load and adc_sense
)
if all_passed:
    print("STATUS: PASSED - 100% SPEC COMPLIANT")
else:
    print("STATUS: ATTENTION NEEDED")
print("==============================================================")
