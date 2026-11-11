# BIÊN BẢN TỔNG KẾT GATE 3 – ROUTING THỬ NGHIỆM PCB 1 LỚP B.Cu
**Tên đồ án:** THIẾT KẾ HỘP ĐEN AIoT THÔNG MINH PHÂN TÍCH VÀ GHI LẠI SỰ CỐ XE MÁY ĐIỆN  
**Project:** `AIOT_BLACKBOX_MAINBOARD_REV1`  
**Thư mục làm việc:** `D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1\GATE_3_ROUTING`  
**Thời gian hoàn thành:** 10/11/2026 – 17:15 (GMT+7)  
**Đánh giá kết quả Gate 3:** **`CONDITIONAL` (ĐẠT MỨC ĐỘ THỬ NGHIỆM KỸ THUẬT / CẦN QUYẾT ĐỊNH CƠ CHẾ JUMPER HOẶC 2 LỚP)**  

---

## 1. MỤC TIÊU VÀ TÔN CHỈ THỰC HIỆN
Thực hiện nghiêm ngặt chỉ đạo của người dùng:
1. **DỪNG TỐI ƯU VÔ HẠN**: Ngừng hoàn toàn việc thử nghiệm các thuật toán routing tự động vô định.
2. **BẢO TOÀN KẾT QUẢ TỐT NHẤT**: Khóa và lưu trữ phiên bản mạch sạch nhất trên `AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pcb`.
3. **TRUNG THỰC VÀ MINH BẠCH**: Báo cáo chính xác từng chỉ số, không giả lập kết quả, không đánh dấu PASS khi chưa hoàn thiện 100%.
4. **KHÔNG XUẤT GERBER, KHÔNG GỬI SẢN XUẤT**: Tạm dừng quy trình sản xuất chờ quyết định phương án từ kỹ sư chủ nhiệm.

---

## 2. KẾT QUẢ KỸ THUẬT ĐẠT ĐƯỢC

### A. Chỉ số tổng hợp
- **Lớp đồng sử dụng:** Duy nhất lớp đáy `B.Cu` ($35\mu m$ đồng).
- **Số track trên F.Cu:** **0** (Tuân thủ nghiêm ngặt chuẩn 1 lớp đồng).
- **Số lượng Via:** **0** (Tuân thủ nghiêm ngặt chuẩn 1 lớp đồng).
- **Số đoạn track đã đi:** **119 đoạn** trên `B.Cu`.
- **Số lượng net đã kết nối:** **14/20 net** (tỷ lệ pads kết nối vật lý: $66/84 = 78.6\%$).
- **Số lượng Jumper dây đã đặt:** **5 jumper tiêu chuẩn** (`JMP1`..`JMP5`).
- **DRC Crossings (Giao cắt track):** **0** (`tracks_crossing = 0`).
- **DRC Shorts (Chập ngắn mạch):** **0** (`shorting_items = 0`).
- **DRC Clearance (Vi phạm khoảng cách):** **0** (`clearance = 0`).
- **DRC Silkscreen Warnings:** **5 cảnh báo** (chữ lụa đè mép solder mask pad jumper).
- **Mối nối chưa nối đồng (Unconnected):** **18 mục trong DRC** (trong đó có 5 jumper chờ hàn dây mặt trên và 11 mối nối airwire đã ghi nhận).

### B. Tình trạng các đường nguồn công suất
- **`SIM_PWR` (Dòng đỉnh 5.5A xung GSM):** Đã đi dây hoàn chỉnh từ C1 (1000uF) đến U5.1 và TP3 với bề rộng **$2.50\text{ mm} / 2.00\text{ mm}$**, khoảng cách cách ly $\ge 0.50\text{ mm}$, sụt áp $< 0.05\text{V}$.
- **`5V_SYS` (Dòng định mức 2.6A):** Đã đi dây hoàn chỉnh dạng trục xương cá với bề rộng **$1.50\text{ mm}$**, cấp đủ cho ESP32 DevKit, Buzzer BZ1, Hạ áp U6 và MicroSD J1.
- **`3V3_SYS` (Dòng định mức 1.8A):** Đã đi dây vành đai và nhánh phân phối với bề rộng **$1.00\text{ mm} / 0.80\text{ mm}$**.
- **`GND` (Mặt phẳng tiếp địa):** Phủ đồng toàn bộ lớp `B.Cu` kết hợp các nhánh dẫn $0.8\text{ mm}$ tạo đường về dòng trực tiếp, độ kháng trở cực thấp.

