# ĐÁNH GIÁ KIẾN TRÚC NGUỒN, CONNECTOR & TÍN HIỆU NGOẠI VI (`POWER AND CONNECTOR REVIEW`) — GATE 0

- **Dự án**: THIẾT KẾ HỘP ĐEN AIoT THÔNG MINH PHÂN TÍCH VÀ GHI LẠI SỰ CỐ XE MÁY ĐIỆN
- **Project KiCad**: `AIOT_BLACKBOX_MAINBOARD_REV1`
- **Căn cứ quy chuẩn**: `D:\ĐỒ ÁN 2\.agents\rules\PCB_DESIGN_RULES_AIOT.md` (RULE 06, RULE 07, RULE 08, RULE 13) và Mục 7 yêu cầu Gate 0.

---

## 1. Kiến trúc phân phối nguồn thực tế trên Carrier Board (`AIOT_BLACKBOX_MAINBOARD_REV1`)

```text
[Module UPS ngoài PCB: LX-2BUPS 5V/3A (2x18650)]
   │
   ├── UPS+ ──► [Connector J2: LX-2BUPS_IN] ──► Đường nguồn 5V_SYS
   │                                               ├──► U1: ESP32-S3-DevKitC-1 (Chân 5V - Pin 21)
   │                                               ├──► BZ1: Mạch Buzzer 5V (Dự phòng UNASSIGNED)
   │                                               └──► U6: Module hạ áp 3.3V (IN+)
   │                                                       └──► Đường nguồn 3V3_SYS (+ Tụ C1 100nF)
   │                                                               ├──► U2: MPU6050 GY-521 (VCC & AD0)
   │                                                               ├──► U3: DS3231 RTC 6-pin (VCC)
   │                                                               ├──► U7: OLED 0.96" SSD1306 (VDD)
   │                                                               ├──► J1: MicroSD Breakout (3V3)
   │                                                               ├──► U4: GPS NEO-M8N (VCC)
   │                                                               └──► R_PU1, R_PU2 (4.7k I2C), R3 (10k SW1)
   │
   └── UPS- ──► [Connector J2: GND] ──────────► Mặt phẳng / Lưới GND chung toàn mạch (`GND`)

[Nhánh nguồn SIM 4G tách biệt - NEEDS_VERIFICATION]
   [Connector J3: SIM_PWR_CONN] ──────────────► Đường nguồn SIM_PWR ──► U5: SIM A7682S Breakout (VCC)
```

### Đánh giá việc loại bỏ lỗi thiết kế nguồn cũ:
- **Trong schematic cũ (`REV8`)**: Chân `3V3` (Pin 1, `power_out`) của `U1 (ESP32-S3-DevKitC-1)` bị nối trực tiếp vào mạng `3V3_SYS`. Điều này biến LDO 3.3V nhỏ trên board ESP32-S3 thành nguồn nuôi cho toàn bộ 5 module ngoại vi (`MPU6050`, `DS3231`, `OLED`, `MicroSD`, `NEO-M8N`), gây sụt áp, nóng LDO trên DevKit và vi phạm RULE 06.
- **Trong schematic mới (`REV1`)**: Đã **ngắt hoàn toàn chân `3V3` của `U1` khỏi `3V3_SYS`** và gắn cờ `no_connect` cho cả hai chân `3V3` của `U1`. Mạng `3V3_SYS` hiện được cấp độc lập từ module hạ áp `U6` (`REG 3.3V MODULE`).

---

## 2. Phân tích kỹ thuật 6 vấn đề trọng tâm theo Mục 7

### 2.1. Cảnh báo kỹ thuật về Module hạ áp `5V_SYS` → `3V3_SYS` (`U6`) — LDO vs. Buck LM2596
- **Vấn đề Dropout Voltage của `LM2596`**:
  Nhiều module buck thông dụng trên thị trường dùng IC **LM2596-3.3 / LM2596-ADJ** (BJT switching stage) có điện áp rơi tối thiểu (**Dropout Voltage**) từ **1.5V đến 2.0V** ở tải trung bình.
  - Khi nguồn vào từ `LX-2BUPS` là `5.0V` (hoặc sụt nhẹ xuống `4.85V` trên dây dẫn khi SIM/ESP32 phát sóng), điện áp chênh lệch chỉ còn:
    $$\Delta V = 4.85\text{V} - 3.3\text{V} = 1.55\text{V}$$
  - Với $\Delta V \approx 1.55\text{V}$, mạch **LM2596 hoạt động sát ngưỡng bão hòa (dropout)**, dẫn đến gợn sóng (ripple) đầu ra lớn hoặc sụt áp dưới `3.3V` khi thẻ MicroSD ghi dữ liệu đồng thời với GPS thu vệ tinh.
