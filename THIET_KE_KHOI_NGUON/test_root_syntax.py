import uuid
import subprocess

def uid():
    return str(uuid.uuid4())

sch = f"""(kicad_sch
	(version 20260306)
	(generator "eeschema")
	(generator_version "10.0")
	(uuid "{uid()}")
	(paper "A4")
	(title_block
		(title "TEST HIERARCHICAL ROOT")
	)
	(sheet
		(at 50.8 50.8)
		(size 50.8 30.48)
		(fields_autoplaced yes)
		(stroke (width 0.1524) (type solid))
		(fill (color 0 0 0 0.0000))
		(uuid "{uid()}")
		(property "Sheetname" "INPUT_SELECTION" (at 50.8 49.53 0) (effects (font (size 1.27 1.27)) (justify left bottom)))
		(property "Sheetfile" "01_INPUT_SELECTION.kicad_sch" (at 50.8 82.55 0) (effects (font (size 1.27 1.27)) (justify left top)))
		(pin "VBUS_MUX" output (at 101.6 63.5 0)
			(effects (font (size 1.27 1.27)) (justify right))
			(uuid "{uid()}")
		)
	)
)
"""

with open("test_root.kicad_sch", "w", encoding="utf-8") as f:
    f.write(sch)

print("test_root.kicad_sch written. Running KiCad ERC...")
cmd = ["D:\\KiCad\\bin\\kicad-cli.exe", "sch", "erc", "--format", "json", "--output", "erc_test_root.json", "test_root.kicad_sch"]
res = subprocess.run(cmd, capture_output=True, text=True)
print("Exit code:", res.returncode)
print(res.stdout)
print(res.stderr)
