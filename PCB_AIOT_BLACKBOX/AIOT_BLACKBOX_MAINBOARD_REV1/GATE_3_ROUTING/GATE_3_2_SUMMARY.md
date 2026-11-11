# BÁO CÁO NGHIỆM THU GATE 3.2: HOÀN THIỆN TOÀN BỘ KẾT NỐI PCB 1 LỚP B.Cu BẰNG 11 JUMPER

> **Dự án**: AIoT Smart Blackbox Carrier Board (Hộp đen AIoT thông minh xe máy điện)  
> **Thư mục dự án**: `D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1`  
> **Giai đoạn**: **GATE 3.2 – HOÀN THIỆN ĐI DÂY PCB 1 LỚP ĐỒNG B.Cu**  
> **Quyết định thiết kế**: Giữ nguyên PCB 1 lớp đồng `B.Cu`, KHÔNG chuyển sang 2 lớp, KHÔNG dùng via, KHÔNG đổi GPIO/firmware (`filecodemain.cpp`), xử lý triệt để toàn bộ kết nối hở bằng cầu nối dây cách điện mặt trên (`Top Wire Jumpers`). KHÔNG xuất Gerber.

---

## 1. TỔNG QUAN KẾT QUẢ NGHIỆM THU GATE 3.2

Sau khi tiến hành kiểm toán hình học, tối ưu hóa điểm đặt và phân tích quy tắc thiết kế (DRC) chính thức bằng `kicad-cli`, bản vẽ PCB đã đạt **100% mục tiêu kỹ thuật**:

| Tiêu chuẩn nghiệm thu | Trạng thái trước Gate 3.2 | Kết quả Gate 3.2 (REV3) | Đánh giá |
|---|---|---|---|
| **Số lớp đồng thực tế** | 1 lớp (`B.Cu`) | **1 lớp duy nhất (`B.Cu`)** | **ĐẠT (PASS)** |
| **Đường mạch trên F.Cu** | 0 | **0 track** | **ĐẠT (PASS)** |
| **Số lượng Via xuyên bo** | 0 | **0 via** | **ĐẠT (PASS)** |
| **Đường đồng giao cắt (Tracks Crossing)** | 0 | **0 vi phạm** | **ĐẠT (PASS)** |
| **Chập ngắn mạch (Shorting Items)** | 0 | **0 vi phạm** | **ĐẠT (PASS)** |
| **Vi phạm khoảng cách an toàn (Clearance)** | 1 (SCK vs JMP11) | **0 vi phạm (Clearance = 0)** | **ĐẠT (PASS)** |
| **Va chạm lỗ khoan (Hole-to-Hole)** | 2 (JMP8/U2, JMP11/J1) | **0 vi phạm (Hole-to-Hole = 0)** | **ĐẠT (PASS)** |
| **Lỗi bắc cầu mặt nạ hàn (Solder Mask Bridge)** | 0 | **0 vi phạm** | **ĐẠT (PASS)** |
| **Kết nối đồng chức năng còn hở** | 5 khối mạch | **0 kết nối hở (100% hoàn tất)** | **ĐẠT (PASS)** |
| **Tổng số Jumper dây cách điện** | 7 jumper (Gate 3.1) | **11 jumper (`JMP1` – `JMP11`)** | **ĐẠT (PASS)** |
| **Kiểm tra Schematic ERC** | 0 Errors, 0 Warnings | **0 Errors, 0 Warnings** | **ĐẠT (PASS)** |

---

## 2. CHI TIẾT XỬ LÝ DỨT ĐIỂM 5 KHỐI KẾT NỐI ƯU TIÊN

Theo yêu cầu của người dùng, toàn bộ 5 kết nối còn thiếu từ Gate 3.1 đã được sửa dứt điểm bằng đồng `B.Cu` và các jumper THT chuyên dụng:

