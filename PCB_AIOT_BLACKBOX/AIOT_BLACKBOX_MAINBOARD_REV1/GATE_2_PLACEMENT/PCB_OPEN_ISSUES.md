# DANH SÁCH VẤN ĐỀ MỞ SAU GATE 2 (`PCB_OPEN_ISSUES.md`)

**Cập nhật:** 2026-11-09 (phiên tiếp quản, sau khi kiểm tra file thực tế). Thay thế bản `GATE_0_AUDIT\PCB_OPEN_ISSUES.md` (ghi "0 BLOCKING", đã lỗi thời).
**Kết luận Gate 2: `CONDITIONAL`** – xem [GATE_2_SUMMARY.md](GATE_2_SUMMARY.md).

Quy ước: **[D] cần người dùng quyết định trước Gate 3** (ảnh hưởng placement) · **[S] cần sửa schematic (chưa được phép trong nhiệm vụ này)** · **[G5] xử lý ở Gate 5** · **[OK] đã xử lý**.

## A. Quyết định cần người dùng trước khi vẽ đường mạch

| Mã | Vấn đề | Căn cứ / số liệu thực | Đề xuất |
| :---: | :--- | :--- | :--- |
| **OI-01 [D]** | **Kiểu lắp module chưa chốt** (nằm phẳng với header thẳng, hay cắm đứng với header 90° như trong ảnh). Khung thân `U2/U3/J1` trên bản vẽ là **giả định nằm phẳng**; kích thước chỉ OLED (24.7×27) là đã xác minh. | `MODULE_MOUNTING_PLAN.md`: header đang là 90°. `MODULE_DIMENSION_CHECKLIST.md` mục C chưa đo. | Chốt kiểu lắp; đo bằng thước kẹp: GY-521, ZS-042, MicroSD, GPS, SIM, module 3.3V. |
| **OI-02 [D]** | **USB-C của `U1` không sát mép bo** (RULE 12.3, 16.4). Anten sát mép Bắc (y=40), đầu USB kết thúc y≈111, mép Nam y=145 → cách ≈ 34 mm. | `U1` bbox y = 39.98…111.03 | Chấp nhận cáp USB nối dài/cửa sổ vỏ lùi vào, hoặc thu chiều cao bo ≈ chiều dài DevKit (đổi toàn bộ placement). |
| **OI-03 [D]** | **OLED ở nửa dưới bo** (RULE 16.1 yêu cầu trung tâm/nửa trên). `U7` tâm y=116.5. | Tâm bo y = 92.5 | Đổi chỗ OLED với cụm khác, hoặc đặt OLED rời lên nắp hộp bằng cáp 4 dây. |
| **OI-04 [D]** | **`MPU6050` chưa được cố định cơ khí** và **lệch tâm 26.5 mm** (RULE 14.1: ở tâm hoặc sát lỗ vít M3). Không có lỗ vít PCB nào cho `U2`; vòng tròn trên silk chỉ là hình vẽ. | `U2` (96.0, 96.0) vs tâm (122.5, 92.5); lỗ M3 gần nhất (H3) cách ≈ 60 mm | Đo lỗ vít GY-521, thêm 2 lỗ + trụ đỡ M3; hoặc dịch `U2` về tâm/gần lỗ vít. |
| **OI-05 [D]** | **Anten GPS và SIM chưa đạt ≥ 50 mm, hai góc đối diện** (RULE 13.1, Gate 2 mục 2). Header `U4` và `U5` cách nhau 22.8 mm; GPS có anten gốm 25×25 mm trên module. | `U5`(100,71) – `U4`(122,77) | Dùng anten GPS rời (SMA) đặt ≥ 50 mm cách anten SIM, hoặc dời `U4` ra góc xa `U5`. |
| **OI-06 [D]** | **Kích thước bo 145×105 mm vượt hộp IP65 tham chiếu 100×68×50 mm** (RULE 17.3). Hộp thật chưa được xác nhận. Bo và 4 lỗ M3 (135×95) đều `PROVISIONAL`. | | Cung cấp kích thước hộp thật để khóa kích thước bo/lỗ vít. |
| **OI-07 [D]** | **`U1.23` (GND hàng phải) vẫn nối vào net GND**; chỉ đến được bằng nhánh GND vòng qua đầu Nam `U1` (x≈183–187 mm). Phản bác lại ghi chú cũ "không cần đi qua hàng phải". | netlist: `U1.23=GND`, `U1.43/44` đã NC | Duyệt cho đánh dấu `U1.23` NC trong schematic, hoặc chấp nhận nhánh GND vòng. |
| **OI-08 [D]** | **Pad `U1` 1.6 mm / drill 1.0 mm → annular ring 0.30 mm < 0.40 mm** (RULE 20; 44 pad). | audit `audit_gate2b.py` | Tăng pad lên ≥ 1.8 mm (đạt chuẩn, nhưng khe giữa pad còn 0.74 mm, không còn luồn dây). Footprint này đã in 1:1 kiểm ở Gate 1.5 nên chưa tự ý đổi. |

