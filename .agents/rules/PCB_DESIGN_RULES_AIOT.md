# BỘ QUY TẮC THIẾT KẾ PCB CARRIER BOARD AIOT BLACK BOX

**Dự án:** THIẾT KẾ HỘP ĐEN AIoT THÔNG MINH PHÂN TÍCH VÀ GHI LẠI SỰ CỐ XE MÁY ĐIỆN  
**Thư mục làm việc:** `D:\ĐỒ ÁN 2`  
**File quy tắc:** `D:\ĐỒ ÁN 2\.agents\rules\PCB_DESIGN_RULES_AIOT.md`  
**Phiên bản:** REV 1.0.0 (Ban hành phục vụ thiết kế bo mạch chính Carrier Board)  
**Tình trạng ràng buộc:** BẮT BUỘC TUÂN THỦ (MANDATORY ENFORCEMENT)

---

## MỤC LỤC TỔNG QUAN

- [PHẦN I: TỔNG QUAN HỆ THỐNG VÀ HIỆN TRẠNG DỰ ÁN](#phần-i-tổng-quan-hệ-thống-và-hiện-trạng-dự-án)
  - [1. Phân cấp thẩm quyền thiết kế](#1-phân-cấp-thẩm-quyền-thiết-kế)
  - [2. Kết quả kiểm tra Firmware thực tế](#2-kết-quả-kiểm-tra-firmware-thực-tế)
  - [3. Kết quả kiểm tra Schematic và Bảng đối chiếu xung đột](#3-kết-quả-kiểm-tra-schematic-và-bảng-đối-chiếu-xung-đột)
  - [4. Danh sách chức năng chưa gán GPIO (UNASSIGNED)](#4-danh-sách-chức-năng-chưa-gán-gpio-unassigned)
  - [5. Hiện trạng khối nguồn phần cứng](#5-hiện-trạng-khối-nguồn-phần-cứng)
- [PHẦN II: 21 QUY TẮC THIẾT KẾ PCB BẮT BUỘC (RULE 01 - RULE 21)](#phần-ii-21-quy-tắc-thiết-kế-pcb-bắt-buộc-rule-01---rule-21)
  - [RULE 01 – Ưu tiên PCB 1 lớp (Single-Layer Copper Priority)](#rule-01--ưu-tiên-pcb-1-lớp-single-layer-copper-priority)
  - [RULE 02 – Giữ nguyên GPIO theo code (Firmware Pinout Authority)](#rule-02--giữ-nguyên-gpio-theo-code-firmware-pinout-authority)
  - [RULE 03 – Kiểm tra schematic trước PCB (Schematic Integrity Audit)](#rule-03--kiểm-tra-schematic-trước-pcb-schematic-integrity-audit)
  - [RULE 04 – Xác minh footprint (Physical Footprint Verification)](#rule-04--xác-minh-footprint-physical-footprint-verification)
  - [RULE 05 – Thiết kế theo module có sẵn (Carrier Board Paradigm)](#rule-05--thiết-kế-theo-module-có-sẵn-carrier-board-paradigm)
  - [RULE 06 – Nguồn chính (Primary Power Architecture - UPS LX-2BUPS)](#rule-06--nguồn-chính-primary-power-architecture---ups-lx-2bups)
  - [RULE 07 – Nguồn 3.3V độc lập (Independent 3.3V System Rail)](#rule-07--nguồn-33v-độc-lập-independent-33v-system-rail)
  - [RULE 08 – Nguồn SIM 4G (High-Priority SIM_PWR Path)](#rule-08--nguồn-sim-4g-high-priority-sim_pwr-path)
  - [RULE 09 – Độ rộng đường mạch (Net Classes & Trace Width Calculation)](#rule-09--độ-rộng-đường-mạch-net-classes--trace-width-calculation)
  - [RULE 10 – Quy tắc GND một lớp (Single-Layer Ground Strategy)](#rule-10--quy-tắc-gnd-một-lớp-single-layer-ground-strategy)
  - [RULE 11 – Jumper trên PCB một lớp (Wire Jumper & 0Ω Protocol)](#rule-11--jumper-trên-pcb-một-lớp-wire-jumper--0ω-protocol)
  - [RULE 12 – Bố trí ESP32 (ESP32-S3 Placement & Antenna Keepout)](#rule-12--bố-trí-esp32-esp32-s3-placement--antenna-keepout)
  - [RULE 13 – Bố trí GPS và SIM (RF Coexistence & Noise Immunity)](#rule-13--bố-trí-gps-và-sim-rf-coexistence--noise-immunity)
  - [RULE 14 – Bố trí MPU6050 (IMU Mechanical Stability & Axis Alignment)](#rule-14--bố-trí-mpu6050-imu-mechanical-stability--axis-alignment)
  - [RULE 15 – Quy tắc đi dây tín hiệu (Signal Routing Discipline)](#rule-15--quy-tắc-đi-dây-tín-hiệu-signal-routing-discipline)
  - [RULE 16 – Vị trí linh kiện để dễ sử dụng (Ergonomics & Serviceability)](#rule-16--vị-trí-linh-kiện-để-dễ-sử-dụng-ergonomics--serviceability)
  - [RULE 17 – Cơ khí và độ bền (Mechanical Durability & Mounting)](#rule-17--cơ-khí-và-độ-bền-mechanical-durability--mounting)
  - [RULE 18 – Silkscreen (Silkscreen Marking & Clearances)](#rule-18--silkscreen-silkscreen-marking--clearances)
  - [RULE 19 – Test point (Test Point Strategy)](#rule-19--test-point-test-point-strategy)
  - [RULE 20 – DRC và kiểm tra chế tạo (DRC & Fabrication Verification)](#rule-20--drc-và-kiểm-tra-chế-tạo-drc--fabrication-verification)
  - [RULE 21 – Điều kiện chuyển sang PCB hai lớp (Two-Layer Fallback Feasibility)](#rule-21--điều-kiện-chuyển-sang-pcb-hai-lớp-two-layer-fallback-feasibility)
- [PHẦN III: QUY TRÌNH THIẾT KẾ PCB THEO 7 GATE](#phần-iii-quy-trình-thiết-kế-pcb-theo-7-gate)
  - [GATE 0 – Audit (Kiểm tra Code, Schematic, GPIO và Nguồn)](#gate-0--audit-kiểm-tra-code-schematic-gpio-và-nguồn)
  - [GATE 1 – Footprint (Xác minh Footprint, Pinout và Cơ khí)](#gate-1--footprint-xác-minh-footprint-pinout-và-cơ-khí)
  - [GATE 2 – Placement (Bố trí Module, Vùng cấm RF, Đường nguồn ngắn)](#gate-2--placement-bố-trí-module-vùng-cấm-rf-đường-nguồn-ngắn)
  - [GATE 3 – Single-Layer Routing (Đi dây B.Cu, Không Via, Tối ưu Jumper)](#gate-3--single-layer-routing-đi-dây-bcu-không-via-tối-ưu-jumper)
  - [GATE 4 – Power Integrity (Kiểm tra Dòng tải, Sụt áp SIM, Vùng GND)](#gate-4--power-integrity-kiểm-tra-dòng-tải-sụt-áp-sim-vùng-gnd)
  - [GATE 5 – Verification (ERC, DRC, Kiểm tra 3D và Tiêu chuẩn)](#gate-5--verification-erc-drc-kiểm-tra-3d-và-tiêu-chuẩn)
  - [GATE 6 – Manufacturing (Xuất Gerber 1 lớp, Drill, BOM, Hướng dẫn lắp ráp)](#gate-6--manufacturing-xuất-gerber-1-lớp-drill-bom-hướng-dẫn-lắp-ráp)
- [PHẦN IV: THAM CHIẾU KỸ THUẬT VÀ PHÂN LOẠI TIÊU CHUẨN](#phần-iv-tham-chiếu-kỹ-thuật-và-phân-loại-tiêu-chuẩn)
  - [1. Danh mục tài liệu tham khảo chính thức](#1-danh-mục-tài-liệu-tham-khảo-chính-thức)
  - [2. Bảng phân định mức độ kỹ thuật](#2-bảng-phân-định-mức-độ-kỹ-thuật)

---

# PHẦN I: TỔNG QUAN HỆ THỐNG VÀ HIỆN TRẠNG DỰ ÁN

## 1. Phân cấp thẩm quyền thiết kế

Tất cả các hành động thiết kế mạch in (PCB) phải tuân theo thứ bậc thẩm quyền nghiêm ngặt sau:

```text
1. Phần cứng thực tế đã kiểm nghiệm / Datasheet chính hãng (Chân lý điện học)
   ↓
2. Firmware đang chạy thành công trên phần cứng thực tế (filecodemain.cpp)
   ↓
3. D:\ĐỒ ÁN 2\SCHEMATIC_DRAWING_RULES.md (Quy tắc trình bày & an toàn hệ thống)
   ↓
4. D:\ĐỒ ÁN 2\.agents\rules\PCB_DESIGN_RULES_AIOT.md (File luật thiết kế PCB này)
   ↓
5. Chỉ đạo trực tiếp của Người dùng (User Directives)
   ↓
6. Quy trình phối hợp phụ trợ (ECC Workflows / Planner / Verification)
```

> [!CRITICAL]
> **Nguyên tắc bất biến:** Tuyệt đối KHÔNG tự ý tráo đổi GPIO, thay đổi kiến trúc cấp nguồn, hoặc tự chọn chân vi điều khiển nhằm mục đích "đi dây cho dễ" hay "cho thuận tiện mạch in". Mọi sự sai lệch giữa firmware thực nghiệm và bản vẽ schematic phải được ghi nhận thành xung đột và trình người dùng phê duyệt trước khi can thiệp.

---

## 2. Kết quả kiểm tra Firmware thực tế

Kiểm tra toàn bộ không gian làm việc `D:\ĐỒ ÁN 2`, nguồn mã nguồn firmware duy nhất và đang chạy trực tiếp trên thiết bị thực tế là:

`D:\ĐỒ ÁN 2\filecodemain.cpp`

Bảng trích xuất chân phần cứng (Hardware Pin Mapping) từ `filecodemain.cpp`:

| Tên tín hiệu | Chân ESP32-S3 | Thiết bị ngoại vi kết nối | Thông số cấu hình / Giao thức | Ghi chú thực tế |
|---|---|---|---|---|
| `I2C_SDA_PIN` | **GPIO8** | OLED SSD1306, RTC DS3231, IMU MPU6050 | I2C Bus, Wire.setTimeOut(200) | Địa chỉ: OLED 0x3C, RTC 0x68, MPU 0x69 |
| `I2C_SCL_PIN` | **GPIO9** | OLED SSD1306, RTC DS3231, IMU MPU6050 | I2C Bus Clock | Kéo chung đường bus ngoại vi |
| `SD_CS_PIN` | **GPIO10** | Module thẻ nhớ MicroSD | SPI Chip Select (CS) | Tần số SPI SD_SCK_MHZ(16), Shared SPI |
| `SPI_MOSI_PIN`| **GPIO11** | Module thẻ nhớ MicroSD | SPI Master Out Slave In | Chân phần cứng chuẩn SPI ESP32-S3 |
| `SPI_SCK_PIN` | **GPIO12** | Module thẻ nhớ MicroSD | SPI Serial Clock | Đồng hồ bus dữ liệu thẻ nhớ |
| `SPI_MISO_PIN`| **GPIO13** | Module thẻ nhớ MicroSD | SPI Master In Slave Out | Chân dữ liệu phản hồi từ thẻ nhớ |
| `SIM_RX_PIN`  | **GPIO15** | Module 4G LTE SIMCom A7682S | UART2 RX (ESP32 nhận từ TXD của SIM) | Tốc độ Baud: 115200 bps |
| `SIM_TX_PIN`  | **GPIO16** | Module 4G LTE SIMCom A7682S | UART2 TX (ESP32 truyền vào RXD của SIM)| Tốc độ Baud: 115200 bps |
| `GPS_RX_PIN`  | **GPIO18** | Module định vị GPS NEO-M8N | UART1 RX (ESP32 nhận từ TX của GPS) | Tốc độ Baud: 9600 bps |
| `GPS_TX_PIN`  | **GPIO17** | Module định vị GPS NEO-M8N | UART1 TX (ESP32 truyền vào RX của GPS) | Tốc độ Baud: 9600 bps |

---

## 3. Kết quả kiểm tra Schematic và Bảng đối chiếu xung đột

Kiểm tra bản vẽ schematic tham chiếu mới nhất tại:
`D:\ĐỒ ÁN 2\Schematic_Thay\AIOT_BLACKBOX_PRESENTATION\AIOT_BLACKBOX_PRESENTATION.kicad_sch`

Phát hiện các điểm **XUNG ĐỘT NGHIÊM TRỌNG** giữa Firmware đang chạy và Schematic:

| Khối chức năng | Chân trong Firmware (`filecodemain.cpp`) | Chân trong Schematic (`AIOT_BLACKBOX_PRESENTATION`) | Bản chất xung đột | Hậu quả nếu đi dây theo Schematic | Hướng xử lý bắt buộc |
|---|---|---|---|---|---|
| **Giao tiếp SIM 4G** | **GPIO15 (RX)<br>GPIO16 (TX)** | **GPIO43 (TX)<br>GPIO44 (RX)** | Mã nguồn thực tế dùng GPIO15/16 cho UART SIM. Schematic lại nối SIM vào GPIO43/44 (U0TXD/U0RXD). | ESP32 nạp code sẽ không giao tiếp được với SIM A7682S; UART0 bị chiếm dụng làm mất chức năng nạp/debug USB CDC. | **PCB BẮT BUỘC theo Firmware: GPIO15 (RX), GPIO16 (TX).** Đề xuất cập nhật lại Schematic. |
| **Xung đột GPIO15** | **SIM_RX_PIN** | **BUZZER_CTRL** | Trong schematic, GPIO15 đang nối vào mạch kích Transistor còi Buzzer. Trong code, GPIO15 là chân thu UART SIM. | Tín hiệu nhận từ SIM bị mạch còi kéo tụt áp/gây nhiễu; còi kêu loạn xạ theo bản tin UART và SIM mất kết nối. | **TÁCH NGAY LẬP TỨC**: Không nối Buzzer vào GPIO15. Buzzer chưa có trong code -> chuyển trạng thái `UNASSIGNED`. |
| **MicroSD Chip Select** | **GPIO10 (SD_CS)** | **GPIO14 (SD_CS)** | Code dùng GPIO10 điều khiển chọn thẻ MicroSD. Schematic dùng GPIO14. | Thẻ MicroSD không thể khởi tạo (`sdOK = false`) vì sai chân chọn chip CS. | **PCB BẮT BUỘC theo Firmware: SD_CS = GPIO10.** |
| **Ngắt MPU6050** | *Không sử dụng* | **GPIO10 (IMU_INT)** | Schematic gán GPIO10 cho chân INT của MPU6050, nhưng GPIO10 đã bị code chiếm làm SD_CS. | Trùng chân phần cứng nghiêm trọng giữa thẻ nhớ và cảm biến quán tính. | **PCB theo Firmware:** GPIO10 là SD_CS. Chân INT của MPU6050 đánh dấu `UNASSIGNED` (Code đọc MPU bằng polling I2C). |
| **Giao tiếp GPS UART**| **GPIO17 (TX)<br>GPIO18 (RX)** | **GPIO17 (TX)<br>GPIO18 (RX)** | **KHỚP HOÀN TOÀN** giữa Code và Schematic. | Không có xung đột. | Duy trì chính xác kết nối chéo: ESP_TX17 -> GPS_RX, ESP_RX18 -> GPS_TX. |
| **Giao tiếp I2C Bus** | **GPIO8 (SDA)<br>GPIO9 (SCL)** | **GPIO8 (SDA)<br>GPIO9 (SCL)** | **KHỚP HOÀN TOÀN** giữa Code và Schematic. | Không có xung đột. | Duy trì bus I2C chung cho OLED, RTC DS3231, MPU6050. |
| **Giao tiếp SPI Bus** | **GPIO11 (MOSI)<br>GPIO12 (SCK)<br>GPIO13 (MISO)** | **GPIO11 (MOSI)<br>GPIO12 (SCK)<br>GPIO13 (MISO)** | **KHỚP HOÀN TOÀN** giữa Code và Schematic. | Không có xung đột. | Duy trì bus SPI tốc độ cao cho MicroSD. |

---

## 4. Danh sách chức năng chưa gán GPIO (UNASSIGNED)

Trong `filecodemain.cpp`, các ngoại vi sau **CHƯA ĐƯỢC LẬP TRÌNH VÀ CHƯA GÁN CHÂN GPIO**:

1. **Còi báo động (BUZZER_CTRL):** `UNASSIGNED` (Schematic cũ dùng GPIO15 nhưng đã bị SIM chiếm).
2. **Nút nhấn hủy cảnh báo (CANCEL BUTTON):** `UNASSIGNED` (Schematic cũ dùng GPIO6, code chưa đọc).
3. **Đèn LED chỉ thị trạng thái (LED_STATUS):** `UNASSIGNED` (Schematic cũ dùng GPIO7, code chưa dùng).
4. **Chân ngắt cảm biến MPU6050 (IMU_INT):** `UNASSIGNED` (Firmware đọc bằng polling chu kỳ 500ms).
5. **Xung đồng bộ vệ tinh GPS (GNSS_PPS):** `UNASSIGNED` (Firmware đồng bộ giờ qua bản tin NMEA và mạng 4G NITZ).
6. **Đo điện áp pin (ADC_VBAT_SENSE):** `UNASSIGNED` (Schematic cũ dự kiến GPIO1, code chưa khởi tạo ADC).
7. **Chân bật nguồn SIM (4G_PWRKEY / 4G_STATUS):** `UNASSIGNED` (Breakout A7682S đang dùng chế độ tự bật nguồn phần cứng khi cấp điện).

> [!WARNING]
> **Quy định nghiêm ngặt:** Cấm tự tiện gán GPIO mới cho các chức năng trên khi thiết kế PCB. Các chân này trên header của bo mạch phải để ở dạng chân chờ (test header/pad chờ) hoặc nối đúng với chân schematic đã được xác nhận, tuyệt đối không đấu nối ngầm gây chập cháy hay chiếm dụng chân của firmware đang chạy.

---

## 5. Hiện trạng khối nguồn phần cứng

1. **Khối nguồn sơ cấp (Primary Power Source):**
   - Thiết bị sử dụng Module nguồn UPS chuyên dụng **LX-2BUPS 5V/3A** tích hợp 2 khay pin Li-ion 18650 mắc song song.
   - Bo mạch chủ PCB là bo mạch mang (Carrier Board), **KHÔNG** tích hợp mạch sạc pin hay boost DC-DC phức tạp trên bo nhằm đảm bảo độ tin cậy.
   - Điểm nhận nguồn chính của PCB:
     - `UPS+` nối vào đường nguồn hệ thống **`5V_SYS`**.
     - `UPS-` nối vào đường trở về chung **`GND`**.
   - Nguồn sạc ngoài (USB-C/VBUS) cắm trực tiếp vào module LX-2BUPS, không đi qua mạch đồng của bo carrier.
2. **Khối hạ áp 3.3V (Peripheral Power Source):**
   - Cấu trúc: `5V_SYS` → **Module Buck 3.3V độc lập** → `3V3_SYS`.
   - ESP32-S3 DevKit nhận `5V_SYS` tại chân `5V` (qua diode/LDO nội bộ của DevKit cấp riêng cho chip).
   - Tuyệt đối **KHÔNG** lấy chân `3V3` của ESP32 để gánh dòng cho các cảm biến, OLED, RTC, GPS.

---

# PHẦN II: 21 QUY TẮC THIẾT KẾ PCB BẮT BUỘC (RULE 01 - RULE 21)

---

### RULE 01 – Ưu tiên PCB 1 lớp (Single-Layer Copper Priority)

1. **Mục tiêu chế tạo:** Toàn bộ mạch in phục vụ đồ án được tối ưu hóa cho công nghệ gia công **PCB 1 lớp đồng (Single-Sided PCB)** nhằm giảm giá thành, dễ tự làm mạch thủ công (etching/phay CNC) hoặc đặt gia công giá rẻ.
2. **Quy định lớp đồng:**
   - **Chỉ đi dây dẫn tín hiệu và nguồn trên lớp đáy `B.Cu` (Bottom Copper).**
   - **Tuyệt đối cấm đi dây trên lớp mặt `F.Cu` (Top Copper).**
   - **Tuyệt đối cấm sử dụng lỗ xuyên lớp (Via) để chuyển lớp mạch tín hiệu.**
   - **Tuyệt đối cấm tạo vùng phủ đồng (Copper Pour / Zone) trên `F.Cu`.**
3. **Bố trí linh kiện và mối hàn:**
   - Linh kiện cắm (Through-Hole), module breakout, header đực/cái được bố trí ở mặt trên (`F.Cu`).
   - Mối hàn và toàn bộ đường mạch đồng nằm ở mặt dưới (`B.Cu`).
4. **Cấu hình phần mềm KiCad:**
   - Trong KiCad Board Setup, có thể để cấu hình 2 lớp đồng mặc định (`F.Cu` và `B.Cu`) để biên tập đồ họa, nhưng thực tế thiết kế chỉ cho phép thực thể đồng tồn tại trên `B.Cu`.
   - Khi xuất file chế tạo (Gerber), phải trao đổi với xưởng gia công về quy chuẩn xuất Gerber bo 1 lớp (chỉ xuất `B.Cu`, `B.Mask`, `F.Silk`, `Edge.Cuts` và file khoan `Drill`).
5. **Cấm tự ý chuyển lớp:** Không được tự ý chuyển sang thiết kế 2 lớp khi chưa thực hiện đầy đủ các bước tối ưu vị trí (Placement) và phương án Jumper theo [RULE 11](#rule-11--jumper-trên-pcb-một-lớp-wire-jumper--0ω-protocol) và [RULE 21](#rule-21--điều-kiện-chuyển-sang-pcb-hai-lớp-two-layer-fallback-feasibility).

---

### RULE 02 – Giữ nguyên GPIO theo code (Firmware Pinout Authority)

1. **Nguồn chân lý tối cao:** Firmware `D:\ĐỒ ÁN 2\filecodemain.cpp` đang chạy ổn định là chuẩn mực duy nhất để xác định kết nối GPIO của các chức năng đã lập trình.
2. **Không tự đổi GPIO:**
   - Cấm thay đổi GPIO để đường mạch đi thẳng hơn hoặc tránh giao cắt.
   - Cấm sửa code firmware để "ép cho khớp" với bản vẽ schematic lỗi thời.
3. **Xử lý xung đột GPIO:**
   - Bắt buộc áp dụng bảng phân chân thực tế tại [Phần I, Mục 2](#2-kết-quả-kiểm-tra-firmware-thực-tế):
     - `SD_CS`: **GPIO10** (Loại bỏ GPIO14 của schematic cũ).
     - `SIM_UART`: **GPIO15 (RX) / GPIO16 (TX)** (Loại bỏ GPIO43/44 của schematic cũ).
     - `GPS_UART`: **GPIO17 (TX) / GPIO18 (RX)**.
     - `I2C_BUS`: **GPIO8 (SDA) / GPIO9 (SCL)**.
     - `SPI_BUS`: **GPIO11 (MOSI) / GPIO12 (SCK) / GPIO13 (MISO)**.
4. **Quản lý chân chưa gán:** Các chức năng Buzzer, CANCEL, LED, IMU INT, GNSS PPS, ADC_VBAT_SENSE phải giữ nguyên trạng thái `UNASSIGNED`, không được tự ý gán vào các chân GPIO còn trống của ESP32-S3 khi chưa có yêu cầu bằng văn bản từ người dùng.

---

### RULE 03 – Kiểm tra schematic trước PCB (Schematic Integrity Audit)

1. **Không dùng PDF làm Netlist:** Tuyệt đối không suy đoán netlist từ tài liệu PDF. Nguồn tạo Netlist duy nhất phải là file schematic KiCad chính thức:
   `D:\ĐỒ ÁN 2\Schematic_Thay\AIOT_BLACKBOX_PRESENTATION\AIOT_BLACKBOX_PRESENTATION.kicad_sch`
2. **Kiểm tra liên kết điện trước khi layout:**
   - Xác minh toàn bộ net nguồn dương (`5V_SYS`, `3V3_SYS`, `SIM_PWR`) và `GND` được kết nối thông suốt, không có net trôi nổi.
   - Kiểm tra kỹ các cặp tín hiệu vi sai/truyền thông: TX phải chéo sang RX của đối tác, SDA/SCL song song, SPI đúng chân định tuyến.
   - Toàn bộ các chân vật lý không sử dụng trên module breakout phải được gắn cờ `no_connect` trong schematic.
3. **Thực thi ERC (Electrical Rules Check):**
   - Chạy lệnh kiểm tra ERC bằng `kicad-cli sch erc`. Báo cáo đầy đủ mọi lỗi và cảnh báo.
   - Nghiêm cấm hành vi đổi kiểu điện học của chân linh kiện (ví dụ đổi pin `power_in` thành `passive` hoặc `unspecified`) chỉ nhằm mục đích dập tắt cảnh báo của trình kiểm tra ERC.

---

### RULE 04 – Xác minh footprint (Physical Footprint Verification)

1. **Cấm phỏng đoán thông số cơ khí:** Nghiêm cấm tự vẽ hoặc phỏng đoán kích thước các module phần cứng, bao gồm:
   - Khoảng cách giữa các hàng chân (Row Pitch) và khoảng cách giữa các chân kề nhau (Pin Pitch).
   - Thứ tự chân (Pinout order), quy ước chân số 1 (Pin 1 index).
   - Chiều cắm module (hướng cổng USB, hướng khe cắm anten, hướng khe thẻ nhớ).
   - Chiều cao linh kiện và vị trí lỗ bắt vít định vị trên module.
2. **Danh mục footprint module bắt buộc kiểm tra thực tế:**
   - **ESP32-S3-DevKitC-1 N16R8:** Chuẩn 44 chân cắm (2 hàng x 22 chân, pitch 2.54mm, khoảng cách hàng 25.4mm / 1000 mil).
   - **OLED SSD1306 0.96 inch:** Chuẩn 4 chân cắm (GND, VCC, SCL, SDA hoặc VCC, GND, SCL, SDA - cực kỳ nguy hiểm, phải đo thực tế chân 1 là GND hay VCC).
   - **MPU6050 (GY-521):** Chuẩn 8 chân cắm đơn (VCC, GND, SCL, SDA, XDA, XCL, AD0, INT).
   - **RTC DS3231:** Chuẩn 6 chân cắm (32K, SQW, SCL, SDA, VCC, GND).
   - **GPS NEO-M8N / GY-NEO6MV2:** Chuẩn 5 chân (VCC, RX, TX, GND, PPS).
   - **MicroSD Breakout Board:** Chuẩn 6 chân SPI (GND, VCC, MISO, MOSI, SCK, CS).
   - **SIM A7682S Breakout:** Kiểm tra chính xác chân nguồn (VCC/VBAT), chân GND, chân TXD/RXD, chân PWRKEY/RST.
   - **Module Buck DC-DC 3.3V:** Xác minh kích thước module (ví dụ Mini-360: 4 chân góc IN+, IN-, OUT+, OUT-).
3. **Phương án an toàn khi chưa có mẫu thực:** Nếu chưa cầm trên tay linh kiện thực tế để dùng thước kẹp cặp cơ khí, **BẮT BUỘC sử dụng socket cắm header hàng rào cái (Female Pin Header pitch 2.54mm)** để nối dây linh hoạt, tuyệt đối không tạo footprint hàn chết giả định.

---

### RULE 05 – Thiết kế theo module có sẵn (Carrier Board Paradigm)

1. **Bản chất bo mạch:** Bo mạch PCB của dự án là **Carrier Board / Motherboard** đóng vai trò kết nối, cố định và phân phối nguồn/tín hiệu cho các module chức năng bán sẵn trên thị trường.
2. **Không tái thiết kế mạch nội vi:**
   - Không thiết kế lại mạch chip vi điều khiển ESP32-S3 (dùng trọn gói DevKitC-1).
   - Không thiết kế lại mạch cao tần RF hay mạch nguồn bên trong module SIM A7682S.
   - Không thiết kế lại mạch RF GPS, mạch đo thạch anh RTC, mạch lọc IMU.
   - Không thiết kế lại khối sạc pin TP4056/UPS trên bo chính.
3. **Khả năng tháo lắp và bảo trì:**
   - Toàn bộ các module đắt tiền hoặc có khả năng hỏng hóc (ESP32, SIM, GPS, OLED, MicroSD, MPU6050, Buck) phải được gắn lên bo carrier thông qua hàng rào socket cái (Female Header Strip).
   - Cho phép người dùng dễ dàng rút module ra đo kiểm độc lập, nâng cấp hoặc thay thế khi gặp sự cố mà không cần rã hàn làm hỏng mạch in.

---

### RULE 06 – Nguồn chính (Primary Power Architecture - UPS LX-2BUPS)

1. **Cấu trúc nguồn sơ cấp:**
   - Sử dụng module nguồn dự phòng **LX-2BUPS 5V/3A** tích hợp 2 cell pin Li-ion 18650 làm nguồn cấp năng lượng chính cho toàn bộ hệ thống hộp đen hoạt động liên tục trên xe máy.
   - Cổng giao tiếp nguồn trên bo carrier:
     - `UPS+` → Kết nối trực tiếp vào net **`5V_SYS`**.
     - `UPS-` → Kết nối trực tiếp vào net **`GND`**.
2. **Định mức công suất và thực nghiệm:**
   - Thông số 5V/3A của module thương mại là thông số danh định đỉnh (Peak Rating). Không được coi đây là mức dòng tải liên tục (Continuous Load) ổn định ở nhiệt độ cao trong cốp xe máy.
   - Carrier board phải chịu được dòng đỉnh 2.5A mà không gây sụt áp quá 0.2V trên đường mạch đồng.
3. **Bố trí cổng nguồn và lọc nhiễu:**
   - Cổng vào nguồn chính từ UPS phải sử dụng **Terminal Block bắt vít 2 pin pitch 5.08mm** (hoặc XH2.54 có khóa cơ khí chống cắm ngược).
   - In rõ ký hiệu cực tính **`+`** và **`-`** cạnh terminal.
   - Bố trí ngay cạnh terminal nguồn:
     - 01 Test Point cho `5V_SYS` và 01 Test Point cho `GND`.
     - Vị trí chân tụ hóa/tụ nhôm kích thước lớn (1000µF / 16V Low-ESR) mắc song song với tụ gốm 100nF để gánh dòng đỉnh và chống sụt áp nguồn hệ thống.

---

### RULE 07 – Nguồn 3.3V độc lập (Independent 3.3V System Rail)

1. **Kiến trúc phân phối:**
   ```text
   5V_SYS (Từ UPS) ───► Module Buck 3.3V ───► 3V3_SYS ───► Cảm biến & Ngoại vi 3.3V
   5V_SYS (Từ UPS) ───► ESP32-S3 DevKit (Chân 5V) ───► LDO nội ESP32 tự cấp cho Chip
   ```
2. **Cấm dùng ESP32 làm nguồn trung tâm:**
   - **Tuyệt đối cấm** lấy chân nguồn `3V3` của bo ESP32-S3-DevKitC-1 để cấp điện nuôi các module ngoại vi bên ngoài (OLED, RTC, MPU6050, GPS, MicroSD). LDO tích hợp trên DevKit chỉ thiết kế đủ tải cho chip ESP32 và Flash/PSRAM; việc kéo dòng ngoại vi sẽ làm chip nóng cục bộ, sụt áp gây lỗi Reset CPU ngẫu nhiên.
3. **Cấm đấu song song nguồn:** Tuyệt đối cấm nối tắt đầu ra `3V3_SYS` của module Buck với chân `3V3` của ESP32. Việc đấu song song hai bộ ổn áp sẽ gây dòng hồi xung đột phá hỏng linh kiện.
4. **Phạm vi cấp tải của `3V3_SYS`:** Chỉ cấp nguồn `3V3_SYS` cho các module đã được xác minh làm việc ở mức 3.3V.
5. **Điểm đo kiểm và chân kết nối:**
   - Bắt buộc bố trí Test Point riêng biệt cho đường **`3V3_SYS`**.
   - Nếu chưa chốt mã module Buck cố định, sử dụng cụm chân cắm Header 4 pin linh hoạt (IN+, IN-, OUT+, OUT-) để có thể cắm module Mini-360 hoặc LM2596.

---

### RULE 08 – Nguồn SIM 4G (High-Priority SIM_PWR Path)

1. **Đặc tính tải khắt khe của Module 4G LTE:**
   - Module SIMCom A7682S khi phát sóng truyền gói dữ liệu lên trạm BTS (4G TX burst) tiêu thụ các xung dòng cực đại tức thời lên tới **2.0A** với thời gian tăng cạnh xung cực nhanh (micro-giây).
   - Nếu đường nguồn bị nghẽn trở kháng, điện áp sẽ sụt sâu dưới ngưỡng 3.4V làm module SIM bị khởi động lại (Brown-out Reset) ngay lập tức.
2. **Quy tắc thiết kế đường `SIM_PWR`:**
   - Tạo đường nguồn **`SIM_PWR`** độc lập hoặc đường **`5V_SYS`** chuyên dụng cho SIM tách riêng từ gốc tụ nguồn chính.
   - Chiều dài đường mạch từ tụ nguồn đến connector SIM phải **ngắn nhất có thể**, độ rộng đường mạch lớn (tối thiểu 2.0mm - 2.5mm hoặc phủ đồng diện tích lớn).
   - Đường hồi tiếp dòng `GND` của SIM phải cực kỳ thông thoáng, chạy thẳng về âm tụ nguồn, không đi vòng vèo qua các cảm biến nhạy cảm.
3. **Mạch lọc đặt sát chân SIM:**
   - Bắt buộc bố trí vị trí đặt tụ điện ngay sát chân cấp nguồn của SIM:
     - 01 tụ hóa hoặc Tantalum dung lượng lớn (470µF – 1000µF Low-ESR) để bù năng lượng xung dòng.
     - 01 tụ gốm 100nF dập nhiễu tần số thấp.
     - 01 tụ gốm 33pF và 01 tụ 10pF dập nhiễu sóng cao tần RF băng tần 900MHz / 1800MHz.
4. **Cách ly tuyến đi dây:** Tuyệt đối cấm chạy đường nguồn SIM đi xuyên qua bên dưới hoặc đi song song sát cạnh các đường tín hiệu của ESP32 và cảm biến.
5. **Xác minh điện áp Breakout SIM:**
   - Kiểm tra kỹ bo breakout A7682S thực tế có tích hợp sẵn mạch diode/LDO hạ áp hay không. Nếu bo breakout nhận trực tiếp mức 3.8V - 4.2V (VBAT) thì cấm cắm thẳng 5V. Trường hợp chưa chắc chắn, ghi rõ nhãn **`NEEDS VERIFICATION`** và để chân jumper lựa chọn nguồn (5V hoặc Buck riêng).
   - Phân biệt chính xác giữa chân bật nguồn `PWRKEY` (kích hoạt bằng kéo xuống GND khoảng 1s) và chân `RESET` (chỉ dùng khi reset cứng), cấm đấu nhầm hai chân này.

---

### RULE 09 – Độ rộng đường mạch (Net Classes & Trace Width Calculation)

1. **Phân chia lớp tín hiệu (Net Classes) trong KiCad:**
   Bắt buộc thiết lập các Net Class với thông số hình học rõ ràng trong Board Setup:

| Tên Net Class | Danh sách đường mạng đại diện | Dòng tải thiết kế | Độ rộng tối thiểu (1 oz Cu) | Độ rộng khuyến nghị | Khoảng cách cách ly (Clearance) |
|---|---|---|---|---|---|
| **SIGNAL** | Các đường logic GPIO thông thường | < 10 mA | 0.25 mm (10 mil) | **0.30 mm (12 mil)** | 0.25 mm (10 mil) |
| **I2C** | `I2C0_SDA`, `I2C0_SCL` | < 10 mA | 0.30 mm (12 mil) | **0.35 mm (14 mil)** | 0.30 mm (12 mil) |
| **UART** | `SIM_TX`, `SIM_RX`, `GPS_TX`, `GPS_RX` | < 10 mA | 0.30 mm (12 mil) | **0.35 mm (14 mil)** | 0.30 mm (12 mil) |
| **SPI** | `SPI_MOSI`, `SPI_MISO`, `SPI_SCK`, `SD_CS` | < 20 mA | 0.30 mm (12 mil) | **0.35 mm (14 mil)** | 0.30 mm (12 mil) |
| **3V3_POWER** | `3V3_SYS` (Cấp OLED, RTC, MPU, GPS, SD) | ~500 mA | 0.60 mm (24 mil) | **0.80 mm - 1.0 mm** | 0.30 mm (12 mil) |
| **5V_POWER** | `5V_SYS` (Đầu ra UPS, cấp ESP32, còi) | ~1.5 A | 1.20 mm (48 mil) | **1.5 mm - 2.0 mm** | 0.40 mm (16 mil) |
| **SIM_POWER** | `SIM_PWR` (Cấp dòng xung đỉnh module 4G) | Đỉnh 2.0 A | 1.80 mm (72 mil) | **2.5 mm hoặc Phủ đồng**| 0.50 mm (20 mil) |
| **GND** | `GND` (Đường hồi dòng toàn hệ thống) | Tổng dòng về | 1.50 mm (60 mil) | **Phủ đồng toàn vùng B.Cu**| 0.40 mm (16 mil) |

2. **Cơ sở tính toán đường mạch:**
   - Áp dụng tiêu chuẩn quốc tế **IPC-2221** và **IPC-2152** cho lớp đồng ngoài (External Traces, 1 oz/ft² tương đương độ dày đồng 35 µm) với độ tăng nhiệt cho phép $\Delta T \le 10^\circ\text{C}$:
     $$I = k \cdot \Delta T^{0.44} \cdot A^{0.725}$$
   - Tuyệt đối cấm áp dụng một độ rộng đường mạch mảnh (như 0.25mm) cho toàn bộ bo mạch hoặc cho các đường dẫn nguồn công suất.

---

### RULE 10 – Quy tắc GND một lớp (Single-Layer Ground Strategy)

1. **Chiến lược phủ đồng mặt đáy:**
   - Vì thiết kế là PCB 1 lớp (`B.Cu`), toàn bộ diện tích trống còn lại sau khi đi dây bắt buộc phải được phủ đồng làm mặt phẳng tiếp địa mass (**GND Copper Pour / Filled Zone**).
   - Không được lầm tưởng vùng phủ đồng này là một mặt phẳng GND hoàn hảo (Ideal Solid Plane). Do bị các đường tín hiệu trên cùng lớp `B.Cu` chia cắt, GND một lớp rất dễ bị phân mảnh thành nhiều dải hẹp.
2. **Tránh chia cắt và đảo đồng cô lập (Orphan/Island Copper):**
   - Cấm để xuất hiện các vùng đồng GND cô lập không có đường dẫn về mass chính (phải đặt tùy chọn `Remove islands = Always` hoặc nối cầu jumper tiếp mass cho đảo đồng).
   - Tránh hiện tượng tạo ra các "nút cổ chai" GND (đoạn đồng kết nối siêu mảnh < 0.5mm giữa hai vùng mass lớn).
3. **Đường hồi dòng riêng cho tải công suất (Return Path Integrity):**
   - Tách biệt rõ ràng đường hồi dòng mass của module SIM 4G và ESP32 về thẳng chân âm của tụ nguồn chính (Point of Load / Star Grounding cục bộ).
   - Tuyệt đối không để dòng xung 2A của SIM chạy qua dải đồng mass đang dùng chung làm điểm tựa điện áp cho cảm biến analog/I2C (MPU6050, ADC).
4. **Kiểm tra sau khi Refill Zone:** Sau mỗi lần thay đổi đường mạch hoặc vị trí linh kiện, bắt buộc phải bấm phím `B` trong KiCad để Refill Zone và dùng mắt kiểm tra thông suốt toàn bộ mạng GND.

---

### RULE 11 – Jumper trên PCB một lớp (Wire Jumper & 0Ω Protocol)

1. **Thứ tự ưu tiên giải quyết giao cắt mạch:**
   Khi hai đường mạch bắt buộc phải cắt nhau trên bo 1 lớp, phải xử lý theo trình tự nghiêm ngặt sau:
   - **Bước 1 (Placement):** Xoay đổi góc module, tráo đổi vị trí linh kiện lân cận để giải tỏa giao cắt.
   - **Bước 2 (Routing detour):** Thử nghiệm kéo đường mạch đi vòng qua khoảng trống giữa các chân linh kiện cắm (pitch 2.54mm cho phép đi 1 đường mạch 0.25mm lọt qua giữa 2 chân có khoảng cách chuẩn).
   - **Bước 3 (Connector Optimization):** Đổi hướng cắm của connector/header.
   - **Bước 4 (Jumper):** Chỉ khi đã thử cả 3 cách trên mà không thể giải quyết thì mới được phép sử dụng **Cầu nối dây (Wire Jumper)** hoặc **Điện trở 0Ω**.
2. **Quy chuẩn quản lý Jumper:**
   - Jumper phải được đặt ở mặt trên (`F.Cu`), hai chân hàn xuyên lỗ xuống mặt dưới (`B.Cu`).
   - Mọi jumper xuất hiện trên PCB **BẮT BUỘC PHẢI CÓ TRÊN SCHEMATIC** với ký hiệu quy ước rõ ràng (RefDes: `JMP1`, `JMP2`, `JMP3`...).
   - Jumper phải được thống kê đầy đủ trong bảng bóc tách linh kiện (BOM) kèm theo ghi chú chiều dài dây nối cách điện (ví dụ: "Dây đồng bọc Teflon cách điện dài 15mm").
3. **Giới hạn kỹ thuật của Jumper:**
   - **Ưu tiên Jumper cho đường tín hiệu:** Jumper chỉ được dùng cho các đường logic dòng nhỏ (< 50mA) như GPIO, CS, INT, TX, RX.
   - **Cấm dùng jumper mảnh cho đường nguồn công suất:** Tuyệt đối cấm dùng điện trở dán 0Ω kích thước nhỏ (0603/0805) hoặc sợi dây jumper đơn mảnh làm cầu nối cho đường nguồn `5V_SYS` hay `SIM_PWR` gánh dòng 2A. Nếu bắt buộc nhảy nguồn, phải dùng dây nối tiết diện tối thiểu 22 AWG (0.32 mm²).
   - **Cấm đi jumper qua vùng RF:** Không đặt jumper vắt ngang qua vùng anten của ESP32, SIM và GPS.
   - **Không biến tướng thành mạch 2 lớp:** Toàn bộ bo mạch phấn đấu có dưới **8 jumper**. Nếu số lượng jumper vượt quá 12 con, chứng tỏ việc bố trí placement bị sai lệch nghiêm trọng, phải làm lại placement từ đầu.

---

### RULE 12 – Bố trí ESP32 (ESP32-S3 Placement & Antenna Keepout)

1. **Hướng đặt Anten vi dải PCB (On-board PCB Antenna):**
   - Bo mạch ESP32-S3-DevKitC-1 phải được bố trí sao cho **phần anten mạ đồng ở đầu bo mạch hướng thẳng ra mép ngoài cùng của bo mạch PCB**.
   - Cấm quay phần anten của ESP32 vào giữa lòng bo mạch hay hướng về phía các module khác.
2. **Vùng cấm đồng tuyệt đối (Antenna Keepout Zone):**
   - Vùng không gian nằm bên dưới phần anten của ESP32 (cả trên `F.Cu`, `B.Cu` và các lớp cơ khí) phải được thiết lập vùng cấm (**Keepout Zone**):
     - Không có đường mạch đồng.
     - Không có vùng phủ đồng GND.
     - Không có linh kiện kim loại, ốc vít, hay dây jumper chạy qua.
     - Cách ly mép bo mạch tối thiểu 15mm tính từ anten theo khuyến cáo của Espressif.
3. **Tiếp cận cổng USB:**
   - Cổng micro-USB hoặc Type-C của DevKit dùng để nạp firmware và xuất log UART phải quay ra sát mép bo mạch và thẳng hàng với cửa sổ mở trên hộp bảo vệ, đảm bảo cắm cáp nạp dễ dàng mà không bị vướng thành hộp.
4. **Không gian thao tác:** Chừa khoảng hở tối thiểu 3.0mm xung quanh 2 hàng chân cắm của DevKit để dễ dùng kẹp nhíp hoặc tay rút bo mạch ra khỏi socket.

---

### RULE 13 – Bố trí GPS và SIM (RF Coexistence & Noise Immunity)

1. **Cách ly không gian Anten:**
   - Anten GPS (anten gốm tích cực/thụ động) và Anten 4G LTE của module SIM phát sóng với công suất rất lớn (lên tới 33 dBm / 2 Watts). Hai anten này phải được đặt ở **hai góc đối diện xa nhau nhất có thể trên bo mạch** (khoảng cách tối thiểu 50mm).
   - Anten GPS phải có tầm nhìn thông thoáng hướng lên bầu trời, không bị các module cao tầng hoặc vỏ kim loại che khuất.
2. **Miễn nhiễm nhiễu nguồn xung (Switching Noise Immunity):**
   - Tuyệt đối cấm đặt module GPS hoặc anten GPS nằm ngay trên hoặc sát cạnh cuộn cảm của module Buck 3.3V hoặc đường cấp nguồn SIM xung 2A. Nhiễu điện từ trường bức xạ từ cuộn cảm switching sẽ làm GPS bị nghẽn kênh thu, mất tín hiệu vệ tinh (mất 3D Fix).
3. **Cáp anten và đầu nối RF:**
   - Dự án sử dụng module GPS và SIM có đầu nối anten chuẩn **IPEX (U.FL) hoặc SMA**. Bo mạch carrier chỉ đóng vai trò gá giữ, không tự ý vẽ đường mạch cao tần RF 50Ω trên bo 1 lớp (vì bo 1 lớp không thể kiểm soát trở kháng vi dải microstrip).
   - Chừa khoảng không gian cơ khí để uốn cáp pigtail anten mà không bị bẹp, gập góc nhọn hay bị đè bởi nắp hộp.

---

### RULE 14 – Bố trí MPU6050 (IMU Mechanical Stability & Axis Alignment)

1. **Vị trí cơ khí vững chắc:**
   - Cảm biến quán tính MPU6050 dùng để phát hiện tai nạn, rung chấn và đo góc lật nghiêng xe máy. Module GY-521 phải được bố trí ở **vị trí trung tâm bo mạch hoặc sát ngay cạnh một lỗ bắt vít cố định M3**.
   - Cấm đặt MPU6050 ở các góc bo mạch mỏng manh hoặc trên các nhánh mạch có độ võng cơ học cao.
2. **Cách ly nguồn rung động cục bộ:**
   - Đặt MPU6050 cách xa còi báo động (Buzzer) tối thiểu 40mm. Khi còi rung cơ học tần số cao (2.7 kHz – 4 kHz), sóng âm truyền qua phíp mạch sẽ gây nhiễu trắng toàn bộ dữ liệu gia tốc kế $A_x, A_y, A_z$ làm thuật toán AIoT nhận diện nhầm là xe va chạm.
   - Cách ly khỏi cuộn cảm nguồn và các linh kiện tỏa nhiệt mạnh.
3. **Quy chuẩn hệ trục tọa độ:**
   - Module MPU6050 phải được đặt song song hoàn toàn với các cạnh của hộp đen.
   - In rõ mũi tên chỉ hướng trục **$X$ (dọc thân xe)**, **$Y$ (ngang thân xe)** và chiều trục **$Z$ (thẳng đứng)** lên lớp lụa Silkscreen của bo mạch để người lắp ráp đặt đúng hướng.
   - Nghiêm cấm việc tự ý xoay module 90° hoặc 45° trong quá trình layout mà không thông báo và đồng bộ lại ma trận xoay trong firmware.

---

### RULE 15 – Quy tắc đi dây tín hiệu (Signal Routing Discipline)

1. **Bus tốc độ cao MicroSD (SPI):**
   - Các đường `SPI_SCK`, `SPI_MOSI`, `SPI_MISO`, `SD_CS` phải được đi ngắn nhất có thể (< 60mm) và đi song song thành một cụm.
   - Tuyệt đối ưu tiên đường xung nhịp `SPI_SCK` (16 MHz) đi thẳng, không bị bẻ cong gấp khúc, có dải mass kẹp bên cạnh để chống bức xạ xuyên âm (crosstalk).
2. **Bus cảm biến I2C:**
   - Cặp tín hiệu `I2C_SDA` và `I2C_SCL` phải đi song song kèm nhau, chiều dài tương đương, hạn chế tối đa các nhánh rẽ dài (stub).
   - Đảm bảo trên bus có điện trở kéo lên nguồn `3V3_SYS` (giá trị 4.7kΩ). Lưu ý kiểm tra xem trên các bo breakout OLED, RTC, MPU đã có sẵn trở kéo hay chưa để tránh bị kéo song song làm giảm tổng trở kháng kéo quá thấp.
3. **Các cặp UART:**
   - Cặp `SIM_TX`/`SIM_RX` và `GPS_TX`/`GPS_RX` phải đi gọn gàng, tránh chạy song song sát cạnh các đường nguồn có dòng biến thiên lớn.
   - Bắt buộc kiểm tra kỹ chiều chéo: TX của vi điều khiển nối vào RX của module ngoại vi và ngược lại.
4. **Hình học đường mạch:**
   - Toàn bộ góc bẻ của đường mạch phải dùng **góc 45° hoặc góc cong tròn**, tuyệt đối cấm bẻ góc vuông 90° nhọn (acid trap gây đứt mạch khi ăn mòn thủ công và gây phản xạ tín hiệu).
   - Khoảng cách từ mép đường mạch ngoài cùng đến đường biên bo mạch (`Edge.Cuts`) tối thiểu là **1.0mm**.

---

### RULE 16 – Vị trí linh kiện để dễ sử dụng (Ergonomics & Serviceability)

Khi bố trí tổng thể bo mạch (Floorplanning), phải tuân thủ nghiêm ngặt tính công thái học và thao tác vận hành thực tế:
1. **Màn hình OLED 0.96 inch:** Đặt ở vị trí trung tâm hoặc nửa trên bo mạch, hướng mặt hiển thị lên trên để người dùng dễ quan sát qua nắp hộp mica trong suốt.
2. **Khe cắm thẻ nhớ MicroSD:** Mặt cắm thẻ của module MicroSD phải quay hướng ra sát mép bo mạch, chừa khe hở để ngón tay hoặc nhíp có thể ấn nhả thẻ nhớ ra vào dễ dàng mà không cần tháo toàn bộ bo mạch ra khỏi hộp.
3. **Nút nhấn khẩn cấp CANCEL và Đèn LED:**
   - Nút nhấn CANCEL (loại nút cắm 4 chân 6x6mm hoặc 12x12mm) phải đặt ở vị trí rìa ngoài bo mạch, hướng lên trên để người lái xe dễ thao tác bấm dừng báo động giả trong vòng 15 giây.
   - Đèn LED trạng thái đặt cạnh nút bấm hoặc cạnh màn hình OLED.
4. **Cổng kết nối nguồn và nạp:**
   - Terminal nguồn UPS đặt ở mép bo mạch, dễ luồn tua-vít vặn siết dây điện.
   - Cổng USB của ESP32 quay ra mép ngoài hộp để cắm nạp code bảo trì định kỳ.
5. **Cọc cắm Anten:** Các đầu nối anten SMA/IPEX của SIM và GPS phải có khoảng không để xoay vặn ren mà không chạm vào các linh kiện khác.

---

### RULE 17 – Cơ khí và độ bền (Mechanical Durability & Mounting)

1. **Lỗ bắt vít định vị cố định (Mounting Holes):**
   - Thiết kế tối thiểu **04 lỗ bắt vít chuẩn M3** (đường kính lỗ khoan 3.2mm) tại 4 góc của bo mạch PCB.
   - Xung quanh mỗi lỗ bắt vít phải có khoảng cách an toàn (Keepout): vòng cách ly đường kính tối thiểu **6.5mm** không có đường mạch đồng, không có linh kiện để tránh vành kim loại của ốc vít hoặc trụ đồng làm chập mạch khi siết chặt.
2. **Chống rung lắc môi trường xe máy:**
   - Xe máy điện và xe máy xăng trong quá trình vận hành liên tục sinh ra rung chấn cơ học mạnh trên đường gồ ghề.
   - Khối pin đôi 18650 và module UPS có khối lượng nặng (~150g). Khối này **BẮT BUỘC phải được gá bắt vít cơ khí độc lập hoặc dán keo silicon định vị cố định vào đáy hộp nhựa ABS**, tuyệt đối không để khối pin đè lên bo mạch PCB hoặc chỉ treo bằng các mối hàn chân điện.
   - Các module cắm trên hàng rào socket cái phải có độ ma sát chặt chẽ, chừa vị trí để có thể gia cố thêm keo nến hoặc đai thắt nhựa (cable tie) chống tuột khi xe rung lắc.
3. **Chiều cao linh kiện trong hộp:**
   - Kiểm tra chiều cao tổng thể của linh kiện cao nhất (thường là tụ hóa nguồn, module SIM hoặc trụ cắm DevKit) so với chiều sâu lọt lòng của hộp nhựa bảo vệ (chuẩn hộp nhựa chống nước IP65 kích thước 100x68x50mm hoặc tương đương).

---

### RULE 18 – Silkscreen (Silkscreen Marking & Clearances)

Lớp in chữ chỉ dẫn (Silkscreen - `F.SilkS` và `B.SilkS`) là yếu tố quyết định để tránh hàn nhầm, đo nhầm làm cháy mạch:
1. **Thông tin định danh bắt buộc trên bo:**
   - Tên dự án: `AIOT SMART BLACK BOX - EDR FOR MOTORBIKE`.
   - Tên bo mạch và phiên bản: `CARRIER BOARD REV 1.0`.
   - Tên tác giả / Ngày hoàn thành: Đồ án tốt nghiệp 2 - 2026.
2. **Chỉ dẫn chân và cực tính:**
   - Mọi cọc kết nối, header và terminal nguồn đều phải in dấu cực tính rõ ràng: dấu cộng **`+`**, dấu trừ **`-`**.
   - Chân số 1 của tất cả các IC, header và socket phải được đánh dấu bằng **chấm tròn hoặc vạch tam giác đậm**.
   - In rõ tên các đường nguồn quan trọng: `5V_SYS`, `3V3_SYS`, `SIM_PWR`, `GND`.
3. **Chỉ dẫn ngoại vi và cảm biến:**
   - In nhãn tên module tại từng vị trí socket: `ESP32-S3 DEVKIT`, `SIM A7682S`, `GPS NEO-M8N`, `OLED 0.96"`, `RTC DS3231`, `MPU-6050`, `MICROSD SPI`, `BUCK 3.3V`.
   - In hình vẽ biểu tượng hệ trục tọa độ $X - Y - Z$ tại vị trí của cảm biến MPU6050.
4. **Quy tắc bố trí chữ:**
   - Toàn bộ chữ silkscreen phải có kích thước đọc được rõ ràng (chiều cao chữ $\ge 1.0\text{mm}$, độ dày nét $\ge 0.15\text{mm}$).
   - **Tuyệt đối cấm để mực silkscreen in đè lên các pad hàn đồng, lỗ chân linh kiện hoặc lỗ vít.**

---

### RULE 19 – Test point (Test Point Strategy)

Bo mạch phải được trang bị hệ thống điểm đo kiểm (**Test Points**) phục vụ gỡ lỗi, kiểm tra chất lượng trước khi cắm module và cứu hộ mạch khi xảy ra sự cố:
1. **Danh mục Test Point bắt buộc:**
   - **Nhóm nguồn:** `TP_5V` (`5V_SYS`), `TP_3V3` (`3V3_SYS`), `TP_SIM_PWR`, `TP_GND` (bố trí ít nhất 2 điểm GND ở 2 đầu bo để kẹp que đo đồng hồ vạn năng).
   - **Nhóm bus I2C:** `TP_SDA`, `TP_SCL` (kiểm tra xung nhịp và dữ liệu giao tiếp cảm biến).
   - **Nhóm UART truyền thông:** `TP_SIM_TX`, `TP_SIM_RX`, `TP_GPS_TX`, `TP_GPS_RX` (kẹp máy phân tích logic Logic Analyzer để bắt bản tin NMEA và lệnh AT).
   - **Nhóm SPI thẻ nhớ:** `TP_SCK`, `TP_MOSI`, `TP_MISO`, `TP_SD_CS`.
2. **Quy cách Test Point trên bo 1 lớp:**
   - Sử dụng linh kiện Test Point dạng lỗ cắm xuyên qua bo mạch (Through-Hole Test Pad đường kính trong 1.0mm, vành khuyên pad ngoài 2.0mm) để có thể xỏ que đo hoặc hàn tạm sợi dây cắm breadboard khi đo sóng Oscilloscope.
   - Xung quanh Test Point phải in chữ silkscreen định danh rõ ràng và chừa đủ khoảng trống cho kẹp que đo an toàn mà không sợ chập sang đường mạch bên cạnh.

---

### RULE 20 – DRC và kiểm tra chế tạo (DRC & Fabrication Verification)

Quy trình xuất xưởng và nghiệm thu thiết kế bắt buộc phải vượt qua toàn bộ các bước kiểm tra tự động:
1. **Kiểm tra Schematic ERC:** Phải chạy lại `kicad-cli sch erc`, đạt kết quả **0 Error**.
2. **Kiểm tra Mạch in DRC (Design Rules Check):**
   - Thiết lập thông số kiểm tra DRC trong KiCad khớp với năng lực công nghệ của nhà sản xuất (hoặc phương pháp làm mạch thủ công):
     - Clearance tối thiểu: $0.25\text{mm}$ (10 mil).
     - Track Width tối thiểu: $0.25\text{mm}$ (10 mil).
     - Annular Ring tối thiểu cho chân hàn: $0.40\text{mm}$ (đảm bảo chân hàn xuyên lỗ không bị đứt vành khi khoan).
   - Chạy `kicad-cli pcb drc`, kết quả bắt buộc:
     - **0 Unconnected nets (Không có đường dây chưa nối).**
     - **0 Short circuit violations (Không có chập ngắn mạch).**
     - **0 Clearance violations (Không vi phạm khoảng cách an toàn).**
3. **Cấm gian lận lỗi DRC:** Nghiêm cấm hành động chuyển các cảnh báo/lỗi DRC sang trạng thái `Ignored` để đối phó. Mọi lỗi báo đỏ đều phải được sửa dứt điểm trên bản vẽ.
4. **Kiểm tra trực quan lớp Gerber và Drill:**
   - Mở file Gerber bằng KiCad GerbView trước khi gửi gia công.
   - Xác minh toàn bộ các lỗ khoan (`*.drl`) nằm đồng tâm chính xác giữa các pad hàn đồng trên lớp `B.Cu`.

---

### RULE 21 – Điều kiện chuyển sang PCB hai lớp (Two-Layer Fallback Feasibility)

1. **Cam kết 1 lớp tối đa:** Thiết kế phải trung thành với định hướng PCB 1 lớp đồng (`B.Cu`). Chỉ được xem xét chuyển sang PCB 2 lớp khi xuất hiện ít nhất một trong các điều kiện bất khả kháng sau:
   - Số lượng đường tín hiệu giao cắt quá dày đặc mà phương án placement và jumper không thể xử lý nổi (số jumper vượt quá 15 điểm hoặc chiều dài jumper gây nguy hiểm).
   - Đường hồi tiếp mass GND bị băm nát hoàn toàn thành các nhánh cụt, không thể bảo đảm đường trở về dòng đỉnh 2.0A cho SIM A7682S.
   - Không gian cơ khí bị giới hạn ngặt nghèo (kích thước bo bắt buộc thu nhỏ dưới diện tích cho phép của các đường mạch công suất 1 lớp).
   - Xuất hiện hiện tượng xuyên âm và nhiễu sóng cao tần làm sai lệch nghiêm trọng dữ liệu truyền thông và hoạt động của GPS.
2. **Quy trình phê duyệt chuyển lớp:**
   - Nếu hội đủ các điều kiện bất khả kháng trên, người thực hiện **KHÔNG ĐƯỢC TỰ Ý TỰ CHUYỂN SANG 2 LỚP**.
   - Bắt buộc phải lập văn bản báo cáo chính thức mang tên:
     `D:\ĐỒ ÁN 2\ONE_LAYER_FEASIBILITY_REPORT.md`
   - Báo cáo phải phân tích chi tiết: Các điểm nghẽn mạch không thể tháo gỡ, bảng thống kê các jumper bắt buộc, mô phỏng rủi ro sụt áp nguồn/nhiễu tín hiệu và đề xuất giải pháp 2 lớp thay thế.
   - Chỉ được kích hoạt thiết kế 2 lớp khi có sự chấp thuận bằng văn bản rõ ràng từ Người dùng (User Approval).

---

# PHẦN III: QUY TRÌNH THIẾT KẾ PCB THEO 7 GATE

Toàn bộ quá trình triển khai thiết kế mạch in cho Hộp đen AIoT phải tuân thủ nghiêm ngặt theo chu trình 7 cổng kiểm soát kỹ thuật (**GATE 0 đến GATE 6**). Không được phép nhảy cóc bước khi chưa đạt điều kiện nghiệm thu của cổng trước.

```text
┌───────────┐     ┌───────────┐     ┌───────────┐     ┌───────────┐
│  GATE 0   │ ──► │  GATE 1   │ ──► │  GATE 2   │ ──► │  GATE 3   │
│   Audit   │     │ Footprint │     │ Placement │     │  Routing  │
└───────────┘     └───────────┘     └───────────┘     └───────────┘
                                                            │
┌───────────┐     ┌───────────┐     ┌───────────┐           │
│  GATE 6   │ ◄── │  GATE 5   │ ◄── │  GATE 4   │ ◄─────────┘
│ Manufact. │     │ Verificat.│     │ Power Int.│
└───────────┘     └───────────┘     └───────────┘
```

---

### GATE 0 – Audit (Kiểm tra Code, Schematic, GPIO và Nguồn)

- **Mục tiêu:** Đồng bộ tuyệt đối giữa mã nguồn firmware đang chạy, bản vẽ nguyên lý schematic và kiến trúc cấp nguồn.
- **Nội dung thực hiện:**
  1. Đọc trực tiếp `filecodemain.cpp`, trích xuất toàn bộ bảng gán chân GPIO của các ngoại vi đang hoạt động.
  2. Mở file nguyên lý KiCad `AIOT_BLACKBOX_PRESENTATION.kicad_sch`, rà soát từng chân kết nối của ESP32-S3.
  3. Lập bảng đối chiếu xung đột chân (như đã phân tích tại Phần I), xử lý triệt để xung đột chân UART SIM (chuyển về GPIO15/16) và MicroSD CS (chuyển về GPIO10).
  4. Đánh dấu trạng thái `UNASSIGNED` cho các chức năng chưa có trong mã nguồn (Buzzer, CANCEL, LED, IMU INT, GNSS PPS, ADC_VBAT_SENSE).
  5. Xác nhận kiến trúc nguồn: UPS LX-2BUPS cấp `5V_SYS` và Buck độc lập cấp `3V3_SYS`.
- **Điều kiện ĐẠT (PASS Criteria):**
  - Đã xử lý 100% xung đột GPIO giữa code và schematic.
  - Không có chân ngoại vi nào trong code bị gán sai trên schematic.
  - Được người dùng phê duyệt phương án điều chỉnh schematic trước khi chuyển sang layout.

---

### GATE 1 – Footprint (Xác minh Footprint, Pinout và Cơ khí)

- **Mục tiêu:** Đảm bảo toàn bộ linh kiện cắm trên mạch in khớp 100% với kích thước hình học của linh kiện thực tế.
- **Nội dung thực hiện:**
  1. Đo đạc hoặc kiểm tra datasheet chuẩn xác của các bo breakout: ESP32-S3-DevKitC-1 (khoảng cách 2 hàng chân 25.4mm), OLED (thứ tự VCC/GND), MPU6050, DS3231, GPS, MicroSD, SIM A7682S, Buck 3.3V.
  2. Kiểm tra đường kính lỗ khoan chân linh kiện: Chân header vuông pitch 2.54mm cần lỗ khoan tối thiểu 1.0mm, vành pad tối thiểu 1.8mm để dễ hàn chì thủ công.
  3. Tạo hoặc gán đúng footprint socket cái (Female Header) cho toàn bộ các module.
  4. Xác định kích thước bao hình bo mạch (`Edge.Cuts`) và 04 lỗ bắt vít M3 ở 4 góc khớp với hộp nhựa ABS.
- **Điều kiện ĐẠT (PASS Criteria):**
  - 100% linh kiện trên schematic đã được gán footprint hợp lệ trong thư viện project.
  - Không còn footprint phỏng đoán; các module chưa chắc chắn đều đã được chuyển thành cụm chân cắm header tiêu chuẩn.

---

### GATE 2 – Placement (Bố trí Module, Vùng cấm RF, Đường nguồn ngắn)

- **Mục tiêu:** Bố trí vị trí linh kiện (Floorplanning) tối ưu nhất cho việc đi dây 1 lớp, cách ly nhiễu và dễ thao tác.
- **Nội dung thực hiện:**
  1. Đặt anten ESP32 hướng ra mép ngoài cùng của bo mạch, tạo vùng cấm Keepout Zone dưới anten.
  2. Đặt anten GPS và anten SIM ở hai góc cách xa nhau tối đa.
  3. Đặt cảm biến MPU6050 ở vị trí cơ khí cứng vững, cách xa còi báo động và cuộn cảm nguồn.
  4. Đặt khe thẻ nhớ MicroSD, màn hình OLED, nút CANCEL và terminal nguồn ở các mép tiện thao tác.
  5. Đặt cụm tụ lọc nguồn công suất lớn ngay sát chân cấp nguồn của SIM A7682S.
  6. Xoay hướng các module để các chân kết nối có đường bay rác (ratsnest) thẳng nhất, giảm thiểu tối đa giao cắt đường tín hiệu.
- **Điều kiện ĐẠT (PASS Criteria):**
  - Không vi phạm vùng cấm anten của ESP32.
  - Các cổng giao tiếp người dùng (USB, thẻ nhớ, nút bấm, màn hình) nằm ở vị trí công thái học chuẩn.
  - Mật độ giao cắt dây rác ratsnest giảm thiểu tối đa trước khi bắt đầu đi dây.

---

### GATE 3 – Single-Layer Routing (Đi dây B.Cu, Không Via, Tối ưu Jumper)

- **Mục tiêu:** Thực hiện kết nối toàn bộ các đường mạch đồng trên duy nhất lớp đáy `B.Cu` theo đúng các Net Class.
- **Nội dung thực hiện:**
  1. Thiết lập Net Classes chuẩn theo [RULE 09](#rule-09--độ-rộng-đường-mạch-net-classes--trace-width-calculation).
  2. Đi dây đường nguồn công suất lớn trước: `SIM_PWR`, `5V_SYS`, `3V3_SYS` với độ rộng lớn.
  3. Đi các đường bus dữ liệu quan trọng: SPI (MicroSD), I2C (OLED, RTC, MPU), UART (SIM, GPS).
  4. Đi các đường tín hiệu điều khiển logic thông thường.
  5. Khi gặp giao cắt bắt buộc, thực hiện quy trình 4 bước tại [RULE 11](#rule-11--jumper-trên-pcb-một-lớp-wire-jumper--0ω-protocol) để chèn jumper dây hoặc điện trở 0Ω lên mặt `F.Cu`.
  6. Đảm bảo toàn bộ đường mạch đi góc 45°, không có góc nhọn.
- **Điều kiện ĐẠT (PASS Criteria):**
  - 100% đường mạch được định tuyến trên lớp `B.Cu`.
  - Không có bất kỳ Via chuyển lớp nào trên bo.
  - Tổng số lượng jumper dây trên bo kiểm soát ở mức tối thiểu (< 8 jumper).
  - Không còn bất kỳ đường ratsnest nào chưa nối (Unrouted = 0).

---

### GATE 4 – Power Integrity (Kiểm tra Dòng tải, Sụt áp SIM, Vùng GND)

- **Mục tiêu:** Bảo đảm hệ thống cung cấp năng lượng ổn định, không sụt áp khi SIM phát xung 2A và mass thông suốt.
- **Nội dung thực hiện:**
  1. Đo đạc kiểm tra độ rộng các đoạn đường nguồn `5V_SYS` và `SIM_PWR`, đảm bảo đủ tiết diện theo chuẩn IPC-2221.
  2. Thực hiện phủ đồng tiếp địa mass (**GND Filled Zone**) trên toàn bộ diện tích còn trống của lớp `B.Cu`.
  3. Bấm `B` refill zone và kiểm tra kỹ đường hồi dòng mass từ SIM và ESP32 về âm tụ chính có bị đứt gãy hay nghẽn nút cổ chai hay không.
  4. Xóa bỏ toàn bộ các đảo đồng mồ côi (Unconnected/Isolated copper islands).
  5. Kiểm tra vị trí tụ lọc chống sụt áp đặt sát chân nguồn module SIM.
- **Điều kiện ĐẠT (PASS Criteria):**
  - Đường nguồn SIM và 5V đạt độ rộng thiết kế $\ge 1.5\text{mm} - 2.5\text{mm}$ hoặc phủ đồng.
  - Không có đảo đồng mass bị thả nổi.
  - Đường hồi tiếp mass của tải công suất độc lập và thông suốt về chân âm tụ nguồn.

---

### GATE 5 – Verification (ERC, DRC, Kiểm tra 3D và Tiêu chuẩn)

- **Mục tiêu:** Nghiệm thu toàn diện thiết kế bằng công cụ tự động và kiểm tra chéo trực quan.
- **Nội dung thực hiện:**
  1. Chạy lại KiCad ERC cho schematic: Kết quả **0 Errors, 0 Warnings nghiêm trọng**.
  2. Chạy KiCad DRC cho bo mạch PCB: Kết quả **0 Errors, 0 Unconnected Items**.
  3. Mở khung nhìn 3D Viewer (`Alt+3`): Kiểm tra va chạm cơ khí giữa các linh kiện, hướng anten, chiều cắm module, độ cao so với nắp hộp.
  4. Rà soát lớp chữ in Silkscreen: Đảm bảo có đầy đủ tên bo, phiên bản, cực tính `+`/`-`, chân số 1, nhãn test point và không có chữ nào đè lên pad hàn.
  5. Đối chiếu danh mục 21 quy tắc trong văn bản này.
- **Điều kiện ĐẠT (PASS Criteria):**
  - Báo cáo DRC đạt kết quả tuyệt đối (0 vi phạm).
  - Khung nhìn 3D trực quan không phát hiện va chạm cơ học.
  - Bản vẽ đạt toàn diện các tiêu chuẩn an toàn hệ thống.

---

### GATE 6 – Manufacturing (Xuất Gerber 1 lớp, Drill, BOM, Hướng dẫn lắp ráp)

- **Mục tiêu:** Xuất gói hồ sơ chế tạo hoàn chỉnh, phục vụ gia công bo mạch và lắp ráp thủ công không sai sót.
- **Nội dung thực hiện:**
  1. Cấu hình xuất file Gerber cho bo mạch 1 lớp đồng:
     - `B.Cu` (Đường mạch đồng mặt dưới).
     - `B.Mask` (Lớp phủ hàn mặt dưới).
     - `F.SilkS` (Lớp in chữ mặt trên).
     - `Edge.Cuts` (Đường biên cắt bo mạch).
  2. Xuất file khoan chuẩn Excellon Drill (`*.drl`): Kiểm tra định dạng tọa độ và đơn vị milimet.
  3. Mở bộ file Gerber bằng KiCad GerbView để kiểm tra chéo lần cuối.
  4. Xuất bảng bóc tách linh kiện (BOM) định dạng CSV/Excel: Thống kê chi tiết từng module, header, terminal, nút bấm, tụ điện và danh sách jumper kèm kích thước.
  5. Soạn tài liệu hướng dẫn lắp ráp và quy trình đo kiểm an toàn điện trước khi cấp nguồn lần đầu.
- **Điều kiện ĐẠT (PASS Criteria):**
  - Trọn bộ file Gerber và Drill sẵn sàng gửi xưởng gia công hoặc in phim ăn mòn thủ công.
  - File BOM đồng bộ 100% với linh kiện thực tế trên bản vẽ.
  - Có văn bản nghiệm thu đóng dấu hoàn thành thiết kế bo mạch chính Carrier Board.

---

# PHẦN IV: THAM CHIẾU KỸ THUẬT VÀ PHÂN LOẠI TIÊU CHUẨN

## 1. Danh mục tài liệu tham khảo chính thức

Mọi thông số hình học, điện áp, dòng điện và quy định cách ly trong bộ luật này được tổng hợp và đối chiếu từ các tài liệu kỹ thuật chính hãng uy tín sau:

1. **KiCad PCB Editor Official Documentation (v8.x / v9.x):**
   - Hướng dẫn thiết lập Net Classes, thiết kế bo 1 lớp, quản lý vùng phủ đồng Filled Zone và cấu hình kiểm tra DRC.
2. **Espressif Systems - ESP32-S3 Hardware Design Guidelines:**
   - Mục *Antenna Placement and Clearance*: Quy chuẩn vùng cấm kim loại dưới anten vi dải.
   - Mục *Power Supply Decoupling*: Quy chuẩn tụ bù lọc nguồn cho khối RF Wi-Fi/Bluetooth.
   - Mục *Strapping Pins*: Các lưu ý về chân khởi động GPIO0, GPIO45, GPIO46.
3. **SIMCom Wireless Solutions - A7682S Hardware Design Guide (Version 1.02+):**
   - Mục *Power Supply (VBAT)*: Dải điện áp hoạt động $3.4\text{V} - 4.2\text{V}$ (danh định 3.8V), dòng xung đỉnh $2.0\text{A}$ trong thời gian truyền GSM/LTE.
   - Mục *Decoupling Network*: Cấu hình tụ $1000\mu\text{F} + 100\text{nF} + 33\text{pF} + 10\text{pF}$.
   - Mục *UART Interface*: Mức logic 1.8V/3.3V và sơ đồ ghép nối vi điều khiển.
4. **u-blox - NEO-M8 Hardware Integration Manual:**
   - Mục *RF Layout Design*: Cách ly nguồn nhiễu switching DC-DC khỏi khối thu GPS.
   - Mục *Antenna Supervision*: Bố trí đường tín hiệu anten chủ động và thụ động.
5. **Texas Instruments - Power Supply Layout Guidelines & Application Reports:**
   - SLVA636: *Basic Calculation of a Boost/Buck Converter Traces*.
   - SNVA054: *Dealing with Ground Loops and Noise in Switching Regulators*.
6. **IPC Standards (Association Connecting Electronics Industries):**
   - **IPC-2221B:** *Generic Standard on Printed Board Design* (Công thức tính toán độ rộng đường mạch theo dòng điện và độ tăng nhiệt).
   - **IPC-2152:** *Standard for Determining Current-Carrying Capacity in Printed Board Design*.
   - **IPC-7351B:** *Generic Requirements for Surface Mount Design and Land Pattern Standard*.

---

## 2. Bảng phân định mức độ kỹ thuật

Để tránh tình trạng phỏng đoán hoặc áp đặt cảm tính, toàn bộ các tiêu chí kỹ thuật của dự án được phân định rạch ròi thành 3 nhóm:

| Mức độ | Định nghĩa | Danh mục áp dụng cụ thể trong dự án AIoT Black Box |
|---|---|---|
| **BẮT BUỘC<br>(Mandatory)** | Quy tắc kỹ thuật tuyệt đối trích từ Datasheet và chuẩn IPC; vi phạm sẽ làm cháy mạch hoặc hỏng chức năng. | - GPIO phải theo đúng `filecodemain.cpp` (RULE 02).<br>- Không đi dây và không phủ đồng trên `F.Cu` cho mạch 1 lớp (RULE 01).<br>- Cấm dùng chân 3V3 của ESP32 nuôi ngoại vi (RULE 07).<br>- Vùng cấm đồng tuyệt đối dưới anten ESP32 (RULE 12).<br>- DRC phải đạt 0 lỗi trước khi xuất Gerber (RULE 20).<br>- Không nối song song hai bộ ổn áp 3.3V (RULE 07). |
| **KHUYẾN NGHỊ<br>(Recommended)** | Giá trị thiết kế tối ưu dựa trên kinh nghiệm kỹ thuật để nâng cao độ bền và chống nhiễu tốt nhất. | - Độ rộng đường mạch nguồn 5V từ 1.5mm - 2.0mm (RULE 09).<br>- Đặt MPU6050 cách xa còi báo động tối thiểu 40mm (RULE 14).<br>- Số lượng jumper dây kiểm soát dưới 8 con (RULE 11).<br>- Trang bị đủ 04 lỗ bắt vít M3 có vành cách ly 6.5mm (RULE 17).<br>- Sử dụng socket cắm thay vì hàn chết linh kiện (RULE 05).<br>- Đặt tụ lọc Low-ESR lớn ngay sát chân SIM (RULE 08). |
| **CẦN ĐO KIỂM<br>(Pending Test)** | Các thông số phụ thuộc vào lô linh kiện thực tế mua tại TP.HCM, bắt buộc phải đo trực tiếp trước khi chốt footprint. | - Điện áp cấp thực tế của bo breakout SIM A7682S (chân VCC là 5V hay 3.8V).<br>- Thứ tự chân thực tế của bo OLED 0.96" mua tại cửa hàng (GND-VCC hay VCC-GND).<br>- Dòng xả thực tế liên tục của module UPS LX-2BUPS dưới tải 2A.<br>- Độ trôi nhiệt và độ ổn định của module Buck 3.3V Mini-360.<br>- Khả năng phát hiện tai nạn thực tế khi gắn trong hộp kín xe máy. |

---

# KẾT LUẬN VÀ HIỆU LỰC THI HÀNH

Văn bản luật thiết kế PCB này là **quy chuẩn kỹ thuật duy nhất và cao nhất** chi phối toàn bộ quá trình vẽ mạch in Carrier Board cho đồ án Hộp đen AIoT.

Mọi thao tác chỉnh sửa schematic, định vị linh kiện, chạy dây mạch in và nghiệm thu xuất file chế tạo từ thời điểm này trở đi bắt buộc phải soi chiếu vào từng điều khoản của văn bản này. Bất kỳ sự điều chỉnh nào đi ngược lại 21 RULE và 7 GATE trên đều bị coi là không hợp lệ cho đến khi được phân tích nguyên nhân và có sự đồng ý chính thức từ người dùng.
