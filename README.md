# AIoT Smart Black Box for Electric Motorcycles

> **Tên đề tài**: Thiết kế hộp đen AIoT thông minh phân tích và ghi lại sự cố xe máy điện  
> **Tác giả**: Nguyễn Lê Công Danh (danhcln)  
> **Ngành**: Kỹ thuật Điện - Điện tử / IoT & Hệ thống nhúng  
> **Nền tảng vi điều khiển**: Espressif ESP32-S3 (N16R8)  
> **Công cụ thiết kế EDA**: KiCad v8 / v9  
> **Trạng thái phần cứng**: Đã hoàn thiện thiết kế mạch in PCB 1 lớp đồng `B.Cu` (Nghiệm thu GATE 3.2 - 0 lỗi ERC/DRC)

---

## 1. Giới thiệu dự án (Project Introduction)

Hộp đen AIoT (Event Data Recorder - EDR) cho xe máy điện là một thiết bị thông minh gắn trên phương tiện hai bánh nhằm liên tục giám sát trạng thái động học, phát hiện các tình huống tai nạn, va chạm, đổ ngã và tự động gửi cảnh báo khẩn cấp (kèm tọa độ định vị GPS toàn cầu) về người thân/cứu hộ thông qua mạng viễn thông 4G LTE.

Đồng thời, toàn bộ dữ liệu cảm biến (gia tốc 3 trục, vận tốc góc, vận tốc di chuyển, thời gian thực và trạng thái hệ thống) được ghi liên tục với tần số cao vào thẻ nhớ MicroSD theo định dạng hộp đen tiêu chuẩn, phục vụ công tác điều tra nguyên nhân tai nạn và phân tích hành vi lái xe.

```
+---------------------------------------------------------------------------------------------------+
|                                 HỆ THỐNG HỘP ĐEN AIoT XE MÁY ĐIỆN                                 |
+---------------------------------------------------------------------------------------------------+
|  [CẢM BIẾN & ĐỘNG HỌC]    [ĐỊNH VỊ & VIỄN THÔNG]     [LƯU TRỮ & HIỂN THỊ]    [NGUỒN & AN TOÀN]    |
|   - MPU6050 (Gia tốc/Góc)  - NEO-M8N (GPS/GNSS)       - MicroSD (SPI Logger)  - UPS LX-2BUPS (5V) |
|   - DS3231 (Thời gian RTC) - A7680C (4G LTE / SMS)    - OLED 0.96" (SSD1306)  - Pin 18650 Li-ion  |
|                                                                               - Còi 5V & Nút Hủy  |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
                               +-------------------------------------+
                               |   VI ĐIỀU KHIỂN TRUNG TÂM ESP32-S3  |
                               |    Dual-Core Xtensa LX7 @ 240MHz    |
                               |    16MB Flash + 8MB Octal PSRAM     |
                               +-------------------------------------+
```

---

## 2. Mục tiêu hệ thống (System Objectives)

1. **Giám sát động học thời gian thực**: Đo lường gia tốc 3 trục ($A_x, A_y, A_z$) và vận tốc góc ($\omega_x, \omega_y, \omega_z$) để phát hiện tức thời trạng thái ngã xe (nghiêng $> 60^\circ$) hoặc va chạm mạnh ($> 3G$).
2. **Định vị toàn cầu chính xác**: Cập nhật tọa độ kinh độ, vĩ độ, độ cao và tốc độ di chuyển từ vệ tinh GPS/GLONASS với chu kỳ 10Hz.
3. **Cảnh báo cứu nạn tự động qua SMS 4G**: Khi xảy ra sự cố, hệ thống đếm ngược 10 giây (kèm còi báo động). Nếu người lái không bấm nút hủy (CANCEL), hệ thống lập tức soạn tin nhắn SMS chứa link Google Maps chính xác gửi tới số điện thoại khẩn cấp.
4. **Ghi nhật ký hộp đen liên tục**: Lưu trữ dữ liệu cảm biến dạng CSV vào thẻ nhớ MicroSD (chu kỳ 100ms/mẫu) với nhãn thời gian thực chính xác đến từng giây từ RTC DS3231.
5. **Giao diện trực quan**: Hiển thị tốc độ xe, trạng thái kết nối GPS, sóng 4G, góc nghiêng và thời gian thực trên màn hình OLED 0.96 inch.
6. **Nguồn điện độc lập, tin cậy**: Sử dụng mạch quản lý sạc/xả thông minh UPS 2 cell 18650, tự động duy trì hoạt động khi ắc quy chính của xe bị ngắt nguồn do va chạm.
7. **Thiết kế phần cứng tối ưu chi phí**: Bo mạch Carrier Board được thiết kế hoàn hảo trên **PCB 1 lớp đồng `B.Cu`**, sử dụng các jumper dây cách điện chuẩn hóa, dễ dàng gia công và hàn thủ công trong điều kiện phòng thí nghiệm tại Việt Nam.