---

## 3. CHỨNG MINH TÔ PÔ HỌC VỀ GIỚI HẠN PCB 1 LỚP
Toàn bộ phân tích đồ thị phẳng cho thấy mạch này có **3 điểm nghẽn tô pô học không thể giải quyết trên 1 lớp đồng phẳng**:
1. **Jordan Curve Enclosure**: Khối I2C (RTC `U3` và IMU `U2`) bị kẹp giữa đường SCL (Bắc) và SDA (Nam). Nguồn $3.3\text{V}$ bắt buộc phải nhảy qua SCL/SDA để vào nuôi 2 IC này.
2. **I2C Parity Inversion**: Chân SDA của ESP32 nằm ở phía BẮC chân SCL, trong khi tại các ngoại vi SDA lại nằm ở phía NAM của SCL. Hai đường này bắt buộc cắt chéo nhau (đã giải quyết bằng `JMP4`).
3. **MicroSD MISO Enclosure**: Chân MISO trên socket J1 bị kẹp kín giữa SCK (Bắc), 5V_SYS (Đông) và MOSI (Nam), không có lối thoát trên lớp đồng B.Cu.

---

## 4. BỘ HỒ SƠ BÀN GIAO GATE 3 (DELIVERABLES)
Toàn bộ tài liệu và sản phẩm của Gate 3 đã được lưu trữ hoàn chỉnh tại thư mục [`GATE_3_ROUTING`](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING):
1. **[`PCB_ROUTING_BOTTOM_COPPER_ONLY.png`](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/PCB_ROUTING_BOTTOM_COPPER_ONLY.png)**: Ảnh kết xuất 300 DPI đường đồng B.Cu thực tế.
2. **[`PCB_ROUTING_BOTTOM.png`](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/PCB_ROUTING_BOTTOM.png)**: Ảnh kết xuất 300 DPI mặt đáy hoàn chỉnh.
3. **[`PCB_ROUTING_TOP.png`](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/PCB_ROUTING_TOP.png)**: Ảnh kết xuất 300 DPI mặt trên thể hiện vị trí 5 cầu nhảy jumper.
4. **[`DRC_ROUTING_REPORT.txt`](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/DRC_ROUTING_REPORT.txt)**: Báo cáo DRC chính thức từ KiCad CLI.
5. **[`UNROUTED_NETS.csv`](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/UNROUTED_NETS.csv)**: Bảng thống kê chi tiết 11 mối nối chưa hoàn thiện đường đồng.
6. **[`JUMPER_LIST.csv`](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/JUMPER_LIST.csv)**: Bảng đặc tả kỹ thuật 5 jumper dây cách điện.
7. **[`ROUTING_REPORT.md`](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/ROUTING_REPORT.md)**: Báo cáo kỹ thuật phân tích chi tiết.

---

## 5. KẾT LUẬN VÀ KIẾN NGHỊ BƯỚC TIẾP THEO

> [!IMPORTANT]
> **GATE 3 ĐÃ DỪNG LẠI Ở TRẠNG THÁI AN TOÀN NHẤT.**  
> File thiết kế chính [`AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pcb`](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pcb) hoàn toàn hợp lệ, không có bất kỳ đường đồng nào chập ngắn mạch hoặc cắt chéo nhau.

### 2 Hướng lựa chọn để hoàn tất dự án:
- **Hướng 1 (Khuyến nghị chuẩn công nghiệp): Nâng cấp sang PCB 2 lớp đồng (`F.Cu` + `B.Cu`)**.
  - Xóa bỏ toàn bộ jumper dây thủ công, thay bằng via chuyển lớp.
  - Tận dụng lớp đồng F.Cu/B.Cu làm Ground Shielding chống nhiễu cực tốt cho 4G SIM và anten định vị GNSS.
  - Đảm bảo độ bền cơ học tối đa chống rung lắc trên xe máy điện.
- **Hướng 2 (Duy trì PCB 1 lớp tự gia công): Bổ sung thêm 2 jumper dây cách điện (`JMP6` và `JMP7`)**.
  - `JMP6`: Dẫn tín hiệu `Net-(J1-MISO)` nhảy qua SCK/5V_SYS.
  - `JMP7`: Dẫn nguồn `3V3_SYS` nhảy qua SCL vào cấp nguồn cho cụm RTC DS3231 và IMU MPU6050.
  - Cập nhật chính thức 2 jumper này vào Schematic và BOM để đạt 100% kết nối với 7 jumper.

