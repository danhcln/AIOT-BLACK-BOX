# BÁO CÁO RÀ SOÁT CUỐI GATE 1.5: FOOTPRINT, NGUỒN & NETLIST TRƯỚC PLACEMENT (`GATE_1_FINAL_REVIEW.md`)

**Dự án**: THIẾT KẾ HỘP ĐEN AIoT THÔNG MINH PHÂN TÍCH VÀ GHI LẠI SỰ CỐ XE MÁY ĐIỆN  
**Project KiCad**: `D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1`  
**Firmware chuẩn**: `D:\ĐỒ ÁN 2\filecodemain.cpp` (Giữ nguyên 100%, không chỉnh sửa)  
**Bộ luật thiết kế**: `D:\ĐỒ ÁN 2\.agents\rules\PCB_DESIGN_RULES_AIOT.md` (Ưu tiên PCB 1 lớp trên `B.Cu`)  
**Trạng thái hiện tại**: **HOÀN THÀNH GATE 1.5 — DỪNG TRƯỚC PLACEMENT (CHƯA VẼ PCB, CHƯA ROUTING, CHƯA XUẤT GERBER)**  

---

## 1. XÁC MINH FOOTPRINT `ESP32-S3` (`U1`) — ĐÃ ĐỦ CĂN CỨ ĐỂ KHÓA CHƯA?

### 1.1. Kết luận trạng thái: **GIỮ `PENDING` (`PENDING_MEASUREMENT`) — CHƯA KHÓA CỨNG KHOẢNG CÁCH 2 HÀNG CHÂN**

Qua đối chiếu trực tiếp giữa 2 ảnh thực tế của bo `ESP32 N16R8` (`84491fa379081b485b62d44112a8bbd7.jpg` mặt trước & `2dad8255752d7c0230db6d0f5b913e92.jpg` mặt sau) với bản vẽ cơ khí chính hãng Espressif (`DXF_ESP32-S3-DevKitC-1_V1_20210312CB.pdf`), phát hiện **bo thực tế trong ảnh KHÔNG PHẢI là bo `ESP32-S3-DevKitC-1 V1` chính hãng Espressif**, mà là phiên bản **`YD-ESP32-S3` (Dual USB Type-C Clone)** của bên thứ ba:

| Tiêu chí đối chiếu | Bản vẽ chính hãng Espressif (`DXF_ESP32-S3-DevKitC-1_V1_20210312CB.pdf`) | Bo thực tế trong ảnh (`D:\ĐỒ ÁN 2\Hình ảnh linh kiện\ESP32 N16R8`) | Kết luận kỹ thuật |
| :--- | :--- | :--- | :--- |
| **Module RF hàn trên bo** | `ESP32-S3-WROOM-1` (`18.0 × 25.5 mm`) | `ESP32-S3-WROOM-1` (`ESP32-S3-N16R8`, `FCC ID: 2AC7Z-ESP32S3N16R8`, rộng `18.0 mm`) | **Khớp 100%** (Module chip chính hãng Espressif) |
| **Vị trí nút `RST` & `BOOT`** | Đặt ở 2 góc dưới (hai bên cổng USB) | Đặt **dọc cạnh nhau ở sườn phải** (ngay dưới module WROOM-1, cạnh chân `39, 38, 37, 36`) | **Khác bố cục cơ khí** (`YD-ESP32-S3` layout) |
| **Cổng USB & Jumper phụ** | 2 cổng Micro-USB (`UART` & `USB`), không có jumper `IN-OUT` | **2 cổng USB Type-C** (in `COM` và `USB` ở mặt sau), có jumper hàn **`IN-OUT`** mặt trước và **`USB-OTG`** mặt sau | **Khác phiên bản PCB** |
| **Chữ in Silkscreen mặt sau** | In tên `ESP32-S3-DevKitC-1` và nhãn `J1`, `J3` | Chỉ in **`ESP32-S3`**, **`USB-OTG`**, **`COM`**, **`USB`**, rào chân đực màu vàng | **Khác nhà sản xuất PCB** |
| **Chiều rộng bo & Khoảng cách 2 hàng chân (Row Pitch)** | • Rộng bo: **`25.40 mm`**<br>• Tâm chân tới mép bo: **`1.27 mm`**<br>• Khoảng cách 2 hàng chân: **`22.86 mm` (`900 mil`)** | Trên thị trường bo `YD-ESP32-S3` Dual Type-C tồn tại cả 2 biến thể:<br>• Biến thể hẹp: Row Pitch **`22.86 mm` (`900 mil`)**, rộng bo `25.40 mm`.<br>• Biến thể rộng: Row Pitch **`25.40 mm` (`1000 mil`)**, rộng bo `27.94 mm` *(Đo tỷ lệ pixel trên ảnh mặt trước so với pitch dọc `2.54 mm` cho tỷ lệ xấp xỉ `~10.0` pitch = `25.40 mm`)*. | **GIỮ `PENDING` — Bắt buộc kiểm tra bằng bản in 1:1 hoặc thước kẹp trước khi khóa!** |