---

## 3. Sơ đồ khối tổng quan (System Architecture)

```
                       +-----------------------------+
                       |   Ắc quy xe / Nguồn USB-C   |
                       +-----------------------------+
                                      |
                                      v
                       +-----------------------------+
                       |    MẠCH NGUỒN LX-2BUPS      |
                       |  (Pin 18650 + Sạc + Boost)  |
                       +-----------------------------+
                                      |
                                      +------------------+
                                      | 5V_SYS (Tải 3A)   |
                                      v                  v
                             +-----------------+  +-----------------+
                             | BUCK MINI-360   |  |   A7680C 4G     |
                             | (5V -> 3V3_SYS) |  | (Đỉnh dòng 2A)  |
                             +-----------------+  +-----------------+
                                      |
       +------------------------------+------------------------------+
       |                              |                              |
       v                              v                              v
+---------------+             +---------------+             +-----------------+
| MPU-6050      |             | DS3231 RTC    |             | OLED 0.96"      |
| I2C: 0x69     |             | I2C: 0x68     |             | I2C: 0x3C       |
+---------------+             +---------------+             +-----------------+
       |                              |                              |
       +------------------------------+------------------------------+
                                      |
                                  Bus I2C (SDA: GPIO8 | SCL: GPIO9)
                                      |
                                      v
                       +-----------------------------+
                       |   ESP32-S3 DEVKITC-1 N16R8  |
                       +-----------------------------+
                        |      |        |          |
      Bus SPI (MOSI:11  |      |        |          |
               MISO:13  |      |        |          | UART (TX:17 | RX:18)
               SCK:12   |      |        |          +---------------------> NEO-M8N GPS
               CS:10)   |      |        |
                        v      |        | UART (TX:16 | RX:15)
                 MicroSD Card  |        +---------------------> SIM A7680C 4G
                               |
                               +------------------------------> Nút CANCEL (GPIO6)
                               |
                               +------------------------------> Còi báo (GPIO5) & LED (GPIO7)
```

---

## 4. Các linh kiện chính & Bảng bóc tách vật tư (BOM)

Toàn bộ các linh kiện trong hệ thống đã được kiểm toán thực tế và khóa mã trong bảng bóc tách vật tư [`BOM_MAINBOARD_REV1.csv`](./PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/BOM_MAINBOARD_REV1.csv):

