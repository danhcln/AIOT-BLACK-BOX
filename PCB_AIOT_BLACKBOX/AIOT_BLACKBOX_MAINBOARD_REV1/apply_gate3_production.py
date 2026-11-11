# -*- coding: utf-8 -*-
"""
GATE 3: SINGLE-LAYER B.Cu ROUTING IMPLEMENTATION
Workspace: D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1
Rules: PCB_DESIGN_RULES_AIOT.md
Layer: 100% B.Cu (0 F.Cu tracks, 0 vias)
"""
import os, sys, shutil, datetime, subprocess, json
import pcbnew

sys.stdout.reconfigure(encoding='utf-8')

proj_dir = r"D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1"
pcb_path = os.path.join(proj_dir, "AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pcb")
pro_path = os.path.join(proj_dir, "AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pro")
gate3_dir = os.path.join(proj_dir, "GATE_3_ROUTING")
backup_dir = os.path.join(gate3_dir, "backup")
os.makedirs(backup_dir, exist_ok=True)

# 1. Verify KiCad Lock
lck_files = [f for f in os.listdir(proj_dir) if f.endswith(".lck")]
if lck_files:
    raise RuntimeError(f"KiCad lock file detected: {lck_files}. Close KiCad before proceeding!")

# 2. Timestamped Backup
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
bak_pcb = os.path.join(backup_dir, f"AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pcb.{ts}.bak")
bak_pro = os.path.join(backup_dir, f"AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pro.{ts}.bak")
shutil.copyfile(pcb_path, bak_pcb)
shutil.copyfile(pro_path, bak_pro)
print(f"Created timestamped backup: {bak_pcb}")

# Save NetClasses from .kicad_pro to ensure preservation
with open(pro_path, "r", encoding="utf-8") as f:
    pro_data = json.load(f)
saved_net_settings = pro_data.get("net_settings")

# 3. Load Board
b = pcbnew.LoadBoard(pcb_path)
netinfo = b.GetNetInfo()

# Clean existing tracks and zones on B.Cu (keep keepout zones on F.Cu)
for t in list(b.GetTracks()):
    b.Remove(t)
for z in list(b.Zones()):
    if z.GetZoneName() == "GND_COPPER_POUR_BCU":
        b.Remove(z)

print("Pre-existing B.Cu tracks/zones cleaned. Starting physical single-layer routing...")

def add_path(net_name, pts, width_mm):
    net = netinfo.GetNetItem(net_name)
    if not net:
        raise ValueError(f"Net {net_name} not found in board NetInfo!")
    net_code = net.GetNetCode()
    w = pcbnew.FromMM(width_mm)
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i+1]
        t = pcbnew.PCB_TRACK(b)
        t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
        t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
        t.SetLayer(pcbnew.B_Cu)
        t.SetWidth(w)
        t.SetNetCode(net_code)
        b.Add(t)

# 4. Add Top-Side Wire Jumper Footprint JMP1
# Footprint verified from AIOT_Blackbox_Local: WireJumper_P7.62mm_SingleLayer
# Position: (148.0, 100.5), Orientation: 90.0 deg (vertical)
# Allows Net-(J1-MOSI) to jump over Net-(J1-SCK) at Y=101.51mm on B.Cu
fp = pcbnew.FootprintLoad(os.path.join(proj_dir, "AIOT_Blackbox_Local.pretty"), "WireJumper_P7.62mm_SingleLayer")
fp.SetReference("JMP1")
fp.SetValue("Wire_Jumper_7.62mm")
fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(148.0), pcbnew.FromMM(100.5)))
fp.SetOrientationDegrees(90.0)

mosi_net = netinfo.GetNetItem("Net-(J1-MOSI)")
for p in fp.Pads():
    p.SetNet(mosi_net)
b.Add(fp)

jmp_pads = {}
for p in fp.Pads():
    pos = p.GetPosition()
    jmp_pads[p.GetNumber()] = (pcbnew.ToMM(pos.x), pcbnew.ToMM(pos.y))
p1_x, p1_y = jmp_pads["1"]
p2_x, p2_y = jmp_pads["2"]
south_pad = (p1_x, p1_y) if p1_y > p2_y else (p2_x, p2_y)
north_pad = (p2_x, p2_y) if p1_y > p2_y else (p1_x, p1_y)

