import fitz
import os
import shutil

pdf_path = r"D:\ĐỒ ÁN 2\Schematic_Thay\AIOT_BLACKBOX_PRESENTATION\AIOT_BLACKBOX_PRESENTATION.pdf"
png_path = r"D:\ĐỒ ÁN 2\Schematic_Thay\AIOT_BLACKBOX_PRESENTATION\AIOT_BLACKBOX_PRESENTATION.png"
artifact_png = r"C:\Users\Danh\.gemini\antigravity-ide\brain\445775bc-37f2-4804-b5f5-a5cc29ef88c2\presentation_schematic.png"

doc = fitz.open(pdf_path)
page = doc[0]
pix = page.get_pixmap(dpi=200)
pix.save(png_path)
shutil.copy2(png_path, artifact_png)
print(f"Rendered {pdf_path} to {png_path} ({pix.width}x{pix.height}) and copied to artifact.")
