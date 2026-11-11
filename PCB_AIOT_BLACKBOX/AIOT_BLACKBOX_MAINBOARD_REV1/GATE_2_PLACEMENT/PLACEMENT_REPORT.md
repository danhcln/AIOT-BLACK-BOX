# BÁO CÁO THIẾT KẾ BỐ TRÍ LINH KIỆN PCB 1 LỚP (GATE 2 PLACEMENT REPORT)

> [!WARNING]
> **ĐÍNH CHÍNH SAU KIỂM TRA LẠI (phiên tiếp quản).** Báo cáo này do phiên trước viết khi chưa đối chiếu file thực tế. Các câu sau KHÔNG còn đúng và được thay bằng nội dung trong [GATE_2_SUMMARY.md](GATE_2_SUMMARY.md) và [PCB_OPEN_ISSUES.md](PCB_OPEN_ISSUES.md):
>
> 1. **"Net Class đã cấu hình trong `.kicad_pro`" – SAI.** `pcbnew.SaveBoard()` đã ghi đè `.kicad_pro` về mặc định và làm mất Net Class. Đã khôi phục 8 Net Class theo RULE 09 (xem mục 5 bên dưới).
> 2. **"`U2` đặt tại tâm cơ học của PCB" – KHÔNG chính xác.** Tâm bo là (122.5, 92.5); `U2` ở (96.0, 96.0), lệch 26.5 mm về phía Tây và **chưa có lỗ vít PCB nào giữ `U2`** (RULE 14 → điều kiện mở).
> 3. **"Không có đường mạch nào cần vòng qua phía phải của `U1`" – CHƯA ĐÚNG.** Chân `U1.23` (hàng phải, GND) đang nối vào net `GND` trong netlist nên vẫn cần một nhánh GND vòng qua đầu Nam của `U1` (xem Open Issues).
> 4. **"Cổng USB-C hướng thẳng ra mép Nam" – KHÔNG chính xác.** Đầu USB của DevKit kết thúc ở y ≈ 111 mm, cách mép Nam bo (y = 145) khoảng 34 mm; cáp USB không ở sát mép bo (RULE 12.3 / 16.4 → điều kiện mở).
> 5. **Các khung viền thân module `U2/U3/J1` (và tên "MPU6050 21.2×16.2", "DS3231 38×22", "MicroSD 24×42") là kích thước GIẢ ĐỊNH lắp nằm phẳng**, chỉ kích thước OLED 24.7×27 mm được xác minh từ ảnh. Ảnh thực tế cho thấy các module này đang hàn header 90° (cắm đứng), nên kiểu lắp (nằm phẳng với header thẳng / cắm đứng) **chưa được chốt**.
> 6. Mục "KHÔNG có chồng lấn thân vật lý của 5 module" chỉ đúng ở mức courtyard của footprint header và khung giả định ở trên, không phải thân module đã đo.
> 7. Tổng linh kiện: **28 linh kiện schematic + 4 lỗ vít = 32 footprint** (đúng); `J3` không còn, thay bằng `NT1` (BOM đã được đồng bộ).

---


- **Dự án**: THIẾT KẾ HỘP ĐEN AIoT THÔNG MINH PHÂN TÍCH VÀ GHI LẠI SỰ CỐ XE MÁY ĐIỆN
- **Project KiCad**: `D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1`
- **File PCB chính thức**:
  - `D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1\AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pcb`
  - `D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1\GATE_2_PLACEMENT\AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pcb`
- **Giai đoạn**: **GATE 2 – Thiết kế Placement PCB 1 lớp (`B.Cu`)** (Chưa routing, chưa xuất Gerber).
- **Trạng thái kiểm tra ERC / DRC Placement**:
  - **ERC Schematic**: `0 Errors, 0 Warnings` (`Found 0 violations`)
  - **DRC Placement (`kicad-cli pcb drc`)**: **`0 DRC placement violations`** (`0 courtyards_overlap`, `0 items_not_allowed`, `0 npth_inside_courtyard`, `0 silk_edge_clearance`, `0 silk_overlap`, `0 silk_over_copper`). Chỉ còn `64 unconnected_items` (ratsnest chưa đi dây vì đang ở Gate 2) và `3 net_conflict` của chân anten/PWRKEY nội bộ trên module breakout (`U4.ANT`, `U5.PWRKEY`, `U5.ANT`).

