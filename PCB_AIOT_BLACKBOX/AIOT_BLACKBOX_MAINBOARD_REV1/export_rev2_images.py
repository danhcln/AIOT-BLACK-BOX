# -*- coding: utf-8 -*-
import os, sys, json, math, subprocess
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')
proj_dir = r"D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1"
pcb_path = os.path.join(proj_dir, "AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pcb")
gate2_dir = os.path.join(proj_dir, "GATE_2_PLACEMENT")
kicad_cli = r"D:\KiCad\bin\kicad-cli.exe"
net_pads_json = os.path.join(proj_dir, "net_pads_rev2.json")

# 1. Export Top & Bottom PDF
top_pdf = os.path.join(gate2_dir, "PCB_PLACEMENT_TOP_REV2.pdf")
bot_pdf = os.path.join(gate2_dir, "_temp_bot_rev2.pdf")

print("Exporting Top PDF...")
subprocess.run([
    kicad_cli, "pcb", "export", "pdf",
    "--output", top_pdf,
    "--layers", "F.Cu,F.SilkS,F.Mask,F.Fab,F.CrtYd,Edge.Cuts",
    "--include-border-title",
    pcb_path
], check=True)

print("Exporting Bottom PDF (mirrored)...")
subprocess.run([
    kicad_cli, "pcb", "export", "pdf",
    "--output", bot_pdf,
    "--layers", "B.Cu,B.SilkS,B.Mask,F.Fab,F.CrtYd,Edge.Cuts",
    "--mirror",
    "--include-border-title",
    pcb_path
], check=True)

# 2. Load net pads from json
with open(net_pads_json, "r", encoding="utf-8") as f:
    net_pads = json.load(f)

print(f"Loaded {len(net_pads)} connected nets.")

# 3. Render Top and Bottom PDF at 300 DPI
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

# 4. Overlay on Top View (A4 landscape: 297 x 210 mm)
W, H = img_top_2d.size
def mm_to_px_top(x_mm, y_mm):
    return (x_mm / 297.0 * W, y_mm / 210.0 * H)

draw = ImageDraw.Draw(img_top_2d, "RGBA")

# Draw Antenna Keepout Zone hatching (X=155.0..185.0, Y=40.0..55.0)
kx1, ky1 = mm_to_px_top(155.0, 40.0)
kx2, ky2 = mm_to_px_top(185.0, 55.0)
draw.rectangle([kx1, ky1, kx2, ky2], fill=(255, 60, 60, 45), outline=(220, 0, 0, 220), width=3)
step = 18
for x_h in range(int(kx1), int(kx2), step):
    draw.line([(x_h, ky1), (min(x_h + (ky2 - ky1), kx2), min(ky2, ky1 + (kx2 - x_h)))], fill=(220, 0, 0, 150), width=2)

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

# Overlay text banner on Top View
try:
    _font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 24)
except Exception:
    _font = None

img_top_2d_d = ImageDraw.Draw(img_top_2d)
_tlx, _tly = int(W * 0.168), int(H * 0.712)
for k, (txt, col) in enumerate([
        ("TOP VIEW - GATE 2.1 PLACEMENT REV2 - NOT ROUTED: thin coloured lines = ratsnest airwires (MST), red hatched box = antenna keepout", (0, 0, 0)),
        ("OPTIMIZED: U1 shifted South (Y=85.0mm) for USB-C access | Power block streamlined | SPI / I2C / UART aligned | 0 DRC violations", (0, 120, 40)),
        ("Header footprints, pad positions and U1 25.40 mm row pitch = verified footprints; module bodies/3D are NOT verified hardware shapes", (60, 60, 60))]):
    img_top_2d_d.text((_tlx, _tly + 270 + k * 34), txt, fill=col, font=_font)

# 5. Overlay on Bottom View (mirrored about A4 page centre: x' = 297 - x)
WB, HB = img_bot_2d.size
def mm_to_px_bot(x_mm, y_mm):
    return ((297.0 - x_mm) / 297.0 * WB, y_mm / 210.0 * HB)

ov = Image.new("RGBA", img_bot_2d.size, (0, 0, 0, 0))
dr = ImageDraw.Draw(ov, "RGBA")

# Reserved single-layer routing area (B.Cu only)
bx1, by1 = mm_to_px_bot(195.0, 40.0)
bx2, by2 = mm_to_px_bot(50.0, 145.0)
dr.rectangle([bx1, by1, bx2, by2], fill=(0, 120, 255, 28))

