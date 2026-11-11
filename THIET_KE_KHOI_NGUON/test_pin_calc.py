# -*- coding: utf-8 -*-
import re
import custom_symbols_def as cust_syms
import generate_symbols as base_syms

def get_pin_offset(sym_str, pin_num, rot=0):
    pattern = rf'\(pin\s+\S+\s+\S+\s+\(at\s+([-\d\.]+)\s+([-\d\.]+)[^\)]*\)(?:(?!\(pin).)*?\(number\s+"{pin_num}"'
    m = re.search(pattern, sym_str, re.DOTALL)
    if not m:
        raise ValueError(f"Pin {pin_num} not found")
    px, py = float(m.group(1)), float(m.group(2))
    if rot == 0:
        return round(px, 4), round(py, 4)
    elif rot == 90:
        return round(-py, 4), round(px, 4)
    elif rot == 180:
        return round(-px, 4), round(-py, 4)
    elif rot == 270:
        return round(py, 4), round(-px, 4)
    return round(px, 4), round(py, 4)

print("TPS2121 Pin 7 at rot=0:", get_pin_offset(cust_syms.SYM_TPS2121, "7", 0))
print("TPS2121 Pin 1 at rot=0:", get_pin_offset(cust_syms.SYM_TPS2121, "1", 0))
print("Fuse Pin 1 at rot=90:", get_pin_offset(base_syms.SYM_FUSE, "1", 90))
print("Fuse Pin 2 at rot=90:", get_pin_offset(base_syms.SYM_FUSE, "2", 90))
print("R Pin 1 at rot=0:", get_pin_offset(base_syms.SYM_R, "1", 0))
print("R Pin 2 at rot=0:", get_pin_offset(base_syms.SYM_R, "2", 0))