| TT | Ký hiệu (RefDes) | Tên linh kiện / Module | Thông số kỹ thuật | Giao tiếp / Chân ESP32-S3 | Ghi chú & Vai trò |
|---|---|---|---|---|---|
| 1 | **U1** | ESP32-S3-DevKitC-1 N16R8 | Dual-Core 240MHz, 16MB Flash, 8MB PSRAM | Bo mạch trung tâm | Điều khiển toàn bộ hệ thống |
| 2 | **U2** | MPU-6050 (GY-521) | Con quay hồi chuyển & Gia tốc kế 6-DOF | I2C (SDA: 8, SCL: 9) | Chân AD0 nối 3V3 $\rightarrow$ Địa chỉ `0x69` |
| 3 | **U3** | DS3231 (ZS-042) | Real-Time Clock có bù nhiệt độ TCXO | I2C (SDA: 8, SCL: 9) | Địa chỉ `0x68` (Đã gỡ bỏ trở sạc R5) |
| 4 | **U4** | NEO-M8N GNSS Module | 72 kênh định vị đa vệ tinh (GPS/GLONASS) | UART (TX: 17, RX: 18) | Baudrate 9600 bps, chu kỳ 10Hz |
| 5 | **U5** | A7680C 4G LTE Breakout | LTE Cat-1 hỗ trợ SMS, TCP/IP, VoLTE | UART (TX: 16, RX: 15) | Baudrate 115200 bps, cấp nguồn hình sao |
| 6 | **J1** | MicroSD Card Adapter | Chuẩn SPI có đệm logic và IC ổn áp 3.3V | SPI (CS: 10, MOSI: 11, SCK: 12, MISO: 13) | Định dạng FAT32, ghi log sự cố liên tục |
| 7 | **U7** | OLED 0.96 inch | 128x64 điểm ảnh, Driver SSD1306 | I2C (SDA: 8, SCL: 9) | Địa chỉ `0x3C`, hiển thị trạng thái |
| 8 | **U6** | Module Buck 3.3V (Mini-360) | Hạ áp xung DC-DC 5V $\rightarrow$ 3.3V / 2A | Nguồn hệ thống | Cung cấp nguồn riêng `3V3_SYS` |
| 9 | **J2** | Module UPS LX-2BUPS | Mạch sạc/xả dự phòng 2 cell 18650, ra 5V/3A | Nguồn tổng `5V_SYS` | Cấp nguồn chính không gián đoạn |
| 10 | **BZ1** | Còi báo chủ động (Active Buzzer) | 5V Piezoelectric Audio Indicator | Điều khiển qua Q1 (GPIO5) | Kêu cảnh báo trước khi phát tín hiệu SOS |
| 11 | **SW1** | Nút bấm hủy cảnh báo (CANCEL) | Nút nhấn nhả THT kèm tụ chống dội 100nF | GPIO6 (Kéo lên $10\text{k}\Omega$) | Hủy phát SMS khẩn cấp trong 10 giây |
| 12 | **D1** | LED báo trạng thái 5mm | LED siêu sáng màu xanh lá kèm trở $330\Omega$ | GPIO7 | Nhấp nháy báo hệ thống hoạt động |
| 13 | **NT1** | Net-Tie hình sao nguồn SIM | Đường đồng liền `B.Cu` rộng 2.5mm | Nối `5V_SYS` $\rightarrow$ `SIM_PWR` | Ngăn sụt áp lan truyền khi phát sóng 4G |
| 14 | **JMP1..11**| 11 Wire Jumper mặt trên | Dây đồng 22/24 AWG bọc cách điện Teflon/PVC | Cắm xuyên lỗ xuống `B.Cu` | Xử lý các đường giao cắt trên PCB 1 lớp |

---

## 5. ESP32-S3 và Firmware (`filecodemain.cpp`)

Toàn bộ logic hoạt động được lập trình tối ưu trong file firmware duy nhất: [`filecodemain.cpp`](./filecodemain.cpp).

### Bản đồ phân bổ chân phần cứng (GPIO Mapping Locked)
```cpp
// 1. I2C Bus (OLED, RTC DS3231, IMU MPU6050)
#define I2C_SDA_PIN         8
#define I2C_SCL_PIN         9

// 2. SPI Bus (MicroSD Card Adapter)
#define SD_CS_PIN          10
#define SPI_MOSI_PIN       11
#define SPI_SCK_PIN        12
#define SPI_MISO_PIN       13

// 3. UART Hardware (Module 4G LTE A7680C)
#define SIM_TX_PIN         16   // ESP32 TX -> SIM RX
#define SIM_RX_PIN         15   // ESP32 RX -> SIM TX

// 4. UART Hardware (Module GPS NEO-M8N)
#define GPS_TX_PIN         17   // ESP32 TX -> GPS RX
#define GPS_RX_PIN         18   // ESP32 RX -> GPS TX

// 5. Điều khiển ngoại vi và an toàn
#define BUZZER_PIN          5   // Điều khiển cực Base transistor Q1
#define CANCEL_BTN_PIN      6   // Nút bấm hủy gửi SMS (kéo lên nội trở + R3)
#define LED_STATUS_PIN      7   // LED nhấp nháy chỉ báo trạng thái
```