---

## 1. XỬ LÝ ĐIỂM NỐI SAO `5V_SYS → SIM_PWR` TRƯỚC KHI PLACEMENT

### 1.1. Phân tích vấn đề của `J3` trước đây
- Ở cuối Gate 1.5, nhánh tách nguồn `5V_SYS → SIM_PWR` tạm thời sử dụng linh kiện `J3` (`PinHeader_1x02_P2.54mm_SingleLayer`).
- Nhược điểm kỹ thuật khi đưa vào PCB thực tế:
  1. `PinHeader_1x02` là 2 chân rời rạc, bản thân footprint không có đường đồng nối liền giữa Pad 1 và Pad 2. Nếu quên cắm cầu nối hoặc cầu jumper `2.54 mm` tiếp xúc kém, nhánh `SIM_PWR` sẽ bị hở mạch hoặc sụt áp khi module SIM A7680C phát xung dòng đỉnh `1.5 A – 2.0 A`.
  2. Luật dự án (`RULE 5` & `HARDWARE_DECISIONS_LOCKED.md`) yêu cầu `SIM_PWR` được cấp từ nguồn ngoài `5V/3A` qua **điểm nối sao (Star-Point)** ngay tại đầu vào nguồn `J2`, nhưng vẫn giữ nguyên 2 tên net riêng biệt (`5V_SYS` và `SIM_PWR`) để kiểm soát độ rộng đường mạch (`POWER_5V_MAIN = 1.5 mm`, `POWER_SIM_PEAK = 2.0 mm`) và tách đường đi dây dòng đỉnh khỏi nhánh nuôi logic `ESP32-S3`.

### 1.2. Giải pháp kỹ thuật đã áp dụng (`NT1 - STAR_5V_TO_SIM_PWR`)
- Thay thế `J3` bằng linh kiện **Star-Point NetTie chuyên dụng của KiCad 10**:
  - **Reference**: `NT1` (`Value: STAR_5V_TO_SIM_PWR`)
  - **Symbol**: `Presentation:NetTie_2_StarPoint`
  - **Footprint**: `AIOT_Blackbox_Local:NetTie_2_StarPoint_BCu_Width2.5mm`
- **Cấu trúc vật lý của `NT1` trên PCB 1 lớp (`B.Cu`)**:
  - Sử dụng thuộc tính chuẩn KiCad 10 `(net_tie_pad_groups "1, 2")` kết hợp với đa giác đồng đặc `(fp_poly ... (layer "B.Cu"))` **bề rộng `2.50 mm`** nối trực tiếp giữa `Pad 1 (5V_SYS)` và `Pad 2 (SIM_PWR)`.
  - Đồng thời 2 pad `1` và `2` vẫn là pad xuyên lỗ THT (`Drill 1.0 mm`, `Pad 2.2 × 2.5 mm`), cho phép đắp thêm thiếc hoặc hàn bồi dây đồng trần nếu muốn gia cường khả năng chịu dòng trên PCB 1 lớp.
  - Kết quả:
    - Mạch liên thông điện 100% bằng đồng `B.Cu` rộng `2.50 mm` ngay từ khi chế tạo PCB (không sợ quên cắm jumper, không có điện trở tiếp xúc).
    - KiCad ERC đạt `0 Errors, 0 Warnings` và KiCad PCB giữ nguyên 2 net độc lập `5V_SYS` và `SIM_PWR` với 2 Net Class riêng biệt.

---

## 2. KÍCH THƯỚC PCB & HỆ LỖ BẮT VÍT CƠ KHÍ (`PROVISIONAL`)