---

### 1.2. Kiểm tra riêng thứ tự 44 Pad theo Silkscreen & Datasheet (Cấm dùng DIP-44 tiêu chuẩn)

> [!CAUTION]
> **Cảnh báo kỹ thuật quan trọng (Non-DIP-44 Pin Numbering)**:
> - Footprint chuẩn **DIP-44 thông thường** đánh số ngược chiều kim đồng hồ (Hàng trái từ trên xuống là `1..22`, nhưng Hàng phải đánh số **từ dưới lên trên** là `23..44`, tức chân dưới cùng bên phải là `23` và chân trên cùng bên phải là `44`).
> - Trong khi đó, Symbol `Presentation:ESP32-S3-DevKitC-1` (`U1`) và tài liệu header `J1`/`J3` đánh số **cả hai hàng từ trên (phía Anten) xuống dưới (phía cổng USB-C)**:
>   - **Hàng Trái (Top-to-Bottom)**: **`Pad 1` (`3V3`) $\rightarrow$ `Pad 22` (`GND`)**.
>   - **Hàng Phải (Top-to-Bottom)**: **`Pad 23` (`GND` trên cùng cạnh anten) $\rightarrow$ `Pad 44` (`GND` dưới cùng cạnh USB-C)**.
> - Nếu dùng footprint DIP-44 máy móc, toàn bộ 22 chân hàng bên phải (`Pad 23..44`) sẽ bị đảo ngược đầu–đuôi!

**Bảng kiểm tra 44 Pad đã chuẩn hóa trong cả 2 Footprint ứng viên (`ESP32_S3_Socket_2x22_Row22.86mm_PENDING_VERIFY` và `ESP32_S3_Socket_2x22_Row25.40mm_PENDING_VERIFY`)**:

