import os, re, sys, uuid

sys.stdout.reconfigure(encoding='utf-8')

# Read current scratch_rev6 schematic
sch_path = os.path.join('scratch_rev6', 'AIOT_BLACKBOX_PRESENTATION.kicad_sch')
with open(sch_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Refine ESP32 box and center text
# Box: start -19.05 28.50, end 19.05 -30.48
# Pin length: 3.81 mm so pin tip stays at -22.86 (left) and 22.86 (right)
# Center text: size 2.0 and size 1.27

# Replace pins in ESP32 lib_symbol to have length 3.81
# Note: left pin tip at -22.86, base at -19.05 -> length 3.81!
# right pin tip at 22.86, base at 19.05 -> length 3.81!
text = re.sub(r'\(symbol "ESP32-S3-DevKitC-1_0_1"[\s\S]*?\(symbol "ESP32-S3-DevKitC-1_1_1"', 
r"""(symbol "ESP32-S3-DevKitC-1_0_1"
				(rectangle
					(start -19.05 28.50)
					(end 19.05 -30.48)
					(stroke
						(width 0.381)
						(type default)
					)
					(fill
						(type background)
					)
				)
				(text "ESP32-S3"
					(at 0 2.54 0)
					(effects
						(font
							(size 2.0 2.0)
							(bold yes)
						)
					)
				)
				(text "DevKitC-1 N16R8"
					(at 0 -2.54 0)
					(effects
						(font
							(size 1.27 1.27)
							(bold yes)
						)
					)
				)
			)
			(symbol "ESP32-S3-DevKitC-1_1_1\"""", text)

# Update pin length in ESP32-S3-DevKitC-1_1_1 to 3.81
m_esp_pins = re.search(r'\(symbol "ESP32-S3-DevKitC-1_1_1"[\s\S]*?\n\t\t\t\)', text)
if m_esp_pins:
    old_pins_block = m_esp_pins.group(0)
    new_pins_block = old_pins_block.replace('(length 5.08)', '(length 3.81)')
    text = text.replace(old_pins_block, new_pins_block)
    print("Updated ESP32 pin lengths to 3.81 mm")

# 2. Fix ADC_VBAT_SENSE label orientation at (121.92, 83.82)
# Change (label "ADC_VBAT_SENSE" (at 121.92 83.82 0) to (at 121.92 83.82 180)
old_label = '(label "ADC_VBAT_SENSE" (at 121.92 83.82 0)'
new_label = '(label "ADC_VBAT_SENSE" (at 121.92 83.82 180)'
if old_label in text:
    text = text.replace(old_label, new_label)
    print("Updated ADC_VBAT_SENSE label orientation to 180 (text points left)")

# Save refined schematic
with open(sch_path, 'w', encoding='utf-8') as f:
    f.write(text)
print("Saved refined scratch_rev6 schematic.")
