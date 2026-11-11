# PHƯƠNG ÁN LẮP ĐẶT CƠ KHÍ TỪNG MODULE (`MODULE_MOUNTING_PLAN.md`)

**Dự án**: THIẾT KẾ HỘP ĐEN AIoT THÔNG MINH PHÂN TÍCH VÀ GHI LẠI SỰ CỐ XE MÁY ĐIỆN  
**Project KiCad**: `D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1`  
**Cơ sở phân loại**: Dựa trên 15 ảnh phần cứng thực tế trong `D:\ĐỒ ÁN 2\Hình ảnh linh kiện` và `PCB_DESIGN_RULES_AIOT.md` (RULE 02, RULE 08, RULE 13, RULE 14, RULE 15).

---

## 1. BẢNG PHÂN LOẠI KIỂU LẮP (`MOUNTING CLASSIFICATION`)

| Ref | Tên Module | Phân loại lắp đặt | Footprint sử dụng trên PCB chính | Lý do kỹ thuật từ ảnh thực tế |
| :--- | :--- | :--- | :--- | :--- |
| **`U1`** | `ESP32-S3-DevKitC-1 N16R8` | **`BOARD_MOUNT`** *(cắm trên 2 hàng Female Header `1x22`)* | **`PENDING_MEASUREMENT`** *(chờ đo khoảng cách 2 hàng chân `22.86mm` vs `25.40mm`)* | Module đã hàn sẵn 2 hàng chân đực `2x22` hướng xuống dưới. Cắm lên 2 thanh rào cái cao trên PCB chính giúp dễ tháo lắp khi nạp code/bảo trì và cho phép đi dây xuyên dưới bụng DevKit. |
| **`U7`** | `OLED 0.96" GM009605v4.3` | **`BOARD_MOUNT`** hoặc **`CONNECTOR_ONLY`** *(cùng dùng rào cái `1x04 P2.54mm`)* | `AIOT_Blackbox_Local:OLED_0.96_GM009605v4.3_1x04_P2.54mm_SingleLayer` | Kích thước `24.7 × 27.0 mm` đã in sẵn trên PCB (`GM009605v4.3`). Có thể cắm trực tiếp lên socket cái `1x04` trên PCB chính hoặc nối dây `4Pin` lên nắp hộp đen. |
| **`U2`** | `MPU6050 GY-521` | **`BOARD_MOUNT`** *(BẮT BUỘC cố định cứng vào PCB chính)* | `AIOT_Blackbox_Local:Module_GY-521_MPU6050_1x08_P2.54mm_SingleLayer` | Cảm biến gia tốc/góc nghiêng phát hiện tai nạn (`RULE 14`). **Lưu ý từ ảnh**: Module hiện đang hàn header đực bẻ góc 90°. Khi lắp thực tế lên PCB chính, nên **thay bằng header đực thẳng đứng** kết hợp trụ đỡ/ốc M3 để mặt phẳng `X-Y` của `GY-521` song song với mặt PCB chính, tránh rung lắc cơ học. |
| **`U3`** | `RTC DS3231 ZS-042` | **`BOARD_MOUNT`** *(Socket `1x06`)* hoặc **`CONNECTOR_ONLY`** | `AIOT_Blackbox_Local:Module_DS3231_ZS042_1x06_P2.54mm_SingleLayer` | Module đang hàn sẵn header đực 90° (`1x06 P2.54mm`) và có khay pin `CR2032` dày `~12mm` ở mặt sau. Dùng rào cái `1x06` ở biên PCB hoặc dây nối ngắn giúp thay pin `CR2032` dễ dàng mà không vướng linh kiện khác. |
| **`J1`** | `MicroSD Card Adapter` | **`BOARD_MOUNT`** *(Socket `1x06` đặt sát mép PCB)* hoặc **`CONNECTOR_ONLY`** | `AIOT_Blackbox_Local:Module_MicroSD_Adapter_1x06_P2.54mm_SingleLayer` | Module đang hàn sẵn header đực 90° (`1x06 P2.54mm`, `1:CS..5:VCC,6:GND`). Nếu cắm trên PCB cần chừa khoảng trống `>= 15mm` phía khe nhấn thẻ `push-push`. |
| **`U4`** | `GPS NEO-M8N V2149` | **`CONNECTOR_ONLY`** *(Đầu nối `1x05 P2.54mm`)* | `AIOT_Blackbox_Local:Conn_GPS_NEO-M8N_V2149_1x05_P2.54mm_SingleLayer` | Mặt sau module GPS có **anten gốm `25 × 25 mm`** dày và mặt trước có đầu SMA nối anten rời (`RULE 13`). Dùng đầu nối `1x05 P2.54mm` (`1:VCC, 2:GND, 3:TXD, 4:RXD, 5:PPS`) trên PCB chính để bắt cố định module GPS ở vị trí cao thoáng sóng trên vỏ hộp đen. |
| **`U5`** | `SIM 4G Breakout` (`A7680C`/`A7682S`) | **`CONNECTOR_ONLY`** *(Đầu nối `1x05 P2.54mm` cho hàng chân `J6`)* | `AIOT_Blackbox_Local:Conn_SIM_Breakout_J6_1x05_P2.54mm_SingleLayer` | Hàng chân trái (`RI..SPKN`) hoàn toàn không dùng. Chỉ cần 1 đầu nối `1x05 P2.54mm` (`1:VCC, 2:RST, 3:RXD, 4:TXD, 5:GND`) ở góc khu vực nguồn của PCB chính giúp đường nguồn dòng đỉnh `2A` ngắn nhất và cách ly bức xạ anten lò xo 4G khỏi `MPU6050` & `GPS` (`>= 50mm`). |
| **`U6`** | `Module Nguồn 3.3V` (`5V_SYS -> 3V3_SYS`) | **`CONNECTOR_ONLY`** *(Đầu nối `1x04 P2.54mm`)* | `AIOT_Blackbox_Local:Conn_Regulator_3V3_1x04_P2.54mm_SingleLayer` | Chưa có ảnh chụp thực tế của module hạ áp 3.3V trong thư mục linh kiện. Sử dụng đầu nối `1x04 P2.54mm` (`1:IN+, 2:IN-, 3:3V3, 4:GND`) giúp linh hoạt kết nối mọi module Buck/LDO `3.3V` bên ngoài. |
| **`J2`, `J3`** | `Domino Nguồn 5V_SYS & SIM_PWR` | **`BOARD_MOUNT`** *(Domino vặn vít 2P `P5.08mm`)* | `AIOT_Blackbox_Local:TermBlock_1x02_P5.08mm_SingleLayer` | Chịu dòng lớn (`3A`), kẹp dây nguồn từ bộ UPS `LX-2BUPS` và nguồn `SIM_PWR` chắc chắn, chống tuột dây khi xe máy điện rung xóc. |
| **`BZ1`, `D1`, `SW1`, `Q1`** | `Buzzer, LED, CANCEL` (Dự phòng) | **`RESERVE_CONNECTOR`** *(Khối dự phòng cô lập)* | Các footprint THT chuẩn trong `AIOT_Blackbox_Local.pretty` | Giữ nguyên trạng thái cô lập (`NC`) không nối vào GPIO của `ESP32-S3` theo đúng quyết định tại Gate 0. |