- **Khuyến nghị kỹ thuật bắt buộc trước Gate 1**:
  1. Kiểm tra mã IC thực tế trên module nguồn 3.3V hiện có của nhóm:
     - Nếu là **Buck đồng bộ (Synchronous Buck)** áp thấp (ví dụ `MP2307`, `MP1584`, `TPS562200`, `SY8089`, `MT3608/buck-boost`) hoặc module **LDO dòng cao Low-Dropout** (`AMS1117-3.3` có dropout $\approx 1.1\text{V} - 1.3\text{V}$, `HT7833` / `XC6206` / `MIC29302` có dropout $< 0.5\text{V}$): có thể chạy tốt từ `5.0V`.
     - Nếu module đang có là **LM2596**: cần đo kiểm thực tế điện áp ngõ ra `3V3_SYS` khi tải đỉnh (~300mA) lúc đầu vào giảm xuống `4.75V`.
  2. Bố trí thêm footprint tụ lọc đầu ra (`100µF`電解/tantalum + `100nF` ceramic `C1`) ngay sát ngõ ra `3V3_SYS` của `U6`.

### 2.2. Xác minh nguồn `SIM_PWR` cho Breakout `A7682S` (`U5` & `J3`)
- **Đặc tính dòng đỉnh của module 4G LTE Cat.1 (`A7682S`)**:
  - Chip lõi `A7682S` hoạt động ở dải `VBAT = 3.4V – 4.2V` (điển hình `3.8V`), nhưng **đa số các module breakout A7682S bán sẵn tại Việt Nam** tích hợp sẵn diode/LDO hoặc mạch hạ áp trên breakout để nhận chân **`VCC = 5V` (hoặc `VIN = 5V–12V`)**.
  - Tuy nhiên, một số breakout nhỏ chỉ đưa trực tiếp chân `VBAT (3.8V–4.2V)` ra chân `VCC`. Nếu cấp nhầm `5.0V` trực tiếp vào chân `VBAT` không qua hạ áp, chip `A7682S` sẽ hỏng.
- **Xử lý trong Gate 0**:
  - Tuyệt đối không nối mù `U5.VCC` vào `5V_SYS`.
  - Đã tách thành nhánh `SIM_PWR` nối với connector `J3` (`SIM_PWR_CONN`) và gắn trạng thái `NEEDS_VERIFICATION`.
- **Yêu cầu cho PCB 1 lớp**:
  - Ngay sau khi chụp ảnh/đo kiểm mặt lưng breakout `A7682S` (xác nhận có LDO/diode nhận 5V từ `LX-2BUPS` hay không), có thể bố trí jumper hàn/cầu chì nối `5V_SYS` sang `SIM_PWR` kèm **tụ hóa dung lượng lớn (`470µF – 1000µF / 10V` Low-ESR) + tụ gốm `100nF`** đặt sát chân `VCC` và `GND` của `U5` để chống sụt áp khi SIM phát sóng/gửi SMS.
  - Độ rộng đường mạch `SIM_PWR` và `5V_SYS` trên lớp `B.Cu` phải đạt tối thiểu **`1.2mm – 2.0mm`** (RULE 09).

### 2.3. Xác minh điện áp `VCC` của Breakout `MicroSD` (`J1`) và `NEO-M8N` (`U4`)
- **MicroSD Breakout (`J1`)**:
  - Cần phân biệt 2 loại breakout phổ biến:
    1. **Loại 6 chân có LDO `AMS1117-3.3` + IC dịch mức `LVC125A` (Catalex / phổ biến nhất)**: Chân `VCC` được thiết kế nhận **`5V`** (qua `AMS1117-3.3` xuống 3.3V nuôi thẻ SD). Nếu cấp `3.3V` vào chân `VCC` của loại này, điện áp sau LDO chỉ còn $\approx 2.1\text{V} - 2.3\text{V}$, khiến thẻ MicroSD không khởi tạo được hoặc lỗi ghi file `blackbox.csv`!
    2. **Loại 6 chân trực tiếp `3V3` (không có LDO)**: Chân nguồn ghi rõ `3V3` và nhận trực tiếp `3.3V`.
  - Hiện trên schematic gốc (`REV8`) và bản `REV1`, chân số 1 của `J1` có tên là `3V3` và nối vào `3V3_SYS`. **Cần kiểm tra thực tế trên bàn thử nghiệm (breadboard) xem chân nguồn của module MicroSD đang cắm vào `3.3V` hay `5V`** trước khi chốt đường mạch đồng trên PCB!
- **GPS `NEO-M8N` (`U4`)**:
  - Tương tự, đa số module `GY-NEO6MV2 / NEO-M8N` có LDO `MIC5205-3.3` (low dropout ~150mV) trên board nên chạy được cả ở `3.3V` lẫn `5V`. Cần xác nhận điện áp đang đấu thực tế.