### Thuật toán vận hành cốt lõi
1. **Khởi tạo (Setup)**:
   - Khởi tạo cổng nạp Serial (115200 bps).
   - Thiết lập I2C Bus tại tần số chuẩn 100kHz.
   - Quét bus I2C và khởi tạo OLED (`0x3C`), DS3231 (`0x68`), MPU6050 (`0x69`).
   - Cấu hình dải đo MPU6050 $\pm 16G$, bộ lọc thông thấp số $21\text{Hz}$.
   - Khởi tạo SPI và mount phân vùng thẻ nhớ MicroSD. Tạo file nhật ký `blackbox_YYYYMMDD.csv` nếu chưa có.
   - Khởi động UART1 (GPS) và UART2 (SIM 4G). Đồng bộ tập lệnh AT cho module SIM.
2. **Vòng lặp chính (Loop - Non-blocking State Machine)**:
   - **Tần số 10Hz (100ms)**: Đọc dữ liệu gia tốc và góc nghiêng từ MPU6050; đọc câu tin NMEA từ GPS. Ghi một dòng log vào thẻ nhớ:
     `Timestamp, AccX, AccY, AccZ, GyroX, GyroY, GyroZ, Lat, Lon, Speed, Status`
   - **Xử lý tai nạn**: Nếu góc nghiêng $|Angle| > 60^\circ$ hoặc $|Acc| > 3.0G$, hệ thống chuyển sang trạng thái `ACCIDENT_TRIGGERED`.
   - **Đếm ngược cứu hộ**: Bật còi BZ1 kêu bíp liên tục trong 10 giây. Nếu trong thời gian này người lái bấm nút CANCEL (GPIO6), hệ thống hủy lệnh và quay về bình thường.
   - **Gửi tin nhắn SOS**: Hết 10 giây, module A7680C kích hoạt lệnh `AT+CMGS`, gửi tin nhắn SMS chứa link Google Maps:
     `[EDR VI TRI XE] https://maps.google.com/?q=<Latitude>,<Longitude>`
   - **Cập nhật màn hình OLED (500ms)**: Hiển thị tọa độ, tốc độ, dung lượng thẻ nhớ và trạng thái kết nối.

> **Lưu ý bảo mật**: Trong bản chia sẻ công khai trên GitHub, số điện thoại khẩn cấp `DEFAULT_PHONE` được thay bằng giá trị placeholder `09xxxxxxxx`. Người triển khai thực tế chỉ cần thay bằng số điện thoại của người thân.

---

## 6. MPU6050 – Phát hiện chuyển động bất thường

- **Địa chỉ phần cứng I2C**: Được khóa cứng ở mức `0x69` bằng cách cấp nguồn `3V3_SYS` vào chân **AD0** (thông qua jumper `JMP8`). Điều này ngăn ngừa hoàn toàn hiện tượng xung đột địa chỉ với RTC DS3231 (`0x68`).
- **Xử lý tín hiệu**: Firmware sử dụng bộ lọc số thông thấp DLPF $21\text{Hz}$ để triệt tiêu dao động rung cơ học từ mặt đường và động cơ xe máy điện, chỉ bắt các xung gia tốc thực của va chạm.
- **Quy chuẩn bố trí trên PCB**: Module MPU6050 được đặt tại tâm trọng lực bo mạch (Zone 4), cách xa còi báo động tối thiểu 40mm để chống nhiễu sóng âm và từ trường.

---

## 7. GPS NEO-M8N – Định vị toàn cầu