| Thứ tự dọc từ Anten xuống USB-C | Tọa độ dọc $Y$ (mm) | **Hàng Trái (`Pad 1..22`)** | Silkscreen Hàng Trái | Kết nối trong Firmware (`filecodemain.cpp`) | **Hàng Phải (`Pad 23..44`)** | Silkscreen Hàng Phải | Kết nối trong Firmware (`filecodemain.cpp`) |
| :---: | :---: | :---: | :---: | :--- | :---: | :---: | :--- |
| Hàng 1 (Trên cùng) | `-26.67` | **Pad `1`** *(Rect)* | `3V3` | `NC` (Cô lập với `3V3_SYS`) | **Pad `23`** | `GND` | **`GND`** |
| Hàng 2 | `-24.13` | **Pad `2`** | `3V3` | `NC` (Cô lập với `3V3_SYS`) | **Pad `24`** | `TX` (`GPIO43`) | `NC` |
| Hàng 3 | `-21.59` | **Pad `3`** | `RST` | `NC` | **Pad `25`** | `RX` (`GPIO44`) | `NC` |
| Hàng 4 | `-19.05` | **Pad `4`** | `4` | `NC` | **Pad `26`** | `1` | `NC` |
| Hàng 5 | `-16.51` | **Pad `5`** | `5` | `NC` | **Pad `27`** | `2` | `NC` |
| Hàng 6 | `-13.97` | **Pad `6`** | `6` | `NC` | **Pad `28`** | `42` | `NC` |
| Hàng 7 | `-11.43` | **Pad `7`** | `7` | `NC` | **Pad `29`** | `41` | `NC` |
| Hàng 8 | `-8.89` | **Pad `8`** | **`15`** | **`SIM_RX_GPIO15`** (`← SIM TXD`) | **Pad `30`** | `40` | `NC` |
| Hàng 9 | `-6.35` | **Pad `9`** | **`16`** | **`SIM_TX_GPIO16`** (`→ SIM RXD`) | **Pad `31`** | `39` | `NC` |
| Hàng 10 | `-3.81` | **Pad `10`** | **`17`** | **`GPS_TX_GPIO17`** (`→ GPS RXD`) | **Pad `32`** | `38` | `NC` |
| Hàng 11 | `-1.27` | **Pad `11`** | **`18`** | **`GPS_RX_GPIO18`** (`← GPS TXD`) | **Pad `33`** | `37` | `NC` |
| Hàng 12 | `+1.27` | **Pad `12`** | **`8`** | **`I2C_SDA_GPIO8`** (`SDA`) | **Pad `34`** | `36` | `NC` |
| Hàng 13 | `+3.81` | **Pad `13`** | `3` | `NC` | **Pad `35`** | `35` | `NC` |
| Hàng 14 | `+6.35` | **Pad `14`** | `46` | `NC` | **Pad `36`** | `0` | `NC` |
| Hàng 15 | `+8.89` | **Pad `15`** | **`9`** | **`I2C_SCL_GPIO9`** (`SCL`) | **Pad `37`** | `45` | `NC` |
| Hàng 16 | `+11.43` | **Pad `16`** | **`10`** | **`SD_CS_GPIO10`** (`MicroSD CS`) | **Pad `38`** | `48` | `NC` |
| Hàng 17 | `+13.97` | **Pad `17`** | **`11`** | **`SPI_MOSI_GPIO11`** (`MOSI`) | **Pad `39`** | `47` | `NC` |
| Hàng 18 | `+16.51` | **Pad `18`** | **`12`** | **`SPI_SCK_GPIO12`** (`SCK`) | **Pad `40`** | `21` | `NC` |
| Hàng 19 | `+19.05` | **Pad `19`** | **`13`** | **`SPI_MISO_GPIO13`** (`MISO`) | **Pad `41`** | `20` | `NC` |
| Hàng 20 | `+21.59` | **Pad `20`** | `14` | `NC` | **Pad `42`** | `19` | `NC` |
| Hàng 21 | `+24.13` | **Pad `21`** | **`5Vin`** | **`5V_SYS`** (Nguồn 5V nuôi ESP32) | **Pad `43`** | `GND` | `NC` (Đã nối nội bộ với `GND`) |
| Hàng 22 (Dưới cùng) | `+26.67` | **Pad `22`** | **`GND`** | **`GND`** | **Pad `44`** | `GND` | `NC` (Đã nối nội bộ với `GND`) |

### 1.3. Đã xuất Bản in thử Footprint tỷ lệ 1:1 (`ESP32_S3_FOOTPRINT_1TO1_CHECK.pdf` & `.svg`)
- Đường dẫn file PDF chuẩn A4 tỷ lệ 1:1: `D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1\GATE_1_FOOTPRINT\ESP32_S3_FOOTPRINT_1TO1_CHECK.pdf`
- Đường dẫn file SVG tỷ lệ 1:1: `D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1\GATE_1_FOOTPRINT\ESP32_S3_FOOTPRINT_1TO1_CHECK.svg`
- Trên trang in có **thước chuẩn `100.0 mm`** và đặt song song **MẪU A (`Row Pitch = 22.86 mm` — chuẩn Espressif DXF)** cùng **MẪU B (`Row Pitch = 25.40 mm` — chuẩn YD-ESP32-S3 Clone)** kèm toàn bộ 6 đầu nối ngoại vi để bạn in ra giấy A4 ở chế độ `Actual Size / 100%` và ướm trực tiếp bo `ESP32-S3` lên kiểm tra trước khi khóa footprint cho Gate 2.

---

## 2. ĐÁNH GIÁ KỸ THUẬT NGUỒN `MICROSD` (`J1`): `5V_SYS → VCC MICROSD BREAKOUT`

### 2.1. Phân tích đường mạch đồng thực tế trên ảnh & Datasheet IC
1. **Dò đường mạch đồng trực tiếp trên ảnh mặt trước (`1794204268884_..._3c29c5070fa32b94e95acbb08c00777d.jpg`)**:
   - **Chân `Pin 5` (`VCC`)** của header 6 chân đi qua một đường đồng ngang dày nối **trực tiếp vào chân số 3 (chân bên phải `VIN`) của IC ổn áp SOT-223 `AMS1117-3.3` (`1117 3.3 BW053`)** và tụ lọc đầu vào `C2`.
   - **Chân số 2 (chân giữa & cánh tản nhiệt `VOUT = 3.3V`) của `AMS1117-3.3`** nối qua tụ `C3, C4` để cấp nguồn **`3.3V` nội bộ** cho khe thẻ nhớ MicroSD, chân nguồn `VCC` (Pin 14) của IC đệm **`74LVC125A` (`LVC125A`)**, và 4 điện trở kéo lên `R1..R4` (`103` = `10kΩ`).
