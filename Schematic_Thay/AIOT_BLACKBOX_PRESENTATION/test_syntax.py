import subprocess

sch1 = '''(kicad_sch
	(version 20260306)
	(generator "eeschema")
	(generator_version "10.0")
	(uuid "test-uuid")
	(paper "A4")
	(text "HELLO" (at 100 100 0) (effects (font (size 1.8 1.8) (bold yes)) (justify center)) (uuid "1111"))
)'''
with open(r'D:\ĐỒ ÁN 2\Schematic_Thay\AIOT_BLACKBOX_PRESENTATION\test1.kicad_sch', 'w', encoding='utf-8') as f:
    f.write(sch1)
res1 = subprocess.run([r'D:\Kicad\bin\kicad-cli.exe', 'sch', 'erc', r'D:\ĐỒ ÁN 2\Schematic_Thay\AIOT_BLACKBOX_PRESENTATION\test1.kicad_sch'], capture_output=True, text=True)
print('res1:', res1.returncode, res1.stdout.strip(), res1.stderr.strip())

sch2 = '''(kicad_sch
	(version 20260306)
	(generator "eeschema")
	(generator_version "10.0")
	(uuid "test-uuid")
	(paper "A4")
	(text "HELLO" (at 100 100 0) (effects (font (size 1.8 1.8) (bold yes))) (uuid "1111"))
)'''
with open(r'D:\ĐỒ ÁN 2\Schematic_Thay\AIOT_BLACKBOX_PRESENTATION\test2.kicad_sch', 'w', encoding='utf-8') as f:
    f.write(sch2)
res2 = subprocess.run([r'D:\Kicad\bin\kicad-cli.exe', 'sch', 'erc', r'D:\ĐỒ ÁN 2\Schematic_Thay\AIOT_BLACKBOX_PRESENTATION\test2.kicad_sch'], capture_output=True, text=True)
print('res2:', res2.returncode, res2.stdout.strip(), res2.stderr.strip())