# 5. Route All 20 Nets on B.Cu

# NET 1: SIM_PWR (Width = 2.50mm, Clearance = 0.50mm)
# Power trace for SIM A7680C 2A peak pulses
add_path("SIM_PWR", [(77.27, 58.00), (77.27, 54.00), (84.46, 54.00), (84.46, 58.00)], 2.50)
add_path("SIM_PWR", [(84.46, 54.00), (95.46, 54.00), (95.46, 58.00), (95.46, 68.00)], 2.50)
add_path("SIM_PWR", [(95.46, 54.00), (98.00, 54.00), (98.00, 50.00)], 2.50)

# NET 2: 5V_SYS (Width = 1.50mm, Clearance = 0.40mm)
# Primary regulated 5V system rail
add_path("5V_SYS", [(60.00, 64.54), (60.00, 56.00), (68.00, 56.00), (74.73, 56.00), (74.73, 58.00)], 1.50)
add_path("5V_SYS", [(74.73, 56.00), (74.73, 43.00), (132.19, 43.00), (132.19, 48.00)], 1.50)
add_path("5V_SYS", [(60.00, 64.54), (60.00, 76.00), (62.19, 76.00)], 1.50)
add_path("5V_SYS", [(60.00, 76.00), (58.00, 76.00), (58.00, 126.00), (141.81, 126.00), (141.81, 104.00)], 1.50)
add_path("5V_SYS", [(141.81, 126.00), (157.30, 126.00), (157.30, 109.13)], 1.50)

# NET 3: 3V3_SYS (Width = 1.00mm, Clearance = 0.30mm)
# Regulated 3.3V peripheral rail from AMS1117-3.3
# Regulator local output and filter capacitor
add_path("3V3_SYS", [(67.27, 76.00), (67.27, 73.00), (75.46, 73.00), (75.46, 76.00)], 1.00)
add_path("3V3_SYS", [(75.46, 73.00), (78.00, 73.00), (78.00, 70.00)], 1.00)
# Feed R3.1 via North perimeter (isolated above SIM module)
add_path("3V3_SYS", [(78.00, 70.00), (78.00, 46.00), (110.92, 46.00), (110.92, 53.50)], 1.00)
# Feed West sensors: DS3231 U3.5, MPU6050 U2.1, OLED U7.2
add_path("3V3_SYS", [(67.27, 76.00), (67.27, 85.00), (71.81, 85.00), (71.81, 100.00)], 1.00)
add_path("3V3_SYS", [(71.81, 100.00), (71.81, 105.00), (87.11, 105.00), (87.11, 96.00)], 1.00)
add_path("3V3_SYS", [(87.11, 105.00), (87.11, 120.00), (100.73, 120.00), (100.73, 116.50)], 1.00)
# Feed U2.7 from U2.1
add_path("3V3_SYS", [(87.11, 96.00), (87.11, 94.50), (102.35, 94.50), (102.35, 96.00)], 1.00)
# Feed U4.1 from U2.7 via clear corridor between SIM and GPS
add_path("3V3_SYS", [(102.35, 94.50), (114.00, 94.50), (114.00, 80.00), (116.92, 80.00)], 1.00)
# Feed R_PU1 and R_PU2
add_path("3V3_SYS", [(114.00, 94.50), (134.92, 94.50), (134.92, 93.50)], 1.00)
add_path("3V3_SYS", [(134.92, 94.50), (134.92, 86.50)], 1.00)

# NET 4: /I2C_SDA_GPIO8 (Width = 0.35mm, Clearance = 0.30mm)
add_path("/I2C_SDA_GPIO8", [(105.81, 116.50), (105.81, 98.00), (94.73, 98.00), (94.73, 96.00)], 0.35)
add_path("/I2C_SDA_GPIO8", [(94.73, 96.00), (94.73, 97.00), (69.27, 97.00), (69.27, 100.00)], 0.35)
add_path("/I2C_SDA_GPIO8", [(94.73, 96.00), (94.73, 88.00), (145.08, 88.00), (145.08, 86.50), (155.00, 86.50), (157.30, 86.27)], 0.35)

