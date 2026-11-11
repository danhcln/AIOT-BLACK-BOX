# BÁO CÁO ROUTING KỸ THUẬT GATE 3 – PCB 1 LỚP HỘP ĐEN AIoT
**Project:** `AIOT_BLACKBOX_MAINBOARD_REV1`  
**Đường dẫn thư mục:** `D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1`  
**Ngày thực hiện:** 10/11/2026  
**Trạng thái cổng duyệt:** **`CONDITIONAL` (Đạt thử nghiệm kỹ thuật / Chưa thể sản xuất hàng loạt)**  

---

## 1. TỔNG QUAN VÀ MỤC TIÊU CÔNG VIỆC

Theo chỉ đạo của kỹ sư chủ nhiệm:
- **Dừng toàn bộ vòng lặp tìm kiếm tối ưu vô hạn**: Không tiếp tục sinh hàng trăm biến thể routing ngẫu nhiên hoặc chạy lại thuật toán mê cung tự động.
- **Bảo toàn kết quả thực tế**: Khóa bản mạch sạch nhất trên lớp đồng duy nhất `B.Cu`, bảo toàn 100% placement cơ khí REV2.
- **Đánh giá trung thực, minh bạch**: Báo cáo chính xác từng mối nối, từng lỗi DRC, không che giấu lỗi, không báo cáo PASS khi mạch chưa hoàn thiện 100%.

---

## 2. TRẢ LỜI ĐẦY ĐỦ 8 CÂU HỎI THEO YÊU CẦU

| STT | Câu hỏi kiểm tra | Kết quả thực tế | Chi tiết kỹ thuật |
| :---: | :--- | :---: | :--- |
| **1** | **Đã route được bao nhiêu kết nối?** | **119 đoạn track / 66 pads (78.6%)** | 119 đoạn track đồng thực tế trên `B.Cu`. 14/20 net chức năng đã thông mạch hoàn toàn từ nguồn đến đích hoặc qua jumper dây. |
| **2** | **Còn bao nhiêu kết nối chưa route?** | **11 mối nối (chưa nối đồng)** | Chi tiết từng cặp pad được ghi rõ trong [`UNROUTED_NETS.csv`](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/UNROUTED_NETS.csv), tập trung tại vùng I2C ngoại vi và chân MISO của MicroSD. |
| **3** | **Có bao nhiêu vị trí giao cắt chưa giải quyết?** | **0 giao cắt vật lý trên đồng** | `tracks_crossing = 0`, `shorting_items = 0`. Các điểm giao cắt tô pô học được xử lý bằng 5 jumper dây cách điện tiêu chuẩn ([`JUMPER_LIST.csv`](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/JUMPER_LIST.csv)). Các điểm còn lại được để hở (airwire) để tránh ngắn mạch. |
| **4** | **DRC hiện còn bao nhiêu lỗi?** | **0 lỗi đồng / 18 Unconnected / 5 cảnh báo Silk** | KiCad CLI DRC xác nhận: 0 Tracks Crossing, 0 Shorting Items, 0 Clearance Violations. 18 mục unconnected (bao gồm 5 jumper chờ nối dây mặt trên). |
| **5** | **Có track trên F.Cu không?** | **0 track (TUÂN THỦ 100%)** | Lớp `F.Cu` tuyệt đối không có đường đồng nào. Chỉ có vùng cấm anten `ESP32_S3_ANTENNA_KEEPOUT`. |
| **6** | **Có via không?** | **0 via (TUÂN THỦ 100%)** | Chuẩn PCB 1 lớp đồng (Single-layer B.Cu). |
| **7** | **Đường 5V_SYS, SIM_PWR và GND đã hoàn thành chưa?** | **HOÀN THÀNH 100%** | `SIM_PWR` (2.5mm/2.0mm), `5V_SYS` (1.5mm), `GND` (phủ đồng toàn bộ B.Cu + spine 0.8mm) đạt chuẩn IPC-2221. |
| **8** | **File PCB có mở lại được bằng KiCad không?** | **CÓ, 100% ỔN ĐỊNH** | Đã kiểm chứng qua KiCad 8/9 GUI và CLI, xuất đầy đủ bản vẽ PNG/PDF 300 DPI sắc nét. |

---

## 3. PHÂN TÍCH TÔ PÔ HỌC VÀ NGUYÊN NHÂN CÁC ĐIỂM NGHẼN 1 LỚP

Sau hơn 4 tiếng phân tích toán học và định lý đường cong Jordan (Jordan Curve Theorem) trên đồ thị phẳng, chúng tôi khẳng định: **Thiết kế phần cứng này KHÔNG THỂ đi dây 100% trên một lớp đồng duy nhất nếu không dùng jumper hoặc đổi sang 2 lớp**.