2. **Phân tích sụt áp Dropout theo Datasheet `AMS1117-3.3`**:
   - Theo datasheet `AMS1117-3.3`, điện áp rơi tối thiểu trên LDO ($V_{\text{DROP}}$) là **$1.1\text{V}$ (typical) đến $1.3\text{V}$ (max)**.
   - Để đầu ra đạt chuẩn $3.3\text{V}$ nuôi thẻ nhớ MicroSD, điện áp tại chân `VCC` (`J1` Pin 5) bắt buộc phải thỏa mãn:
     $$V_{\text{VCC(min)}} = 3.3\text{V} + 1.1\text{V} = 4.4\text{V} \implies \text{Phải cấp } \mathbf{5V\_SYS\ (5.0V)}$$
   - Nếu giữ `3V3_SYS` ($3.3\text{V}$) vào chân `VCC` như schematic cũ, điện áp sau `AMS1117-3.3` bị sụt còn $\approx 2.1\text{V} - 2.2\text{V}$ (thấp hơn mức tối thiểu $2.7\text{V}$ của chuẩn thẻ SDXC/SDHC), gây lỗi khởi tạo `sd.cardBegin()` hoặc lỗi ghi file khi điện áp sụt nhẹ.

### 2.2. Kiểm tra mức logic các đường SPI (`CS, SCK, MOSI, MISO`) ở phía `ESP32-S3` khi cấp `5V_SYS` cho `J1`
- **Câu hỏi an toàn**: *Khi cấp `5V_SYS` ($5.0\text{V}$) vào chân `VCC` (Pin 5) của module MicroSD, các chân SPI (`CS`, `SCK`, `MOSI`, `MISO`) có xuất áp $5\text{V}$ làm hỏng GPIO $3.3\text{V}$ của `ESP32-S3` không?*
- **Kết luận kỹ thuật**: **TUYỆT ĐỐI AN TOÀN Ở MỨC LOGIC $3.3\text{V}$ (`100% 3.3V-SAFE`)**.
  - **Lý do 1**: Nguồn $5\text{V}$ tại chân `VCC` **chỉ đi vào chân `VIN` của `AMS1117-3.3`**, hoàn toàn không nối tới IC `74LVC125A`, không nối tới thẻ nhớ và không nối tới các điện trở kéo lên `R1..R4`.
  - **Lý do 2**: Toàn bộ IC `74LVC125A`, khe thẻ nhớ MicroSD và 4 điện trở pull-up `R1..R4` (`10kΩ`) đều được nuôi bởi đường **`3.3V` sau ổn áp `AMS1117-3.3`**.
  - **Lý do 3**:
    - 3 đường đầu vào `CS` (`GPIO10`), `SCK` (`GPIO12`), `MOSI` (`GPIO11`) đi vào ngõ vào của `74LVC125A` (nuôi ở $V_{CC}=3.3\text{V}$, ngưỡng nhận mức cao $V_{IH(\text{min})} = 2.0\text{V}$, tương thích hoàn hảo với mức $3.3\text{V}$ từ `ESP32-S3`).
    - Đường phản hồi `MISO` (`GPIO13`) đi từ chân `DO` của thẻ nhớ ($3.3\text{V}$) về `ESP32-S3` `GPIO13`, nên mức áp tối đa trên `MISO` luôn là **$3.3\text{V}$**.

### 2.3. Đề xuất thay đổi chính xác trên Schematic (Chờ người dùng xác nhận — Chưa tự ý sửa file)
- **Đề xuất**: **Thay đổi net cấp nguồn cho chân `VCC` của `MicroSD` (`J1`) từ `3V3_SYS` sang `5V_SYS`**.
- **Chi tiết chân/net sẽ thay đổi khi được bạn phê duyệt**:
  - **Linh kiện**: `J1` (`Presentation:MicroSD_SPI_Module`, Value `MICROSD`)
  - **Chân**: **`Pin 5`** (tên trong symbol là `3V3`, tương ứng chân `VCC` trên silkscreen module tại tọa độ `(67.31 mm, 162.56 mm)`)
  - **Symbol nguồn tại `(63.50 mm, 157.48 mm)`**: Đổi từ `Presentation:3V3_SYS` (`#PWR0216`) sang **`Presentation:5V_SYS`** (nối vào net **`5V_SYS`**).
  - **Tác động**: Tất cả 4 đường tín hiệu SPI (`Pin 1: CS`, `Pin 2: SCK`, `Pin 3: MOSI`, `Pin 4: MISO`) và `Pin 6: GND` giữ nguyên 100%.

