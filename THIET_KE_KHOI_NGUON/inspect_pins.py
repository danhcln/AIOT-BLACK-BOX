# -*- coding: utf-8 -*-
import os, re
import generate_symbols as s

for name, sym in [
    ('R', s.SYM_R), 
    ('C', s.SYM_C), 
    ('L', s.SYM_L), 
    ('TVS', s.SYM_D_TVS), 
    ('FUSE', s.SYM_FUSE), 
    ('GND', s.SYM_GND), 
    ('PWR_FLAG', s.SYM_PWR_FLAG), 
    ('Conn02', s.SYM_CONN_02), 
    ('Conn05', s.SYM_CONN_05), 
    ('Conn10', s.SYM_CONN_10), 
    ('TP', s.SYM_TESTPOINT), 
    ('Jumper3', s.SYM_JUMPER3)
]:
    pins = re.findall(r'\(pin\s+\w+\s+\w+\s+\(at\s+([-\d\.]+)\s+([-\d\.]+)\s*(\d*)\).*?\(number\s+"([^"]+)"', sym, re.DOTALL)
    print(f'{name}: {pins}')
