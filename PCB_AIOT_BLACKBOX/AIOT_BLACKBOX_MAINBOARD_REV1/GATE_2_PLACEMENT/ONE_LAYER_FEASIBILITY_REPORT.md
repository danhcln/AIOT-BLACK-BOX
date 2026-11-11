# BÁO CÁO ĐÁNH GIÁ TÍNH KHẢ THI ĐI DÂY PCB 1 LỚP (`ONE_LAYER_FEASIBILITY_REPORT.md`)

> [!WARNING]
> **ĐÍNH CHÍNH:** (1) Mục 2.4 phía dưới nói hoán vị SCK/MOSI của `J1` "đi vòng, không cần jumper" là **không chứng minh được**: hai hàng chân đối diện có thứ tự `CS,SCK,MOSI,MISO` ↔ `CS,MOSI,SCK,MISO` (1 nghịch thế) nên trên 1 lớp **bắt buộc 1 điểm giao SPI** (1 jumper tín hiệu) trừ khi đổi gán chân (cấm). (2) Tương tự, bus I2C đảo thứ tự làn (SDA ở trên, SCL ở dưới tại `U1`; module có SCL trái, SDA phải) → dự kiến ≥ 1 giao cắt. (3) Việc "khe giữa pad `U1` không luồn được dây" chỉ đúng với dây 0.5 mm; với `Default` 0.30 mm/0.25 mm clearance của RULE 09 thì khe 0.94 mm giữa pad 1.6 mm **luồn được 1 dây**. (4) Kết luận "KHẢ THI CAO" được thay bằng **KHẢ THI CÓ ĐIỀU KIỆN** (mục 3 mới bên dưới).

- **Dự án**: THIẾT KẾ HỘP ĐEN AIoT THÔNG MINH PHÂN TÍCH VÀ GHI LẠI SỰ CỐ XE MÁY ĐIỆN
- **Project KiCad**: `D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1`
- **Giai đoạn**: **GATE 2 – Kiểm tra khả thi đi dây 1 lớp (`B.Cu`) trước khi sang Gate 3 (Routing)**

---

## 1. PHÂN TÍCH TÔ-PÔ BỐ TRÍ LINH KIỆN & RATSNEST (AIRWIRES)

### 1.1. Tối ưu hóa Tô-pô theo thứ tự chân `ESP32-S3` (`U1`)
- Trên socket 44 chân của `U1 (ESP32-S3-DevKitC-1 N16R8)`, toàn bộ **17 chân có kết nối mạch** đều nằm trên **Hàng Chân Bên Trái (`Pads 5..19, 21, 22`, tại `X = 156.30 mm`)** theo đúng trình tự từ trên xuống dưới (`Y = 61.99 mm` đến `Y = 105.17 mm`):
  1. **Dải 1 (`Y = 61.99 .. 67.07 mm`)**:
     - `Pad 5 (GPIO5 - Buzzer)` $\rightarrow$ đối diện trực tiếp `R5` (`(148.0, 60.5)`), `Q1` (`(136.0, 60.5)`), `BZ1` (`(136.0, 48.0)`).
     - `Pad 6 (GPIO6 - CANCEL)` $\rightarrow$ đi ngang sang cụm `R3/C2/SW1` (`X = 114.0, Y = 46.5..58.0`).
     - `Pad 7 (GPIO7 - LED)` $\rightarrow$ đi ngang sang `R4` (`(121.0, 64.0)`) và `D1` (`(110.0, 64.0)`).
  2. **Dải 2 (`Y = 69.61 .. 72.15 mm`)**:
     - `Pad 8 (GPIO15 - SIM_RX)` & `Pad 9 (GPIO16 - SIM_TX)` $\rightarrow$ đi ngang sang `U5 (SIM A7680C)` tại `(100.0, 71.0)`.
  3. **Dải 3 (`Y = 74.69 .. 77.23 mm`)**:
     - `Pad 10 (GPIO17 - GPS_TX)` & `Pad 11 (GPIO18 - GPS_RX)` $\rightarrow$ đi ngang sang `U4 (GPS NEO-M8N)` tại `(122.0, 77.0)`.
  4. **Dải 4 (`Y = 79.77 .. 87.39 mm`)**:
     - `Pad 12 (GPIO8 - I2C_SDA)` & `Pad 15 (GPIO9 - I2C_SCL)` $\rightarrow$ đối diện trực tiếp `R_PU1 (4.7k)` tại `(139.0, 81.5)` và `R_PU2 (4.7k)` tại `(139.0, 87.5)`, sau đó đi xuống cụm I2C `U2 (MPU6050)` tại `(96.0, 96.0)`, `U7 (OLED)` tại `(102.0, 116.5)` và `U3 (DS3231)` tại `(68.0, 100.0)`.
  5. **Dải 5 (`Y = 89.93 .. 97.55 mm`)**:
     - `Pad 16 (GPIO10 - SD_CS)`, `Pad 17 (GPIO11 - SD_MOSI)`, `Pad 18 (GPIO12 - SD_SCK)`, `Pad 19 (GPIO13 - SD_MISO)` $\rightarrow$ đối diện trực tiếp `J1 (MicroSD Adapter)` tại `(137.0, 101.0)`.
  6. **Dải 6 (`Y = 102.63 .. 105.17 mm`)**:
     - `Pad 21 (5V_SYS)` & `Pad 22 (GND)` $\rightarrow$ nằm ngay cạnh `J1 Pad 5 (5V_SYS)` và `J1 Pad 6 (GND)` (`len = 13.6 .. 15.6 mm`).

