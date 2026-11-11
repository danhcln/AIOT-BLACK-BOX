# -*- coding: utf-8 -*-
"""
Main runner script to generate the entire Chapter 3 Microsoft Word Document.
Output file: D:\\ĐỒ ÁN 2\\Bao_Cao\\CHUONG_3_THIET_KE_VA_XAY_DUNG_HE_THONG_AIOT_BLACKBOX.docx
"""

import os
import sys
import io

# Ensure UTF-8 output on Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

# Import section builders
from ch3_sec31 import add_section_3_1
from ch3_sec32_p1 import add_section_3_2_part1
from ch3_sec32_p2 import add_section_3_2_part2
from ch3_sec32_p3 import add_section_3_2_part3
from ch3_sec33 import add_section_3_3

def main():
    print("==============================================================")
    print("STARTING CHAPTER 3 DOCX BUILD PROCESS")
    print("==============================================================")
    
    output_dir = r"D:\ĐỒ ÁN 2\Bao_Cao"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "CHUONG_3_THIET_KE_VA_XAY_DUNG_HE_THONG_AIOT_BLACKBOX.docx")
    assets_dir = r"D:\ĐỒ ÁN 2\report_assets"
    
    doc = Document()
    
    # Page Setup: A4, Standard academic margins (Left 35mm, Right 20mm, Top 25mm, Bottom 25mm)
    section = doc.sections[0]
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.top_margin = Mm(25)
    section.bottom_margin = Mm(25)
    section.left_margin = Mm(35)
    section.right_margin = Mm(20)
    
    # Configure Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(13)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.35
    normal_style.paragraph_format.space_before = Pt(0)
    normal_style.paragraph_format.space_after = Pt(6)
    normal_style.paragraph_format.first_line_indent = Inches(0.5)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    # Setup Footer
    footer = section.footer
    f_p = footer.paragraphs[0]
    f_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    f_run = f_p.add_run("Báo cáo Đồ án 2: Hộp đen AIoT phân tích và ghi lại sự cố xe máy điện | Chương 3")
    f_run.font.name = "Times New Roman"
    f_run.font.size = Pt(9.5)
    f_run.font.italic = True
    f_run.font.color.rgb = RGBColor(128, 128, 128)
    
    # Build Document Sections
    print("-> Adding Section 3.1: Yeu cau va So do khoi he thong...")
    add_section_3_1(doc, assets_dir)
    
    print("-> Adding Section 3.2 Part 1: Khoi xu ly trung tam, Khoi cam bien quan tinh, Khoi thoi gian thuc...")
    add_section_3_2_part1(doc, assets_dir)
    
    print("-> Adding Section 3.2 Part 2: Khoi GPS, Khoi luu tru, Khoi 4G LTE...")
    add_section_3_2_part2(doc, assets_dir)
    
    print("-> Adding Section 3.2 Part 3: Khoi hien thi, Khoi canh bao, Khoi nut nhan, Khoi nguon, So do toan he thong...")
    add_section_3_2_part3(doc, assets_dir)
    
    print("-> Adding Section 3.3: Thuat toan phan tich va ghi nhan su co...")
    add_section_3_3(doc, assets_dir)
    
    # Save the output file
    print(f"-> Saving final document to: {output_file}")
    doc.save(output_file)
    print("DOCX BUILD COMPLETED SUCCESSFULLY!")
    print(f"File size: {os.path.getsize(output_file)} bytes")

if __name__ == "__main__":
    main()