| Thông số cơ khí | Giá trị chọn | Tọa độ trên bản vẽ (`mm`) | Trạng thái | Lý do kỹ thuật |
| :--- | :--- | :--- | :--- | :--- |
| **Chiều rộng PCB (`X`)** | **`145.0 mm`** | `X = 50.00 .. 195.00 mm` | `PROVISIONAL` | Đủ không gian xếp ngang 3 cụm: Cụm Nguồn/RTC (`X=57..79`), Cụm Trung tâm IMU/OLED/SIM/GPS (`X=85..128`), Cụm MicroSD (`X=125..149`) và Cụm ESP32-S3 (`X=154.7..183.3`) mà không chồng lấn thân module. |
| **Chiều cao PCB (`Y`)** | **`105.0 mm`** | `Y = 40.00 .. 145.00 mm` | `PROVISIONAL` | Đủ chiều dọc cho `ESP32-S3` (`66.0 mm`) + hành lang cắm cáp Dual USB-C ở mép dưới (`35.5 mm`), đồng thời chứa gọn thân `DS3231` (`38.0 mm`) và `MicroSD` (`42.0 mm`) mà không cần xếp chồng 2 tầng. |
| **Lỗ bắt vít `H1` (Top-Left)** | `M3 NPTH` (`Ø3.2 mm`) | `(55.00, 45.00)` | `PROVISIONAL` | Cách mép trái và mép trên `5.0 mm`, courtyard `Ø6.4 mm` hoàn toàn tách biệt khỏi linh kiện. |
| **Lỗ bắt vít `H2` (Top-Right)** | `M3 NPTH` (`Ø3.2 mm`) | `(190.00, 45.00)` | `PROVISIONAL` | Cách mép phải và mép trên `5.0 mm`, nằm ngoài vùng cấm anten `ESP32-S3` (`X <= 183.5 mm`). |
| **Lỗ bắt vít `H3` (Bottom-Left)** | `M3 NPTH` (`Ø3.2 mm`) | `(55.00, 140.00)` | `PROVISIONAL` | Cách mép trái và mép dưới `5.0 mm`, cách thân module `DS3231` `> 3.5 mm`. |
| **Lỗ bắt vít `H4` (Bottom-Right)** | `M3 NPTH` (`Ø3.2 mm`) | `(190.00, 140.00)` | `PROVISIONAL` | Cách mép phải và mép dưới `5.0 mm`. Tâm 4 lỗ tạo hình chữ nhật chuẩn **`135.0 mm × 95.0 mm`**. |

---

## 3. PHÂN VÙNG CHỨC NĂNG TRÊN PCB (FUNCTIONAL ZONING)

Bố cục mặt bằng PCB được chia thành **7 vùng chức năng rõ ràng**, sắp xếp theo luồng công suất và theo đúng thứ tự hàng chân trái (`Pads 5..22`) của `ESP32-S3` để tối ưu tuyệt đối cho **PCB 1 lớp (`B.Cu`)**:

1. **Vùng Phải (`X = 154.5 .. 183.5 mm, Y = 40.5 .. 109.5 mm`) — Khối Trung tâm `U1` (`ESP32-S3-DevKitC-1 N16R8`)**:
   - **Phát hiện topo quan trọng nhất cho PCB 1 lớp**: Trên footprint `ESP32-S3` 44 chân, **100% các chân tín hiệu đang sử dụng (`Pads 5..19`) và chân nguồn (`Pad 21 = 5V_SYS`, `Pad 22 = GND`) đều nằm ở Hàng Chân Bên Trái (`Pads 1..22`, tại `X = 156.30 mm`)**. Hàng chân bên phải (`Pads 23..44`, tại `X = 181.70 mm`) hoàn toàn không có tín hiệu nào (`Pads 24..44` đều là `NC`).
   - Do khoảng cách giữa 2 pad liên tiếp (`2.54 mm - 1.60 mm = 0.94 mm`) nhỏ hơn bề rộng tối thiểu của 1 đường mạch `0.50 mm` + `2 × 0.35 mm` clearance (`1.20 mm`), **không một đường đồng nào được phép luồn qua khe giữa các chân của `ESP32-S3`**.
   - Việc đặt `U1` ở phía **Bên Phải PCB** (`(169.00, 78.50)`, góc `0°`) giúp toàn bộ 100% module ngoại vi nằm ở phía **Bên Trái của `U1`**, kết nối trực tiếp vào hàng chân trái `Pads 5..22` mà **không cần bất kỳ đường mạch nào vòng qua phía phải của `U1`**.
   - **Anten PCB của `U1`** nằm sát mép Bắc (`Y = 40.50 .. 49.50 mm`) với vùng cấm đồng `ESP32_S3_ANTENNA_KEEPOUT` (`X = 154.5 .. 183.5 mm, Y = 40.0 .. 50.0 mm`) trên cả `F.Cu` và `B.Cu`.
   - **2 cổng USB-C (`USB` & `UART`)** hướng thẳng về mép Nam (`Y = 109.5 .. 145.0 mm`), hoàn toàn trống trải để cắm cáp nạp code/debug.

