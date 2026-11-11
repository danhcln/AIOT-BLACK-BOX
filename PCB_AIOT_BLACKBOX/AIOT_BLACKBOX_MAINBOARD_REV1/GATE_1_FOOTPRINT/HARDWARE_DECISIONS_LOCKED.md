# BẢNG CHỐT THÔNG SỐ PHẦN CỨNG CHÍNH THỨC (`HARDWARE_DECISIONS_LOCKED.md`)

**Dự án:** Thiết kế Hộp Đen AIoT Thông Minh Phân Tích và Ghi Lại Sự Cố Xe Máy Điện  
**Thư mục Project KiCad:** `D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1`  
**Firmware chuẩn:** `D:\ĐỒ ÁN 2\filecodemain.cpp` (Giữ nguyên 100%, không sửa đổi)  
**Trạng thái:** **`LOCKED — ĐÃ CHỐT TOÀN BỘ PHẦN CỨNG & SCHEMATIC TRƯỚC PLACEMENT PCB 1 LỚP (GATE 2)`**

---

## 1. BẢNG TỔNG HỢP 4 QUYẾT ĐỊNH PHẦN CỨNG ĐÃ CHỐT

| STT | Hạng mục phần cứng | Thông số chính thức đã chốt (`LOCKED`) | Áp dụng trong Schematic & Thư viện PCB Local | Trạng thái |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **Footprint `ESP32-S3 N16R8` (`U1`)** | - Hai hàng header `1x22` (**44 chân**)<br>- Pitch dọc: **`2.54 mm`** (`100 mil`)<br>- Khoảng cách 2 hàng chân (**Row Pitch**): **`25.40 mm`** (`1000 mil`)<br>- Đánh số **Top-to-Bottom** (Trái `1..22`, Phải `23..44` — không dùng DIP-44) | - Footprint chính thức: `AIOT_Blackbox_Local:ESP32_S3_N16R8_Socket_2x22_P2.54mm_Row25.40mm_SingleLayer`<br>- Đã xóa hoàn toàn footprint `22.86 mm` khỏi thư viện local | **`LOCKED / VERIFIED`** |
| **2** | **Nguồn `MicroSD Breakout` (`J1`)** | - Đầu vào `VCC` (Pin 5) dùng **`5V`** (`5V_SYS`)<br>- Breakout có sẵn IC LDO `3.3V` (`U2`) + IC đệm mức logic (`U3`) cấp cho thẻ MicroSD<br>- SPI giữ nguyên theo firmware (`CS=GPIO10`, `MOSI=GPIO11`, `SCK=GPIO12`, `MISO=GPIO13`) | - Nối `5V_SYS → J1 Pin 5 (VCC)`<br>- Nối `GND → J1 Pin 6 (GND)`<br>- Footprint: `AIOT_Blackbox_Local:Module_MicroSD_Adapter_1x06_P2.54mm_SingleLayer` | **`LOCKED / VERIFIED`** |
| **3** | **Module SIM 4G (`U5`): Tên `A7680C` & Nguồn `5V`** | - Tên module thống nhất toàn dự án: **`A7680C`** (Breakout 4G LTE)<br>- Đầu vào `VCC` (Pin 1 trên J6) dùng **`5V`** qua nhánh nguồn riêng **`SIM_PWR`** tách hình sao từ `5V_SYS`<br>- Tụ lọc nguồn đặt sát nhánh SIM: **`C3 = 470µF` (Low-ESR)** + **`C4 = 100nF`**<br>- UART giữ nguyên theo firmware (`GPIO15 RX ← TXD`, `GPIO16 TX → RXD`, `RST = NC`) | - Symbol/Value `U5` đổi thành **`A7680C`** (`4G BREAKOUT`)<br>- Nối `5V_SYS → J3 (SIM_PWR_BRANCH) → SIM_PWR → U5 Pin 1 (VCC)`<br>- Bổ sung `C3 (470uF)`, `C4 (100nF)` và 4 điểm đo `TP1 (TP_5V)`, `TP2 (TP_3V3)`, `TP3 (TP_SIM_PWR)`, `TP4 (TP_GND)`<br>- Footprint: `AIOT_Blackbox_Local:Conn_SIM_Breakout_J6_1x05_P2.54mm_SingleLayer` | **`LOCKED / VERIFIED`** |
| **4** | **Chân dự phòng `BUZZER`, `CANCEL`, `LED_STATUS`** | - **`BUZZER_CTRL = GPIO5`** (`U1` Pin 5): Qua `R5 (1kΩ)` vào Base `Q1 (2SC1815)`, có điện trở kéo xuống **`R6 = 10kΩ` (`R_BE`)** từ Base xuống `GND`, Emitter nối `GND`, Collector kéo `BZ1 (-)` xuống mass, `BZ1 (+)` nối `5V_SYS`<br>- **`CANCEL_BUTTON = GPIO6`** (`U1` Pin 6): Nối nút nhấn `SW1` xuống `GND`, kéo lên `3V3_SYS` qua `R3 (10kΩ)`, lọc nhiễu `C2 (100nF)` xuống `GND`<br>- **`LED_STATUS = GPIO7`** (`U1` Pin 7): Qua `R4 (330Ω)` vào Anode `D1`, Cathode `D1` nối `GND`<br>- **`GPIO4`** (`U1` Pin 4): Để trống (`NC` dự phòng) | - Đã nối hoàn chỉnh trên `AIOT_BLACKBOX_MAINBOARD_REV1.kicad_sch` và xuất vào Netlist<br>- **Không sửa `filecodemain.cpp`**: Ghi nhận trạng thái *"Đã khóa chân phần cứng trên schematic/PCB để sẵn sàng lập trình ở phiên bản firmware tiếp theo"* | **`LOCKED / VERIFIED`** |

