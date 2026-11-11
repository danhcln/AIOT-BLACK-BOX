import subprocess, sys

# Test exporting current schematic to test svg and pdf
sch_path = r'AIOT_BLACKBOX_PRESENTATION.kicad_sch'
svg_out = r'temp_test.svg'
pdf_out = r'temp_test.pdf'

res_svg = subprocess.run([r'D:\KiCad\bin\kicad-cli.exe', 'sch', 'export', 'svg', '-o', svg_out, sch_path], capture_output=True, text=True)
print("SVG export returncode:", res_svg.returncode)

res_pdf = subprocess.run([r'D:\KiCad\bin\kicad-cli.exe', 'sch', 'export', 'pdf', '-o', pdf_out, sch_path], capture_output=True, text=True)
print("PDF export returncode:", res_pdf.returncode)