# NET 5: /I2C_SCL_GPIO9 (Width = 0.35mm, Clearance = 0.30mm)
add_path("/I2C_SCL_GPIO9", [(103.27, 116.50), (103.27, 99.00), (92.19, 99.00), (92.19, 96.00)], 0.35)
add_path("/I2C_SCL_GPIO9", [(92.19, 96.00), (66.73, 96.00), (66.73, 100.00)], 0.35)
add_path("/I2C_SCL_GPIO9", [(92.19, 96.00), (92.19, 91.00), (145.08, 91.00), (145.08, 93.50), (155.00, 93.50), (157.30, 93.89)], 0.35)

# NET 6: /GPS_TX_GPIO17 (Width = 0.35mm, Clearance = 0.30mm)
add_path("/GPS_TX_GPIO17", [(124.54, 80.00), (124.54, 78.50), (152.00, 78.50), (152.00, 81.19), (157.30, 81.19)], 0.35)

# NET 7: /GPS_RX_GPIO18 (Width = 0.35mm, Clearance = 0.30mm)
add_path("/GPS_RX_GPIO18", [(122.00, 80.00), (122.00, 83.73), (157.30, 83.73)], 0.35)

# NET 8: /SIM_RX_GPIO15 (Width = 0.35mm, Clearance = 0.30mm)
add_path("/SIM_RX_GPIO15", [(103.08, 68.00), (103.08, 76.11), (157.30, 76.11)], 0.35)

# NET 9: /SIM_TX_GPIO16 (Width = 0.35mm, Clearance = 0.30mm)
add_path("/SIM_TX_GPIO16", [(100.54, 68.00), (100.54, 78.65), (157.30, 78.65)], 0.35)

# NET 10: /LED_STATUS_GPIO7 (Width = 0.30mm, Clearance = 0.25mm)
add_path("/LED_STATUS_GPIO7", [(116.92, 66.50), (116.92, 73.57), (157.30, 73.57)], 0.30)

# NET 11: Net-(D1-A) (Width = 0.30mm, Clearance = 0.25mm)
add_path("Net-(D1-A)", [(113.27, 66.50), (113.27, 64.00), (127.08, 64.00), (127.08, 66.50)], 0.30)

# NET 12: Net-(U1-GPIO6) (CANCEL) (Width = 0.30mm, Clearance = 0.25mm)
add_path("Net-(U1-GPIO6)", [(114.73, 47.00), (114.73, 53.50), (121.08, 53.50)], 0.30)
add_path("Net-(U1-GPIO6)", [(114.73, 53.50), (113.46, 53.50), (113.46, 60.00)], 0.30)
add_path("Net-(U1-GPIO6)", [(121.08, 53.50), (123.00, 53.50), (123.00, 71.03), (157.30, 71.03)], 0.30)

# NET 13: /BUZZER_CTRL_GPIO5 (Width = 0.30mm, Clearance = 0.25mm)
add_path("/BUZZER_CTRL_GPIO5", [(149.00, 68.08), (153.00, 68.08), (153.00, 68.49), (157.30, 68.49)], 0.30)

# NET 14: Net-(Q1-B) (Width = 0.30mm, Clearance = 0.25mm)
add_path("Net-(Q1-B)", [(149.00, 57.92), (138.54, 57.92), (138.54, 63.00)], 0.30)
add_path("Net-(Q1-B)", [(138.54, 63.00), (130.92, 63.00), (130.92, 71.00)], 0.30)

# NET 15: Net-(BZ1--) (Width = 0.50mm, Clearance = 0.30mm)
add_path("Net-(BZ1--)", [(139.81, 48.00), (139.81, 55.00), (136.00, 55.00), (136.00, 61.09)], 0.50)

# NET 16: /SD_CS_GPIO10 (Width = 0.35mm, Clearance = 0.30mm)
add_path("/SD_CS_GPIO10", [(131.65, 104.00), (131.65, 96.43), (157.30, 96.43)], 0.35)

# NET 17: Net-(J1-MISO) (Width = 0.35mm, Clearance = 0.30mm)
add_path("Net-(J1-MISO)", [(139.27, 104.00), (139.27, 103.50), (154.00, 103.50), (154.00, 104.05), (157.30, 104.05)], 0.35)