### 2.1. MPU6050 Chân 7 (AD0) $\rightarrow$ `3V3_SYS` (Khóa cứng địa chỉ I2C `0x69`)
- **Vấn đề trước đó**: Chân AD0 (U2.7) bị hở mạch, nguy cơ trôi mức logic về 0 làm cảm biến MPU6050 nhận nhầm địa chỉ `0x68`, gây xung đột bus nghiêm trọng với RTC DS3231 (`0x68`).
- **Giải pháp Gate 3.2**: Bố trí jumper `JMP8` (`WireJumper_P12.70mm_SingleLayer`) tại tọa độ `(102.35, 87.00)`, góc quay 90°.
  - Đầu Bắc `j8_n` tại `(102.35, 80.65)` nối vào đường nguồn `3V3_SYS` tại `Y=84.50`.
  - Đầu Nam `j8_s` tại `(102.35, 93.35)` nối vào chân U2.7 `(102.35, 96.00)`.
  - Jumper bay ở mặt Top vượt qua hoàn toàn hai đường bus SDA (`Y=88.50`) và SCL (`Y=91.50`).
  - Khoảng cách tim lỗ khoan tới chân U2.7 đạt $2.65\text{mm} > 1.30\text{mm}$ (chuẩn an toàn), loại bỏ hoàn toàn cảnh báo va chạm lỗ khoan. Khoảng cách cách điện tới SCL đạt $0.575\text{mm} > 0.400\text{mm}$.

### 2.2. Điện trở kéo lên `R_PU2` $\rightarrow$ `3V3_SYS` (Hoàn thiện Pull-up cho Bus I2C SCL)
- **Vấn đề trước đó**: Chân 1 của `R_PU2` chưa được cấp nguồn `3V3_SYS`, khiến đường xung nhịp SCL (GPIO9) thiếu điện trở kéo lên phần cứng $4.7\text{k}\Omega$.
- **Giải pháp Gate 3.2**: Bố trí jumper `JMP9` (`WireJumper_P7.62mm_SingleLayer`) tại tọa độ `(130.00, 90.00)`, góc quay 90°.
  - Đầu Bắc `j9_n` tại `(130.00, 86.19)` nhận nguồn từ rail `3V3_SYS` tại `(134.92, 86.50)`.
  - Đầu Nam `j9_s` tại `(130.00, 93.81)` cấp thẳng vào chân 1 của `R_PU2` tại `(134.92, 93.50)`.
  - Vượt qua vùng giao cắt SDA/SCL an toàn, đảm bảo đường xung nhịp SCL có sườn lên vuông vắn, chống nhiễu tuyệt đối.

### 2.3. Màn hình OLED U7 Chân 3 $\rightarrow$ `I2C_SCL_GPIO9`
- **Vấn đề trước đó**: Chân SCL của màn hình OLED 0.96" (U7.3 tại `103.27, 116.50`) bị chặn bởi đường ngang SDA (`Y=104.00`), không thể kéo dây tới bus SCL chung.
- **Giải pháp Gate 3.2**: Bố trí jumper `JMP10` (`WireJumper_P7.62mm_SingleLayer`) tại tọa độ `(103.27, 106.00)`, góc quay 90°.
  - Đầu Bắc `j10_n` tại `(103.27, 102.19)` đón tín hiệu SCL từ xương trục `X=108.00, Y=100.00`.
  - Đầu Nam `j10_s` tại `(103.27, 109.81)` đi thẳng xuống chân U7.3 tại `(103.27, 116.50)`.
  - Dây jumper bay qua đường SDA chạy ngang ở `Y=104.00`, bảo đảm tính phẳng và liên tục cho toàn bộ bus I2C.

### 2.4. Phân nhánh Bus Dữ liệu `I2C_SDA_GPIO8`
- **Vấn đề trước đó**: Các nhánh SDA tới OLED (U7.4), MPU6050 (U2.4) và DS3231 (U3.4) bị gián đoạn.
- **Giải pháp Gate 3.2**: Thiết lập xương trục SDA chạy ngang ở `Y=104.00`, tiếp nhận tín hiệu từ đầu Nam của `JMP4` (`112.00, 98.58`).
  - Phân nhánh thẳng vào U7.4 tại `(105.81, 104.00) -> (105.81, 116.50)`.
  - Phân nhánh thẳng vào U2.4 tại `(94.73, 104.00) -> (94.73, 96.00)`.
  - Kéo dài sang phía Tây vào U3.4 tại `(69.27, 104.00) -> (69.27, 100.00)`.
  - Toàn bộ 4 thiết bị I2C (ESP32 master, OLED, MPU6050, DS3231) kết nối chung một mạng duy nhất, thông suốt 100%.