### 1.2. Đánh giá độ dài các đường tín hiệu và nguồn chính từ Ratsnest
| Nhóm mạch / Bus | Đường kết nối chính | Chiều dài Airwire (`mm`) | Đánh giá cho PCB 1 lớp (`B.Cu`) |
| :--- | :--- | :---: | :--- |
| **Nhánh dòng đỉnh `SIM_PWR` (`2.0 mm`)** | `J2.1 -> TP1 -> NT1 -> C3 -> C4 -> U5.1` | `7.5 – 15.1 mm` | **Xuất sắc**: Đường nguồn ngắn, đi hoàn toàn ở góc trên-trái, không cắt qua bất kỳ đường tín hiệu nào của MCU. |
| **Nhánh hạ áp `3V3_SYS` (`1.0 mm`)** | `U6.3 -> C1.1 -> TP2.1 -> U2 / U3 / U7 / U4 / R_PU` | `7.4 – 23.9 mm` | **Rất tốt**: Nằm ở nửa trái/giữa bo, phân phối trực tiếp cho cụm cảm biến 3.3V. |
| **Bus SPI (`MicroSD`) (`0.5 mm`)** | `U1.Pads 16..19 <-> J1.Pads 1..4` | `18.4 – 27.9 mm` | **Rất tốt**: Ngắn, nằm gọn trong hành lang `X = 130..156 mm, Y = 89..102 mm`. |
| **Bus I2C (`MPU6050, DS3231, OLED`)** | `U1.12/15 -> R_PU1/2 -> U2.3/4 -> U7.3/4 & U3.3/4` | `12.2 – 25.8 mm` | **Rất tốt**: Các chân `Pad 3 = SCL` và `Pad 4 = SDA` trên `U2`, `U3`, `U7` có cùng thứ tự trái-sang-phải (`3:SCL`, `4:SDA`), nên 2 đường `SCL` và `SDA` chạy song song **không bao giờ tự cắt nhau**! |
| **UART GPS (`NEO-M8N`)** | `U1.10/11 <-> U4.4/3` | `31.8 – 34.3 mm` | **Tốt**: Đi ngang trực tiếp ở cao độ `Y = 74..77 mm`. |
| **UART SIM (`A7680C`)** | `U1.8/9 <-> U5.4/3` | `53.8 – 56.3 mm` | **Tốt**: Đi ngang trực tiếp ở cao độ `Y = 69..72 mm`. |
| **Mạch Buzzer (`GPIO5`)** | `U1.5 -> R5.1 -> R5.2 -> Q1.3 -> Q1.2 -> BZ1.2` | `9.0 – 11.3 mm` | **Xuất sắc**: Ngắn gọn, nằm trên đỉnh hành lang, sử dụng lợi thế bước chân `10.16 mm` của `R5` và `R6`. |

---

## 2. KIỂM TRA CÁC ĐIỂM GIAO CẮT TIỀM NĂNG & KHẢ NĂNG VƯỢT CẦU TỰ NHIÊN (NATURAL THT COMPONENT SPANS)