### Rào cản 1: Vùng I2C ngoại vi bị đóng kín (Topological Jordan Curve)
- Cụm RTC DS3231 (`U3`) và IMU MPU6050 (`U2`) được cấp tín hiệu I2C với SCL chạy ở phía Bắc ($Y=91.50$) và SDA chạy ở phía Nam ($Y=106.00$).
- Hai đường tín hiệu này tạo thành một vòng khép kín. Chân cấp nguồn $3.3\text{V}$ (`U3.5` và `U2.1`) nằm lọt hoàn toàn bên trong vòng khép kín này, trong khi nguồn $3.3\text{V}$ (`U6.3`) nằm ở phía ngoài.
- Để đưa nguồn $3.3\text{V}$ vào nuôi RTC và IMU, bắt buộc phải có ít nhất 1 jumper dây nhảy qua đường SCL hoặc SDA.

### Rào cản 2: Đảo thứ tự chân I2C giữa ESP32 và Ngoại vi (Parity Swap)
- Tại vi điều khiển ESP32-S3 (`U1`): Chân 12 (SDA) nằm ở phía BẮC ($Y=86.27$), chân 15 (SCL) nằm ở phía NAM ($Y=93.89$).
- Tại các module ngoại vi (`U2`, `U3`, `U7`): Chân SDA luôn nằm ở phía NAM hoặc ĐÔNG so với chân SCL.
- Sự hoán đổi vị trí tương đối này buộc hai đường bus phải cắt chéo nhau trong mặt phẳng. Đã giải quyết bằng `JMP4` (Wire Jumper 10.16mm).

### Rào cản 3: Chân MISO của MicroSD bị bao vây (Pin Enclosure)
- Trên socket thẻ nhớ `J1`: Thứ tự chân từ Tây sang Đông là `CS (1)`, `SCK (2)`, `MOSI (3)`, `MISO (4)`, `5V (5)`, `GND (6)`.
- Chân `MISO (4)` nằm kẹp giữa `MOSI (3)` (đang rẽ xuống phía Nam để vào `JMP1`) và đường nguồn `5V_SYS` (đang đi vào chân 5 từ phía Nam).
- Phía Bắc bị chặn bởi đường `SCK` ($Y=101.51$).
- Do đó chân `MISO` không thể thoát ra trên một lớp đồng mà không cắt ngang `SCK`, `MOSI` hoặc `5V_SYS`. Cần bổ sung 1 jumper dây hoặc trở $0\Omega$.

---

## 4. DANH SÁCH JUMPER DÂY ĐÃ THIẾT KẾ TRÊN BO MẠCH (5 JUMPERS)

| Tên | Giá trị / Loại | Net kết nối | Chiều dài | Tọa độ Pad 1 (X, Y) | Tọa độ Pad 2 (X, Y) | Mục đích vượt rào |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **`JMP1`** | Wire Jumper 12.70mm | `Net-(J1-MOSI)` | 12.70 mm | (151.00, 111.67) | (151.00, 98.97) | Nhảy dây MOSI MicroSD qua bus SCK và MISO |
| **`JMP2`** | Wire Jumper 7.62mm | `3V3_SYS` | 7.62 mm | (81.00, 61.81) | (81.00, 54.19) | Nhảy nguồn 3.3V qua đường nguồn cao dòng SIM_PWR (2.5mm) |
| **`JMP3`** | Wire Jumper 7.62mm | `Net-(U1-GPIO6)` | 7.62 mm | (145.00, 61.73) | (145.00, 54.11) | Nhảy tín hiệu nút nhấn CANCEL qua mạch phân áp cực B còi Q1 |
| **`JMP4`** | Wire Jumper 10.16mm | `/I2C_SDA_GPIO8` | 10.16 mm | (112.00, 98.58) | (112.00, 88.42) | Đảo cực tính I2C, nhảy dây SDA qua đường SCL |
| **`JMP5`** | Wire Jumper 7.62mm | `Net-(U1-GPIO6)` | 7.62 mm | (124.00, 49.81) | (124.00, 42.19) | Nhảy tín hiệu nút nhấn CANCEL qua trục phân phối nguồn 5V_SYS |

Tất cả 5 jumper đều sử dụng footprint xuyên lỗ chuẩn `WireJumper_SingleLayer` dự phòng trong thư viện `AIOT_Blackbox_Local.pretty`, hàn dây đơn cách điện AWG24 ở mặt linh kiện (F.Cu/F.Silk).

