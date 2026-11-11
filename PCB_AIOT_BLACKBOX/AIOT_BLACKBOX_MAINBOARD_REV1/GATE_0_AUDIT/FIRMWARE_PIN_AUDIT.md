# BÁO CÁO ĐỐI CHIẾU CHÂN GPIO FIRMWARE VÀ SCHEMATIC ĐÃ CHỐT (`FIRMWARE_PIN_AUDIT.md`)

**Firmware chuẩn:** `D:\ĐỒ ÁN 2ilecodemain.cpp` (Giữ nguyên 100%, không chỉnh sửa)  
**Schematic KiCad:** `D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1\AIOT_BLACKBOX_MAINBOARD_REV1.kicad_sch`

---

## 1. BẢNG PHÂN LOẠI TOÀN BỘ CHÂN GPIO TRÊN BO MẠCH

| Nhóm chức năng | Chân ESP32-S3 (`U1`) | Số Pad trên Symbol/Footprint `U1` | Tên Net trên Schematic | Khối ngoại vi kết nối | Trạng thái trong `filecodemain.cpp` | Trạng thái Phần cứng / Schematic |
| :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **1. I2C Bus** | **`GPIO8`** | Pad `12` (Hàng trái) | `I2C_SDA_GPIO8` | `U7` OLED (Pin 4) + `U2` MPU6050 (Pin 4) + `U3` DS3231 (Pin 4) + `R_PU1 (4.7k)` | **ACTIVE** (`#define I2C_SDA 8`) | **LOCKED** |
| **1. I2C Bus** | **`GPIO9`** | Pad `15` (Hàng trái) | `I2C_SCL_GPIO9` | `U7` OLED (Pin 3) + `U2` MPU6050 (Pin 3) + `U3` DS3231 (Pin 3) + `R_PU2 (4.7k)` | **ACTIVE** (`#define I2C_SCL 9`) | **LOCKED** |
| **2. SPI MicroSD** | **`GPIO10`** | Pad `16` (Hàng trái) | `SD_CS_GPIO10` | `J1` MicroSD (Pin 1 `CS`) | **ACTIVE** (`#define SD_CS 10`) | **LOCKED** |
| **2. SPI MicroSD** | **`GPIO11`** | Pad `17` (Hàng trái) | `Net-(J1-MOSI)` | `J1` MicroSD (Pin 3 `MOSI`) | **ACTIVE** (`#define SPI_MOSI 11`) | **LOCKED** |
| **2. SPI MicroSD** | **`GPIO12`** | Pad `18` (Hàng trái) | `Net-(J1-SCK)` | `J1` MicroSD (Pin 2 `SCK`) | **ACTIVE** (`#define SPI_SCK 12`) | **LOCKED** |
| **2. SPI MicroSD** | **`GPIO13`** | Pad `19` (Hàng trái) | `Net-(J1-MISO)` | `J1` MicroSD (Pin 4 `MISO`) | **ACTIVE** (`#define SPI_MISO 13`) | **LOCKED** |
| **3. UART1 SIM 4G** | **`GPIO15`** | Pad `8` (Hàng trái) | `SIM_RX_GPIO15` | `U5` **`A7680C`** (Pin 4 `TXD`) | **ACTIVE** (`#define SIM_RX 15`) | **LOCKED** |
| **3. UART1 SIM 4G** | **`GPIO16`** | Pad `9` (Hàng trái) | `SIM_TX_GPIO16` | `U5` **`A7680C`** (Pin 3 `RXD`) | **ACTIVE** (`#define SIM_TX 16`) | **LOCKED** |
| **4. UART2 GPS** | **`GPIO17`** | Pad `10` (Hàng trái) | `GPS_TX_GPIO17` | `U4` `NEO-M8N` (Pin 4 `RXD`) | **ACTIVE** (`#define GPS_TX 17`) | **LOCKED** |
| **4. UART2 GPS** | **`GPIO18`** | Pad `11` (Hàng trái) | `GPS_RX_GPIO18` | `U4` `NEO-M8N` (Pin 3 `TXD`) | **ACTIVE** (`#define GPS_RX 18`) | **LOCKED** |
| **5. Dự phòng đã khóa** | **`GPIO5`** | Pad `5` (Hàng trái) | `BUZZER_CTRL_GPIO5` | `R5 (1kΩ)` → Base `Q1 (2SC1815)` + `R6 (10kΩ R_BE)` → `BZ1 (5V Buzzer)` | **RESERVE** *(Chưa khai báo trong `filecodemain.cpp` hiện tại)* | **LOCKED IN HARDWARE** *(Sẵn sàng cho firmware tiếp theo)* |
| **5. Dự phòng đã khóa** | **`GPIO6`** | Pad `6` (Hàng trái) | `CANCEL` | `SW1` (Nút nhấn `CANCEL`) + `R3 (10kΩ -> 3V3_SYS)` + `C2 (100nF -> GND)` | **RESERVE** *(Chưa khai báo trong `filecodemain.cpp` hiện tại)* | **LOCKED IN HARDWARE** *(Sẵn sàng cho firmware tiếp theo)* |
| **5. Dự phòng đã khóa** | **`GPIO7`** | Pad `7` (Hàng trái) | `LED_STATUS_GPIO7` | `R4 (330Ω)` → Anode `D1 (LED)` → `GND` | **RESERVE** *(Chưa khai báo trong `filecodemain.cpp` hiện tại)* | **LOCKED IN HARDWARE** *(Sẵn sàng cho firmware tiếp theo)* |
| **6. Chân để trống** | **`GPIO4`** | Pad `4` (Hàng trái) | `unconnected` | Không nối (`no_connect`) | Không dùng | **NC (Dự phòng trống)** |
| **6. Chân để trống** | `GPIO1, GPIO14, GPIO21, GPIO43, GPIO44...` | Các pad còn lại | `unconnected` | Không nối (`no_connect`) | Không dùng | **NC** |

---

## 2. KẾT LUẬN ĐỒNG BỘ GPIO
- **10/10 chân GPIO đang chạy trong `filecodemain.cpp`** (`GPIO8, 9, 10, 11, 12, 13, 15, 16, 17, 18`) khớp tuyệt đối 100% giữa Firmware, Schematic và Netlist.
- **3/3 chân dự phòng giao diện người dùng & cảnh báo** (`GPIO5 = BUZZER_CTRL`, `GPIO6 = CANCEL_BUTTON`, `GPIO7 = LED_STATUS`) đã được khóa cố định trên Schematic và Netlist, hoàn toàn tách biệt với các chân truyền thông đang chạy.