2. **Vùng 1 (Góc Trên – Trái, `X = 56 .. 106 mm, Y = 48 .. 74 mm`) — Nguồn vào `5V/3A` & Nhánh Dòng Đỉnh `SIM_PWR`**:
   - Domino nguồn `J2` (`LX-2BUPS 5V_3A`) đặt sát mép Tây tại `(60.00, 62.00, 90°)` để dây nguồn từ ngoài đi vào ngắn nhất.
   - Ngay sát `J2` là `TP1 (TP_5V)` tại `(69.00, 58.00)`, `TP4 (TP_GND)` tại `(69.00, 66.00)` và điểm tách sao `NT1` tại `(78.00, 58.00)`.
   - Từ `NT1 Pad 2 (SIM_PWR)`, đường nguồn đi thẳng sang phải qua tụ hóa lọc nguồn chính **`C3 (470µF Low-ESR)`** tại `(89.00, 56.00)`, tụ gốm cao tần **`C4 (100nF)`** tại `(99.00, 56.00)` và `TP3 (TP_SIM_PWR)` tại `(99.00, 49.00)`, rồi cấp trực tiếp xuống chân `Pad 1 (VCC)` của connector `U5 (SIM A7680C J6)` tại `(100.00, 71.00)`.
   - Khoảng cách từ `C4` đến `U5.Pad 1` chỉ **`15.1 mm`** và từ `C3` đến `C4` chỉ **`10.0 mm`**, đảm bảo dòng xung `2A` của SIM 4G được cấp tức thời ngay tại chân module, không gây sụt áp lên `ESP32-S3`.
   - Hai chân UART của `U5` (`Pad 3 = RXD`, `Pad 4 = TXD` tại `Y = 71.00 mm`) nằm ngang hàng hoàn hảo với `U1 Pad 8 (GPIO15, Y = 69.61 mm)` và `U1 Pad 9 (GPIO16, Y = 72.15 mm)`.

3. **Vùng 2 (Giữa – Trái, `X = 58 .. 85 mm, Y = 74 .. 86 mm`) — Nhánh Nguồn Hạ Áp `3V3_SYS`**:
   - Module hạ áp `U6 (REG_3V3_MODULE 1x04)` đặt tại `(66.00, 82.00)` ngay dưới `J2` (khoảng cách `J2.1 -> U6.1` chỉ `17.6 mm`).
   - Đầu ra `3V3_SYS` (`U6.Pad 3`) đi sang phải qua tụ lọc `C1 (100nF)` tại `(80.00, 82.00)` và `TP2 (TP_3V3)` tại `(80.00, 75.00)`, từ đó phân phối trực tiếp đến cụm cảm biến `3.3V` (`U2 MPU6050`, `U3 DS3231`, `U7 OLED`, `U4 GPS` và `R_PU1/R_PU2`).

4. **Vùng 3 (Giữa – Trên, `X = 108 .. 151 mm, Y = 45 .. 70 mm`) — Khối Giao Diện Cảnh Báo (`BZ1`, `Q1`, `SW1`, `D1`)**:
   - Đặt ở dải trên cùng để thẳng hàng ngang với các chân điều khiển UI trên `U1`:
     - `U1 Pad 5 (GPIO5 - Buzzer)` tại `Y = 61.99 mm` $\leftrightarrow$ `R5 (1k)` tại `(148.00, 60.50, 90°)` (`len = 9.0 mm`) $\rightarrow$ `Q1 (2SC1815)` tại `(136.00, 60.50)` & `R6 (10k)` tại `(136.00, 68.00)` $\rightarrow$ `BZ1 (Buzzer 5V)` tại `(136.00, 48.00)`.
     - `U1 Pad 6 (GPIO6 - CANCEL)` tại `Y = 64.53 mm` $\leftrightarrow$ cụm nút nhấn `SW1` tại mép Bắc `(114.00, 46.50)`, trở kéo lên `R3 (10k)` tại `(114.00, 52.50)` và tụ chống dội `C2 (100nF)` tại `(114.00, 58.00)`.
     - `U1 Pad 7 (GPIO7 - LED)` tại `Y = 67.07 mm` $\leftrightarrow$ trở hạn dòng `R4 (330R)` tại `(121.00, 64.00)` và `D1 (LED 5mm)` tại `(110.00, 64.00)`.
   - **Cách ly rung động cơ học**: `BZ1` (`(136.00, 48.00)`) cách tâm cảm biến gia tốc `U2 (MPU6050)` (`(96.00, 96.00)`) một khoảng **`62.5 mm`** (`> 60 mm`), tránh hoàn toàn nhiễu rung âm học từ còi báo động truyền sang IMU.