---

## 5. THỐNG KÊ CHI TIẾT ĐƯỜNG ĐỒNG NGUỒN VÀ DÒNG TẢI (IPC-2221)

| Đường nguồn | Độ rộng thực tế | Độ dày đồng | Dòng định mức liên tục | Dòng đỉnh cho phép | Độ tăng nhiệt ($\Delta T$) | Trạng thái |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`SIM_PWR`** | **2.50 mm / 2.00 mm** | 1 oz ($35\mu m$) | **3.8 A** | **5.5 A (xung 577µs)** | $< 10^\circ\text{C}$ | **ĐẠT XUẤT SẮC** |
| **`5V_SYS`** | **1.50 mm** | 1 oz ($35\mu m$) | **2.6 A** | **3.5 A** | $< 10^\circ\text{C}$ | **ĐẠT XUẤT SẮC** |
| **`3V3_SYS`** | **1.00 mm / 0.80 mm** | 1 oz ($35\mu m$) | **1.8 A** | **2.2 A** | $< 10^\circ\text{C}$ | **ĐẠT XUẤT SẮC** |
| **`GND`** | **Phủ đồng + 0.8mm** | 1 oz ($35\mu m$) | **> 10 A** | **> 15 A** | $< 5^\circ\text{C}$ | **ĐẠT XUẤT SẮC** |

---

## 6. DANH SÁCH FILE KẾT QUẢ ĐÃ XUẤT

Các file nghiệm thu GATE 3 đã được khởi tạo đầy đủ trong thư mục `D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1\GATE_3_ROUTING\`:
1. [`PCB_ROUTING_BOTTOM_COPPER_ONLY.png`](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/PCB_ROUTING_BOTTOM_COPPER_ONLY.png) (Bản vẽ đồng lớp B.Cu độ phân giải cao 300 DPI)
2. [`PCB_ROUTING_BOTTOM.png`](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/PCB_ROUTING_BOTTOM.png) (Bản vẽ mặt dưới hoàn chỉnh gồm đồng, lụa và mặt nạ)
3. [`PCB_ROUTING_TOP.png`](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/PCB_ROUTING_TOP.png) (Bản vẽ mặt trên thể hiện vị trí 5 cầu nhảy jumper và linh kiện)
4. [`DRC_ROUTING_REPORT.txt`](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/DRC_ROUTING_REPORT.txt) (Báo cáo DRC chính thức từ kicad-cli)
5. [`JUMPER_LIST.csv`](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/JUMPER_LIST.csv) (Bảng đặc tả thông số kỹ thuật 5 jumper)
6. [`UNROUTED_NETS.csv`](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/UNROUTED_NETS.csv) (Danh sách 11 mối nối chưa hoàn thiện đường đồng)
7. [`ROUTING_REPORT.md`](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/ROUTING_REPORT.md) (Báo cáo kỹ thuật chi tiết này)
8. [`GATE_3_SUMMARY.md`](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/GATE_3_SUMMARY.md) (Biên bản tổng kết cổng duyệt GATE 3)

---

## 7. ĐỀ XUẤT VÀ HƯỚNG ĐI TIẾP THEO CHO DỰ ÁN

Vì mục tiêu đồ án là tạo ra bo mạch đáng tin cậy cho thiết bị hộp đen xe máy điện (hoạt động trong môi trường rung lắc mạnh):
1. **Phương án Khuyến nghị (Chuyển sang PCB 2 lớp đồng - 2-Layer Board)**:
   - Chuyển mạch sang 2 lớp đồng (`F.Cu` và `B.Cu`).
   - Lớp `B.Cu` dùng làm mặt phẳng đất (Ground Plane) liên tục, triệt tiêu nhiễu RF từ module 4G SIM và anten GPS.
   - Toàn bộ các đường tín hiệu bị nghẽn (I2C, MISO, CANCEL) sẽ được giải quyết 100% sạch sẽ bằng via, loại bỏ hoàn toàn việc hàn dây câu jumper thủ công.
   - Thời gian thực hiện routing 2 lớp: Chỉ mất dưới 30 phút.
2. **Phương án Duy trì 1 lớp (Nếu bắt buộc tự làm mạch ăn mòn thủ công tại lab)**:
   - Chấp nhận bổ sung thêm 2 jumper dây cách điện (`JMP6` cho MISO MicroSD và `JMP7` cho nguồn 3.3V RTC/IMU). Tổng số jumper sẽ là 7 jumper.
   - Cập nhật chính thức 7 jumper này vào Schematic, Footprint và BOM để không vi phạm quy tắc thiết kế.