---

## 3. NGUỒN VÀ MÃ MODULE SIM (`U5`) — BẢNG BẰNG CHỨNG TÊN MODEL

### 3.1. Bảng bằng chứng đối chiếu tên Model SIM (`MODEL_UNVERIFIED`)

| Nguồn bằng chứng | Nội dung ghi nhận | Phân tích kỹ thuật |
| :--- | :--- | :--- |
| **1. Tên thư mục ảnh của người dùng** | `D:\ĐỒ ÁN 2\Hình ảnh linh kiện\Module Sim A7680C` | Ghi rõ mã **`A7680C`**. |
| **2. Kiểu vỏ LCC & Số pad trên ảnh mặt trước (`e48892d98332388c5f711227cc6e4e73.jpg`)** | Module SIMCom dạng vuông có **12 pad khuyết (castellated pads) ở cạnh trên, 12 pad cạnh dưới, 8 pad cạnh trái, 8 pad cạnh phải** (tổng 40 pad biên). | Theo Datasheet SIMCom:<br>• **`A7680C`** dùng vỏ `16.0 × 16.0 mm` LCC với đúng cấu hình **12 pad trên/dưới × 8 pad trái/phải**.<br>• **`A7682S`** dùng vỏ `19.6 × 19.6 mm` 42-LCC (tương thích SIM800C với 10 pad trên/dưới × 11 pad trái/phải).<br>$\rightarrow$ Hình học vỏ chip trên ảnh khớp với họ **`A7680C`**. |
| **3. Chữ khắc laser trên nắp shield (`e48892d98332388c5f711227cc6e4e73.jpg`)** | Khi tăng tương phản gấp 4 lần vùng nắp shield (cạnh chấm tròn Pin 1 góc dưới trái), hiện ra các nét đầu **`A7680C-...`** kèm logo SIMCom tròn ở góc trên phải, nhưng phần đuôi mã bị lóa sáng. | Không đọc được 100% chuỗi ký tự đầy đủ bằng mắt thường do phản xạ ánh sáng trên bề mặt kim loại nhám. |
| **4. Chú thích trong Firmware (`filecodemain.cpp`)** | Dòng 23–24: `// Nối vào TXD của SIM A7682S` và dòng 283: `[6] 4G LTE A7682S ... OK` (Cả `A7680C` và `A7682S` đều dùng tập lệnh AT SIMCom A76xx giống hệt nhau: `AT`, `ATE0`, `AT+CTZU=1`, `AT+CMGF=1`, `AT+CNMI=2,2,0,0,0`, `AT+CSQ`, `AT+CCLK?`, `AT+CMGS`). | Firmware chạy chung tập lệnh AT của dòng SIMCom `A76xx` nên không phân biệt được mã phần cứng chỉ qua code. |
| **KẾT LUẬN TRẠNG THÁI MODEL** | **`MODEL_UNVERIFIED` (`A7680C` vs `A7682S`)** | Tuân thủ nghiêm ngặt Nhiệm vụ 3: **Không coi `A7680C` và `A7682S` là cùng một loại**, giữ trạng thái `MODEL_UNVERIFIED` chờ bạn xác nhận chữ in thực tế trên nắp module. |

### 3.2. Trạng thái Footprint và Nguồn `SIM_PWR`
- **Kiểu lắp**: Giữ nguyên **`CONNECTOR_ONLY`** sử dụng footprint đã xác minh `AIOT_Blackbox_Local:Conn_SIM_Breakout_J6_1x05_P2.54mm_SingleLayer` khớp với 5 chân hàng phải `J6` (`1:VCC, 2:RST, 3:RXD, 4:TXD, 5:GND`).
- **Nguồn `SIM_PWR`**: Giữ nguyên **`SIM_PWR = NEEDS_VERIFICATION`** (cấp qua domino độc lập `J3`, **không tự nối vào `5V_SYS`** và không suy đoán điện áp từ linh kiện trên ảnh).

---

## 4. KIỂM TRA ĐỒNG BỘ 4 TẦNG (SYMBOL SCHEMATIC ↔ SYMBOL LIBRARY ↔ FOOTPRINT PAD ↔ KICAD NETLIST) & KẾT QUẢ ERC