5. **Vùng 4 (Tâm Cơ Học PCB & Giữa Bản Mạch, `X = 85 .. 145 mm, Y = 74 .. 110 mm`) — Cảm Biến `U2 (MPU6050)`, `U4 (GPS NEO-M8N)` & Pull-up `I2C`**:
   - **`U2 (MPU6050 GY-521)`** đặt tại **vị trí trung tâm cơ học của PCB**: `(96.00, 96.00, 0°)`.
     - Hướng trục cảm biến được in rõ trên `F.SilkS`: **`+X: UP (Hướng mũi xe / Phía Bắc PCB)`**, **`+Y: LEFT (Hướng bên trái xe / Phía Tây PCB)`**, cùng 2 lỗ định vị cơ khí `Ø3.0 mm` của bo `GY-521` để cố định cứng vào khung hộp đen.
   - **`U4 (GPS NEO-M8N V2149 1x05)`** đặt tại `(122.00, 77.00, 0°)`:
     - Chân `Pad 3 (TXD)` và `Pad 4 (RXD)` tại `Y = 77.00 mm` nằm thẳng hàng ngang với `U1 Pad 10 (GPIO17, Y = 74.69 mm)` và `U1 Pad 11 (GPIO18, Y = 77.23 mm)` (`len = 31.8 .. 34.3 mm`).
   - **Cặp điện trở kéo lên I2C `R_PU1 (4.7k SDA)` & `R_PU2 (4.7k SCL)`**:
     - Đặt tại `(139.00, 81.50)` và `(139.00, 87.50)` ngay sát bên trái `U1 Pad 12 (GPIO8 - SDA, Y = 79.77 mm)` và `U1 Pad 15 (GPIO9 - SCL, Y = 87.39 mm)` (`len = 12.2 .. 12.3 mm`).

6. **Vùng 5 & Vùng 6 (Góc Dưới – Trái & Giữa – Dưới, `X = 57 .. 114.5 mm, Y = 98 .. 141.5 mm`) — Khối I2C `U3 (DS3231)` & `U7 (OLED 0.96")`**:
   - **`U3 (RTC DS3231 ZS-042 1x06)`** đặt tại `(68.00, 100.00, 0°)` ở góc dưới bên trái. Toàn bộ thân module `22.0 × 38.0 mm` (`X = 57..79, Y = 98.2..136.2 mm`) và khay pin cúc áo `CR2032` (`Ø20 mm` tại `(68.0, 121.0)`) nằm hoàn toàn thông thoáng, thuận tiện tháo lắp thay pin.
   - **`U7 (OLED 0.96" GM009605v4.3 1x04)`** đặt tại `(102.00, 116.50, 0°)` ngay phía dưới `U2 (MPU6050)`:
     - Chân `Pad 3 (SCK/SCL)` tại `X = 103.27 mm` và `Pad 4 (SDA)` tại `X = 105.81 mm` gióng thẳng đứng với `U2 Pad 3 (SCL)` và `U2 Pad 4 (SDA)`, tạo thành trục bus I2C ngắn gọn nối liền `U1 (GPIO8/9) -> R_PU1/R_PU2 -> U2 -> U7 -> U3`.

