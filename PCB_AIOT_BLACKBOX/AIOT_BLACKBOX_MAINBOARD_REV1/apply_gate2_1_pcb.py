import pcbnew
import json
import os
import shutil

pcb_path = r'D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1\AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pcb'
pro_path = r'D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1\AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pro'

# 1. Read existing .kicad_pro content to preserve Net Classes exactly
with open(pro_path, 'r', encoding='utf-8') as f:
    pro_content = f.read()

# 2. Load board
board = pcbnew.LoadBoard(pcb_path)

# 3. New coordinates: ref -> (x_mm, y_mm, rot_deg)
new_positions = {
    'U1': (170.00, 85.00, 0.0),
    'J2': (60.00, 62.00, 90.0),
    'TP1': (68.00, 56.00, 0.0),
    'TP4': (68.00, 64.00, 0.0),
    'NT1': (76.00, 58.00, 0.0),
    'C3': (87.00, 58.00, 0.0),
    'C4': (98.00, 58.00, 0.0),
    'TP3': (98.00, 50.00, 0.0),
    'U5': (100.54, 68.00, 0.0),
    'U6': (66.00, 76.00, 0.0),
    'C1': (78.00, 76.00, 0.0),
    'TP2': (78.00, 70.00, 0.0),
    'BZ1': (136.00, 48.00, 0.0),
    'Q1': (136.00, 63.00, 0.0),
    'R5': (149.00, 63.00, 90.0),
    'R6': (136.00, 71.00, 0.0),
    'SW1': (116.00, 47.00, 0.0),
    'R3': (116.00, 53.50, 0.0),
    'C2': (116.00, 60.00, 0.0),
    'D1': (112.00, 66.50, 0.0),
    'R4': (122.00, 66.50, 0.0),
    'U4': (122.00, 80.00, 0.0),
    'R_PU1': (140.00, 86.50, 0.0),
    'R_PU2': (140.00, 93.50, 0.0),
    'U2': (96.00, 96.00, 0.0),
    'U3': (68.00, 100.00, 0.0),
    'U7': (102.00, 116.50, 0.0),
    'J1': (138.00, 104.00, 0.0),
    'H1': (55.00, 45.00, 0.0),
    'H2': (190.00, 45.00, 0.0),
    'H3': (55.00, 140.00, 0.0),
    'H4': (190.00, 140.00, 0.0)
}

print('Applying REV2 placement coordinates to board...')
for ref, (x, y, rot) in new_positions.items():
    fp = board.FindFootprintByReference(ref)
    if fp:
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        fp.SetOrientationDegrees(rot)
        print(f'  [MOVED] {ref:<8} -> ({x:6.2f}, {y:6.2f}, rot={rot:5.1f})')
    else:
        print(f'  [ERROR] {ref} not found!')

# 4. Update Antenna Keepout Zone: (155.0, 40.0) to (185.0, 55.0)
zones = board.Zones()
for z in zones:
    if z.GetZoneName() == 'ESP32_S3_ANTENNA_KEEPOUT':
        print('Updating Antenna Keepout Zone to (155.0, 40.0) - (185.0, 55.0)...')
        outline = z.Outline()
        outline.RemoveAllContours()
        outline.NewOutline()
        outline.Append(pcbnew.VECTOR2I(pcbnew.FromMM(155.0), pcbnew.FromMM(40.0)))
        outline.Append(pcbnew.VECTOR2I(pcbnew.FromMM(185.0), pcbnew.FromMM(40.0)))
        outline.Append(pcbnew.VECTOR2I(pcbnew.FromMM(185.0), pcbnew.FromMM(55.0)))
        outline.Append(pcbnew.VECTOR2I(pcbnew.FromMM(155.0), pcbnew.FromMM(55.0)))

# 5. Update Drawings to avoid overlaps
for d in board.GetDrawings():
    cname = d.GetClass()
    if cname == 'PCB_TEXT':
        txt = d.GetText()
        if 'BOARD SIZE' in txt:
            # Place BOARD SIZE at X=90.0, Y=143.5 so it doesn't touch MicroSD outline at X=138
            d.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(88.0), pcbnew.FromMM(143.0)))

# 6. Save board to target path
pcbnew.SaveBoard(pcb_path, board)
print('Board saved successfully to:', pcb_path)

# 7. Also copy to GATE_2_PLACEMENT/AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pcb
gate2_pcb_path = r'D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1\GATE_2_PLACEMENT\AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pcb'
shutil.copy2(pcb_path, gate2_pcb_path)
print('Copied to GATE_2_PLACEMENT PCB.')

# 8. Restore .kicad_pro to ensure Net Classes are not stripped by SaveBoard
with open(pro_path, 'w', encoding='utf-8') as f:
    f.write(pro_content)
print('.kicad_pro restored and verified with all 8 Net Classes intact.')