- **Độ nhạy & Băng tần**: Hỗ trợ đồng thời hệ thống định vị GPS của Mỹ và GLONASS của Nga. Tốc độ cập nhật 10Hz, độ chính xác vị trí $< 2.5\text{m}$.
- **Bảo toàn tín hiệu**: Giao tiếp qua UART phần cứng (GPIO17 / GPIO18) với baudrate 9600 bps. Pin dự phòng trên module giúp duy trì dữ liệu ephemeris vệ tinh (Hot Start $< 1\text{s}$).

---

## 8. SIM A7680C – Viễn thông 4G LTE & Gửi SMS

- **Băng tần mạng**: Hỗ trợ 4G LTE Cat-1 (B1/B3/B5/B8/B34/B38/B39/B40/B41) tương thích hoàn toàn với tất cả nhà mạng tại Việt Nam (Viettel, Vinaphone, Mobifone).
- **Chống sụt áp phát sóng**: Module 4G tiêu thụ dòng đỉnh lên tới $2\text{A}$ trong thời gian ngắn (xung phát RF 577µs). Mạch in được trang bị nhánh nguồn hình sao `SIM_PWR` rộng 2.5mm đi qua Net-Tie `NT1` cùng cặp tụ lọc Low-ESR $470\mu\text{F}$ và $100\text{nF}$ đặt sát chân cấp nguồn module.

---

## 9. RTC DS3231 – Thời gian thực chính xác cao

- **Độ chính xác**: Sử dụng thạch anh tích hợp có bù nhiệt độ (TCXO), sai số cực thấp $< \pm 2\text{ppm}$ ($< 1$ phút mỗi năm).
- **An toàn pin**: Đã gỡ bỏ điện trở sạc R5 trên module ZS-042 để sử dụng an toàn với pin cúc áo thông thường CR2032 không sạc, loại bỏ triệt để nguy cơ phồng nổ pin.

---

## 10. MicroSD – Ghi dữ liệu hộp đen

- Giao tiếp qua bus SPI tốc độ cao. Dữ liệu được ghi theo khối nhị phân và đóng gói định dạng CSV tiêu chuẩn.
- Tự động kiểm tra tính toàn vẹn của thẻ nhớ khi khởi động; chỉ thị cảnh báo lỗi lên OLED nếu thẻ chưa được cắm hoặc hỏng định dạng.

---

## 11. OLED 0.96 inch – Màn hình hiển thị

- Sử dụng màn hình OLED công nghệ SSD1306 độ phân giải 128x64 điểm ảnh, giao tiếp I2C 2 dây.
- Hiển thị trực quan tốc độ di chuyển hiện tại, số lượng vệ tinh GPS kết nối, trạng thái sóng 4G, góc nghiêng thời gian thực và thời gian ngày/giờ.

---

## 12. Khối nguồn thông minh UPS LX-2BUPS

- **Nguồn cấp chính**: 2 cell pin Lithium-ion 18650 mắc song song, tích hợp IC quản lý sạc/xả thông minh và mạch boost DC-DC đồng bộ cho ra điện áp ổn định $5\text{V} / 3\text{A}$ (`5V_SYS`).
- **Nguồn sạc ngoài**: Cổng USB-C / VBUS hỗ trợ sạc điện tự động khi cắm sạc ngoài.
- **Nguồn thứ cấp**: Module Buck xung Mini-360 hạ áp từ `5V_SYS` xuống `3V3_SYS` cấp riêng cho khối logic cảm biến, tuyệt đối không dùng nguồn từ chân 3.3V của ESP32 để nuôi ngoại vi.

---

## 13. Bản vẽ Schematic KiCad