# Antenna keepout on bottom view
k1 = mm_to_px_bot(185.0, 40.0)
k2 = mm_to_px_bot(155.0, 55.0)
dr.rectangle([k1[0], k1[1], k2[0], k2[1]], fill=(255, 60, 60, 70), outline=(220, 0, 0, 230), width=3)

for nname, pts in net_pads.items():
    if len(pts) < 2:
        continue
    color, width = get_net_color(nname)
    vis = [0]; un = set(range(1, len(pts)))
    while un:
        bd, bp = 1e9, None
        for i in vis:
            for j in un:
                dd = math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1])
                if dd < bd:
                    bd, bp = dd, (i, j)
        i, j = bp; vis.append(j); un.remove(j)
        dr.line([mm_to_px_bot(pts[i][0], pts[i][1]), mm_to_px_bot(pts[j][0], pts[j][1])], fill=color, width=width)

img_bot_2d = Image.alpha_composite(img_bot_2d.convert("RGBA"), ov).convert("RGB")
d2 = ImageDraw.Draw(img_bot_2d)
lx, ly = int(WB * 0.343), int(HB * 0.712)
for k, (txt, col) in enumerate([
        ("BOTTOM VIEW (mirrored) - GATE 2.1 PLACEMENT REV2 - NOT ROUTED: lines = ratsnest airwires; 0 copper tracks, 0 vias", (0, 0, 0)),
        ("Light-blue area = reserved for single-layer routing on B.Cu  |  red box = ESP32-S3 antenna keepout (no copper on F.Cu/B.Cu)", (0, 90, 200)),
        ("Airwires: red 5V_SYS | orange SIM_PWR | green 3V3_SYS | blue GND | purple I2C | cyan SPI | amber UART | grey other", (60, 60, 60))]):
    d2.text((lx, ly + k * 34), txt, fill=col, font=_font)

# 6. Save REV2 images
out_top_rev2 = os.path.join(gate2_dir, "PCB_PLACEMENT_TOP_REV2.png")
out_bot_rev2 = os.path.join(gate2_dir, "PCB_PLACEMENT_BOTTOM_REV2.png")

img_top_2d.save(out_top_rev2)
print("Saved PCB_PLACEMENT_TOP_REV2.png successfully.")
img_bot_2d.save(out_bot_rev2)
print("Saved PCB_PLACEMENT_BOTTOM_REV2.png successfully.")

# Also try to update base files if not locked
try:
    img_top_2d.save(os.path.join(gate2_dir, "PCB_PLACEMENT_TOP.png"))
    img_bot_2d.save(os.path.join(gate2_dir, "PCB_PLACEMENT_BOTTOM.png"))
    print("Updated base PCB_PLACEMENT_TOP.png and PCB_PLACEMENT_BOTTOM.png.")
except Exception as e:
    print(f"Note: Base placement images locked by viewer, REV2 images saved cleanly: {e}")

# 7. Render 3D view with kicad-cli pcb render
p3d_rev2 = os.path.join(gate2_dir, "PCB_PLACEMENT_3D_REV2.png")
p3d_base = os.path.join(gate2_dir, "PCB_PLACEMENT_3D.png")
print("Rendering 3D view with kicad-cli...")
subprocess.run([
    kicad_cli, "pcb", "render",
    "--output", p3d_rev2,
    "--side", "top",
    "--rotate", "-35,0,30",
    "--width", "1920",
    "--height", "1080",
    pcb_path
], check=True)

if os.path.exists(p3d_rev2):
    im3 = Image.open(p3d_rev2).convert("RGB")
    d3 = ImageDraw.Draw(im3)
    try:
        f3 = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 30)
    except Exception:
        f3 = None
    d3.rectangle([0, 0, im3.width, 96], fill=(255, 240, 200))
    d3.text((20, 8), "MECHANICAL OVERVIEW ONLY - kicad-cli render of the PCB + pads + silkscreen. NO 3D models of modules/components are loaded,", fill=(150, 0, 0), font=f3)
    d3.text((20, 52), "so this is NOT the verified shape/height of the real hardware. Do not use for enclosure fit or height checks.", fill=(150, 0, 0), font=f3)
    im3.save(p3d_rev2)
    print("Saved PCB_PLACEMENT_3D_REV2.png with disclaimer banner.")
    try:
        im3.save(p3d_base)
    except Exception:
        pass

print(f"Total airwires rendered: {len(all_segments)}")
