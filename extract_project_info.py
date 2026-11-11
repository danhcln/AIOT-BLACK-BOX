import docx
import openpyxl

print("=== DINH HUONG NGHIEN CUU ===")
try:
    doc = docx.Document('Dinh_Huong_Nghien_Cuu_FINAL.docx')
    with open('extracted_dinh_huong.txt', 'w', encoding='utf-8') as out:
        for i, p in enumerate(doc.paragraphs):
            if p.text.strip():
                out.write(f"{i}: {p.text}\n")
        for t_idx, table in enumerate(doc.tables):
            out.write(f"\n--- TABLE {t_idx} ---\n")
            for row in table.rows:
                row_txt = [cell.text.replace('\n', ' ').strip() for cell in row.cells]
                out.write(" | ".join(row_txt) + "\n")
    print("Extracted Dinh_Huong_Nghien_Cuu_FINAL.docx successfully.")
except Exception as e:
    print("Error docx:", e)

print("=== EXCEL BOM / BAO GIA ===")
try:
    wb = openpyxl.load_workbook('BAO_GIA_LINH_KIEN_AIOT_SMART_BLACK_BOX.xlsx', data_only=True)
    with open('extracted_excel.txt', 'w', encoding='utf-8') as out:
        for sheet in wb.sheetnames:
            out.write(f"\n=== SHEET: {sheet} ===\n")
            ws = wb[sheet]
            for row in ws.iter_rows(values_only=True):
                if any(row):
                    out.write(str([r for r in row if r is not None]) + "\n")
    print("Extracted Excel successfully.")
except Exception as e:
    print("Error excel:", e)