7. **Vùng 7 (Dưới – Phải, `X = 125 .. 149 mm, Y = 99 .. 141.5 mm`) — Khối Lưu Trữ SPI `J1 (MicroSD Adapter)`**:
   - Đặt tại `(137.00, 101.00, 0°)` ngay bên trái cụm chân SPI của `U1`:
     - `J1 Pad 1..4 (CS, SCK, MOSI, MISO)` đối diện trực tiếp với `U1 Pads 16..19 (GPIO10, GPIO11, GPIO12, GPIO13)` ở `Y = 89.93 .. 97.55 mm` (`len = 18.8 .. 28.8 mm`, ngắn nhất trong tất cả các module).
     - `J1 Pad 5 (VCC = 5V_SYS)` và `J1 Pad 6 (GND)` nằm ngay sát `U1 Pad 21 (5V_SYS, Y = 102.63 mm)` và `U1 Pad 22 (GND, Y = 105.17 mm)` (`len = 13.1 .. 15.5 mm`).
     - Thân module `MicroSD` (`24.0 × 42.0 mm`) hướng về **mép Nam PCB (`Y = 141.2 mm`)** để khe cắm thẻ nhớ MicroSD quay ra mặt trước hộp đen, nằm song song với hành lang cắm cáp USB-C của `ESP32-S3`.

---

## 4. BẢNG TỌA ĐỘ PLACEMENT TOÀN BỘ 32 FOOTPRINT TRÊN PCB