### 2.5. Mass Chân 6 Header MicroSD J1 $\rightarrow$ Mặt phẳng `GND`
- **Vấn đề trước đó**: Chân 6 của header J1 (GND tại `144.35, 104.00`) bị bao vây tứ phía bởi SCK (phía Bắc), đường nguồn lớn 5V_SYS (phía Nam) và MISO (phía Đông), không thể chạm tới mặt phẳng mass đồng B.Cu.
- **Giải pháp Gate 3.2**: Bố trí jumper `JMP11` (`WireJumper_P12.70mm_SingleLayer`) tại tọa độ `(144.35, 112.50)`, góc quay 90°.
  - Đầu Bắc `j11_n` tại `(144.35, 106.15)` nối trực tiếp vào J1.6 bằng đoạn đồng ngắn 0.50mm.
  - Đầu Nam `j11_s` tại `(144.35, 118.85)` cắm thẳng vào mặt phẳng mass GND nguyên khối.
  - Đồng thời nâng cấp jumper `JMP6` (MISO) lên pitch 10.16mm (`WireJumper_P10.16mm_SingleLayer`) tại `(144.35, 106.30)`, mở rộng khoảng cách cách điện giữa pad JMP6 và pad JMP11 lên $2.88\text{mm} \gg 0.400\text{mm}$, xóa bỏ hoàn toàn vi phạm clearance cuối cùng.

---

## 3. DANH BẠ VẬT TƯ & LẮP RÁP 11 WIRE JUMPER (REV3)

Toàn bộ 11 jumper được cắm ở mặt trên (`Top`), hai chân xuyên lỗ hàn xuống mặt dưới (`B.Cu`), sử dụng dây đồng lõi đơn cách điện chất lượng cao (Teflon / PVC chịu nhiệt):

| RefDes | Pitch (mm) | Pitch (mil) | Net kết nối | Tọa độ Pad 1 (X, Y) | Tọa độ Pad 2 (X, Y) | Cỡ dây | Chiều dài | Màu dây | Vai trò chức năng trong hệ thống |
|---|---|---|---|---|---|---|---|---|---|
| **`JMP1`** | 12.70 | 500 | `Net-(J1-MOSI)` | (151.00, 111.67) | (151.00, 98.97) | 24 AWG | 15 mm | Xanh dương | Nhảy tín hiệu SPI MOSI qua SCK và MISO vào ESP32 Pin 17 |
| **`JMP2`** | 7.62 | 300 | `3V3_SYS` | (81.00, 61.81) | (81.00, 54.19) | 22 AWG | 10 mm | Đỏ | Nhảy nguồn 3V3_SYS qua đường SIM_PWR (2.5mm) cấp R3 nút bấm |
| **`JMP3`** | 7.62 | 300 | `Net-(U1-GPIO6)` | (145.00, 61.73) | (145.00, 54.11) | 24 AWG | 10 mm | Vàng | Nhảy tín hiệu nút nhấn CANCEL qua chân Base Q1 còi báo động |
| **`JMP4`** | 10.16 | 400 | `/I2C_SDA_GPIO8` | (112.00, 98.58) | (112.00, 88.42) | 24 AWG | 13 mm | Xanh lá | Nhảy bus dữ liệu I2C_SDA qua đường ngang SCL (Y=91.50) |
| **`JMP5`** | 7.62 | 300 | `Net-(U1-GPIO6)` | (124.00, 49.81) | (124.00, 42.19) | 24 AWG | 10 mm | Vàng | Nhảy tín hiệu CANCEL qua xương nguồn 5V_SYS (Y=43.50) |
| **`JMP6`** | 10.16 | 400 | `Net-(J1-MISO)` | (139.27, 106.30) | (149.43, 106.30) | 24 AWG | 13 mm | Tím / Trắng | Nhảy tín hiệu SPI MISO qua chân 5V và GND của header MicroSD J1 |
| **`JMP7`** | 10.16 | 400 | `3V3_SYS` | (80.00, 96.00) | (80.00, 85.84) | 22 AWG | 13 mm | Đỏ | Nhảy nguồn 3V3_SYS qua SCL cấp cho RTC DS3231 và IMU MPU6050 |
| **`JMP8`** | 12.70 | 500 | `3V3_SYS` | (102.35, 93.35) | (102.35, 80.65) | 24 AWG | 15 mm | Đỏ | Nhảy 3V3_SYS cấp AD0 MPU6050 để khóa cứng địa chỉ I2C `0x69` |
| **`JMP9`** | 7.62 | 300 | `3V3_SYS` | (130.00, 93.81) | (130.00, 86.19) | 24 AWG | 10 mm | Đỏ | Nhảy 3V3_SYS cấp trở kéo lên R_PU2 ($4.7\text{k}\Omega$) cho bus SCL |
| **`JMP10`** | 7.62 | 300 | `/I2C_SCL_GPIO9` | (103.27, 109.81) | (103.27, 102.19) | 24 AWG | 10 mm | Cam | Nhảy xung I2C_SCL qua sống ngang SDA (Y=104.00) cấp màn hình OLED |
| **`JMP11`** | 12.70 | 500 | `GND` | (144.35, 118.85) | (144.35, 106.15) | 22 AWG | 15 mm | Đen | Nhảy mass GND MicroSD J1.6 qua sống 5V_SYS vào mặt phẳng mass GND |