### 4.1. Kết quả chạy lại ERC (`kicad-cli sch erc`)
- File báo cáo ERC mới nhất: `D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1\GATE_1_FOOTPRINT\ERC_REPORT_GATE1_5.txt`
- **Kết quả**: **`1 Error, 0 Warnings`** (So sánh với kết quả cuối Gate 0: **Giữ nguyên 100%, không phát sinh bất kỳ lỗi hay cảnh báo mới nào**).
  - Lỗi duy nhất được giữ lại có chủ đích: `[power_pin_not_driven]` tại `#PWR086` (`SIM_PWR` ở tọa độ `(149.86 mm, 33.02 mm)`).
- Ngoài ra, đã chuẩn hóa toàn bộ số thứ tự tham chiếu `#PWR0xx` trong schematic giúp lệnh xuất Netlist `kicad-cli sch export netlist` chạy sạch sẽ với **`0 Warnings, Exit Code = 0`**.

### 4.2. Bảng đối chiếu Netlist xuất từ KiCad (`AIOT_BLACKBOX_MAINBOARD_REV1.net`) cho 3 Module vừa cập nhật Pin Number (`J1`, `U4`, `U5`) và toàn hệ thống

Đã xuất trực tiếp file Netlist chuẩn KiCad tại:  
`D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1\GATE_1_FOOTPRINT\AIOT_BLACKBOX_MAINBOARD_REV1.net`

