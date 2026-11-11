import subprocess, json

sch_content = """(kicad_sch
\t(version 20260306)
\t(generator "eeschema")
\t(generator_version "10.0")
\t(uuid "test-rot-uuid")
\t(paper "A4")
\t(lib_symbols
\t\t(symbol "Device:R"
\t\t\t(pin passive line (at 2 3 270) (length 2.54) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
\t\t)
\t)
\t(symbol (lib_id "Device:R") (at 100 100 0) (unit 1) (uuid "r0") (property "Reference" "R0" (at 100 100 0)) (property "Value" "R" (at 100 100 0)) (pin "1" (uuid "p1")))
\t(symbol (lib_id "Device:R") (at 100 100 90) (unit 1) (uuid "r90") (property "Reference" "R90" (at 100 100 0)) (property "Value" "R" (at 100 100 0)) (pin "1" (uuid "p3")))
\t(symbol (lib_id "Device:R") (at 100 100 180) (unit 1) (uuid "r180") (property "Reference" "R180" (at 100 100 0)) (property "Value" "R" (at 100 100 0)) (pin "1" (uuid "p5")))
\t(symbol (lib_id "Device:R") (at 100 100 270) (unit 1) (uuid "r270") (property "Reference" "R270" (at 100 100 0)) (property "Value" "R" (at 100 100 0)) (pin "1" (uuid "p7")))
)
"""

with open('test_asym.kicad_sch', 'w', encoding='utf-8') as f:
    f.write(sch_content)

subprocess.run([r'D:\KiCad\bin\kicad-cli.exe', 'sch', 'erc', '--format', 'json', '--output', 'erc_asym.json', 'test_asym.kicad_sch'], capture_output=True, text=True, encoding='utf-8', errors='ignore')

data = json.load(open('erc_asym.json', encoding='utf-8'))
for sheet in data.get('sheets', []):
    for v in sheet.get('violations', []):
        for item in v.get('items', []):
            if 'Pin 1' in item.get('description', ''):
                print(item.get('description'), item.get('pos'))
