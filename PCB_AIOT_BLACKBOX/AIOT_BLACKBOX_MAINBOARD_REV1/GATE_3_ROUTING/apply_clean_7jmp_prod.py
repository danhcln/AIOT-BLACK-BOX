import pcbnew, os, shutil, subprocess, re

proj_dir = r'D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1'
base_bak = os.path.join(proj_dir, 'GATE_3_ROUTING', 'backup', 'AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pcb.20261110_103027.bak')
target_pcb = os.path.join(proj_dir, 'AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pcb')
kicad_cli = r'D:\KiCad\bin\kicad-cli.exe'
lib_path = os.path.join(proj_dir, 'AIOT_Blackbox_Local.pretty')

# Copy base to target
shutil.copyfile(base_bak, target_pcb)
b = pcbnew.LoadBoard(target_pcb)
netinfo = b.GetNetInfo()

def add_path(net_name, pts, width_mm):
    net = netinfo.GetNetItem(net_name)
    if not net: raise ValueError(f"Net {net_name} not found!")
    w = pcbnew.FromMM(width_mm)
    for i in range(len(pts) - 1):
        t = pcbnew.PCB_TRACK(b)
        t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(pts[i][0]), pcbnew.FromMM(pts[i][1])))
        t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(pts[i+1][0]), pcbnew.FromMM(pts[i+1][1])))
        t.SetLayer(pcbnew.B_Cu)
        t.SetWidth(w)
        t.SetNetCode(net.GetNetCode())
        b.Add(t)

def add_jumper(fp_name, ref, val, x, y, angle, netname, ref_pos):
    fp = pcbnew.FootprintLoad(lib_path, fp_name)
    fp.SetReference(ref)
    fp.SetValue(val)
    fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    fp.SetOrientationDegrees(angle)
    fp.Reference().SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(ref_pos[0]), pcbnew.FromMM(ref_pos[1])))
    net = netinfo.GetNetItem(netname)
    for p in fp.Pads(): p.SetNet(net)
    b.Add(fp)
    pads = {}
    for p in fp.Pads():
        pos = p.GetPosition()
        pads[p.GetNumber()] = (round(pcbnew.ToMM(pos.x), 2), round(pcbnew.ToMM(pos.y), 2))
    p1, p2 = pads['1'], pads['2']
    if angle == 90.0:
        return (p1, p2) if p1[1] < p2[1] else (p2, p1)
    else:
        return (p1, p2) if p1[0] < p2[0] else (p2, p1)

# ====================================================
# 7 JUMPERS (JMP1 - JMP7)
# ====================================================
j1_n, j1_s = add_jumper('WireJumper_P12.70mm_SingleLayer', 'JMP1', 'Wire_Jumper_12.70mm', 151.00, 105.32, 90.0, 'Net-(J1-MOSI)', (146.0, 105.32))
j2_n, j2_s = add_jumper('WireJumper_P7.62mm_SingleLayer', 'JMP2', 'Wire_Jumper_7.62mm', 81.00, 58.00, 90.0, '3V3_SYS', (81.0, 49.0))
j3_n, j3_s = add_jumper('WireJumper_P7.62mm_SingleLayer', 'JMP3', 'Wire_Jumper_7.62mm', 145.00, 57.92, 90.0, 'Net-(U1-GPIO6)', (141.0, 57.92))
j4_n, j4_s = add_jumper('WireJumper_P10.16mm_SingleLayer', 'JMP4', 'Wire_Jumper_10.16mm', 112.00, 93.50, 90.0, '/I2C_SDA_GPIO8', (112.00, 85.0))
j5_n, j5_s = add_jumper('WireJumper_P7.62mm_SingleLayer', 'JMP5', 'Wire_Jumper_7.62mm', 124.00, 46.00, 90.0, 'Net-(U1-GPIO6)', (124.0, 40.0))
# JMP6 at Y=106.30 (maintains >0.40mm clearance to 5V_SYS at Y=109.13):
j6_w, j6_e = add_jumper('WireJumper_P7.62mm_SingleLayer', 'JMP6', 'Wire_Jumper_7.62mm', 143.08, 106.30, 0.0, 'Net-(J1-MISO)', (143.08, 109.0))
# JMP7 at X=80.00:
j7_n, j7_s = add_jumper('WireJumper_P10.16mm_SingleLayer', 'JMP7', 'Wire_Jumper_10.16mm', 80.00, 90.92, 90.0, '3V3_SYS', (76.0, 90.92))

# ====================================================
# 1. POWER RAILS
# ====================================================
# SIM_PWR (2.50mm / 2.00mm, clearance >= 0.50mm to PWRKEY)
add_path('SIM_PWR', [(77.27, 58.00), (78.50, 58.00)], 1.00)
add_path('SIM_PWR', [(78.50, 58.00), (84.46, 58.00)], 2.50)
add_path('SIM_PWR', [(84.46, 58.00), (84.46, 55.00), (95.00, 55.00)], 2.50)
add_path('SIM_PWR', [(95.00, 55.00), (95.00, 68.00), (95.46, 68.00)], 2.00)
add_path('SIM_PWR', [(95.00, 55.00), (98.00, 55.00), (98.00, 50.00)], 2.00)