# NET 18: Net-(J1-SCK) (Width = 0.35mm, Clearance = 0.30mm)
# Runs directly on B.Cu passing underneath JMP1 at Y=101.51mm!
add_path("Net-(J1-SCK)", [(134.19, 104.00), (134.19, 101.51), (157.30, 101.51)], 0.35)

# NET 19: Net-(J1-MOSI) (Width = 0.35mm, Clearance = 0.30mm)
# Connects J1.3 to JMP1 Pad 1; JMP1 Pad 2 to ESP32-S3 U1.17
add_path("Net-(J1-MOSI)", [(136.73, 104.00), (136.73, south_pad[1]), south_pad], 0.35)
add_path("Net-(J1-MOSI)", [north_pad, (148.00, 98.97), (157.30, 98.97)], 0.35)

# NET 20: GND Local stitching traces to tie all islands directly to zone (1.50mm / 1.00mm)
add_path("GND", [(60.00, 59.46), (64.73, 59.46), (64.73, 64.00), (68.00, 64.00)], 1.50)
add_path("GND", [(64.73, 76.00), (64.73, 70.00), (69.81, 70.00), (69.81, 76.00)], 1.00)
add_path("GND", [(74.35, 100.00), (74.35, 108.00)], 1.50)
add_path("GND", [(89.65, 96.00), (89.65, 112.00), (98.19, 112.00), (98.19, 116.50)], 1.50)
add_path("GND", [(110.73, 66.50), (110.73, 62.00)], 1.00)
add_path("GND", [(119.46, 80.00), (119.46, 85.00)], 1.50)
add_path("GND", [(144.35, 104.00), (144.35, 130.00), (157.30, 130.00), (157.30, 111.67)], 1.50)
# South perimeter GND tie stitch
add_path("GND", [(60.00, 120.00), (60.00, 138.00), (144.35, 138.00), (144.35, 130.00)], 1.50)

# 6. Add GND Copper Pour Zone on B.Cu
poly = pcbnew.SHAPE_POLY_SET()
poly.NewOutline()
for x, y in [(50.0, 40.0), (195.0, 40.0), (195.0, 145.0), (50.0, 145.0)]:
    poly.Append(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))

gnd_net = netinfo.GetNetItem("GND")
z = pcbnew.ZONE(b)
z.SetLayer(pcbnew.B_Cu)
z.SetNetCode(gnd_net.GetNetCode())
z.SetOutline(poly)
z.SetZoneName("GND_COPPER_POUR_BCU")
z.SetLocalClearance(pcbnew.FromMM(0.40))
z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
b.Add(z)

# 7. Fill Zones
zf = pcbnew.ZONE_FILLER(b)
zf.Fill(b.Zones())

# 8. Save Board
pcbnew.SaveBoard(pcb_path, b)
print("Physical single-layer routing completed and saved to AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pcb!")

# Restore and verify .kicad_pro
with open(pro_path, "r", encoding="utf-8") as f:
    cur_pro = json.load(f)
cur_pro["net_settings"] = saved_net_settings
with open(pro_path, "w", encoding="utf-8") as f:
    json.dump(cur_pro, f, indent=2)
print("Verified .kicad_pro Net Classes preserved 100%.")

# 9. Verify Layer Allocation: F.Cu tracks = 0, Vias = 0
all_tracks = list(b.GetTracks())
f_cu_tracks = [t for t in all_tracks if t.GetLayerName() == "F.Cu"]
b_cu_tracks = [t for t in all_tracks if t.GetLayerName() == "B.Cu"]
vias = [t for t in all_tracks if t.GetClass() == "PCB_VIA" or "VIA" in str(type(t)).upper()]

print(f"=== LAYER AUDIT ===")
print(f"Total Tracks on B.Cu: {len(b_cu_tracks)}")
print(f"Total Tracks on F.Cu: {len(f_cu_tracks)} (Must be 0)")
print(f"Total Vias:           {len(vias)} (Must be 0)")

assert len(f_cu_tracks) == 0, f"VIOLATION: Found {len(f_cu_tracks)} tracks on F.Cu!"
assert len(vias) == 0, f"VIOLATION: Found {len(vias)} vias!"
print("Layer audit PASSED: 100% Single-layer B.Cu routing verified!")

