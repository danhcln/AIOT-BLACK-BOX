# GATE 2 SUMMARY – PLACEMENT PCB 1 LỚP

- **Project:** `D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1`
- **Kiểm tra lúc:** 2026-11-09, KiCad 10.0.6 (`kicad-cli`, `pcbnew`), chỉ đọc PCB (băm SHA-256 `A6321C09…917C` của `.kicad_pcb` không đổi trong phiên kiểm tra; bản trong `GATE_2_PLACEMENT\` trùng hệt).
- **Chưa làm (đúng giới hạn):** routing, đồng `F.Cu`, via, Gerber, sửa firmware/schematic gốc/GPIO.

## KẾT LUẬN: **GATE 2 = CONDITIONAL** (chưa đủ điều kiện sang Gate 3)

PCB mở được, placement không vi phạm DRC, nhưng còn **6 quyết định cơ khí cần người dùng** (OI-01…OI-06) và một số điểm lệch RULE 12/13/14/16/17. Không ghi PASS vì các điểm này là lỗi cơ khí quan trọng chưa giải quyết.

## 1. Kích thước PCB
145.0 × 105.0 mm (X 50–195, Y 40–145), bốn lỗ M3 Ø3.2 tại (55,45) (190,45) (55,140) (190,140) = 135 × 95 mm. **Cả hai đều `PROVISIONAL`**; lớn hơn hộp IP65 tham chiếu 100×68×50 của RULE 17 (OI-06).

## 2. Tổng số footprint
**32** = 28 linh kiện schematic (`U1–U7, J1, J2, NT1, R_PU1/2, R3–R6, C1–C4, Q1, BZ1, D1, SW1, TP1–TP4`) + 4 lỗ vít. Không có `track`, `via`; 1 zone (keepout anten). Khớp netlist: 58 net, 122 kết nối pad.

## 3. Module đã bố trí
| Khối | Vị trí (mm) | Ghi chú |
| :--- | :--- | :--- |
| `U1` ESP32-S3 | (169.0, 78.5) | Row pitch 25.40 mm xác nhận từ pad (156.3 ↔ 181.7); pitch dọc 2.54; anten sát mép Bắc |
| `J2` nguồn UPS / `TP1,TP4` / `NT1` | (60,62) / (69,58),(69,66) / (78,58) | `J2.1(+)=5V_SYS`, `J2.2(-)=GND`, silk `1(+)` `2(-)` |
| `C3`,`C4`,`TP3` → `U5` SIM | (89,56),(99,56),(99,49) → (100,71) | `C4→U5.1` 15 mm, `C3→C4` 10 mm |
| `U6` buck 3.3 V, `C1`, `TP2` | (66,82),(80,82),(80,75) | |
| UI: `BZ1`,`Q1`,`R5`,`R6`,`SW1`,`R3`,`C2`,`D1`,`R4` | cụm trên cùng, Y 46–68 | `BZ1`–`U2` = 62.5 mm (≥ 40 mm) |
| `U4` GPS, `R_PU1/2` | (122,77); (139,81.5),(139,87.5) | |
| `U2` MPU6050, `U3` DS3231, `U7` OLED, `J1` MicroSD | (96,96); (68,100); (102,116.5); (137,101) | Khung thân là giả định (OI-01) |

Đã xác minh khớp firmware: `U1` pad 5/6/7 = GPIO5/6/7; 8/9 = GPIO15/16; 10/11 = GPIO17/18; 12/15 = GPIO8/9; 16–19 = GPIO10–13; 21 = 5V_SYS; 22 = GND (đối chiếu `filecodemain.cpp` và netlist). SIM VCC = `SIM_PWR`, MicroSD VCC = `5V_SYS`, `U6` cấp `3V3_SYS`; GPIO không bị đổi.

## 4. Kết quả DRC / ERC (chạy lại, không dùng Ignore)
| Kiểm tra | Kết quả |
| :--- | :--- |
| `kicad-cli sch erc --severity-all` | **0 lỗi, 0 cảnh báo** |
| `kicad-cli pcb drc --schematic-parity --severity-all` | **0 vi phạm** (courtyard, keepout, NPTH, silk, clearance) |
| Unconnected items | **64** = đường chưa route, bình thường ở Gate 2 (không phải lỗi pad/footprint) |
| Schematic parity | **3 cảnh báo `net_conflict`** (`U4.ANT`, `U5.ANT`, `U5.STATUS`): chân symbol không có pad trên header 1x05 — không phải kết nối điện |

**Khác biệt với báo cáo trước:** kết quả "0 vi phạm" lặp lại được; nhưng báo cáo trước ghi Net Class đã cấu hình là **sai** — `.kicad_pro` bị `pcbnew.SaveBoard()` ghi đè về mặc định. Đã khôi phục 8 Net Class theo RULE 09 và đặt `min_clearance/min_track = 0.25` (RULE 20); DRC/ERC chạy lại vẫn 0 vi phạm. Kiểm tra thêm ngoài DRC (script riêng): courtyard bbox giao nhau 1 cặp `D1/U5` chỉ ở góc bbox (DRC đa giác xác nhận không giao), mọi pad cách mép bo ≥ 3.47 mm (lỗ vít), không footprint nào vào vòng cấm 6.5 mm quanh lỗ vít, annular ring < 0.40 mm ở **44 pad `U1`** (OI-08), 12 chữ silk < 1.0 mm (Gate 5).

## 5. NetTie `NT1`
- Footprint đúng `AIOT_Blackbox_Local:NetTie_2_StarPoint_BCu_Width2.5mm`, có `(net_tie_pad_groups "1, 2")`.
- Pad 1 = `5V_SYS` (76.73, 58.0), Pad 2 = `SIM_PWR` (79.27, 58.0); mỗi pad 2.5 × 2.5 mm, lỗ 1.0 mm; đa giác đồng `B.Cu` 2.54 × 2.5 mm nối hai pad.
- Không ngắn mạch ngoài ý muốn: DRC 0 `shorting_items`; hai net chỉ nối với nhau tại net-tie.
- Khả năng tải ước lượng IPC-2221 (đồng 35 µm, ΔT 10 °C): ≈ 4.6 A cho 2.5 mm so với đỉnh SIM 2 A. Là ước lượng, đồng PCB tự làm có thể mỏng hơn; phải đo ở Gate 4.
- **Không phải linh kiện thay được bằng jumper nhỏ** (đã ghi trong BOM; BOM/`HARDWARE_DECISIONS_LOCKED.md` đã đồng bộ từ `J3` sang `NT1`).

## 6. Hình placement (đã mở và xem từng ảnh)
| File | Trạng thái |
| :--- | :--- |
| [PCB_PLACEMENT_TOP.png](PCB_PLACEMENT_TOP.png) | Có: outline, footprint, reference, keepout, airwire; chú thích khung thân là giả định |
| [PCB_PLACEMENT_BOTTOM.png](PCB_PLACEMENT_BOTTOM.png) | Đã làm lại: lật gương, vị trí pad, airwire chưa nối, vùng B.Cu dự kiến, keepout, chú thích |
| [PCB_PLACEMENT_TOP.pdf](PCB_PLACEMENT_TOP.pdf) | Hợp lệ (1 trang A4); bản in KiCad, không có airwire |
| [PCB_PLACEMENT_3D.png](PCB_PLACEMENT_3D.png) | **Không có mô hình 3D module**; đã gắn cảnh báo lên ảnh, chỉ tham khảo cơ khí sơ bộ |

Airwire trong ảnh là cây khung nhỏ nhất (MST) do script vẽ, không phải ratsnest chính xác của KiCad.

## 7. Khả thi PCB một lớp
**Khả thi có điều kiện.** Căn cứ chi tiết: [ONE_LAYER_FEASIBILITY_REPORT.md](ONE_LAYER_FEASIBILITY_REPORT.md). Điểm chính: toàn bộ chân dùng nằm ở hàng trái của `U1` (trừ `U1.23` GND), thứ tự chân I2C trên 3 module cùng chiều, nguồn SIM ngắn (≈ 32 mm từ `NT1` đến `U5.1`). Giới hạn: SPI và I2C có nghịch thế thứ tự chân nên không tránh được giao cắt.

## 8. Số jumper dự kiến
**Tối thiểu chứng minh được: 2** (SPI SCK×MOSI = 1; I2C đảo làn ≥ 1). **Ước lượng 2–6, dự kiến 3–4**, dưới ngưỡng < 8 của RULE 11 nhưng **chưa xác nhận** đến khi route. **Jumper cho `5V_SYS`/`SIM_PWR`: 0** (cấm). Hiện chưa có ký hiệu `JMP` trong schematic (OI-11).

## 9. Vấn đề còn tồn tại
Chi tiết ở [PCB_OPEN_ISSUES.md](PCB_OPEN_ISSUES.md): OI-01 kiểu lắp/kích thước module · OI-02 USB không sát mép · OI-03 OLED ở nửa dưới · OI-04 MPU6050 chưa cố định, lệch tâm · OI-05 anten GPS/SIM · OI-06 kích thước hộp · OI-07 `U1.23` GND · OI-08 annular ring `U1` · OI-09/10/11 tụ 1000 µF + 33/10 pF, test point, jumper (cần sửa schematic) · các mục silkscreen/3D ở Gate 5.

## 10. Sang Gate 3?
**Chưa.** Cần người dùng quyết OI-01…OI-06 (có thể thay đổi vị trí module), và duyệt/không duyệt OI-07, OI-08. Sau đó cập nhật placement rồi mới route. Dừng tại Gate 2 theo yêu cầu.

---
**Phụ lục – việc đã làm trong phiên này:** khôi phục `.kicad_pro` (có backup trong `backup\`); đồng bộ BOM/Hardware Decisions `J3→NT1`; làm lại ảnh dưới/trên/3D có chú thích; thêm khối ĐÍNH CHÍNH vào `PLACEMENT_REPORT.md` và `ONE_LAYER_FEASIBILITY_REPORT.md`; viết lại `PCB_OPEN_ISSUES.md`; thêm `ERC_REPORT_GATE2.txt`, `DRC_PLACEMENT_CHECK.txt`. Không sửa `.kicad_pcb`, `.kicad_sch`, firmware, schematic REV8 gốc. Không chạy lại `build_gate2_pcb.py` (không an toàn, xem Open Issues).