Trên PCB 1 lớp đồng (`B.Cu`, không dùng via, không đi mạch trên `F.Cu`), một ưu điểm lớn của linh kiện xuyên lỗ (Through-Hole) là **khoảng trống dưới gầm điện trở `R_Axial_DIN0207_P10.16mm` (`pitch = 10.16 mm`, khe trống giữa 2 pad rộng `7.96 mm`)** cho phép đi thoải mái **3 đến 4 đường đồng `B.Cu`** xuyên qua dưới bụng điện trở mà không cần thêm bất kỳ cầu nhảy `JW` nào!

Cụ thể, trong bố cục Gate 2 hiện tại:
1. **Dưới gầm `R_PU1 (4.7k)` và `R_PU2 (4.7k)` (`X = 133.92 .. 144.08 mm`)**:
   - Chân trái (`Pad 1`) của `R_PU1` và `R_PU2` nối chung `3V3_SYS`, chân phải (`Pad 2`) nối `I2C_SDA` và `I2C_SCL` sang `U1.Pad 12` và `U1.Pad 15`.
   - Khoảng trống `7.96 mm` giữa hai chân của `R_PU1` và `R_PU2` tạo thành **hành lang tự nhiên** cho đường `3V3_SYS` hoặc các đường tín hiệu đi dọc mà không bị chặn.
2. **Dưới gầm `R5 (1k)` (`Y = 55.42 .. 65.58 mm`) và `R6 (10k)` (`X = 130.92 .. 141.08 mm`)**:
   - Cho phép đường tín hiệu `CANCEL (GPIO6)` và `LED_STATUS (GPIO7)` từ `U1.Pad 6, 7` đi thẳng sang trái tới `R3/C2/SW1` và `R4/D1` hoàn toàn dưới gầm `R5` mà **không có bất kỳ giao cắt nào với mạch Buzzer (`GPIO5`)**!
3. **Thứ tự chân đồng bộ trên `U2 (MPU6050)`, `U3 (DS3231)` và `U7 (OLED)`**:
   - Cả 3 module I2C đều có **`Pad 3 = SCL` bên trái** và **`Pad 4 = SDA` bên phải**!
   - Nhờ đặt cả 3 module cùng góc xoay `0.0°`, hai đường bus `I2C_SCL` và `I2C_SDA` đi song song tuyệt đối giữa `U2`, `U3` và `U7` mà **0 lần cắt nhau**.
4. **Hoán vị thứ tự chân SPI giữa `U1` và `J1 (MicroSD)`**:
   - Trên `U1`: `Pad 16 = CS (GPIO10)`, `Pad 17 = MOSI (GPIO11)`, `Pad 18 = SCK (GPIO12)`, `Pad 19 = MISO (GPIO13)`.
   - Trên `J1`: `Pad 1 = CS`, `Pad 2 = SCK`, `Pad 3 = MOSI`, `Pad 4 = MISO`.
   - Nhận xét: Chỉ có cặp `MOSI` (`Pad 17`) và `SCK` (`Pad 18`) đảo vị trí cho nhau. Trên 1 lớp `B.Cu`, đường `MOSI` (`U1.17 -> J1.3`) có thể đi vòng nhẹ qua phía ngoài `J1.Pad 1 (CS)` và `J1.Pad 2 (SCK)` (hoặc đi dưới gầm 1 cầu nhảy `0Ω` nếu muốn đường thẳng tuyệt đối). Do có hành lang rộng `18 mm` giữa `J1` và `U1`, đường vòng quanh đầu `J1.Pad 1` hoàn toàn khả thi mà **không cần bất kỳ jumper nào**!
5. **Điểm giao cắt duy nhất có thể cần 1–2 cầu nhảy `JW` (`0Ω` / dây jumper chuẩn `P7.62mm`) ở Gate 3**:
   - Đường nguồn `5V_SYS` từ vùng nguồn bên trái (`J2 / NT1`) đi sang phải để cấp cho `BZ1.Pad 1`, `J1.Pad 5` và `U1.Pad 21`:
     - **Phương án A (0 Jumper - Đi vòng mép)**: Đường `5V_SYS` (`1.5 mm`) đi dọc theo hành lang mép Bắc (`Y = 42.5 mm`, phía trên `SW1` và `BZ1`) hoặc hành lang mép Nam (`Y = 142.0 mm`, phía dưới `U3`, `U7`, `J1`) tới thẳng `J1.Pad 5` và `U1.Pad 21`, mientras `GND` phủ đồng toàn mặt `B.Cu` bao quanh!
     - **Phương án B (Dùng 1–2 cầu nhảy `JW` chuẩn `WireJumper_P7.62mm_SingleLayer`)**: Nếu muốn đi đường `5V_SYS` và `GND` ngắn nhất băng ngang qua giữa bản mạch, sử dụng tối đa `1–2` linh kiện `JW` (`0Ω` resistor / wire jumper `7.62 mm`) có sẵn trong thư viện `AIOT_Blackbox_Local`.