| Linh kiện (`Ref`) | Số chân Symbol (`.kicad_sch` & `.kicad_sym`) | Số Pad Footprint (`.kicad_mod`) | Tên chân trên Silkscreen ảnh thực tế | Net thực tế trong `AIOT_BLACKBOX_MAINBOARD_REV1.net` | Chân đối ứng trên `ESP32-S3` (`U1`) / Nguồn | Kiểm tra chiều `TX/RX` & `VCC/GND` |
| :--- | :---: | :---: | :--- | :--- | :--- | :---: |
| **`J1` (`MicroSD`)** | **Pin `1` (`CS`)** | **Pad `1`** *(Rect)* | **`1: CS`** | `/SD_CS_GPIO10` | `U1` **Pin `16` (`GPIO10`)** | **ĐÚNG 100%** (`SD_CS_PIN = 10`) |
| **`J1` (`MicroSD`)** | **Pin `2` (`SCK`)** | **Pad `2`** | **`2: SCK`** | `Net-(J1-SCK)` | `U1` **Pin `18` (`GPIO12`)** | **ĐÚNG 100%** (`SPI_SCK_PIN = 12`) |
| **`J1` (`MicroSD`)** | **Pin `3` (`MOSI`)** | **Pad `3`** | **`3: MOSI`** | `Net-(J1-MOSI)` | `U1` **Pin `17` (`GPIO11`)** | **ĐÚNG 100%** (`SPI_MOSI_PIN = 11`) |
| **`J1` (`MicroSD`)** | **Pin `4` (`MISO`)** | **Pad `4`** | **`4: MISO`** | `Net-(J1-MISO)` | `U1` **Pin `19` (`GPIO13`)** | **ĐÚNG 100%** (`SPI_MISO_PIN = 13`) |
| **`J1` (`MicroSD`)** | **Pin `5` (`3V3`)** | **Pad `5`** | **`5: VCC`** | `3V3_SYS` *(Đề xuất đổi sang `5V_SYS`)* | Nguồn hệ thống | **ĐÚNG VỊ TRÍ CHÂN 5** *(Chờ duyệt đổi sang `5V_SYS`)* |
| **`J1` (`MicroSD`)** | **Pin `6` (`GND`)** | **Pad `6`** | **`6: GND`** | `GND` | `GND` chung | **ĐÚNG 100%** |
| **`U4` (`GPS NEO-M8N`)** | **Pin `1` (`VCC`)** | **Pad `1`** *(Rect)* | **`1: VCC`** (Pad vuông) | `3V3_SYS` | `3V3_SYS` (Từ `U6` Pin 3) | **ĐÚNG 100%** |
| **`U4` (`GPS NEO-M8N`)** | **Pin `2` (`GND`)** | **Pad `2`** | **`2: GND`** | `GND` | `GND` chung | **ĐÚNG 100%** |
| **`U4` (`GPS NEO-M8N`)** | **Pin `3` (`TX`)** | **Pad `3`** | **`3: TXD`** | `/GPS_RX_GPIO18` | `U1` **Pin `11` (`GPIO18` = `GPS_RX_PIN`)** | **ĐÚNG CHIỀU CHÉO** (`GPS TXD → ESP32 RX GPIO18`) |
| **`U4` (`GPS NEO-M8N`)** | **Pin `4` (`RX`)** | **Pad `4`** | **`4: RXD`** | `/GPS_TX_GPIO17` | `U1` **Pin `10` (`GPIO17` = `GPS_TX_PIN`)** | **ĐÚNG CHIỀU CHÉO** (`ESP32 TX GPIO17 → GPS RXD`) |
| **`U4` (`GPS NEO-M8N`)** | **Pin `5` (`PPS`)** | **Pad `5`** | **`5: PPS`** | `unconnected-(U4-PPS-Pad5)` | `NC` (Chưa dùng trong code) | **ĐÚNG 100%** |
| **`U5` (`SIM J6`)** | **Pin `1` (`VCC`)** | **Pad `1`** *(Rect)* | **`1: VCC`** | `SIM_PWR` | `J3` Pin 1 (`V_SIM`) | **ĐÚNG 100%** (`NEEDS_VERIFICATION`) |
| **`U5` (`SIM J6`)** | **Pin `2` (`PWRKEY`)**| **Pad `2`** | **`2: RST`** | `unconnected-(U5-PWRKEY-Pad2)`| `NC` (Để hở an toàn) | **ĐÚNG 100%** |
| **`U5` (`SIM J6`)** | **Pin `3` (`RX`)** | **Pad `3`** | **`3: RXD`** | `/SIM_TX_GPIO16` | `U1` **Pin `9` (`GPIO16` = `SIM_TX_PIN`)** | **ĐÚNG CHIỀU CHÉO** (`ESP32 TX GPIO16 → SIM RXD`) |
| **`U5` (`SIM J6`)** | **Pin `4` (`TX`)** | **Pad `4`** | **`4: TXD`** | `/SIM_RX_GPIO15` | `U1` **Pin `8` (`GPIO15` = `SIM_RX_PIN`)** | **ĐÚNG CHIỀU CHÉO** (`SIM TXD → ESP32 RX GPIO15`) |
| **`U5` (`SIM J6`)** | **Pin `5` (`GND`)** | **Pad `5`** | **`5: GND`** | `GND` | `GND` chung | **ĐÚNG 100%** |
| **`U7` (`OLED 0.96"`)**| **Pin `1..4`** | **Pad `1..4`** | `1:GND, 2:VDD, 3:SCK, 4:SDA` | `1:GND`, `2:3V3_SYS`, `3:/I2C_SCL_GPIO9`, `4:/I2C_SDA_GPIO8` | `U1` `GPIO9` (`SCL`), `GPIO8` (`SDA`) | **ĐÚNG 100%** |
| **`U2` (`MPU6050`)** | **Pin `1..8`** | **Pad `1..8`** | `1:VCC, 2:GND, 3:SCL, 4:SDA, 5:XDA, 6:XCL, 7:AD0, 8:INT` | `1:3V3_SYS`, `2:GND`, `3:SCL`, `4:SDA`, `5:NC`, `6:NC`, `7:3V3_SYS (0x69)`, `8:NC` | `U1` `GPIO9` (`SCL`), `GPIO8` (`SDA`), `AD0=HIGH (0x69)` | **ĐÚNG 100%** (`mpu.begin(0x69)`) |
| **`U3` (`DS3231`)** | **Pin `1..6`** | **Pad `1..6`** | `1:32K, 2:SQW, 3:SCL, 4:SDA, 5:VCC, 6:GND` | `1:NC`, `2:NC`, `3:SCL`, `4:SDA`, `5:3V3_SYS`, `6:GND` | `U1` `GPIO9` (`SCL`), `GPIO8` (`SDA`) | **ĐÚNG 100%** (`0x68`) |

> [!TIP]
> **Xác nhận không làm sai lệch Net**: Việc cập nhật số chân `(number "...")` trên `J1`, `U4`, `U5` chỉ thay đổi nhãn số thứ tự pad gắn với mỗi chân mà không dịch chuyển tọa độ `(at ...)` của bất kỳ chân nào trên schematic. Do đó 100% dây nối trong schematic giữ nguyên kết nối điện và xuất ra Netlist chính xác tuyệt đối.

---

## 5. DANH SÁCH MODULE ĐÃ SẴN SÀNG CHO GATE 2 (`READY FOR GATE 2`) VS CẦN CHỐT CUỐI (`PENDING`)