Hệ thống được thiết kế hoàn chỉnh trên KiCad EDA với đầy đủ các dự án nguyên lý:
1. **Schematic hệ thống chính**: Nằm tại [`PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/AIOT_BLACKBOX_MAINBOARD_REV1.kicad_sch`](./PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/AIOT_BLACKBOX_MAINBOARD_REV1.kicad_sch).
2. **Schematic báo cáo & thuyết minh chuẩn A4 Landscape**: Nằm tại [`Schematic_Thay/AIOT_BLACKBOX_PRESENTATION/AIOT_BLACKBOX_PRESENTATION.kicad_sch`](./Schematic_Thay/AIOT_BLACKBOX_PRESENTATION/AIOT_BLACKBOX_PRESENTATION.kicad_sch).
3. **Schematic chuyên sâu khối nguồn**: Nằm tại [`THIET_KE_KHOI_NGUON/AIOT_BLACKBOX_POWER_SUPPLY.kicad_sch`](./THIET_KE_KHOI_NGUON/AIOT_BLACKBOX_POWER_SUPPLY.kicad_sch).

---

## 14. Thiết kế PCB một lớp đồng `B.Cu` & 11 Wire Jumper

Nhằm phục vụ chế tạo thủ công trong phòng thí nghiệm (phương pháp ủi phim nhiệt, rửa mạch hóa chất $\text{FeCl}_3$ hoặc phay cơ CNC PCB 1 mặt), bo mạch được thiết kế theo các nguyên tắc nghiêm ngặt:
- **Chỉ 1 lớp đồng dẫn điện**: Toàn bộ đường mạch đồng, pad hàn và mặt phẳng mass GND đều nằm độc quyền trên lớp đáy **`B.Cu`**.
- **Không sử dụng Via**: Tuyệt đối không có via xuyên bo, loại bỏ hoàn toàn công đoạn gia công mạ lỗ phức tạp.
- **Giải quyết giao cắt bằng 11 Jumper dây cách điện**: Các đường tín hiệu logic bị giao cắt được xử lý bằng 11 cầu nhảy dây đồng lõi đơn (Teflon/PVC) cắm mặt trên (`Top`) và hàn vào các pad THT chuyên dụng.

### Bảng thông số kỹ thuật 11 Jumper dây (REV3)
| Jumper | Pitch (mm) | Net kết nối | Vai trò kỹ thuật |
|---|---|---|---|
| **`JMP1`** | 12.70 mm | `Net-(J1-MOSI)` | Nhảy tín hiệu SPI MOSI qua SCK và MISO vào ESP32 Pin 17 |
| **`JMP2`** | 7.62 mm | `3V3_SYS` | Nhảy nguồn 3V3_SYS qua đường SIM_PWR (2.5mm) cấp R3 nút bấm |
| **`JMP3`** | 7.62 mm | `Net-(U1-GPIO6)` | Nhảy tín hiệu CANCEL qua chân Base Q1 còi báo động vào ESP32 Pin 6 |
| **`JMP4`** | 10.16 mm | `/I2C_SDA_GPIO8` | Nhảy bus dữ liệu I2C_SDA qua đường ngang SCL (Y=91.50) |
| **`JMP5`** | 7.62 mm | `Net-(U1-GPIO6)` | Nhảy tín hiệu CANCEL qua xương nguồn 5V_SYS (Y=43.50) |
| **`JMP6`** | 10.16 mm | `Net-(J1-MISO)` | Nhảy tín hiệu SPI MISO qua chân 5V và GND của header MicroSD J1 |
| **`JMP7`** | 10.16 mm | `3V3_SYS` | Nhảy nguồn 3V3_SYS qua SCL cấp cho RTC DS3231 và IMU MPU6050 |
| **`JMP8`** | 12.70 mm | `3V3_SYS` | Nhảy 3V3_SYS cấp AD0 MPU6050 để khóa cứng địa chỉ I2C `0x69` |
| **`JMP9`** | 7.62 mm | `3V3_SYS` | Nhảy 3V3_SYS cấp trở kéo lên R_PU2 ($4.7\text{k}\Omega$) cho bus SCL |
| **`JMP10`** | 7.62 mm | `/I2C_SCL_GPIO9` | Nhảy xung I2C_SCL qua sống ngang SDA (Y=104.00) cấp màn hình OLED |
| **`JMP11`** | 12.70 mm | `GND` | Nhảy mass GND MicroSD J1.6 qua sống 5V_SYS vào mặt phẳng mass GND |