# 5V_SYS (1.50mm)
add_path('5V_SYS', [(60.00, 64.54), (56.00, 64.54), (56.00, 56.00), (68.00, 56.00), (74.73, 56.00), (74.73, 58.00)], 1.50)
add_path('5V_SYS', [(60.00, 64.54), (56.00, 64.54), (56.00, 76.00), (62.19, 76.00)], 1.50)
add_path('5V_SYS', [(68.00, 56.00), (68.00, 43.50), (120.00, 43.50), (120.00, 46.00), (132.19, 46.00), (132.19, 48.00)], 1.50)
add_path('5V_SYS', [(56.00, 76.00), (56.00, 126.00), (154.00, 126.00), (154.00, 109.13), (157.30, 109.13)], 1.50)
add_path('5V_SYS', [(154.00, 109.13), (141.81, 109.13), (141.81, 104.00)], 1.50)

# 3V3_SYS (1.00mm / 0.80mm)
add_path('3V3_SYS', [(67.27, 76.00), (67.27, 78.50), (75.46, 78.50), (75.46, 76.00)], 1.00)
add_path('3V3_SYS', [(75.46, 78.50), (78.00, 78.50), (78.00, 70.00), (81.00, 70.00), j2_s], 1.00)
add_path('3V3_SYS', [j2_n, (81.00, 47.50), (110.92, 47.50), (110.92, 53.50)], 1.00)
add_path('3V3_SYS', [(75.46, 78.50), (75.46, 84.50), (116.92, 84.50), (116.92, 80.00)], 1.00)
add_path('3V3_SYS', [(116.92, 84.50), (134.92, 84.50), (134.92, 86.50)], 0.80)
# South perimeter rail to U7.2
add_path('3V3_SYS', [(67.27, 78.50), (58.50, 78.50), (58.50, 122.00), (100.73, 122.00), (100.73, 116.50)], 1.00)

# 3V3_SYS via JMP7 to U3.5 and U2.1
add_path('3V3_SYS', [(75.46, 84.50), (80.00, 84.50), j7_n], 0.80)
add_path('3V3_SYS', [j7_s, (80.00, 96.00), (71.81, 96.00), (71.81, 100.00)], 0.80)
add_path('3V3_SYS', [(80.00, 96.00), (87.11, 96.00)], 0.80)

# ====================================================
# 2. SPI BUS
# ====================================================
add_path('/SD_CS_GPIO10', [(131.65, 104.00), (127.00, 104.00), (127.00, 96.43), (157.30, 96.43)], 0.35)
add_path('Net-(J1-MOSI)', [(136.73, 104.00), (136.73, 111.67), j1_s], 0.35)
add_path('Net-(J1-MOSI)', [j1_n, (157.30, 98.97)], 0.35)
add_path('Net-(J1-SCK)', [(134.19, 104.00), (134.19, 101.51), (157.30, 101.51)], 0.35)

# Net-(J1-MISO) via JMP6
add_path('Net-(J1-MISO)', [(139.27, 104.00), (139.27, 106.30), j6_w], 0.35)
add_path('Net-(J1-MISO)', [j6_e, (146.89, 104.05), (157.30, 104.05)], 0.35)

# ====================================================
# 3. UART & CONTROLS
# ====================================================
add_path('/GPS_TX_GPIO17', [(124.54, 80.00), (124.54, 82.00), (154.00, 82.00), (154.00, 81.19), (157.30, 81.19)], 0.35)
add_path('/GPS_RX_GPIO18', [(122.00, 80.00), (122.00, 83.50), (154.00, 83.50), (154.00, 83.73), (157.30, 83.73)], 0.35)
add_path('/SIM_RX_GPIO15', [(103.08, 68.00), (103.08, 75.00), (154.00, 75.00), (154.00, 76.11), (157.30, 76.11)], 0.35)
add_path('/SIM_TX_GPIO16', [(100.54, 68.00), (100.54, 77.00), (154.00, 77.00), (154.00, 78.65), (157.30, 78.65)], 0.35)
add_path('/LED_STATUS_GPIO7', [(116.92, 66.50), (116.92, 73.57), (157.30, 73.57)], 0.30)
add_path('Net-(D1-A)', [(113.27, 66.50), (113.27, 63.50), (127.08, 63.50), (127.08, 66.50)], 0.30)

add_path('Net-(U1-GPIO6)', [(114.73, 47.00), (114.73, 49.81), (121.08, 49.81), (121.08, 53.50)], 0.30)
add_path('Net-(U1-GPIO6)', [(114.73, 49.81), (113.46, 49.81), (113.46, 60.00)], 0.30)
add_path('Net-(U1-GPIO6)', [(121.08, 49.81), j5_s], 0.30)
add_path('Net-(U1-GPIO6)', [j5_n, (124.00, 42.19), (145.00, 42.19), (145.00, 54.11), j3_n], 0.30)
add_path('Net-(U1-GPIO6)', [j3_s, (145.00, 61.73), (145.00, 71.03), (157.30, 71.03)], 0.30)