| Nhóm | Danh sách Linh kiện / Module | Footprint trong `AIOT_Blackbox_Local.pretty` | Trạng thái cho GATE 2 |
| :--- | :--- | :--- | :---: |
| **1. ĐÃ SẴN SÀNG 100% (`READY`)** | • **`U7` (`OLED 0.96" GM009605v4.3`)**<br>• **`U2` (`MPU6050 GY-521` — Header `1x08`)**<br>• **`U3` (`RTC DS3231 ZS-042` — Header `1x06`)**<br>• **`J1` (`MicroSD Adapter` — Header `1x06`)**<br>• **`U4` (`GPS NEO-M8N V2149` — Connector `1x05`)**<br>• **`U5` (`SIM Breakout J6` — Connector `1x05`)**<br>• **`U6` (`3.3V Regulator` — Connector `1x04`)**<br>• **`J2`, `J3` (`Domino nguồn P5.08mm`)**<br>• **`R_PU1, R_PU2, C1` & Khối dự phòng (`BZ1, D1, SW1, Q1, R3..R5, C2`)** | • `OLED_0.96_GM009605v4.3_1x04_P2.54mm_SingleLayer`<br>• `Module_GY-521_MPU6050_1x08_P2.54mm_SingleLayer`<br>• `Module_DS3231_ZS042_1x06_P2.54mm_SingleLayer`<br>• `Module_MicroSD_Adapter_1x06_P2.54mm_SingleLayer`<br>• `Conn_GPS_NEO-M8N_V2149_1x05_P2.54mm_SingleLayer`<br>• `Conn_SIM_Breakout_J6_1x05_P2.54mm_SingleLayer`<br>• `Conn_Regulator_3V3_1x04_P2.54mm_SingleLayer`<br>• `TermBlock_1x02_P5.08mm_SingleLayer`<br>• Các footprint THT chuẩn PCB 1 lớp | **`READY FOR GATE 2`** |
| **2. CHỜ XÁC NHẬN TRƯỚC KHI KHÓA (`PENDING`)** | • **`U1` (`ESP32-S3 N16R8` — Chọn giữa Mẫu A `22.86mm` và Mẫu B `25.40mm`)** | • Mẫu A: `ESP32_S3_Socket_2x22_Row22.86mm_PENDING_VERIFY`<br>• Mẫu B: `ESP32_S3_Socket_2x22_Row25.40mm_PENDING_VERIFY` | **`PENDING` (1 quyết định chọn Mẫu A hay Mẫu B)** |

---

## 6. NHỮNG QUYẾT ĐỊNH CẦN NGƯỜI DÙNG PHÊ DUYỆT ĐỂ BẮT ĐẦU GATE 2 (PLACEMENT)

Để chính thức khóa Gate 1.5 và chuyển sang **GATE 2 (Placement trên PCB 1 lớp `B.Cu`)**, xin bạn phê duyệt **3 quyết định ngắn gọn** sau:

1. **Quyết định 1 — Chọn Footprint `ESP32-S3` (`U1`)**:
   - Sau khi in thử tờ `ESP32_S3_FOOTPRINT_1TO1_CHECK.pdf` ở tỷ lệ `100% (Actual Size)` (hoặc đo khoảng cách 2 hàng chân của bo `ESP32-S3`), bo thực tế của bạn khớp với **MẪU A (`Row Pitch = 22.86 mm / 900 mil`)** hay **MẪU B (`Row Pitch = 25.40 mm / 1000 mil`)**?
2. **Quyết định 2 — Phê duyệt đổi nguồn `VCC` của `MicroSD` (`J1` Pin 5) sang `5V_SYS`**:
   - Bạn có đồng ý áp dụng thay đổi **đổi chân `Pin 5 (VCC)` của `J1` từ `3V3_SYS` sang `5V_SYS`** trên schematic (để cấp đúng áp đầu vào cho IC `AMS1117-3.3` trên module thẻ nhớ, trong khi giao tiếp SPI với `ESP32-S3` vẫn giữ nguyên mức logic $3.3\text{V}$ an toàn) không?
3. **Quyết định 3 — Xác nhận thông tin `Module Sim` (`U5`)**:
   - Chữ khắc thực tế trên nắp kim loại module SIM của bạn là **`A7680C`** hay **`A7682S`**, và khi chạy thử nghiệm thực tế bạn cấp nguồn mấy Volt vào chân `VCC` (Pin 1 của `J6`)? (Nếu chưa cần gộp chung với `5V_SYS`, ta có thể giữ nguyên domino `J3` `SIM_PWR` độc lập trên PCB để đảm bảo an toàn tuyệt đối).

