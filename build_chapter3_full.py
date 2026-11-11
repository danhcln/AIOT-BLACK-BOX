# -*- coding: utf-8 -*-
r"""
Script to generate the complete, comprehensive Chapter 3 for the AIoT Smart Black Box project.
Target: D:\ĐỒ ÁN 2\Bao_Cao\CHUONG_3_THIET_KE_VA_XAY_DUNG_HE_THONG_AIOT_BLACKBOX.docx
"""

import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def create_element(name):
    return OxmlElement(name)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, hex_color):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_table_borders(table, color="B0B0B0", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders_xml = f'''
    <w:tblBorders {nsdecls("w")}>
        <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
    </w:tblBorders>
    '''
    tblPr.append(parse_xml(borders_xml))

def add_p(doc, text="", bold_prefix="", italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, 
          indent=True, space_after=6, space_before=0, line_spacing=1.35):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if indent:
        p.paragraph_format.first_line_indent = Inches(0.5) # ~1.27 cm
    else:
        p.paragraph_format.first_line_indent = Inches(0)
        
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(13)
        r_pre.font.color.rgb = RGBColor(0, 0, 0)
        
    if text:
        r_txt = p.add_run(text)
        r_txt.italic = italic
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(13)
        r_txt.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_bullet(doc, bold_prefix="", text=""):
    p = doc.add_paragraph(style='List Paragraph')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.3
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.first_line_indent = Inches(0.2)
    
    r_bullet = p.add_run("• ")
    r_bullet.bold = True
    r_bullet.font.name = "Times New Roman"
    r_bullet.font.size = Pt(13)
    r_bullet.font.color.rgb = RGBColor(0, 0, 0)
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(13)
        r_pre.font.color.rgb = RGBColor(0, 0, 0)
        
    if text:
        r_txt = p.add_run(text)
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(13)
        r_txt.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_h1(doc, text):
    h = doc.add_paragraph(style='Heading 1')
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(8)
    h.paragraph_format.keep_with_next = True
    h.paragraph_format.first_line_indent = Inches(0)
    h.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = h.add_run(text)
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(15)
    r.font.color.rgb = RGBColor(0, 0, 0)
    return h

def add_h2(doc, text):
    h = doc.add_paragraph(style='Heading 2')
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.keep_with_next = True
    h.paragraph_format.first_line_indent = Inches(0)
    h.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = h.add_run(text)
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.color.rgb = RGBColor(0, 0, 0)
    return h

def add_h3(doc, text):
    h = doc.add_paragraph(style='Heading 3')
    h.paragraph_format.space_before = Pt(10)
    h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True
    h.paragraph_format.first_line_indent = Inches(0)
    h.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = h.add_run(text)
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(0, 0, 0)
    return h

def add_figure(doc, img_path, caption_text, width_inches=5.0):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.paragraph_format.first_line_indent = Inches(0)
    p_img.paragraph_format.keep_with_next = True
    
    if os.path.exists(img_path):
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(width_inches))
    else:
        run_ph = p_img.add_run(f"[CHÈN HÌNH: {os.path.basename(img_path)}]")
        run_ph.bold = True
        run_ph.font.name = "Times New Roman"
        run_ph.font.size = Pt(12)
        run_ph.font.color.rgb = RGBColor(192, 0, 0)
        
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(4)
    p_cap.paragraph_format.space_after = Pt(8)
    p_cap.paragraph_format.first_line_indent = Inches(0)
    r_cap = p_cap.add_run(caption_text)
    r_cap.bold = True
    r_cap.font.name = "Times New Roman"
    r_cap.font.size = Pt(13)
    r_cap.font.color.rgb = RGBColor(0, 0, 0)
    return p_cap

def add_table_with_caption(doc, caption_text, headers, rows_data, col_widths=None):
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_cap.paragraph_format.space_before = Pt(10)
    p_cap.paragraph_format.space_after = Pt(4)
    p_cap.paragraph_format.first_line_indent = Inches(0)
    p_cap.paragraph_format.keep_with_next = True
    r_cap = p_cap.add_run(caption_text)
    r_cap.bold = True
    r_cap.font.name = "Times New Roman"
    r_cap.font.size = Pt(13)
    r_cap.font.color.rgb = RGBColor(0, 0, 0)
    
    table = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, color="808080", sz="4", val="single")
    
    # Header Row
    hdr_cells = table.rows[0].cells
    hdr_tr = table.rows[0]._tr.get_or_add_trPr()
    hdr_tr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    hdr_tr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    
    for i, h_text in enumerate(headers):
        cell = hdr_cells[i]
        set_cell_background(cell, "F2F2F2")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.first_line_indent = Inches(0)
        r = p.add_run(h_text)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0, 0, 0)
        
    # Data Rows
    for r_idx, row_values in enumerate(rows_data):
        row_cells = table.rows[r_idx + 1].cells
        r_tr = table.rows[r_idx + 1]._tr.get_or_add_trPr()
        r_tr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        bg_col = "FFFFFF" if r_idx % 2 == 0 else "FBFBFB"
        for c_idx, val in enumerate(row_values):
            cell = row_cells[c_idx]
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.first_line_indent = Inches(0)
            p.paragraph_format.line_spacing = 1.2
            
            # Align center for short columns (STT, Chân, Tên tín hiệu), left for description
            if len(headers) >= 3 and c_idx in [0, 1] and len(str(val)) < 15:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif c_idx == 0 and len(str(val)) < 6:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
            r = p.add_run(str(val))
            r.font.name = "Times New Roman"
            r.font.size = Pt(11.5)
            r.font.color.rgb = RGBColor(0, 0, 0)
            
    if col_widths:
        for row in table.rows:
            for idx, w in enumerate(col_widths):
                if idx < len(row.cells):
                    row.cells[idx].width = Inches(w)
                    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return table

def add_code_snippet(doc, code_str):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F8F9FA")
    set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
    
    borders_xml = f'''
    <w:tcBorders {nsdecls("w")}>
        <w:left w:val="single" w:sz="18" w:space="0" w:color="004B87"/>
        <w:top w:val="single" w:sz="4" w:space="0" w:color="D0D5DD"/>
        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="D0D5DD"/>
        <w:right w:val="single" w:sz="4" w:space="0" w:color="D0D5DD"/>
    </w:tcBorders>
    '''
    cell._tc.get_or_add_tcPr().append(parse_xml(borders_xml))
    
    p = cell.paragraphs[0]
    p.paragraph_format.first_line_indent = Inches(0)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    
    lines = code_str.strip().split("\n")
    for i, line in enumerate(lines):
        r = p.add_run(line + ("\n" if i < len(lines)-1 else ""))
        r.font.name = "Consolas"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(30, 41, 59)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

print("Helper library initialized.")