---

## 2. LƯU Ý CƠ KHÍ ĐẶC BIỆT TỪ ẢNH THỰC TẾ

1. **Hướng hàn Header 90° trên `MPU6050` (`U2`), `RTC DS3231` (`U3`) và `MicroSD` (`J1`)**:
   - Trong ảnh thực tế, cả 3 module `MPU6050`, `RTC DS3231`, và `MicroSD` đều đang được nhà sản xuất hàn sẵn **header đực bẻ góc vuông 90°**.
   - Đối với **`MPU6050` (`U2`)**: Cần lưu ý trục gia tốc `X, Y, Z` trong thuật toán phát hiện tai nạn (`filecodemain.cpp` đang tính `totalG = sqrt(ax^2 + ay^2 + az^2)` và kiểm tra biến thiên vector gia tốc `deltaG` để xác định xe đổ nghiêng). Dù thuật toán tính độ lớn tổng `totalG` và `deltaG` ít phụ thuộc góc xoay tĩnh, `MPU6050` vẫn **bắt buộc phải gắn cứng vào vỏ hộp/PCB chính** (không để treo lơ lửng trên dây cáp Dupont vì rung động dây sẽ tạo gia tốc giả `> 3.5G`).
2. **Tối ưu hóa hướng đặt `ESP32-S3` (`U1`) trên PCB 1 lớp**:
   - Do toàn bộ 10 chân GPIO đang dùng (`GPIO8..13, 15..18`) + `5Vin` + `GND` đều nằm ở **Hàng chân Trái (`Pin 1..22`)** của `ESP32-S3`, khi sang Gate 2 (Placement), ta sẽ quay Hàng chân Trái của `U1` hướng thẳng về phía nhóm ngoại vi (`I2C`, `SPI`, `UART`), giúp đi dây 1 lớp `B.Cu` thẳng hàng và gần như không cần nhảy dây qua hàng chân Phải!
