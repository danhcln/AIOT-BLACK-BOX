# DANH MỤC SỐ ĐO ĐÃ XÁC MINH & CẦN ĐO BỔ SUNG (`MODULE_DIMENSION_CHECKLIST.md`)

**Dự án**: THIẾT KẾ HỘP ĐEN AIoT THÔNG MINH PHÂN TÍCH VÀ GHI LẠI SỰ CỐ XE MÁY ĐIỆN  
**Project KiCad**: `D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1`  

---

## 1. CÁC THÔNG SỐ ĐÃ XÁC MINH ĐỦ ĐỘ TIN CẬY TỪ ẢNH (`VERIFIED`)

Các thông số dưới đây đã được xác minh trực tiếp từ chữ in trên PCB trong bộ ảnh `D:\ĐỒ ÁN 2\Hình ảnh linh kiện` và chuẩn pitch header `2.54 mm` (100 mil):

1. **`OLED 0.96" GM009605v4.3` (`U7`)**:
   - Kích thước bao ngoài PCB: **`27.0 mm (Rộng) × 24.7 mm (Cao) × 1.2 mm (Dày)`** *(in trực tiếp `24.7x27x1.2` trên silkscreen mặt sau trong ảnh `6ea5164c1a8d3554c625e8bc03efef54.jpg`)*.
   - Hàng chân: `1x04`, pitch `2.54 mm`, thứ tự `1:GND, 2:VDD, 3:SCK, 4:SDA`.
2. **`ESP32-S3-N16R8` (`U1`) — Số lượng chân & Thứ tự chân**:
   - Số lượng chân: **`44 chân` (`2 hàng × 22 chân`)**, pitch dọc theo mỗi hàng là **`2.54 mm`** (tổng chiều dài mỗi hàng chân = `21 × 2.54 = 53.34 mm`).
   - Thứ tự 44 chân: Đã xác minh 100% từ ảnh mặt sau `2dad8255752d7c0230db6d0f5b913e92.jpg`.
3. **Pitch và Thứ tự chân Header của 5 Module Ngoại vi**:
   - **`MPU6050 GY-521` (`U2`)**: Header `1x08`, pitch `2.54 mm` (`1:VCC..8:INT`).
   - **`RTC DS3231 ZS-042` (`U3`)**: Header `1x06`, pitch `2.54 mm` (`1:32K..5:VCC, 6:GND`).
   - **`MicroSD Card Adapter` (`J1`)**: Header `1x06`, pitch `2.54 mm` (`1:CS, 2:SCK, 3:MOSI, 4:MISO, 5:VCC, 6:GND`).
   - **`GPS NEO-M8N V2149` (`U4`)**: Header `1x05`, pitch `2.54 mm` (`1:VCC, 2:GND, 3:TXD, 4:RXD, 5:PPS`).
   - **`SIM Breakout J6` (`U5`)**: Header phải `1x05`, pitch `2.54 mm` (`1:VCC, 2:RST, 3:RXD, 4:TXD, 5:GND`).

---

## 2. DANH MỤC SỐ ĐO CÒN THIẾU CẦN ĐO BẰNG THƯỚC KẸP (`PENDING_MEASUREMENT`)

Do các ảnh chụp trong `D:\ĐỒ ÁN 2\Hình ảnh linh kiện` không đặt kèm thước đo milimet nên theo đúng quy tắc **không ước lượng kích thước từ ảnh thiếu thước**, bạn chỉ cần đo **1 thông số bắt buộc** (và 2 thông số tùy chọn nếu muốn bắt ốc cố định trực tiếp lên PCB) trước khi sang Gate 2:

### A. THÔNG SỐ BẮT BUỘC PHẢI ĐO TRƯỚC KHI TẠO FOOTPRINT `ESP32-S3` (1 Số đo duy nhất)

- [ ] **Khoảng cách tâm-đến-tâm giữa 2 hàng chân `ESP32-S3 N16R8` (`U1` Row-to-Row Pitch)**:
  - **Cách đo**: Dùng thước kẹp (caliper) hoặc thước thẳng milimet đo khoảng cách từ tâm chân hàng bên trái sang tâm chân đối diện ở hàng bên phải (hoặc cắm thử lên breadboard và đếm số lỗ trống giữa 2 hàng chân).
  - **Giá trị thường gặp**:
    - Phương án A: **`25.40 mm`** (`1000 mil` = cách nhau **10 khoảng lỗ** breadboard) — rất phổ biến trên board `YD-ESP32-S3` có 2 cổng USB-C.
    - Phương án B: **`22.86 mm`** (`900 mil` = cách nhau **9 khoảng lỗ** breadboard) — chuẩn Espressif `DevKitC-1` đời đầu.
  - **Kích thước Dài × Rộng bao ngoài PCB `ESP32-S3`** (để vẽ đường bao silkscreen/courtyard): `.......... mm × .......... mm`.

---

### B. THÔNG SỐ XÁC NHẬN ĐIỆN ÁP & MÃ MODULE TRƯỚC KHI ĐẤU NGUỒN THẬT (2 Câu hỏi kỹ thuật)

- [ ] **1. Giải quyết `CONFLICT` nguồn `VCC` của `MicroSD Card Adapter` (`J1`)**:
  - Ảnh thực tế cho thấy `J1` có IC ổn áp **`AMS1117-3.3`** nối ở đầu vào chân `VCC` (Pin 5), nghĩa là module này cần cấp **`5V_SYS`** vào chân `VCC` (khi thử nghiệm thực tế trước đây bạn đã cắm `VCC` của MicroSD vào chân `5Vin` hay `3V3` của ESP32?).
  - **Lựa chọn của bạn cho PCB**:
    - [ ] Chuyển chân `VCC` (Pin 5) của `J1` sang **`5V_SYS`**.
    - [ ] Đặt **Jumper 3 chân (`JP_SD_VCC`)** trên PCB để chọn linh hoạt giữa `5V_SYS` và `3V3_SYS` *(Khuyến nghị an toàn nhất cho PCB 1 lớp)*.
- [ ] **2. Xác nhận điện áp `VCC` (`SIM_PWR`) và mã hiệu trên nắp shield của `Module Sim` (`U5`)**:
  - Mã chữ in trên mặt nắp kim loại của module SIM khi nhìn nghiêng ngoài đời thực là **`A7680C`** hay **`A7682S`**?
  - Khi chạy thử nghiệm với `filecodemain.cpp`, chân `VCC` của module SIM được cấp từ nguồn mấy Volt (`5.0V` từ bộ UPS `LX-2BUPS` hay nguồn `4.0V–4.2V` riêng)?

---

### C. THÔNG SỐ TÙY CHỌN (Chỉ cần đo nếu muốn khoan lỗ bắt vít M2/M3 cho module con ngay trên mặt PCB chính)

- [ ] **Khoảng cách tâm 2 lỗ vít M3 của `MPU6050 GY-521` (`U2`)** và khoảng cách từ hàng chân `1x08` tới tâm lỗ vít (nếu muốn bắt vít cố định `GY-521` nằm ngang trên PCB chính sau khi đổi sang header thẳng).
- [ ] **Thông tin Module nguồn `3.3V` (`U6`)**: Bạn dự kiến dùng module hạ áp `5V -> 3.3V` loại nào (ví dụ `AMS1117-3.3` breakout 3 chân/4 chân hay `MP1584/MINI360` buck), hay chỉ cần để domino/header chờ `1x04 P2.54mm` trên PCB?