add_path('/BUZZER_CTRL_GPIO5', [(149.00, 68.08), (153.00, 68.08), (153.00, 68.49), (157.30, 68.49)], 0.30)
add_path('Net-(Q1-B)', [(149.00, 57.92), (138.54, 57.92), (138.54, 63.00)], 0.30)
add_path('Net-(Q1-B)', [(138.54, 63.00), (138.54, 66.00), (130.92, 66.00), (130.92, 71.00)], 0.30)
add_path('Net-(BZ1--)', [(139.81, 48.00), (139.81, 55.00), (136.00, 55.00), (136.00, 61.09)], 0.50)

# ====================================================
# 4. I2C BUS (SDA & SCL)
# ====================================================
add_path('/I2C_SDA_GPIO8', [j4_n, (112.00, 88.50), (145.08, 88.50), (145.08, 86.50)], 0.35)
add_path('/I2C_SDA_GPIO8', [(145.08, 86.50), (153.00, 86.50), (153.00, 86.27), (157.30, 86.27)], 0.35)

add_path('/I2C_SCL_GPIO9', [(145.08, 93.50), (153.00, 93.50), (153.00, 93.89), (157.30, 93.89)], 0.35)
add_path('/I2C_SCL_GPIO9', [(145.08, 93.50), (145.08, 91.50), (92.19, 91.50), (92.19, 96.00)], 0.35)
# SCL continuing West to U3.3 under JMP7
add_path('/I2C_SCL_GPIO9', [(92.19, 91.50), (66.73, 91.50), (66.73, 100.00)], 0.35)

# ====================================================
# 5. SOLID GROUND COPPER POUR & SPINES
# ====================================================
add_path('GND', [(80.54, 76.00), (80.54, 73.00)], 0.50)
add_path('GND', [(89.54, 58.00), (89.54, 62.00)], 0.50)
add_path('GND', [(100.54, 58.00), (100.54, 62.00)], 0.50)
add_path('GND', [(98.19, 116.50), (98.19, 120.00)], 0.50)
add_path('GND', [(89.65, 96.00), (89.65, 100.00)], 0.50)
add_path('GND', [(157.30, 111.67), (157.30, 116.00)], 0.50)
add_path('GND', [(51.50, 43.00), (51.50, 142.00)], 0.80)
# Dedicated ground track connecting U1.22 and U1.23 along East margin (X=187.00)
add_path('GND', [(157.30, 116.00), (187.00, 116.00), (187.00, 58.33), (182.70, 58.33)], 0.80)

gnd_net = netinfo.GetNetItem('GND')
poly = pcbnew.SHAPE_POLY_SET()
poly.NewOutline()
for x, y in [(50.0, 40.0), (195.0, 40.0), (195.0, 145.0), (50.0, 145.0)]:
    poly.Append(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
z = pcbnew.ZONE(b)
z.SetLayer(pcbnew.B_Cu)
z.SetNetCode(gnd_net.GetNetCode())
z.SetOutline(poly)
z.SetZoneName('GND_COPPER_POUR_BCU')
z.SetLocalClearance(pcbnew.FromMM(0.40))
z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
b.Add(z)

ds = b.GetDesignSettings()
ds.m_MinResolvedSpokes = 1
zf = pcbnew.ZONE_FILLER(b)
zf.Fill(b.Zones())

pcbnew.SaveBoard(target_pcb, b)
print("Production board updated successfully:", target_pcb)

# Run official DRC on production board
drc_out = os.path.join(proj_dir, 'GATE_3_ROUTING', 'DRC_ROUTING_FINAL.txt')
subprocess.run([kicad_cli, 'pcb', 'drc', '--severity-all', '--output', drc_out, target_pcb], capture_output=True)
with open(drc_out, 'r', encoding='utf-8') as f: txt = f.read()

crossings = len(re.findall(r'\[tracks_crossing\]', txt))
shorts = len(re.findall(r'\[shorting_items\]', txt))
clearance = len(re.findall(r'\[clearance\]', txt))
unconnected = len(re.findall(r'\[unconnected_items\]', txt))
courtyard = len(re.findall(r'\[courtyard[s_overlap]+\]', txt)) + len(re.findall(r'\[pth_inside_courtyard\]', txt))
warnings = len(re.findall(r'\[silk_[a-z_]+\]', txt))

print(f"\n=== OFFICIAL PRODUCTION DRC REPORT ===")
print(f"Tracks Crossing: {crossings}")
print(f"Shorting Items:  {shorts}")
print(f"Clearance:       {clearance}")
print(f"Courtyard:       {courtyard}")
print(f"Unconnected:     {unconnected}")
print(f"Silk Warnings:   {warnings}")
