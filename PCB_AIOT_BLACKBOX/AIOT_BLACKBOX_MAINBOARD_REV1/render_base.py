# -*- coding: utf-8 -*-
import os, sys, json, math, subprocess
import fitz  # PyMuPDF
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='utf-8')
proj_dir = r"D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1"
pcb_path = os.path.join(proj_dir, "AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pcb")
gate2_dir = os.path.join(proj_dir, "GATE_2_PLACEMENT")
kicad_cli = r"D:\KiCad\bin\kicad-cli.exe"
net_pads_json = r"C:\Users\Danh\.gemini\antigravity\brain\129ea0c8-203e-468b-ad30-d772b9c45265\scratch\net_pads.json"

# 1. Export Bottom PDF for rendering PCB_PLACEMENT_BOTTOM.png
bot_pdf = os.path.join(gate2_dir, "_temp_bot.pdf")
subprocess.run([
    kicad_cli, "pcb", "export", "pdf",
    "--output", bot_pdf,
    "--layers", "B.Cu,B.SilkS,B.Mask,F.Fab,F.CrtYd,Edge.Cuts",
    "--mirror",
    "--include-border-title",
    pcb_path
], check=True)

# 2. Render PCB_PLACEMENT_TOP.pdf and _temp_bot.pdf at 300 DPI using PyMuPDF
top_pdf = os.path.join(gate2_dir, "PCB_PLACEMENT_TOP.pdf")
doc_top = fitz.open(top_pdf)
pix_top = doc_top[0].get_pixmap(dpi=300)
img_top_2d = Image.frombytes("RGB", [pix_top.width, pix_top.height], pix_top.samples)
doc_top.close()

doc_bot = fitz.open(bot_pdf)
pix_bot = doc_bot[0].get_pixmap(dpi=300)
img_bot_2d = Image.frombytes("RGB", [pix_bot.width, pix_bot.height], pix_bot.samples)
doc_bot.close()
if os.path.exists(bot_pdf):
    os.remove(bot_pdf)

# 3. Overlay Antenna Keepout Zone & Color-Coded Ratsnest Airwires on Top 2D view (A4 landscape: 297 x 210 mm)
W, H = img_top_2d.size
def mm_to_px_top(x_mm, y_mm):
    return (x_mm / 297.0 * W, y_mm / 210.0 * H)

draw = ImageDraw.Draw(img_top_2d, "RGBA")

# Draw Antenna Keepout Zone hatching (X=154.5..183.5, Y=40.0..50.0)
kx1, ky1 = mm_to_px_top(154.5, 40.0)
kx2, ky2 = mm_to_px_top(183.5, 50.0)
draw.rectangle([kx1, ky1, kx2, ky2], fill=(255, 60, 60, 45), outline=(220, 0, 0, 220), width=3)
step = 18
for x_h in range(int(kx1), int(kx2), step):
    draw.line([(x_h, ky1), (min(x_h + (ky2 - ky1), kx2), min(ky2, ky1 + (kx2 - x_h)))], fill=(220, 0, 0, 150), width=2)

with open(net_pads_json, "r", encoding="utf-8") as f:
    net_pads = json.load(f)

def get_net_color(nname):
    if nname == "5V_SYS":
        return (220, 20, 20, 190), 3
    if nname == "SIM_PWR":
        return (255, 110, 0, 210), 4
    if nname == "3V3_SYS":
        return (0, 160, 60, 190), 3
    if nname == "GND":
        return (30, 100, 220, 140), 2
    if "I2C" in nname:
        return (160, 32, 240, 200), 2
    if "SD_" in nname or "J1-" in nname:
        return (0, 140, 180, 200), 2
    if "SIM_" in nname or "GPS_" in nname:
        return (180, 130, 0, 200), 2
    return (100, 100, 100, 170), 2

all_segments = []
for nname, pts in net_pads.items():
    if len(pts) < 2:
        continue
    visited = [0]
    unvisited = set(range(1, len(pts)))
    color, width = get_net_color(nname)
    while unvisited:
        best_d = 1e9
        best_pair = None
        for i in visited:
            for j in unvisited:
                d = math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1])
                if d < best_d:
                    best_d = d
                    best_pair = (i, j)
        i, j = best_pair
        visited.append(j)
        unvisited.remove(j)
        p1 = mm_to_px_top(pts[i][0], pts[i][1])
        p2 = mm_to_px_top(pts[j][0], pts[j][1])
        draw.line([p1, p2], fill=color, width=width)
        all_segments.append((nname, (pts[i][0], pts[i][1]), (pts[j][0], pts[j][1]), f"{pts[i][2]}.{pts[i][3]}->{pts[j][2]}.{pts[j][3]}", best_d))

img_top_2d.save(os.path.join(gate2_dir, "PCB_PLACEMENT_TOP.png"))
img_bot_2d.save(os.path.join(gate2_dir, "PCB_PLACEMENT_BOTTOM.png"))
print(f"Saved PCB_PLACEMENT_TOP.png and PCB_PLACEMENT_BOTTOM.png ({len(all_segments)} ratsnest airwires).")
for seg in sorted(all_segments, key=lambda x: x[0]):
    print(f"  [{seg[0]:18s}] {seg[3]:22s} | len = {seg[4]:5.1f} mm")