---

## 4. CHI TIẾT CÁC FILE BÀN GIAO TRONG THƯ MỤC `GATE_3_ROUTING`

Toàn bộ hồ sơ bàn giao của Gate 3.2 đã được biên dịch hoàn chỉnh, lưu trữ tập trung tại:
`D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1\GATE_3_ROUTING`

1. [PCB_ROUTING_BOTTOM_COPPER_ONLY_REV3.png](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/PCB_ROUTING_BOTTOM_COPPER_ONLY_REV3.png): Bản vẽ độ phân giải cao 300 DPI (3508 x 2481 px) lớp đồng đáy `B.Cu` soi gương (Mirrored) kèm đường viền cắt bo `Edge.Cuts` và phủ đồng mass GND nguyên khối, phục vụ trực tiếp cho việc in phim rửa mạch / phay CNC PCB 1 lớp.
2. [PCB_ROUTING_TOP_JUMPERS_REV3.png](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/PCB_ROUTING_TOP_JUMPERS_REV3.png): Bản vẽ 300 DPI mặt trên thể hiện trực quan vị trí, màu sắc, chiều dài và mã hiệu của toàn bộ 11 jumper dây cách điện kết hợp khung định vị linh kiện và chữ in Silkscreen.
3. [DRC_GATE3_2.txt](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/DRC_GATE3_2.txt): Báo cáo kiểm tra luật thiết kế chính thức từ `kicad-cli pcb drc --severity-all` xác nhận: **0 Tracks Crossing, 0 Shorting Items, 0 Clearance Violations, 0 Hole-to-Hole Violations**.
4. [JUMPER_ASSEMBLY_REV3.csv](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/JUMPER_ASSEMBLY_REV3.csv): Bảng tra cứu kỹ thuật chi tiết phục vụ lắp ráp thủ công trong phòng thí nghiệm (tọa độ pad, pitch, cỡ dây AWG, chiều dài cắt dây, màu vỏ bọc cách điện và hướng dẫn hàn).
5. [UNROUTED_GATE3_2.csv](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/UNROUTED_GATE3_2.csv): Bảng thống kê chi tiết xác nhận không còn đường dây đồng vật lý nào bị bỏ sót; 11 airwire tương ứng với 11 jumper mặt trên đã được khép kín 100% bằng dây hàn, 4 đảo đồng mass cô lập ở rìa bo không gây ảnh hưởng.
6. [BOM_MAINBOARD_REV1.csv](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/BOM_MAINBOARD_REV1.csv): Bảng bóc tách linh kiện chính thức của dự án đã đồng bộ đầy đủ 40 hạng mục (tất cả linh kiện active, passive, connector, terminal, test point và 11 wire jumper).
7. [AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pcb](file:///D:/ĐỒ%20ÁN%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pcb): File cơ sở dữ liệu mạch in KiCad chính thức đã áp dụng hoàn chỉnh layout REV3.

---

## 5. KẾT LUẬN & ĐIỀU KIỆN CHUYỂN TIẾP GATE 4

- **Trạng thái Gate 3.2**: **HOÀN THÀNH TOÀN DIỆN (100% PASSED)**.
- Mạch in đã thỏa mãn tuyệt đối nguyên lý **PCB 1 LỚP ĐỒNG `B.Cu`**, bảo vệ nguyên vẹn cấu trúc phần cứng, ánh xạ GPIO chuẩn theo `filecodemain.cpp`, không cần can thiệp bất kỳ dòng code firmware nào.
- Hồ sơ kỹ thuật đảm bảo tính khả thi cao nhất cho phương pháp gia công mạch in thủ công và hàn ráp trong điều kiện phòng thí nghiệm tại Việt Nam.
- **Tuân thủ chỉ thị người dùng**: Dừng ngay sau Gate 3.2; **KHÔNG xuất Gerber**, sẵn sàng bước vào giai đoạn tiếp theo (GATE 4 - Phân tích toàn vẹn nguồn & Chuẩn bị chế tạo) khi người dùng ra lệnh.