### 2.4. An toàn khi cắm đồng thời `USB` của `ESP32-S3-DevKitC-1` và nguồn `5V_SYS`
- Trong `filecodemain.cpp`, chương trình mở `Serial.begin(115200)` để theo dõi log qua cổng USB khi xe/hệ thống đang chạy bằng nguồn ngoài `5V_SYS`.
- Trên board `ESP32-S3-DevKitC-1` chính hãng / tương đương:
  - Ngõ vào cổng `USB` đi qua diode Schottky bảo vệ ngược dòng trước khi vào đường `5V`, **NHƯNG chân header `5V` (Pin 21)** thường nối thẳng vào đường `5V` sau diode USB (hoặc trước LDO `AMS1117-3.3`).
  - Nếu `5V_SYS` từ `LX-2BUPS` có áp cao hơn `VBUS` của máy tính, một số board clone không có diode chống ngược từ chân `5V` về cổng USB.
- **Khuyến nghị cho PCB 1 lớp**:
  - Đặt **1 jumper 2 chân (`JP_5V_ESP`) hoặc 1 diode Schottky dòng 1A–2A (`1N5819` / `SS14` / `SS34` kiểu chân cắm DO-41 để vừa làm cầu nhảy 1 lớp vừa chống dòng ngược)** nối giữa đường `5V_SYS` và chân `5V` (Pin 21) của `U1`. Nhờ đó có thể cắm cáp USB debug thoải mái khi `LX-2BUPS` đang bật mà không lo xung đột nguồn 5V.

### 2.5. Kiểm tra điện trở kéo lên (`Pull-up`) cộng dồn trên Bus I2C (`GPIO8` / `GPIO9`)
- Trên bus I2C hiện có 3 module mắc song song + 2 điện trở kéo lên ngoài `R_PU1 = 4.7kΩ`, `R_PU2 = 4.7kΩ`:
  1. `MPU6050 (GY-521)`: thường có sẵn điện trở kéo lên `4.7kΩ` (hoặc `2.2kΩ`) trên module.
  2. `DS3231 (Module 6 chân / ZS-042)`: thường có sẵn khối điện trở kéo lên `4.7kΩ` (4P2R `472`) trên module.
  3. `OLED 0.96" SSD1306`: thường có sẵn điện trở kéo lên `4.7kΩ` hoặc `10kΩ` trên module.
- **Tính toán trở kháng kéo lên tương đương ($R_{eq}$)**:
  Nếu cả 3 module đều có trở `4.7kΩ` lên `3.3V` và gắn thêm `R_PU1 / R_PU2 = 4.7kΩ` trên PCB:
  $$R_{eq} = \frac{4.7\text{k}\Omega}{4} \approx 1.175\text{k}\Omega \quad \Rightarrow \quad I_{sink} = \frac{3.3\text{V}}{1.175\text{k}\Omega} \approx 2.8\text{mA}$$
  Nếu `GY-521` dùng trở `2.2kΩ`, $R_{eq}$ giảm xuống dưới `900Ω` ($I_{sink} > 3.6\text{mA}$, vượt chuẩn Standard-mode I2C $3\text{mA}$, làm sườn xung `LOW` không kéo sát `0V` và dễ gây timeout I2C).
- **Khuyến nghị cho PCB**:
  - Giữ footprint của `R_PU1` và `R_PU2` trên PCB, nhưng đánh dấu **`DNP` (Do Not Populate — Không hàn)** nếu đo tổng trở từ `SDA`/`SCL` lên `3V3_SYS` khi đã cắm đủ 3 module nằm trong khoảng **`1.8kΩ – 4.7kΩ`**.

### 2.6. Giải pháp nếu sau này cần đo điện áp pin thật (`BAT_RAW`)
- Tuyệt đối không đo điện áp đường `5V_SYS` hoặc `3V3_SYS` để suy ra % pin 18650 (vì đầu ra của `LX-2BUPS` đã qua mạch ổn áp Boost 5V).
- Nếu muốn bổ sung tính năng báo % pin thật:
  1. Phải kéo 1 dây phụ từ cực `B+` (`BAT_RAW`, `3.0V – 4.2V`) của đế pin 18650 trên module `LX-2BUPS` qua connector phụ 2 chân về PCB.
  2. Dùng cầu phân áp `100kΩ / 100kΩ` + tụ lọc `100nF` đưa vào `GPIO1` (`ADC1_CH0`).
  3. Nếu không kéo dây `BAT_RAW`, giữ nguyên trạng thái `UNASSIGNED` (không vẽ cầu phân áp giả trên PCB).