---

## 3. KẾT LUẬN ĐÁNH GIÁ KHẢ THI 1 LỚP (ĐÃ SỬA SAU KIỂM TRA LẠI)

**Kết luận: KHẢ THI CÓ ĐIỀU KIỆN (CONDITIONAL).** Chưa routing, nên mọi số liệu là ước lượng.

### 3.1 Căn cứ định lượng (từ `audit_gate2b.py`, chỉ đọc PCB)
- Tracks = 0, vias = 0, zones = 1 (keepout anten, `F.Cu`+`B.Cu`). Không có đồng `F.Cu`.
- Ratsnest thẳng (MST mỗi net, bỏ GND): 45 đoạn, 37 điểm cắt giữa các net khác nhau. Trong đó chỉ **3 giao cắt tín hiệu–tín hiệu** (SCL×SDA ×2, MOSI×SCK ×1); **34 giao cắt tín hiệu/nguồn × nguồn** là hệ quả của việc MST kéo thẳng các net nguồn qua giữa bo, **không phải cách sẽ đi dây** (nguồn sẽ được đi thành trục riêng). Đây chỉ là chỉ báo thô, không phải số jumper.
- Giao cắt chứng minh được bằng thứ tự chân: **SPI 1** (SCK×MOSI), **I2C ≥ 1** (đảo làn SDA/SCL ở phía `U1`). UART SIM/GPS có thể 0 giao cắt nếu cả hai chân cùng thoát về phía Nam của hàng chân (đã kiểm tra thứ tự).
- **Ước lượng jumper tín hiệu: 2–6 (dự kiến 3–4)**, dưới ngưỡng < 8 của RULE 11, nhưng **chưa được xác nhận** cho đến Gate 3.
- **Không được dùng jumper nhỏ cho `5V_SYS`/`SIM_PWR`**: các trục nguồn phải là đồng liền; jumper tín hiệu sẽ phải bắc qua trục nguồn.

### 3.2 Điểm rủi ro đã biết
1. **`U1.23` (GND, hàng phải)** vẫn nằm trong netlist GND: cần nhánh GND vòng qua đầu Nam `U1` (x ≈ 183–187 mm) hoặc cho phép đánh dấu NC trong schematic (chỉ khi người dùng duyệt). Các chân `U1.43/44` GND đã để NC trong schematic.
2. **GND một lớp**: các pad GND ở cuối hàng header (vd. `U5.5`, `U6.2/4`) có nguy cơ bị bao bởi tín hiệu và thành "túi" GND; có thể cần đổ đồng + 1 jumper GND (dây ≥ 22 AWG, RULE 11).
3. **Đường hồi dòng SIM**: `U5.5` GND phải về âm `C3` bằng đường riêng (RULE 10.3). `C3`/`C4` GND hiện chỉ nối đến `TP4/J2`; cần kiểm tra ở Gate 4.
4. **Pad `U1` 1.6 mm, drill 1.0 mm → annular ring 0.30 mm < 0.40 mm** (RULE 20). Tăng pad lên 1.8 mm đạt chuẩn nhưng thu khe giữa pad còn 0.74 mm (không còn luồn được dây). Cần người dùng quyết định.
5. Ba `net_conflict` của DRC-parity (`U4.ANT`, `U5.ANT`, `U5.STATUS`) là chân anten/STATUS của symbol không có pad trên header 1x05; không phải lỗi nối điện.

### 3.3 Điều kiện để sang Gate 3
Xem `PCB_OPEN_ISSUES.md`: chốt kiểu lắp module (phẳng/đứng), vị trí OLED, cố định MPU6050, anten GPS/SIM, kích thước hộp, pad `U1`, test point và tụ theo RULE 06/08/19.
