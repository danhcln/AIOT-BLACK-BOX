import os
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

proj_dir = r"D:\ĐỒ ÁN 2\Schematic_Thay\AIOT_BLACKBOX_PRESENTATION"
sch_file = os.path.join(proj_dir, "AIOT_BLACKBOX_PRESENTATION.kicad_sch")
backup_file = os.path.join(proj_dir, "AIOT_BLACKBOX_PRESENTATION_REV3_backup.kicad_sch")
scratch_sch = r"C:\Users\Danh\.gemini\antigravity-ide\brain\445775bc-37f2-4804-b5f5-a5cc29ef88c2\scratch\test_rev4.kicad_sch"
scratch_wks = r"C:\Users\Danh\.gemini\antigravity-ide\brain\445775bc-37f2-4804-b5f5-a5cc29ef88c2\scratch\border_only.kicad_wks"
target_wks = os.path.join(proj_dir, "border_only.kicad_wks")
main_wks = os.path.join(proj_dir, "AIOT_BLACKBOX_PRESENTATION.kicad_wks")

print("1. Creating NEW backup of REV3...")
shutil.copy2(sch_file, backup_file)
print(f"Backup created: {backup_file}")

print("2. Setting worksheet files to border-only...")
border_only_content = """( page_layout
    ( setup (textsize 1.5 1.5) (linewidth 0.15) (textlinewidth 0.15)
      (left_margin 10) (right_margin 10) (top_margin 10) (bottom_margin 10) )
    ( rect (start 0 0 ltcorner) (end 0 0 rbcorner) )
)
"""
with open(target_wks, 'w', encoding='utf-8') as f:
    f.write(border_only_content)
with open(main_wks, 'w', encoding='utf-8') as f:
    f.write(border_only_content)

print("3. Applying validated REV4 schematic to MAIN source...")
shutil.copy2(scratch_sch, sch_file)
print(f"Main source {sch_file} updated successfully!")

print("4. Running ERC on MAIN source...")
kicad_cli = r"D:\Kicad\bin\kicad-cli.exe"
erc_cmd = [kicad_cli, "sch", "erc", "--severity-all", sch_file]
erc_res = subprocess.run(erc_cmd, cwd=proj_dir, capture_output=True, text=True)
print(erc_res.stdout)

print("5. Exporting REV4 PDF from MAIN source...")
pdf_out = os.path.join(proj_dir, "AIOT_BLACKBOX_PRESENTATION_A4_REV4.pdf")
cmd_pdf = [kicad_cli, "sch", "export", "pdf", "-o", pdf_out, sch_file]
subprocess.run(cmd_pdf, cwd=proj_dir, check=True)
print(f"Exported: {pdf_out}")

print("6. Exporting REV4 SVG from MAIN source...")
svg_out = os.path.join(proj_dir, "AIOT_BLACKBOX_PRESENTATION_A4_REV4.svg")
cmd_svg = [kicad_cli, "sch", "export", "svg", "-o", svg_out, sch_file]
subprocess.run(cmd_svg, cwd=proj_dir, check=True)
print(f"Exported: {svg_out}")

print("ALL REV4 OPERATIONS COMPLETED SUCCESSFULLY!")
