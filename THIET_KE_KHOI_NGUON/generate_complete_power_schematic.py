# -*- coding: utf-8 -*-
"""
COMPLETE KICAD 10 POWER SCHEMATIC GENERATOR
AIOT BLACK BOX - POWER SUPPLY SYSTEM
Generates Root Sheet + 4 Hierarchical Sub-sheets:
1. 01_INPUT_SELECTION.kicad_sch: VEHICLE_5V_IN, USB_5V_IN, PPTC, TVS, TPS2121 Power Mux
2. 02_CHARGER_BATTERY.kicad_sch: BQ25895 NVDC Charger, DW01A + 2x FS8205A 18650 Protection, NTC, ADC VBAT Sense
3. 03_BOOST_BUCK_RAILS.kicad_sch: TPS61088 5V Boost (3A), TPS62162 3.3V Buck (1A)
4. 04_SIM_POWER_OUTPUTS.kicad_sch: Dedicated SIM Power Stage (Option A 5V / Option B TPS62130 3.8V), Decoupling, Test Points, Load Headers
"""

import os
import sys
import uuid
import re

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"D:\ĐỒ ÁN 2\THIET_KE_KHOI_NGUON"

def uid():
    return str(uuid.uuid4())

# Title Block Generator
def get_tb(title, sheet_num, total_sheets=5):
    return f"""\t(title_block
\t\t(title "{title}")
\t\t(date "2026-10-18")
\t\t(rev "REV 1.0")
\t\t(company "AIOT SMART BLACK BOX - ELECTRIC MOTORCYCLE")
\t\t(comment 1 "ĐỀ TÀI: THIẾT KẾ HỘP ĐEN AIOT THÔNG MINH - PHÂN TÍCH VÀ GHI LẠI SỰ CỐ XE MÁY ĐIỆN")
\t\t(comment 2 "SVTH: NGUYỄN LÊ CÔNG DANH (23161240) - PHẠM TRẦN HUY (21161131)")
\t\t(comment 3 "GVHD: THS. NGUYỄN NGÔ LÂM")
\t\t(comment 4 "SHEET {sheet_num} OF {total_sheets} - BUILDABLE POWER SUPPLY ARCHITECTURE")
\t)"""

print("Helper functions initialized.")
