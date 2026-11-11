import pcbnew
import json
import os

proj_dir = r"D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1"
pcb_path = os.path.join(proj_dir, "AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pcb")
out_json = os.path.join(proj_dir, "net_pads_rev2.json")

board = pcbnew.LoadBoard(pcb_path)
net_pads = {}
for fp in board.GetFootprints():
    ref = fp.GetReference()
    for pad in fp.Pads():
        nname = pad.GetNetname()
        if not nname or "unconnected" in nname:
            continue
        pos = pad.GetPosition()
        x_mm = pcbnew.ToMM(pos.x)
        y_mm = pcbnew.ToMM(pos.y)
        pnum = pad.GetNumber()
        if nname not in net_pads:
            net_pads[nname] = []
        net_pads[nname].append([x_mm, y_mm, ref, pnum])

with open(out_json, "w", encoding="utf-8") as f:
    json.dump(net_pads, f, indent=2)

print(f"Dumped {len(net_pads)} connected nets to {out_json}")