---

## 15. Hình ảnh phần cứng & Bản vẽ PCB (Gallery)

Các bản vẽ độ phân giải cao 300 DPI phục vụ chế tạo và lắp ráp được lưu trữ tại thư mục [`PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/`](./PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/):

- **Bản vẽ mặt đồng đáy (B.Cu Mirrored)**: [`PCB_ROUTING_BOTTOM_COPPER_ONLY_REV3.png`](./PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/PCB_ROUTING_BOTTOM_COPPER_ONLY_REV3.png) – Bản vẽ soi gương sẵn sàng in phim rửa mạch.
- **Bản vẽ lắp ráp & Jumper mặt trên (Top Assembly)**: [`PCB_ROUTING_TOP_JUMPERS_REV3.png`](./PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/PCB_ROUTING_TOP_JUMPERS_REV3.png) – Hướng dẫn chi tiết vị trí và màu sắc dây jumper.
- **Bản vẽ bố trí linh kiện tổng thể (Top Placement)**: [`PCB_PLACEMENT_TOP_REV2.png`](./PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_2_PLACEMENT/PCB_PLACEMENT_TOP_REV2.png).
- **Hình ảnh linh kiện module thực tế**: Lưu trữ trong thư mục [`Hình ảnh linh kiện/`](./Hình%20ảnh%20linh%20kiện/).

---

## 16. Cấu trúc thư mục Repository & Hướng dẫn tra cứu (Navigation Guide)

```
AIOT-BLACK-BOX/
├── .agents/                                # Quy tắc thiết kế và skill của hệ thống Antigravity
│   ├── rules/                              # PCB_DESIGN_RULES_AIOT.md và quy tắc an toàn
│   └── skills/                             # Các công cụ kiểm toán, xác minh và sửa lỗi
├── Bao_Cao/                                # Báo cáo đồ án định dạng Word (.docx) và PDF
├── DATASHEET_LINH_KIEN/                    # Chỉ mục tra cứu thông số kỹ thuật và link chính hãng
│   ├── DATASHEET_INDEX.csv                 # Bảng tra cứu CSV 30 tài liệu sản xuất
│   ├── DATASHEET_INDEX.xlsx                # Bảng tính Excel định dạng màu
│   └── README.md                           # Hướng dẫn và link tải trực tiếp từ nhà sản xuất
├── Hình ảnh linh kiện/                     # Thư viện ảnh chụp thực tế hai mặt của các module
├── Mẫu của thầy/                           # Biểu mẫu, nhật ký và sơ đồ khối mẫu từ giảng viên
├── PCB_AIOT_BLACKBOX/                      # Dự án thiết kế mạch in PCB KiCad
│   └── AIOT_BLACKBOX_MAINBOARD_REV1/       # Project PCB chính thức của hệ thống
│       ├── AIOT_Blackbox_Local.pretty/     # Thư viện Footprint KiCad nội bộ dự án
│       ├── BOM_MAINBOARD_REV1.csv          # Bảng bóc tách vật tư 40 linh kiện (kèm 11 jumper)
│       ├── GATE_0_AUDIT/                   # Hồ sơ kiểm toán code, sơ đồ chân và công suất
│       ├── GATE_1_FOOTPRINT/               # Hồ sơ xác minh footprint và kích thước cơ khí
│       ├── GATE_2_PLACEMENT/               # Hồ sơ và hình ảnh định vị linh kiện chuẩn RF
│       ├── GATE_3_ROUTING/                 # Bản vẽ PCB hoàn thiện REV3 (Bottom & Top Jumpers)
│       ├── AIOT_BLACKBOX_MAINBOARD_REV1.kicad_pcb # File thiết kế mạch in KiCad PCB chính thức
│       ├── AIOT_BLACKBOX_MAINBOARD_REV1.kicad_sch # File nguyên lý kết nối bo mạch
│       └── fp-lib-table, sym-lib-table     # Cấu hình thư viện dự án
├── Schematic/                              # Thiết kế nguyên lý ban đầu
├── Schematic_Thay/                         # Thiết kế nguyên lý chuẩn hóa thuyết minh A4 Landscape
├── THIET_KE_KHOI_NGUON/                    # Dự án thiết kế và tính toán chi tiết khối nguồn
├── filecodemain.cpp                        # Firmware chính thức của ESP32-S3
├── SCHEMATIC_DRAWING_RULES.md              # Bộ quy chuẩn trình bày bản vẽ nguyên lý
├── BAO_GIA_LINH_KIEN_AIOT_SMART_BLACK_BOX.xlsx # Bảng báo giá linh kiện thị trường TP.HCM
├── .gitignore                              # Cấu hình loại bỏ file rác, file tạm và cache
└── README.md                               # Tài liệu giới thiệu tổng quan dự án (File này)
```