## B. Cần sửa schematic (chưa thực hiện vì ngoài phạm vi)

| Mã | Vấn đề | Quy tắc |
| :---: | :--- | :--- |
| **OI-09 [S]** | Chưa có tụ **1000 µF/16 V** ở đầu vào `J2`; chưa có tụ **33 pF + 10 pF** cạnh chân VCC SIM (hiện chỉ `C3` 470 µF + `C4` 100 nF). | RULE 06.3, 08.3 |
| **OI-10 [S]** | Test point mới có 4 (`5V`, `3V3`, `SIM_PWR`, `GND`). Thiếu `TP_SDA/SCL`, `TP_SIM_TX/RX`, `TP_GPS_TX/RX`, `TP_SCK/MOSI/MISO/SD_CS` và điểm GND thứ hai ở đầu bo bên kia. | RULE 19 |
| **OI-11 [S]** | Chưa có ký hiệu jumper `JMP1…` trên schematic; cần trước khi dùng jumper ở Gate 3 (dự kiến ≥ 2 jumper tín hiệu: SPI SCK/MOSI, I2C). | RULE 11.2 |

## C. Xử lý ở Gate 5 (silkscreen/hồ sơ)

- **[G5]** 12 chữ silkscreen cao < 1.0 mm (`D1 K/A` 0.9; `Q1 E/C/B` 0.8; chữ trên bo: `USB-C`, `UART`, `+X:UP | +Y:LEFT`, `SD CARD SLOT`, ZONE 4, `GY-521 MPU6050`, `ESP32-S3 DUAL USB-C…`). RULE 18 yêu cầu ≥ 1.0 mm / nét ≥ 0.15 mm.
- **[G5]** Thiếu dòng chữ bắt buộc `AIOT SMART BLACK BOX - EDR FOR MOTORBIKE`, `CARRIER BOARD REV 1.0`, tác giả/ngày; chưa đánh dấu chân 1 cho mọi header; chưa có ký hiệu trục X–Y–Z đầy đủ cho `U2`; chưa in nhãn `SIM A7682S/A7680C`, `BUCK 3.3V`.
- **[G5]** Ảnh 3D không có mô hình 3D module (đã gắn cảnh báo lên ảnh). Phải kiểm va chạm/chiều cao bằng số đo thật.
- **[G5]** 3 cảnh báo parity `net_conflict` (`U4.ANT`, `U5.ANT`, `U5.STATUS`): chân anten/STATUS của symbol không có pad trên header 1x05 (có chủ đích, không có kết nối điện).

## D. Đã xử lý trong phiên này

| Mã | Nội dung | Trạng thái |
| :---: | :--- | :---: |
| **OI-12 [OK]** | `AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pro` bị `pcbnew.SaveBoard()` ghi đè về mặc định ở phiên trước (mất toàn bộ Net Class, báo cáo cũ nói sai là đã cấu hình). **Đã khôi phục 8 Net Class đúng RULE 09**, patterns gán net, `min_clearance=0.25`, `min_track=0.25` (RULE 20); backup ở `GATE_2_PLACEMENT\backup\`. ERC/DRC chạy lại: 0 vi phạm. | **RESOLVED** |
| **OI-13 [OK]** | `BOM_MAINBOARD_REV1.csv` và `HARDWARE_DECISIONS_LOCKED.md` còn ghi `J3` → đã đồng bộ thành `NT1`. | **RESOLVED** |
| **OI-14 [OK]** | Các báo cáo placement/feasibility phiên trước có nhiều phát biểu quá mức → đã thêm khối ĐÍNH CHÍNH và thay các mục sai. | **RESOLVED** |

> [!CAUTION]
> **Không chạy lại `scratch\build_gate2_pcb.py`.** Script tạo lại PCB từ đầu (mất mọi chỉnh sửa tay) và `SaveBoard()` sẽ lại ghi đè `.kicad_pro`. Chỉnh sửa tiếp nên làm trong KiCad GUI, hoặc phải sao lưu/khôi phục `.kicad_pro` quanh mỗi lần `SaveBoard()`.
