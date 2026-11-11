# -*- coding: utf-8 -*-
"""
Generator for 05_POWER_BOM.xlsx
Comprehensive Bill of Materials for AIOT_BLACKBOX_POWER_SUPPLY project.
Formatted professionally with openpyxl.
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def generate_bom():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "BOM_POWER_SUPPLY"

    # Title block
    ws.merge_cells("A1:J1")
    title_cell = ws["A1"]
    title_cell.value = "AIOT SMART BLACK BOX - POWER SUPPLY SYSTEM BILL OF MATERIALS (BOM)"
    title_cell.font = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
    title_cell.fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 40

    ws.merge_cells("A2:J2")
    sub_cell = ws["A2"]
    sub_cell.value = "Project: AIOT_BLACKBOX_POWER_SUPPLY | Revision: REV 1.0 | Date: 2026-10-18 | Author: Senior Power Hardware Engineer"
    sub_cell.font = Font(name="Calibri", size=11, italic=True, color="FFFFFF")
    sub_cell.fill = PatternFill(start_color="244061", end_color="244061", fill_type="solid")
    sub_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 24

    ws.merge_cells("A3:J3")
    warn_cell = ws["A3"]
    warn_cell.value = "CRITICAL HARDWARE STATUS: DESIGN COMPLETE FOR ENGINEERING REVIEW. PHYSICAL A7682S BREAKOUT INPUT VOLTAGE REQUIRES BENCH VERIFICATION BEFORE POPULATING JP1."
    warn_cell.font = Font(name="Calibri", size=10, bold=True, color="9C0006")
    warn_cell.fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    warn_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[3].height = 24

    headers = [
        "Item", "Designator", "Qty", "Value", "Manufacturer", "Manufacturer Part Number (MPN)",
        "Package / Footprint", "Key Electrical Ratings & Specs", "Functional Role in Circuit", "Datasheet / Sourcing Link"
    ]

    header_row = 5
    ws.row_dimensions[header_row].height = 28
    for col_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=header_row, column=col_idx, value=h)
        cell.font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    # BOM Data
    bom_data = [
        # ICs
        ("1", "U1", "1", "TPS2121RUXR", "Texas Instruments", "TPS2121RUXR", "VQFN-12 (RUX0012A, 2x2.5mm)",
         "VIN: 2.7V-22V, 4.5A max, RDSon=56mOhm, Fast switchover 5us",
         "External 5V Power Mux (Vehicle 5V Priority vs USB-C 5V)", "https://www.ti.com/lit/ds/symlink/tps2121.pdf"),

        ("2", "U2", "1", "BQ25895RTWR", "Texas Instruments", "BQ25895RTWR", "WQFN-24 (RTW0024A, 4x4mm)",
         "VIN: 3.9V-14V, 5A Fast Charge, 3.25A ILIM, NVDC Power-Path, I2C Control",
         "1S Li-ion Battery Charger & NVDC System Power Path Manager", "https://www.ti.com/lit/ds/symlink/bq25895.pdf"),

        ("3", "U3", "1", "DW01A-G", "Fortune Semiconductor", "DW01A-G", "SOT-23-6",
         "Overcharge: 4.30V±50mV, Overdischarge: 2.40V±100mV, Overcurrent: 150mV",
         "1S Li-ion Battery Primary Protection IC", "https://datasheet.lcsc.com/lcsc/1811151441_Fortune-Semicon-DW01A-G_C24339.pdf"),

        ("4", "Q1, Q2", "2", "FS8205A", "Fortune Semiconductor", "FS8205A", "TSSOP-8",
         "VDS: 20V, ID: 6A, RDS(ON) < 25mOhm @ 4.5V (Paralleled: 12.5mOhm total, 6A continuous trip)",
         "Dual N-Channel Battery Protection MOSFETs (Dual Paralleled for <0.12V drop @ 5A)", "https://datasheet.lcsc.com/lcsc/1811151441_Fortune-Semicon-FS8205A_C32254.pdf"),

        ("5", "U4", "1", "TPS61088RHLR", "Texas Instruments", "TPS61088RHLR", "VQFN-20 (RHL0020A, 3.5x4.5mm)",
         "VIN: 2.7V-12V, VOUT: 5.0V, 10A switch current, 600kHz PWM, Eff > 93%",
         "High-Current Synchronous Boost Converter (SYS -> 5V_SYS, 3.5A / 5A Peak)", "https://www.ti.com/lit/ds/symlink/tps61088.pdf"),

        ("6", "U5", "1", "TPS62162DSGR", "Texas Instruments", "TPS62162DSGR", "WSON-8 (2x2mm)",
         "VIN: 3V-17V, VOUT: 3.3V Fixed, IOUT: 1.0A, Fsw: 2.25MHz, DCS-Control",
         "Synchronous Step-Down Buck Converter (5V_SYS -> 3V3_SYS Logic Rail)", "https://www.ti.com/lit/ds/symlink/tps62162.pdf"),

        ("7", "U6", "1", "TPS62130RGTR", "Texas Instruments", "TPS62130RGTR", "VQFN-16 (RGT0016A, 3x3mm)",
         "VIN: 3V-17V, VOUT: 3.8V, IOUT: 3.0A continuous, Fsw: 1.25MHz, DCS-Control",
         "Cellular Option B Dedicated Step-Down Converter (5V_SYS -> 3.8V SIM_PWR_B)", "https://www.ti.com/lit/ds/symlink/tps62130.pdf"),

        ("8", "Q3", "1", "AO3401A", "Alpha & Omega Semiconductor", "AO3401A", "SOT-23",
         "VDS: -30V, ID: -4.0A, RDS(ON) < 45mOhm @ -4.5V",
         "Cellular Option A P-MOSFET Power Gate Switch (5V_SYS -> SIM_PWR_A)", "http://www.aosmd.com/pdfs/datasheet/AO3401A.pdf"),

        # Inductors
        ("9", "L1", "1", "1.0uH (7.5A Sat)", "Bourns", "SRP6540-1R0M", "SMD 6.5x6.5x4.0mm",
         "Inductance: 1.0uH±20%, Isat: 7.5A, Irms: 6.0A, DCR: 12.0mOhm max",
         "BQ25895 NVDC Charger Switching Inductor", "https://www.bourns.com/docs/product-datasheets/srp6540.pdf"),

        ("10", "L2", "1", "1.0uH (10A Sat)", "Bourns", "SRP6540-1R0M", "SMD 6.5x6.5x4.0mm",
         "Inductance: 1.0uH±20%, Isat: 10A, Irms: 8.5A, DCR: 9.0mOhm max",
         "TPS61088 High-Current Boost Inductor (5V_SYS)", "https://www.bourns.com/docs/product-datasheets/srp6540.pdf"),

        ("11", "L3", "1", "2.2uH (2.5A Sat)", "Bourns", "SRP4020TA-2R2M", "SMD 4.0x4.0x2.0mm",
         "Inductance: 2.2uH±20%, Isat: 2.5A, Irms: 2.0A, DCR: 45mOhm max",
         "TPS62162 Buck Inductor (3V3_SYS)", "https://www.bourns.com/docs/product-datasheets/srp4020ta.pdf"),

        ("12", "L4", "1", "1.0uH (4.0A Sat)", "Bourns", "SRP6540-1R0M", "SMD 6.5x6.5x4.0mm",
         "Inductance: 1.0uH±20%, Isat: 4.0A, Irms: 3.5A, DCR: 15mOhm max",
         "TPS62130 Option B Cellular Buck Inductor (3.8V)", "https://www.bourns.com/docs/product-datasheets/srp6540.pdf"),

        # High-Capacity & Polymer Capacitors
        ("13", "C35", "1", "1000uF/6.3V Polymer", "Panasonic", "EEFHX0J102R", "Radial SMD 8x10.2mm",
         "Capacitance: 1000uF±20%, 6.3V, ESR: 12mOhm @ 100kHz, Ripple: 4500mA",
         "A7682S 4G Cellular Burst Current Energy Buffer (ESR Droop < 25mV @ 2A burst)", "https://industrial.panasonic.com/cdvis/browse/do/product/EEF-HX/EEFHX0J102R"),

        ("14", "C36", "1", "100uF/6.3V (X5R)", "Murata / Samsung", "GRM31CR60J107ME39L", "1206 (3216 Metric)",
         "Capacitance: 100uF±20%, 6.3V, X5R dielectric, Ceramic MLCC",
         "Cellular Rail Intermediate High-Frequency Energy Reservoir", "https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM31CR60J107ME39-01.pdf"),

        # Ceramic Capacitors 22uF
        ("15", "C11, C12, C18, C19, C24, C25, C26, C27, C33, C41, C42", "11", "22uF/10V (X5R)", "Murata / TDK", "GRM21BR61A226ME51L", "0805 (2012 Metric)",
         "Capacitance: 22uF±20%, 10V, X5R, Low-ESR Ceramic MLCC",
         "SYS Output Caps (C11, C12), Boost Input (C18, C19), Boost Output (C24-C27), Buck Output (C33, C41, C42)", "https://www.murata.com/"),

        # Ceramic Capacitors 10uF
        ("16", "C1, C4, C7, C8, C13, C14, C31, C38", "8", "10uF/25V & 10V (X7R/X5R)", "Murata / TDK", "GRM21BZ71E106KE15L", "0805 (2012 Metric)",
         "Capacitance: 10uF±10%, 25V (C1,C4,C7,C8) / 10V (C13,C14,C31,C38), X7R/X5R",
         "Input Filtering (C1, C4, C7), PMID HF Filter (C8), Battery Rail (C13, C14), Buck Inputs (C31, C38)", "https://www.murata.com/"),

        # Ceramic Capacitors 4.7uF
        ("17", "C9, C21", "2", "4.7uF/10V (X5R)", "Murata", "GRM188R61A475KE15D", "0603 (1608 Metric)",
         "Capacitance: 4.7uF±10%, 10V, X5R Ceramic MLCC",
         "BQ25895 REGN LDO Bypass (C9), TPS61088 VCC LDO Bypass (C21)", "https://www.murata.com/"),

        # Decoupling & Timing Capacitors
        ("18", "C2, C3, C5, C6, C10, C15, C17, C20, C23, C32, C34, C37, C39", "13", "100nF/16V & 47nF", "Murata / TDK", "GRM188R71C104KA01D", "0603 (1608 Metric)",
         "Capacitance: 100nF±10%, 16V / 25V (C10 47nF), X7R Ceramic MLCC",
         "High-Frequency RF & Switching Decoupling across all rails and bootstrap capacitors", "https://www.murata.com/"),

        ("19", "C22, C29, C40", "3", "47nF, 2.2nF, 3.3nF", "Murata", "GRM188R71H222KA01D", "0603 (1608 Metric)",
         "Soft-Start: 47nF (C22), 3.3nF (C40); Compensation: 2.2nF (C29), X7R",
         "Converter Soft-Start Timing and Loop Compensation", "https://www.murata.com/"),

        ("20", "C28, C30, C43", "3", "10pF, 47pF, 22pF (C0G)", "Murata", "GRM1885C1H100JA01D", "0603 (1608 Metric)",
         "Capacitance: 10pF / 47pF / 22pF ±5%, 50V, C0G/NP0 Ultra-Stable Dielectric",
         "Feedback Feedforward Phase Margin Boost (C28, C43) & High-Frequency Noise Attenuation (C30)", "https://www.murata.com/"),

        # Resistors
        ("21", "R1, R3, R4, R6", "4", "49.9k, 137k, 100k (1%)", "Yageo / Panasonic", "RC0603FR-0749K9L", "0603 (1608 Metric)",
         "Resistance: 49.9k / 137k / 100k, 1%, 1/10W, ±100ppm/°C",
         "TPS2121 Overvoltage & Priority Comparators (OV1=5.8V, OV2=5.8V, PR1=4.4V)", "https://www.yageo.com/"),

        ("22", "R2, R5, R8, R21", "4", "10k, 158, 12k (1%)", "Yageo / Panasonic", "RC0603FR-07158RL", "0603 (1608 Metric)",
         "Current limit resistors: 10k (TPS2121 2.5A), 158 Ohm (BQ25895 3.25A), 12k (TPS61088 10A peak)",
         "Cycle-by-Cycle Overcurrent & Source Protection Resistors", "https://www.yageo.com/"),

        ("23", "R9, R10", "2", "5.23k, 30.1k (1%)", "Yageo", "RC0603FR-075K23L", "0603 (1608 Metric)",
         "Resistance: 5.23k / 30.1k, 1%, 1/10W",
         "BQ25895 JEITA Temperature Monitoring Window Divider (0°C to 45°C/60°C)", "https://www.yageo.com/"),

        ("24", "R11, R12, R13, R14, R25, R26, R27, R28", "8", "10k & 100k (1%)", "Yageo", "RC0603FR-0710KL", "0603 (1608 Metric)",
         "Resistance: 10k / 100k, 1%, 1/10W",
         "Open-Drain Pullups (STAT, INT, I2C), Enable Pullups (TPS62162, TPS62130, AO3401A)", "https://www.yageo.com/"),

        ("25", "R15, R16", "2", "100, 1k (1%)", "Yageo", "RC0603FR-07100RL", "0603 (1608 Metric)",
         "Resistance: 100 Ohm (R15), 1k Ohm (R16), 1%, 1/10W",
         "DW01A Battery Protection VCC Filter Resistor & Current Sense Input Resistor", "https://www.yageo.com/"),

        ("26", "R17, R18", "2", "100k (1%, ±25ppm)", "Vishay / Susumu", "MC06030F1003BP100", "0603 (1608 Metric)",
         "Resistance: 100k±0.1% / 1%, 25ppm/°C High-Precision Thin Film",
         "Battery Voltage Sensing Divider to ESP32 GPIO1 (ADC_VBAT_SENSE, Division 1:2)", "https://www.vishay.com/"),

        ("27", "R20, R24", "2", "200k, 20k (1%)", "Yageo", "RC0603FR-07200KL", "0603 (1608 Metric)",
         "Resistance: 200k (FSW 600kHz), 20k (COMP Resistor), 1%, 1/10W",
         "TPS61088 Boost Switching Frequency Setting & Loop Compensation", "https://www.yageo.com/"),

        ("28", "R22, R23, R29, R30", "4", "316k, 100k, 374k (1%)", "Yageo", "RC0603FR-07316KL", "0603 (1608 Metric)",
         "Resistance: 316k (5V_SYS Top), 374k (3.8V Top), 100k (Bottom), 1%, 1/10W",
         "Output Voltage Feedback Dividers for TPS61088 (5.0V) and TPS62130 (3.8V)", "https://www.yageo.com/"),

        # Protections: Fuses & TVS
        ("29", "F1, F2", "2", "2.0A & 3.0A PTC Fuse", "Bourns", "MF-MSMF200-2 / MF-MSMF300-2", "1812 (4532 Metric)",
         "Hold: 2.0A / 3.0A, Trip: 4.0A / 6.0A, Vmax: 16V / 24V, Resettable PPTC",
         "Input Overcurrent Protection on VEHICLE_5V_IN (F1) and USB_5V_IN (F2)", "https://www.bourns.com/docs/product-datasheets/mf-msmf.pdf"),

        ("30", "D1, D2, D3", "3", "SMAJ5.0A (TVS)", "Littelfuse", "SMAJ5.0A", "DO-214AC (SMA)",
         "Vwm: 5.0V, Vbr: 6.4V-7.0V, Vc_max: 9.2V @ 43.5A, 400W Peak Pulse Power",
         "Automotive ESD & Transient Voltage Suppressors on Inputs (D1, D2) and SIM_PWR (D3)", "https://www.littelfuse.com/"),

        ("31", "LED1, LED2", "2", "Green / Amber 0603", "Lite-On", "LTST-C190GKT", "0603 (1608 Metric)",
         "Vf: 2.0V, If: 5mA, Luminous Intensity: 15mcd",
         "Input Power Presence Indicators (Vehicle 5V Good / USB 5V Good)", "https://optoelectronics.liteon.com/"),

        # Connectors & Headers
        ("32", "J1", "1", "VEHICLE_5V_IN", "JST", "B2P-VH", "JST VH 2-Pin 3.96mm Vertical",
         "Pitch: 3.96mm, Current Rating: 10A AC/DC, Withstanding Voltage: 1500V AC",
         "External Regulated Vehicle 5V Power Input Header", "https://www.jst-mfg.com/product/pdf/eng/eVH.pdf"),

        ("33", "J2", "1", "USB_C_16P", "Korean Hroparts Elec", "TYPE-C-31-M-12", "USB-C 16-Pin SMD Receptacle",
         "USB 2.0 Type-C, 16-pin, 5.0A VBUS rating, CC1/CC2 5.1k pulldown resistors onboard",
         "External Bench Charging & Programming USB-C Input Port", "https://datasheet.lcsc.com/lcsc/1912111437_Korean-Hroparts-Elec-TYPE-C-31-M-12_C165948.pdf"),

        ("34", "J3", "1", "18650_CELL_IN", "JST", "B2P-VH", "JST VH 2-Pin 3.96mm Vertical",
         "Pitch: 3.96mm, Current Rating: 10A, Low Contact Resistance < 5mOhm",
         "Single-Cell 18650 Li-ion Battery Connector", "https://www.jst-mfg.com/product/pdf/eng/eVH.pdf"),

        ("35", "JP1", "1", "SIM_PWR_SEL", "Wurth Elektronik / Harwin", "61300311121", "Pin Header 1x03 2.54mm Vertical",
         "Pitch: 2.54mm, 3A rating, Gold plated with Shunt Jumper Cap",
         "Cellular Supply Hardware Selection (Pin 1-2: 5V Option A, Pin 2-3: 3.8V Option B)", "https://www.we-online.com/"),

        ("36", "J4", "1", "SYSTEM_POWER_BUS", "Wurth Elektronik", "61301011121", "Pin Header 1x10 2.54mm Vertical",
         "Pitch: 2.54mm, 3A per pin, 10-pin (Pins 1-2: 5V, 3-4: 3.3V, 5-6: VBAT, 7-10: GND)",
         "System Main Power Distribution Header to ESP32 DevKit & Peripherals", "https://www.we-online.com/"),

        ("37", "J5", "1", "A7682S_BREAKOUT_PWR", "Wurth Elektronik", "61300511121", "Pin Header 1x05 2.54mm Vertical",
         "Pitch: 2.54mm, 3A per pin, 5-pin (Pins 1-2: SIM_PWR, Pin 3: PWRKEY, Pins 4-5: GND)",
         "Dedicated Power & Control Cable Header to Physical A7682S Cellular Breakout", "https://www.we-online.com/"),

        ("38", "TP1-TP9", "9", "TestPoint_Pad_D1.5mm", "Keystone Electronics", "5015", "SMD Test Point Pad D1.5mm",
         "Through-Hole / SMD Miniature Test Point, Color Coded / Pad",
         "Diagnostic & Oscilloscope Probe Points (VBUS, SYS, VBAT, 5V, 3.3V, SIM, ADC, PWRKEY)", "https://www.keyelco.com/")
    ]

    # Write data rows
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )

    for row_idx, item in enumerate(bom_data, header_row + 1):
        ws.row_dimensions[row_idx].height = 22
        # Zebra striping
        row_fill = PatternFill(start_color="F2F5F9" if row_idx % 2 == 0 else "FFFFFF",
                               end_color="F2F5F9" if row_idx % 2 == 0 else "FFFFFF",
                               fill_type="solid")
        for col_idx, val in enumerate(item, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            cell.font = Font(name="Calibri", size=10)
            cell.fill = row_fill
            cell.border = thin_border
            if col_idx in [1, 3]: # Item, Qty
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx in [2, 4, 6]: # Designator, Value, MPN
                cell.alignment = Alignment(horizontal="left", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

    # Auto-fit column widths
    col_widths = {
        1: 8,   # Item
        2: 24,  # Designator
        3: 8,   # Qty
        4: 26,  # Value
        5: 22,  # Manufacturer
        6: 28,  # MPN
        7: 28,  # Package
        8: 45,  # Key Ratings
        9: 45,  # Function
        10: 35  # Link
    }
    for col_idx, width in col_widths.items():
        col_letter = get_column_letter(col_idx)
        ws.column_dimensions[col_letter].width = width

    out_file = "05_POWER_BOM.xlsx"
    wb.save(out_file)
    print(f"BOM successfully generated: {out_file}")

if __name__ == "__main__":
    generate_bom()