| STT | Ref | Giá trị / Chức năng | Footprint (`AIOT_Blackbox_Local`) | Tọa độ `(X, Y)` (`mm`) | Góc xoay (`deg`) | Vùng chức năng |
| :---: | :---: | :--- | :--- | :---: | :---: | :--- |
| 1 | **`U1`** | `ESP32-S3` (DevKitC-1 N16R8) | `ESP32_S3_N16R8_Socket_2x22_P2.54mm_Row25.40mm_SingleLayer` | `(169.00, 78.50)` | `0.0°` | MCU Phải (Anten mép Bắc, USB-C mép Nam) |
| 2 | **`J2`** | `LX-2BUPS 5V_3A` | `TermBlock_1x02_P5.08mm_SingleLayer` | `(60.00, 62.00)` | `90.0°` | Vùng 1: Nguồn vào 5V/3A (Mép Tây) |
| 3 | **`TP1`** | `TP_5V` | `TestPoint_THTPad_D2.2mm_Drill1.0mm_SingleLayer` | `(69.00, 58.00)` | `0.0°` | Vùng 1: Điểm đo nguồn `5V_SYS` |
| 4 | **`TP4`** | `TP_GND` | `TestPoint_THTPad_D2.2mm_Drill1.0mm_SingleLayer` | `(69.00, 66.00)` | `0.0°` | Vùng 1: Điểm đo `GND` chính |
| 5 | **`NT1`** | `STAR_5V_TO_SIM_PWR` | `NetTie_2_StarPoint_BCu_Width2.5mm` | `(78.00, 58.00)` | `0.0°` | Vùng 1: Điểm nối sao `5V_SYS -> SIM_PWR` |
| 6 | **`C3`** | `470uF` (Low-ESR ≥10V) | `CP_Radial_D8.0mm_P5.08mm_SingleLayer` | `(89.00, 56.00)` | `0.0°` | Vùng 1: Tụ bù dòng đỉnh `SIM_PWR` |
| 7 | **`C4`** | `100nF` | `C_Disc_D5.0mm_P5.08mm_SingleLayer` | `(99.00, 56.00)` | `0.0°` | Vùng 1: Tụ lọc cao tần sát chân SIM |
| 8 | **`TP3`** | `TP_SIM_PWR` | `TestPoint_THTPad_D2.2mm_Drill1.0mm_SingleLayer` | `(99.00, 49.00)` | `0.0°` | Vùng 1: Điểm đo nhánh `SIM_PWR` |
| 9 | **`U5`** | `A7680C` (Breakout J6 1x05) | `Conn_SIM_Breakout_J6_1x05_P2.54mm_SingleLayer` | `(100.00, 71.00)` | `0.0°` | Vùng 1: Header 5 chân Module SIM 4G |
| 10 | **`U6`** | `REG_3V3_MODULE` (1x04) | `Conn_Regulator_3V3_1x04_P2.54mm_SingleLayer` | `(66.00, 82.00)` | `0.0°` | Vùng 2: Module nguồn hạ áp 3.3V |
| 11 | **`C1`** | `100nF` | `C_Disc_D5.0mm_P5.08mm_SingleLayer` | `(80.00, 82.00)` | `0.0°` | Vùng 2: Tụ lọc đầu ra `3V3_SYS` |
| 12 | **`TP2`** | `TP_3V3` | `TestPoint_THTPad_D2.2mm_Drill1.0mm_SingleLayer` | `(80.00, 75.00)` | `0.0°` | Vùng 2: Điểm đo nhánh `3V3_SYS` |
| 13 | **`BZ1`** | `BUZZER` (Active 5V 12mm) | `Buzzer_D12.0mm_P7.62mm_SingleLayer` | `(136.00, 48.00)` | `0.0°` | Vùng 3: Còi báo động (cách `U2` `62.5mm`) |
| 14 | **`Q1`** | `2SC1815` (`1=E, 2=C, 3=B`) | `TO-92_2SC1815_ECB_Staggered_SingleLayer` | `(136.00, 60.50)` | `0.0°` | Vùng 3: Transistor NPN kích còi |
| 15 | **`R5`** | `1k` (Trở hạn dòng Base `Q1`) | `R_Axial_DIN0207_P10.16mm_SingleLayer` | `(148.00, 60.50)` | `90.0°` | Vùng 3: Nối `U1.GPIO5` vào `Q1.B` |
| 16 | **`R6`** | `10k` (Trở khóa `R_BE`) | `R_Axial_DIN0207_P10.16mm_SingleLayer` | `(136.00, 68.00)` | `0.0°` | Vùng 3: Khóa `Q1.B` xuống `GND` khi boot |
| 17 | **`SW1`** | `CANCEL` (Header 1x02) | `PinHeader_1x02_P2.54mm_SingleLayer` | `(114.00, 46.50)` | `0.0°` | Vùng 3: Ngõ cắm nút nhấn hủy cảnh báo |
| 18 | **`R3`** | `10k` (Pull-up `CANCEL`) | `R_Axial_DIN0207_P10.16mm_SingleLayer` | `(114.00, 52.50)` | `0.0°` | Vùng 3: Kéo `GPIO6` lên `3V3_SYS` |
| 19 | **`C2`** | `100nF` (Debounce `CANCEL`) | `C_Disc_D5.0mm_P5.08mm_SingleLayer` | `(114.00, 58.00)` | `0.0°` | Vùng 3: Chống dội phần cứng nút `CANCEL` |
| 20 | **`D1`** | `LED` (Status 5mm) | `LED_D5.0mm_P2.54mm_SingleLayer` | `(110.00, 64.00)` | `0.0°` | Vùng 3: LED báo trạng thái |
| 21 | **`R4`** | `330R` (Hạn dòng `D1`) | `R_Axial_DIN0207_P10.16mm_SingleLayer` | `(121.00, 64.00)` | `0.0°` | Vùng 3: Nối `U1.GPIO7` tới Anode `D1` |
| 22 | **`U4`** | `NEO-M8N` (V2149 1x05) | `Conn_GPS_NEO-M8N_V2149_1x05_P2.54mm_SingleLayer` | `(122.00, 77.00)` | `0.0°` | Vùng 4: Header 5 chân Module GPS |
| 23 | **`R_PU1`** | `4.7k` (`I2C_SDA` Pull-up) | `R_Axial_DIN0207_P10.16mm_SingleLayer` | `(139.00, 81.50)` | `0.0°` | Vùng 4: Kéo `I2C_SDA (GPIO8)` lên `3V3_SYS` |
| 24 | **`R_PU2`** | `4.7k` (`I2C_SCL` Pull-up) | `R_Axial_DIN0207_P10.16mm_SingleLayer` | `(139.00, 87.50)` | `0.0°` | Vùng 4: Kéo `I2C_SCL (GPIO9)` lên `3V3_SYS` |
| 25 | **`U2`** | `MPU6050` (GY-521 1x08) | `Module_GY-521_MPU6050_1x08_P2.54mm_SingleLayer` | `(96.00, 96.00)` | `0.0°` | Vùng 4: Tâm cơ học PCB (`+X UP / +Y LEFT`) |
| 26 | **`U3`** | `DS3231` (ZS-042 1x06) | `Module_DS3231_ZS042_1x06_P2.54mm_SingleLayer` | `(68.00, 100.00)` | `0.0°` | Vùng 5: Đồng hồ thời gian thực + Pin CR2032 |
| 27 | **`U7`** | `OLED 0.96"` (GM009605v4.3) | `OLED_0.96_GM009605v4.3_1x04_P2.54mm_SingleLayer` | `(102.00, 116.50)` | `0.0°` | Vùng 6: Màn hình hiển thị I2C |
| 28 | **`J1`** | `MICROSD` (Adapter 1x06) | `Module_MicroSD_Adapter_1x06_P2.54mm_SingleLayer` | `(137.00, 101.00)` | `0.0°` | Vùng 7: Khe thẻ nhớ MicroSD hướng mép Nam |
| 29 | **`H1`** | `M3_NPTH_PROVISIONAL` | `MountingHole_3.2mm_M3_NPTH` | `(55.00, 45.00)` | `0.0°` | Lỗ bắt vít M3 Góc Trên – Trái |
| 30 | **`H2`** | `M3_NPTH_PROVISIONAL` | `MountingHole_3.2mm_M3_NPTH` | `(190.00, 45.00)` | `0.0°` | Lỗ bắt vít M3 Góc Trên – Phải |
| 31 | **`H3`** | `M3_NPTH_PROVISIONAL` | `MountingHole_3.2mm_M3_NPTH` | `(55.00, 140.00)` | `0.0°` | Lỗ bắt vít M3 Góc Dưới – Trái |
| 32 | **`H4`** | `M3_NPTH_PROVISIONAL` | `MountingHole_3.2mm_M3_NPTH` | `(190.00, 140.00)` | `0.0°` | Lỗ bắt vít M3 Góc Dưới – Phải |