> **Lưu ý về thư viện KiCad**: Để đảm bảo tính độc lập và khả năng mở dự án trên mọi máy tính khác nhau mà không bị mất dấu thư viện, dự án sử dụng bảng ánh xạ thư viện cục bộ (`sym-lib-table` và `fp-lib-table`). Nếu mở trên máy mới, hãy giữ nguyên cấu trúc thư mục để KiCad tự động nhận diện biến môi trường `${KIPRJMOD}`.

---

## 17. Trạng thái phát triển hiện tại (Development Status)

- **Firmware**: Đã nạp và kiểm tra thành công trên phần cứng rời (ESP32-S3, OLED, MPU6050, DS3231, NEO-M8N, A7680C, MicroSD).
- **Schematic**: Đạt **0 Error, 0 Warning** khi chạy kiểm tra tự động `kicad-cli sch erc`.
- **PCB Carrier Board**: Đã hoàn thành nghiệm thu **GATE 3.2** trên bo mạch 1 lớp đồng `B.Cu` với 11 wire jumper, đạt **0 vi phạm chập mạch, 0 vi phạm khoảng cách cách điện, 0 vi phạm va chạm lỗ khoan và 0 đường dây giao cắt**.
- **Kế hoạch tiếp theo**: Tiến hành phân tích toàn vẹn nguồn điện tải nặng (GATE 4), chuẩn bị xuất Gerber và chế tạo mẫu thử nghiệm vật lý (GATE 5 & 6).

---

## 18. Các bước thử nghiệm & Hạn chế kỹ thuật (Testing & Limitations)

1. **Hạn chế của mạch in 1 lớp**: Việc sử dụng 11 wire jumper ở mặt trên là bắt buộc do định lý tô-pô mặt phẳng đối với các mạch có mật độ bus song song cao (I2C, SPI, UART). Người lắp ráp cần tuân thủ nghiêm ngặt bảng hướng dẫn chiều dài và cỡ dây trong file [`JUMPER_ASSEMBLY_REV3.csv`](./PCB_AIOT_BLACKBOX/AIOT_BLACKBOX_MAINBOARD_REV1/GATE_3_ROUTING/JUMPER_ASSEMBLY_REV3.csv).
2. **Yêu cầu đo kiểm trước khi cấp nguồn**: Do các lô linh kiện mua thực tế tại cửa hàng có thể có sự khác biệt về điện áp chân VCC của module SIM (3.8V hay 5V) hoặc thứ tự chân OLED (GND-VCC hay VCC-GND), bắt buộc phải dùng đồng hồ VOM đo kiểm tra thông mạch và điện áp tại các Test Point (`TP1`, `TP2`, `TP3`, `TP4`) trước khi cắm module vào socket.
3. **Môi trường hoạt động**: Thiết bị được thiết kế thử nghiệm trong môi trường xe máy điện tiêu chuẩn; khi đóng vỏ thực tế cần bổ sung đệm mút cao su chống sốc quanh cảm biến MPU6050 để giảm thiểu tối đa hiện tượng báo động giả do rung xóc cơ học.