---

## 2. KIỂM TRA XUNG ĐỘT & TÍNH NHẤT QUÁN TOÀN HỆ THỐNG

1. **Không xung đột với các chân đang chạy trong `filecodemain.cpp`:**
   - I2C Bus (`OLED SSD1306` + `MPU6050` + `DS3231`): **`GPIO8` (`SDA`)**, **`GPIO9` (`SCL`)** — Giữ nguyên.
   - SPI Bus (`MicroSD`): **`GPIO10` (`CS`)**, **`GPIO11` (`MOSI`)**, **`GPIO12` (`SCK`)**, **`GPIO13` (`MISO`)** — Giữ nguyên.
   - UART1 (`SIM A7680C`): **`GPIO15` (`ESP_RX ← SIM_TXD`)**, **`GPIO16` (`ESP_TX → SIM_RXD`)** — Giữ nguyên.
   - UART2 (`GPS NEO-M8N`): **`GPIO17` (`ESP_TX → GPS_RXD`)**, **`GPIO18` (`ESP_RX ← GPS_TXD`)** — Giữ nguyên.
   - Dự phòng phần cứng đã khóa (`UI / Cảnh báo`): **`GPIO5` (`BUZZER_CTRL`)**, **`GPIO6` (`CANCEL`)**, **`GPIO7` (`LED_STATUS`)** — Nằm hoàn toàn ở cụm chân `GPIO5–GPIO7` bên sườn trái vật lý của ESP32-S3, không đụng chạm bất kỳ bus nào đang chạy.
2. **Đánh giá mạch Buzzer (`BZ1` + `Q1 2SC1815` + `R5 1kΩ` + `R6 10kΩ`):**
   - `BZ1` sử dụng **Active Buzzer 5V THT đường kính 12mm, pitch 7.62mm** (có mạch dao động bên trong, dòng tiêu thụ ~25–30 mA).
   - Điện trở kéo xuống **`R6 = 10kΩ` (`R_BE`)** giữ cực Base của `Q1` (`2SC1815`) ở mức `0V` khi chân `GPIO5` của ESP32-S3 đang ở trạng thái High-Z lúc mới cấp nguồn/boot, triệt tiêu hoàn toàn hiện tượng kêu誤 (false beep).
   - Đối với Active Buzzer piezo/transistor nội, xung ngược cảm ứng rất nhỏ; tuy nhiên thư viện local `AIOT_Blackbox_Local.pretty` đã chuẩn bị sẵn footprint `D_DO-41_SOD81_P10.16mm_SingleLayer` nếu người dùng muốn lắp thêm diode dập xung ngược (`1N4148`/`1N4007`) khi đổi sang còi từ tính cuộn dây (magnetic inductive buzzer).
3. **Kết quả kiểm tra ERC & Netlist (`kicad-cli`):**
   - **ERC (`kicad-cli sch erc`):** **`0 Errors, 0 Warnings`** (Không dùng `PWR_FLAG` giả để che lỗi).
   - **Netlist (`kicad-cli sch export netlist`):** **`Exit Code = 0, 0 Warnings`**, xuất đầy đủ **28 linh kiện** với 100% footprint thuộc thư viện local `AIOT_Blackbox_Local.pretty`.