---

## 5. NET CLASS (ĐÃ KHÔI PHỤC THEO RULE 09, ĐƯỢC pcbnew ĐỌC LẠI VÀ XÁC NHẬN)

Khôi phục trong `AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pro` (có backup trong `GATE_2_PLACEMENT\backup\`). `Default` đóng vai trò lớp `SIGNAL` của RULE 09. Đã kiểm tra bằng `pcbnew`: `SIM_PWR→SIM_POWER`, `5V_SYS→5V_POWER`, `3V3_SYS→3V3_POWER`, `GND→GND`, SDA→`I2C`, SD_CS/MOSI→`SPI`, SIM_RX/GPS_TX→`UART`, BUZZER→`Default`.

| Net Class | Net | Track (mm) | Clearance (mm) | Ghi chú |
| :--- | :--- | :---: | :---: | :--- |
| `Default` (= SIGNAL) | GPIO logic còn lại | 0.30 | 0.25 | RULE 09 |
| `I2C` | `/I2C_SDA_GPIO8`, `/I2C_SCL_GPIO9` | 0.35 | 0.30 | |
| `UART` | `SIM_RX/TX`, `GPS_RX/TX` | 0.35 | 0.30 | |
| `SPI` | `SD_CS`, `MOSI`, `SCK`, `MISO` | 0.35 | 0.30 | |
| `3V3_POWER` | `3V3_SYS` | 1.00 | 0.30 | |
| `5V_POWER` | `5V_SYS` | 1.50 | 0.40 | ≈3.2 A (IPC-2221, 1 oz, ΔT 10 °C) |
| `SIM_POWER` | `SIM_PWR` | 2.50 | 0.50 | ≈4.6 A (IPC-2221); thắt nhỏ lại gần pad khi cần |
| `GND` | `GND` | 1.50 | 0.40 | đổ đồng B.Cu ở Gate 3/4 |

Giới hạn DRC của project đặt theo RULE 20: `min_clearance = 0.25`, `min_track_width = 0.25` (trước đó 0.35/0.40 là giá trị tự đặt, chặn mất độ rộng 0.30–0.35 của RULE 09). Các số IPC-2221 là ước lượng giả định đồng 35 µm; PCB tự ăn mòn có thể mỏng hơn.
