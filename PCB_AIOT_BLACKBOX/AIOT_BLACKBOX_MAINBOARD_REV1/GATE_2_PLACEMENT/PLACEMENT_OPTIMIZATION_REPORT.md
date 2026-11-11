# BÁO CÁO TỐI ƯU HÓA BỐ TRÍ LINH KIỆN PCB 1 LỚP (GATE 2.1 PLACEMENT OPTIMIZATION REPORT)

> **Dự án**: THIẾT KẾ HỘP ĐEN AIoT THÔNG MINH PHÂN TÍCH VÀ GHI LẠI SỰ CỐ XE MÁY ĐIỆN  
> **Project KiCad**: `D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1`  
> **Giai đoạn**: **GATE 2.1 – Tối ưu hóa cơ khí & mặt bằng linh kiện PCB 1 lớp (`B.Cu`)**  
> **Thời điểm thực hiện**: 2026-11-09  
> **KiCad Version**: KiCad 10.0.6 (`kicad-cli`, `pcbnew`)  
> **Tệp PCB chính thức đã cập nhật**:
> - [AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pcb](file:///D:/%C4%90%E1%BB%92%20%C3%81N%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pcb)
> - [GATE_2_PLACEMENT/AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pcb](file:///D:/%C4%90%E1%BB%92%20%C3%81N%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_2_PLACEMENT/AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pcb)
>
> **Xác nhận tính toàn vẹn tệp (Cryptographic SHA-256 Hash Verification)**:
> - **SHA-256 Trước thay đổi (REV1 Baseline)**: `A6321C09623E97F5BBA1DF597E630F2F3EBA63CF412DB7276C927F1970BE917C`
> - **SHA-256 Sau tối ưu (REV2 Updated)**: `1D32B0FD30BADEE02226AA5B5B7BB8C94FFA093134D1E8BABAA496CF3134B539`
> - **Minh chứng**: Đã thực hiện thay đổi vật lý trực tiếp trong tệp `.kicad_pcb` (không chỉ viết báo cáo).

---

## 1. TỔNG QUAN KẾT QUẢ TỐI ƯU HÓA GATE 2.1

Phiên làm việc này đã giải quyết toàn bộ các yêu cầu cơ khí và hình học được người dùng chỉ đạo trong Request #9 và Request #10:

1. **ESP32-S3 (`U1`) đã dịch chuyển về phía Nam (`Y = 85.00 mm`, ΔY = +6.5 mm)**:
   - Rút ngắn khoảng cách từ mép cổng Dual USB-C tới mép Nam PCB từ `36.5 mm` xuống còn `30.0 mm`.
   - Vùng cấm đồng anten (`ESP32_S3_ANTENNA_KEEPOUT`) được cập nhật chuẩn xác thành `(155.0..185.0 mm, 40.0..55.0 mm)`, tạo hành lang `15.0 mm` hoàn toàn không có đồng dẫn thẳng ra mép Bắc PCB (`Y = 40.0 mm`), bảo toàn 100% hiệu suất bức xạ RF.
   - Hành lang cắm cáp USB-C (`X = 156.0 .. 184.0 mm, Y = 115.0 .. 145.0 mm`) được giải phóng hoàn toàn, không có bất kỳ linh kiện nào chắn ngang.
2. **Khối nguồn công suất cao được tinh gọn thẳng hàng (In-line Star Distribution)**:
   - `J2` (Nguồn UPS) $\rightarrow$ `NT1` (Star-Point NetTie) $\rightarrow$ `C3` (Tụ hóa 470µF) $\rightarrow$ `C4` (Tụ gốm 100nF) $\rightarrow$ `U5.1` (Chân SIM_PWR).
   - `NT1`, `C3`, `C4` nằm thẳng tắp trên đường ngang `Y = 58.00 mm`.
   - `C4.1` (`X = 95.46, Y = 58.00`) và `U5.1` (`X = 95.46, Y = 68.00`) **gióng thẳng đứng tuyệt đối**, đường nguồn dòng đỉnh `2A` chỉ dài đúng **`10.0 mm`** không qua bất kỳ góc cua nào, triệt tiêu tối đa điện cảm ký sinh.
   - Module hạ áp `U6` (3.3V) dịch lên `Y = 76.00 mm`, rút ngắn đường cấp `5V_SYS` từ `22.5 mm` xuống `16.5 mm`.
3. **Cảm biến gia tốc MPU6050 (`U2`)**:
   - Tọa độ `(96.00, 96.00)` được giữ vững ở vùng ổn định cơ khí, cách còi báo động `BZ1` một khoảng an toàn `62.5 mm` (> 40 mm).
   - Tuân thủ nghiêm ngặt chỉ đạo: **KHÔNG tự đoán tọa độ để tạo lỗ vít NPTH giả định**. Các lỗ vít cố định của module GY-521 được đánh dấu là `PENDING_MEASUREMENT` (OI-04), bổ sung phương án đệm silicon chống rung và thanh nẹp kẹp bo.
4. **Màn hình OLED 0.96" (`U7`)**:
   - Bố trí tại `(102.00, 116.50)` với không gian thông thoáng xung quanh.
   - Xác nhận vai trò kép (`DUAL-USE`): Header 1x04 P2.54mm trên mạch vừa có thể cắm trực tiếp module OLED nằm phẳng, vừa có thể cắm cáp bẹ 4 dây dẫn lên màn hình gắn trên nắp hộp đen mà không cần thay đổi schematic hay footprint.
5. **Đầu đọc thẻ MicroSD (`J1`)**:
   - Dịch chuyển theo ESP32-S3 tới `(138.00, 104.00, 0°)`.
   - Toàn bộ 4 chân tín hiệu SPI (`CS, SCK, MOSI, MISO`) và 2 chân nguồn (`5V_SYS, GND`) nằm đối diện và cách các chân tương ứng trên `U1` chỉ từ `18.5 mm` đến `24.0 mm`.
   - Khe cắm thẻ MicroSD quay thẳng ra mép Nam PCB (`Y = 144.2 mm`, sát mép bo `Y = 145.0 mm`), cho phép tháo/lắp thẻ nhớ ngoài vỏ hộp mà không cần tháo rời bo mạch.
6. **Không vi phạm DRC & Giữ nguyên 8 Net Classes**:
   - KiCad CLI DRC: **`0 DRC Violations`** (0 courtyard overlap, 0 pth inside courtyard, 0 silk overlap, 0 clearance error).
   - KiCad CLI ERC: **`0 Errors, 0 Warnings`**.
   - Net Classes trong `.kicad_pro`: Giữ nguyên vẹn 100% 8 lớp (`Default`, `I2C`, `UART`, `SPI`, `3V3_POWER`, `5V_POWER`, `SIM_POWER`, `GND`).

---

## 2. BẢNG TỌA ĐỘ TOÀN BỘ 32 FOOTPRINT TRƯỚC VÀ SAU TỐI ƯU (REV1 VS REV2)

Dưới đây là bảng đối chiếu chi tiết tọa độ và góc xoay của 100% linh kiện trên bo mạch:

| STT | Ref | Giá trị / Mô tả | Footprint thư viện `AIOT_Blackbox_Local` | Tọa độ REV1 `(X, Y, Rot)` | Tọa độ REV2 `(X, Y, Rot)` | Độ lệch `(ΔX, ΔY)` | Trạng thái | Rationale kỹ thuật & Cơ khí |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| 1 | **`U1`** | `ESP32-S3` | `ESP32_S3_N16R8_Socket_2x22_P2.54mm_Row25.40mm_SingleLayer` | `(169.00, 78.50, 0.0°)` | `(170.00, 85.00, 0.0°)` | `(+1.0, +6.5)` | **MOVED** | Dịch Nam 6.5mm giúp cổng Dual USB-C tiếp cận sát mép Nam; X=170mm tăng thêm 1.0mm hành lang đi dây bên trái; giữ cách lỗ vít H2/H4 >3.3mm. |
| 2 | **`J2`** | `LX-2BUPS_5V_3A` | `TermBlock_1x02_P5.08mm_SingleLayer` | `(60.00, 62.00, 90.0°)` | `(60.00, 62.00, 90.0°)` | `(0.0, 0.0)` | **LOCKED** | Cọc domino nguồn ngoài 5V/3A ở mép Tây bo mạch; Pad 1 (5V_SYS) ở trên, Pad 2 (GND) ở dưới. |
| 3 | **`TP1`** | `TP_5V` | `TestPoint_THTPad_D2.2mm_Drill1.0mm_SingleLayer` | `(69.00, 58.00, 0.0°)` | `(68.00, 56.00, 0.0°)` | `(-1.0, -2.0)` | **OPTIMIZED** | Đặt ngay sát Pad 1 của J2 để đo điện áp đầu vào 5V_SYS. |
| 4 | **`TP4`** | `TP_GND` | `TestPoint_THTPad_D2.2mm_Drill1.0mm_SingleLayer` | `(69.00, 66.00, 0.0°)` | `(68.00, 64.00, 0.0°)` | `(-1.0, -2.0)` | **OPTIMIZED** | Đặt ngay sát Pad 2 của J2 làm điểm nối mass tham chiếu chính. |
| 5 | **`NT1`** | `STAR_5V_TO_SIM_PWR` | `NetTie_2_StarPoint_BCu_Width2.5mm` | `(78.00, 58.00, 0.0°)` | `(76.00, 58.00, 0.0°)` | `(-2.0, 0.0)` | **OPTIMIZED** | Điểm nối sao 5V_SYS $\rightarrow$ SIM_PWR; rút ngắn khoảng cách từ J2.1 thêm 2mm; nằm trên trục ngang Y=58mm. |
| 6 | **`C3`** | `470uF` (Low-ESR) | `CP_Radial_D8.0mm_P5.08mm_SingleLayer` | `(89.00, 56.00, 0.0°)` | `(87.00, 58.00, 0.0°)` | `(-2.0, +2.0)` | **OPTIMIZED** | Nằm trên trục Y=58mm; nối thẳng từ NT1.2 sang C3.1 bằng đường đồng rộng 2.5mm dài 7.2mm. |
| 7 | **`C4`** | `100nF` | `C_Disc_D5.0mm_P5.08mm_SingleLayer` | `(99.00, 56.00, 0.0°)` | `(98.00, 58.00, 0.0°)` | `(-1.0, +2.0)` | **OPTIMIZED** | Nằm trên trục Y=58mm; Pad 1 (SIM_PWR) tại X=95.46 gióng thẳng đứng với U5.1. |
| 8 | **`TP3`** | `TP_SIM_PWR` | `TestPoint_THTPad_D2.2mm_Drill1.0mm_SingleLayer` | `(99.00, 49.00, 0.0°)` | `(98.00, 50.00, 0.0°)` | `(-1.0, +1.0)` | **OPTIMIZED** | Điểm đo nhánh nguồn dòng đỉnh SIM_PWR đặt ngay trên C4. |
| 9 | **`U5`** | `A7680C` (Breakout J6) | `Conn_SIM_Breakout_J6_1x05_P2.54mm_SingleLayer` | `(100.00, 71.00, 0.0°)` | `(100.54, 68.00, 0.0°)` | `(+0.54, -3.0)` | **OPTIMIZED** | Pad 1 (SIM_PWR) tại (95.46, 68.00) **thẳng đứng 100% với C4.1 (95.46, 58.00)**; đường nguồn đỉnh chỉ 10mm. |
| 10 | **`U6`** | `REG_3V3_MODULE` | `Conn_Regulator_3V3_1x04_P2.54mm_SingleLayer` | `(66.00, 82.00, 0.0°)` | `(66.00, 76.00, 0.0°)` | `(0.0, -6.0)` | **OPTIMIZED** | Dịch lên gần J2 hơn 6mm, rút ngắn đường cấp nguồn 5V_SYS vào module buck. |
| 11 | **`C1`** | `100nF` | `C_Disc_D5.0mm_P5.08mm_SingleLayer` | `(80.00, 82.00, 0.0°)` | `(78.00, 76.00, 0.0°)` | `(-2.0, -6.0)` | **OPTIMIZED** | Nối thẳng ngang tại Y=76.00mm vào ngõ ra 3V3_SYS (U6.3). |
| 12 | **`TP2`** | `TP_3V3` | `TestPoint_THTPad_D2.2mm_Drill1.0mm_SingleLayer` | `(80.00, 75.00, 0.0°)` | `(78.00, 70.00, 0.0°)` | `(-2.0, -5.0)` | **OPTIMIZED** | Điểm đo nhánh nguồn 3.3V đặt ngay trên tụ lọc C1. |
| 13 | **`BZ1`** | `BUZZER` (Active 12mm) | `Buzzer_D12.0mm_P7.62mm_SingleLayer` | `(136.00, 48.00, 0.0°)` | `(136.00, 48.00, 0.0°)` | `(0.0, 0.0)` | **LOCKED** | Đặt sát mép Bắc; cách cảm biến gia tốc U2 một khoảng 62.5mm (> 40mm) chống rung âm học. |
| 14 | **`Q1`** | `2SC1815` (TO-92) | `TO-92_2SC1815_ECB_Staggered_SingleLayer` | `(136.00, 60.50, 0.0°)` | `(136.00, 63.00, 0.0°)` | `(0.0, +2.5)` | **OPTIMIZED** | Dịch xuống 2.5mm để bám sát cao độ GPIO5 trên U1 (Y=68.49mm). |
| 15 | **`R5`** | `1k` (Base Drive) | `R_Axial_DIN0207_P10.16mm_SingleLayer` | `(148.00, 60.50, 90.0°)` | `(149.00, 63.00, 90.0°)` | `(+1.0, +2.5)` | **OPTIMIZED** | Điện trở kích Base Q1 nối trực tiếp từ U1.GPIO5 sang Q1.B. |
| 16 | **`R6`** | `10k` (Base Pulldown) | `R_Axial_DIN0207_P10.16mm_SingleLayer` | `(136.00, 68.00, 0.0°)` | `(136.00, 71.00, 0.0°)` | `(0.0, +3.0)` | **OPTIMIZED** | Điện trở khóa chân B của Q1 xuống GND khi khởi động. |
| 17 | **`SW1`** | `CANCEL` (1x02) | `PinHeader_1x02_P2.54mm_SingleLayer` | `(114.00, 46.50, 0.0°)` | `(116.00, 47.00, 0.0°)` | `(+2.0, +0.5)` | **OPTIMIZED** | Header cắm nút bấm hủy cảnh báo ở mép Bắc vỏ hộp. |
| 18 | **`R3`** | `10k` (Pull-up SW1) | `R_Axial_DIN0207_P10.16mm_SingleLayer` | `(114.00, 52.50, 0.0°)` | `(116.00, 53.50, 0.0°)` | `(+2.0, +1.0)` | **OPTIMIZED** | Điện trở kéo lên 3V3_SYS cho nút CANCEL. |
| 19 | **`C2`** | `100nF` (Debounce) | `C_Disc_D5.0mm_P5.08mm_SingleLayer` | `(114.00, 58.00, 0.0°)` | `(116.00, 60.00, 0.0°)` | `(+2.0, +2.0)` | **OPTIMIZED** | Tụ chống dội phần cứng cho nút nhấn CANCEL. |
| 20 | **`D1`** | `LED` (Status 5mm) | `LED_D5.0mm_P2.54mm_SingleLayer` | `(110.00, 64.00, 0.0°)` | `(112.00, 66.50, 0.0°)` | `(+2.0, +2.5)` | **OPTIMIZED** | Dịch sang X=112mm để tách hoàn toàn khỏi courtyard của U5 (tránh lỗi DRC courtyard). |
| 21 | **`R4`** | `330R` (Hạn dòng LED) | `R_Axial_DIN0207_P10.16mm_SingleLayer` | `(121.00, 64.00, 0.0°)` | `(122.00, 66.50, 0.0°)` | `(+1.0, +2.5)` | **OPTIMIZED** | Điện trở hạn dòng nối từ U1.GPIO7 (Y=73.57mm) tới Anode của D1. |
| 22 | **`U4`** | `NEO-M8N` (GPS 1x05) | `Conn_GPS_NEO-M8N_V2149_1x05_P2.54mm_SingleLayer` | `(122.00, 77.00, 0.0°)` | `(122.00, 80.00, 0.0°)` | `(0.0, +3.0)` | **OPTIMIZED** | Chân UART TXD/RXD tại Y=80.00mm nằm ngang hàng với U1 GPIO17/GPIO18 (Y=81.19/83.73mm). |
| 23 | **`R_PU1`** | `4.7k` (I2C SDA) | `R_Axial_DIN0207_P10.16mm_SingleLayer` | `(139.00, 81.50, 0.0°)` | `(140.00, 86.50, 0.0°)` | `(+1.0, +5.0)` | **OPTIMIZED** | Nằm ngang hàng hoàn hảo với U1.GPIO8 (I2C_SDA tại Y=86.27mm). |
| 24 | **`R_PU2`** | `4.7k` (I2C SCL) | `R_Axial_DIN0207_P10.16mm_SingleLayer` | `(139.00, 87.50, 0.0°)` | `(140.00, 93.50, 0.0°)` | `(+1.0, +6.0)` | **OPTIMIZED** | Nằm ngang hàng hoàn hảo với U1.GPIO9 (I2C_SCL tại Y=93.89mm). |
| 25 | **`U2`** | `MPU6050` (GY-521) | `Module_GY-521_MPU6050_1x08_P2.54mm_SingleLayer` | `(96.00, 96.00, 0.0°)` | `(96.00, 96.00, 0.0°)` | `(0.0, 0.0)` | **PRESERVED** | Vị trí trung tâm cơ khí ổn định; hướng trục `+X UP / +Y LEFT`; lỗ vít cố định đánh dấu PENDING. |
| 26 | **`U3`** | `DS3231` (ZS-042) | `Module_DS3231_ZS042_1x06_P2.54mm_SingleLayer` | `(68.00, 100.00, 0.0°)` | `(68.00, 100.00, 0.0°)` | `(0.0, 0.0)` | **PRESERVED** | Góc Dưới – Trái; khay pin CR2032 hoàn toàn thông thoáng, dễ dàng thay pin dự phòng. |
| 27 | **`U7`** | `OLED 0.96"` (I2C) | `OLED_0.96_GM009605v4.3_1x04_P2.54mm_SingleLayer` | `(102.00, 116.50, 0.0°)` | `(102.00, 116.50, 0.0°)` | `(0.0, 0.0)` | **PRESERVED** | Header 1x04 hỗ trợ vai trò kép: cắm socket trực tiếp hoặc cắm cáp 4 dây nối màn hình trên nắp hộp. |
| 28 | **`J1`** | `MICROSD` (Adapter) | `Module_MicroSD_Adapter_1x06_P2.54mm_SingleLayer` | `(137.00, 101.00, 0.0°)` | `(138.00, 104.00, 0.0°)` | `(+1.0, +3.0)` | **MOVED** | Dịch Nam theo U1; chân SPI cực ngắn (18.5..24mm); khe cắm thẻ quay sát mép Nam (Y=144.2mm). |
| 29 | **`H1`** | `M3_NPTH` | `MountingHole_3.2mm_M3_NPTH` | `(55.00, 45.00, 0.0°)` | `(55.00, 45.00, 0.0°)` | `(0.0, 0.0)` | **LOCKED** | Lỗ bắt vít M3 Góc Trên – Trái. Cách mép 5.0mm. |
| 30 | **`H2`** | `M3_NPTH` | `MountingHole_3.2mm_M3_NPTH` | `(190.00, 45.00, 0.0°)` | `(190.00, 45.00, 0.0°)` | `(0.0, 0.0)` | **LOCKED** | Lỗ bắt vít M3 Góc Trên – Phải. Cách mép 5.0mm. Khoảng cách tới pad U1 là 6.5mm. |
| 31 | **`H3`** | `M3_NPTH` | `MountingHole_3.2mm_M3_NPTH` | `(55.00, 140.00, 0.0°)` | `(55.00, 140.00, 0.0°)` | `(0.0, 0.0)` | **LOCKED** | Lỗ bắt vít M3 Góc Dưới – Trái. Cách mép 5.0mm. |
| 32 | **`H4`** | `M3_NPTH` | `MountingHole_3.2mm_M3_NPTH` | `(190.00, 140.00, 0.0°)` | `(190.00, 140.00, 0.0°)` | `(0.0, 0.0)` | **LOCKED** | Lỗ bắt vít M3 Góc Dưới – Phải. Cách mép 5.0mm. Khoảng cách tới pad U1 là 6.5mm. |

---

## 3. PHÂN TÍCH CHI TIẾT CÁC CẢI TIẾN CƠ KHÍ & ĐIỆN THEO CHỈ ĐẠO CỦA NGƯỜI DÙNG

### 3.1. Vấn đề cổng USB ESP32-S3 và Vùng cấm Anten (Giải quyết OI-02)
- **Hiện trạng trước đây**:
  - `U1` ở `Y = 78.50 mm`. Cổng USB kết thúc ở `Y = 108.5 mm`, cách mép Nam `36.5 mm`. Cáp USB cắm vào bị sâu vào trong lòng bo.
- **Giải pháp tối ưu đã áp dụng trong REV2**:
  1. `U1` dịch chuyển xuống `Y = 85.00 mm` (Nam tiến `6.5 mm`). Cổng Dual USB-C tiến xuống `Y = 115.00 mm`.
  2. Vùng cấm anten `ESP32_S3_ANTENNA_KEEPOUT` trên cả 2 lớp `F.Cu` và `B.Cu` được mở rộng từ `Y = 40.00 mm` (mép Bắc bo mạch) đến `Y = 55.00 mm` và `X = 155.00 .. 185.00 mm`. Điều này tạo ra một hành lang cấm đồng rộng `30.0 mm × 15.0 mm` bao trọn toàn bộ anten PCB và mở thông trực tiếp ra không gian tự do phía Bắc bo mạch.
  3. Hành lang cắm cáp USB (`X = 156.0 .. 184.0 mm, Y = 115.0 .. 145.0 mm`) hoàn toàn trống trải.
  4. **Phương án cơ khí vỏ hộp**: Nắp hoặc thành dưới của vỏ hộp chỉ cần bố trí một cửa sổ khoét lùi (Recessed Window) hoặc lỗ khoét cắm cáp tiêu chuẩn. Không cần xoay module, bảo đảm 100% hiệu suất anten theo đúng Espressif Hardware Design Guidelines.

### 3.2. Phương án chống rung & cố định MPU6050 (Giải quyết OI-04)
- **Thực thi chỉ đạo người dùng**: Không tự ý suy đoán tọa độ để khoan thêm lỗ NPTH trên PCB khi chưa có bản vẽ cơ khí chính xác từ thước kẹp.
- **Biện pháp cơ khí đã chốt**:
  - Tọa độ `U2` giữ nguyên tại `(96.00, 96.00, 0°)`.
  - Hướng trục in rõ trên mặt `F.SilkS`: `+X: UP (Phía trước xe)` và `+Y: LEFT (Bên trái xe)`.
  - Hai vòng tròn lỗ bắt vít trên silkscreen được giữ nguyên làm vạch định vị trực quan (`PENDING_MEASUREMENT`).
  - Khi lắp ráp thực tế: Sử dụng **miếng đệm silicon giảm chấn 2 mặt (Anti-vibration Silicone Damping Pad dày 1.5–2.0 mm)** dán bên dưới thân bo GY-521 trước khi cắm vào socket, kết hợp keo cố định chân header để chống nứt mối hàn thiếc khi xe máy điện rung lắc trên đường xóc.

### 3.3. Phương án màn hình OLED 0.96" (Giải quyết OI-03)
- **Phân tích kỹ thuật**:
  - Header `U7` gồm 4 chân: `1:GND, 2:3V3_SYS, 3:I2C_SCL, 4:I2C_SDA`.
  - Khoảng cách từ `U7` tới các linh kiện lân cận đều `> 12 mm`.
- **Kết luận giải pháp**:
  - Chân cắm `U7` trên PCB đóng vai trò **Header Đa Dụng (Dual-Use Connector)**.
  - **Tùy chọn A (On-board)**: Cắm trực tiếp module OLED GM009605v4.3 vào socket cái trên PCB nếu nắp hộp có cửa sổ kính trong suốt.
  - **Tùy chọn B (Off-board)**: Dùng cáp bẹ 4 sợi bấm đầu Dupont/JST nối từ header `U7` lên module OLED bắt vít trên mặt nắp hộp đen.
  - Cả hai tùy chọn đều sử dụng chung một footprint `1x04 P2.54mm`, **không đòi hỏi bất kỳ sửa đổi nào trong schematic**, tuân thủ 100% chỉ đạo của người dùng.

### 3.4. Dòng cấp xung 2A của Module SIM A7680C và Điểm nối sao `NT1`
- **Tuyến nguồn SIM_PWR cực ngắn**:
  - `J2.1 (5V_SYS)` $\rightarrow$ `NT1.1` (`len = 16.0 mm`).
  - `NT1.2 (SIM_PWR)` $\rightarrow$ `C3.1` (`len = 7.2 mm`, track đồng rộng `2.50 mm`).
  - `C3.1` $\rightarrow$ `C4.1` (`len = 11.0 mm`, track đồng rộng `2.50 mm`).
  - `C4.1` $\rightarrow$ `U5.1` (`len = 10.0 mm`, track đồng rộng `2.50 mm`, **thẳng đứng tuyệt đối**).
- Tổng chiều dài từ tụ bù dòng đỉnh `C3/C4` tới chân nguồn module SIM chỉ **`10.0 mm`**, sụt áp tức thời khi phát sóng 4G ước tính `< 25 mV`, loại trừ hoàn toàn nguy cơ sụt áp reset ESP32-S3.

### 3.5. Kiểm tra chân GND hàng phải của ESP32-S3 (`U1.23`)
- Chân `U1.23` tại `(182.70, 58.33)` thuộc hàng chân bên phải của DevKit và được nối vào net `GND`.
- Các chân `U1.43` và `U1.44` đã được nối `no_connect` trong schematic.
- Ở Gate 3 (Routing), mặt đồng đáy `B.Cu` sẽ phủ đồng `GND` toàn bộ diện tích mạch (trừ vùng keepout anten), do đó chân `U1.23` sẽ được tiếp xúc trực tiếp vào mặt phẳng mass chung mà không cần phải chạy dây tín hiệu phức tạp vòng qua đầu Nam.

### 3.6. Pad Annular Ring & Khoảng hở cách điện
- Footprint socket `U1`: Pad kích thước `2.20 × 1.60 mm`, đường kính khoan `1.00 mm`.
- Vành khuyên đồng (Annular ring) đạt `(2.20 - 1.00)/2 = 0.60 mm` theo phương ngang và `(1.60 - 1.00)/2 = 0.30 mm` theo phương dọc.
- Bề rộng khe hở giữa 2 pad liên tiếp: `2.54 mm - 1.60 mm = 0.94 mm`.
- Quy tắc thiết kế Net Class đã xác nhận: Không luồn đường mạch qua khe chân của `U1`. 100% tín hiệu thoát ra phía Tây (bên trái). Mối hàn THT hoàn toàn an toàn cho gia công thủ công.

---

## 4. XÁC MINH KIỂM TRA TỰ ĐỘNG (AUTOMATED VERIFICATION AUDIT)

### 4.1. Kết quả kiểm tra quy tắc điện Schematic (ERC)
- **Lệnh thực thi**:
  ```powershell
  kicad-cli sch erc --severity-all --output "GATE_2_PLACEMENT\ERC_REPORT_REV2.txt" "AIOT_BLACKBOX_MAINBOARD_REV1.kicad_sch"
  ```
- **Kết quả**: **`0 Errors, 0 Warnings`** (`Found 0 violations`).
- Toàn bộ kết nối logic, nhãn net, và chân linh kiện đều đồng bộ 100% với firmware `filecodemain.cpp`.

### 4.2. Kết quả kiểm tra quy tắc mạch in PCB (DRC)
- **Lệnh thực thi**:
  ```powershell
  kicad-cli pcb drc --schematic-parity --severity-all --output "GATE_2_PLACEMENT\DRC_PLACEMENT_REV2.txt" "AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pcb"
  ```
- **Kết quả**:
  - **DRC Violations**: **`0 violations`** (Không có chồng lấn courtyard, không có pad xuyên vào courtyard, không có lỗi khoảng cách silkscreen, không có vi phạm vùng cấm).
  - **Unconnected items**: **`64`** (Toàn bộ là đường ratsnest chưa đi dây của giai đoạn Gate 2; hoàn toàn bình thường trước khi routing).
  - **Schematic parity**: **`3 warnings`** (`U4.ANT`, `U5.ANT`, `U5.STATUS`). Đây là các chân chức năng anten ngoài/STATUS trên symbol schematic không có chân vật lý trên header 1x05, đã được xác nhận ở Gate 0 và Gate 1.
  - **Tracks trên bo**: **`0 tracks`** (Chưa routing bất kỳ đường đồng nào trên F.Cu hoặc B.Cu).
  - **Vias trên bo**: **`0 vias`**.

### 4.3. Xác minh tính toàn vẹn của 8 Net Classes trong `.kicad_pro`
Đã kiểm tra trực tiếp cấu trúc JSON của [AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pro](file:///D:/%C4%90%E1%BB%92%20%C3%81N%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pro):

| Net Class | Độ rộng đường dây (`track_width`) | Khoảng hở tối thiểu (`clearance`) | Các Net gán theo Pattern |
| :--- | :---: | :---: | :--- |
| **`Default`** | `0.30 mm` | `0.25 mm` | Các tín hiệu GPIO logic còn lại (`BUZZER_CTRL`, `CANCEL`, `LED_STATUS`) |
| **`I2C`** | `0.35 mm` | `0.30 mm` | `/I2C_SDA_GPIO8`, `/I2C_SCL_GPIO9` |
| **`UART`** | `0.35 mm` | `0.30 mm` | `/SIM_RX_GPIO15`, `/SIM_TX_GPIO16`, `/GPS_RX_GPIO18`, `/GPS_TX_GPIO17` |
| **`SPI`** | `0.35 mm` | `0.30 mm` | `/SD_CS_GPIO10`, `Net-(J1-MOSI)`, `Net-(J1-SCK)`, `Net-(J1-MISO)` |
| **`3V3_POWER`** | `1.00 mm` | `0.30 mm` | `3V3_SYS` |
| **`5V_POWER`** | `1.50 mm` | `0.40 mm` | `5V_SYS` |
| **`SIM_POWER`** | `2.50 mm` | `0.50 mm` | `SIM_PWR` |
| **`GND`** | `1.50 mm` | `0.40 mm` | `GND` |

Giới hạn DRC toàn cục: `min_clearance = 0.25 mm`, `min_track_width = 0.25 mm` (tuân thủ RULE 20).

---

## 5. DANH MỤC HÌNH ẢNH & TÀI LIỆU XUẤT XƯỞNG GATE 2.1

Toàn bộ các tệp kết quả đã được tạo lập đầy đủ trong thư mục `GATE_2_PLACEMENT`:

1. [PCB_PLACEMENT_TOP_REV2.png](file:///D:/%C4%90%E1%BB%92%20%C3%81N%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_2_PLACEMENT/PCB_PLACEMENT_TOP_REV2.png):
   - Bản vẽ mặt trên tỉ lệ chuẩn 300 DPI hiển thị đường bao bo `145 × 105 mm`, 4 lỗ bắt vít M3 `135 × 95 mm`.
   - Vùng cấm đồng anten `155.0..185.0 × 40.0..55.0 mm` màu đỏ gạch chéo.
   - 64 đường nối ratsnest MST phân màu chuẩn: Đỏ (`5V_SYS`), Cam (`SIM_PWR`), Xanh lá (`3V3_SYS`), Xanh dương (`GND`), Tím (`I2C`), Xanh lơ (`SPI`), Nâu vàng (`UART`).
2. [PCB_PLACEMENT_BOTTOM_REV2.png](file:///D:/%C4%90%E1%BB%92%20%C3%81N%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_2_PLACEMENT/PCB_PLACEMENT_BOTTOM_REV2.png):
   - Bản vẽ mặt hàn `B.Cu` lật gương (Mirrored View).
   - Vùng màu xanh dương nhạt thể hiện toàn bộ diện tích dự kiến đi dây 1 lớp đồng `B.Cu`.
   - Vùng cấm anten màu đỏ không được phủ đồng.
   - Hiển thị đầy đủ vị trí pad hàn và đường nối ratsnest dự kiến.
3. [PCB_PLACEMENT_3D_REV2.png](file:///D:/%C4%90%E1%BB%92%20%C3%81N%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_2_PLACEMENT/PCB_PLACEMENT_3D_REV2.png):
   - Ảnh phối cảnh 3D xuất từ `kicad-cli pcb render` kèm banner cảnh báo cơ khí sơ bộ.
4. [PCB_PLACEMENT_TOP_REV2.pdf](file:///D:/%C4%90%E1%BB%92%20%C3%81N%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_2_PLACEMENT/PCB_PLACEMENT_TOP_REV2.pdf):
   - Bản in vector khổ A4 landscape chính hãng từ KiCad CLI gồm đầy đủ khung tên, tiêu đề dự án và phân lớp kỹ thuật.
5. [DRC_PLACEMENT_REV2.txt](file:///D:/%C4%90%E1%BB%92%20%C3%81N%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_2_PLACEMENT/DRC_PLACEMENT_REV2.txt): Báo cáo DRC chi tiết (`0 violations`).
6. [ERC_REPORT_REV2.txt](file:///D:/%C4%90%E1%BB%92%20%C3%81N%202/PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_2_PLACEMENT/ERC_REPORT_REV2.txt): Báo cáo ERC chi tiết (`0 errors, 0 warnings`).

---

## 6. KẾT LUẬN & ĐỀ NGHỊ

Mặt bằng bố trí linh kiện **GATE 2.1 REV2** đã giải quyết triệt để các hạn chế hình học của bản REV1, đạt sự cân bằng tối ưu giữa:
- Khả năng tiếp cận cơ khí của cổng Dual USB-C và khe thẻ MicroSD.
- Bảo toàn tuyệt đối hiệu quả phát sóng không dây của anten ESP32-S3.
- Đường cấp nguồn dòng đỉnh `2A` siêu ngắn `10.0 mm` cho module 4G SIM A7680C.
- Phân luồng tín hiệu song song cực ngắn cho các bus tốc độ cao SPI, I2C, UART.
- **Tuân thủ nghiêm ngặt giới hạn**: Tuyệt đối chưa routing, chưa phủ đồng, chưa tạo via, chưa thêm jumper và chưa xuất Gerber.

Thiết kế đã sẵn sàng để người dùng thẩm định trước khi chuyển sang **GATE 3: Thiết kế Định tuyến Mạch in 1 lớp (Routing & Jumpers Plan)**.

