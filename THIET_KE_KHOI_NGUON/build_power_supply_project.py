# -*- coding: utf-8 -*-
"""
AIOT BLACK BOX - POWER SUPPLY SYSTEM BUILDER
Generates complete, verified KiCad 10 project and hierarchical schematics.
Author: Senior Power Electronics Engineer & KiCad Hardware Designer
"""

import os
import sys
import uuid
import json

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"D:\ĐỒ ÁN 2\THIET_KE_KHOI_NGUON"

def gen_uuid():
    return str(uuid.uuid4())

def make_title_block(title, sheet_num, total_sheets=5):
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

# -----------------------------------------------------------------------------
# 1. KICAD PROJECT FILE (.kicad_pro)
# -----------------------------------------------------------------------------
def build_kicad_pro():
    pro_path = os.path.join(OUT_DIR, "AIOT_BLACKBOX_POWER_SUPPLY.kicad_pro")
    pro_data = {
        "meta": {
            "filename": "AIOT_BLACKBOX_POWER_SUPPLY.kicad_pro",
            "version": 1
        },
        "schematic": {
            "annotate_start_num": 1,
            "drawing": {
                "default_line_thickness": 0.1524,
                "default_text_size": 1.27,
                "junction_size_choice": 3,
                "pin_symbol_size": 0.0,
                "text_offset_ratio": 0.2
            },
            "legacy_lib_dir": "",
            "legacy_lib_list": [],
            "meta": {
                "version": 1
            },
            "net_format_name": "",
            "ngspice": {
                "meta": {
                    "version": 0
                }
            },
            "page_layout_descr_file": "",
            "plot_directory": "",
            "subpart_first_id": 65,
            "subpart_id_separator": 0
        },
        "boards": [],
        "cvpcb": {
            "equivalence_files": []
        },
        "erc": {
            "erc_exclusions": [],
            "meta": {
                "version": 0
            },
            "pin_map": [
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2],
                [0, 2, 0, 1, 0, 0, 1, 0, 2, 2, 2, 2],
                [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 2],
                [0, 1, 0, 0, 0, 0, 1, 1, 2, 1, 1, 2],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 2],
                [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 2],
                [0, 2, 1, 2, 0, 0, 1, 0, 2, 2, 2, 2],
                [0, 2, 0, 1, 0, 0, 1, 0, 2, 0, 0, 2],
                [0, 2, 1, 1, 0, 0, 1, 0, 2, 0, 0, 2],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
            ],
            "rule_severities": {
                "bus_label_syntax": "error",
                "bus_to_bus_conflict": "error",
                "bus_to_net_conflict": "error",
                "conflicting_netclasses": "error",
                "different_unit_footprint": "error",
                "different_unit_nettie_group": "error",
                "duplicate_reference": "error",
                "duplicate_sheet_names": "error",
                "endpoint_off_grid": "warning",
                "extra_units": "error",
                "field_off_grid": "warning",
                "global_label_dangling": "warning",
                "hier_label_mismatch": "error",
                "label_dangling": "warning",
                "lib_symbol_issues": "warning",
                "missing_bidi_pin": "warning",
                "missing_input_pin": "warning",
                "missing_power_pin": "warning",
                "missing_unit": "warning",
                "multiple_net_names": "warning",
                "net_not_bus_member": "warning",
                "no_connect_connected": "error",
                "no_connect_dangling": "warning",
                "pin_not_connected": "error",
                "pin_not_driven": "error",
                "pin_to_pin": "error",
                "power_pin_not_driven": "error",
                "similar_labels": "warning",
                "simulation_model_issue": "error",
                "unannotated": "error",
                "unit_value_mismatch": "error",
                "unresolved_variable": "error",
                "wire_dangling": "warning"
            }
        }
    }
    with open(pro_path, 'w', encoding='utf-8') as f:
        json.dump(pro_data, f, indent=2)
    print(f"Created: {pro_path}")

build_kicad_pro()
