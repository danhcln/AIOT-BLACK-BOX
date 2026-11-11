# BÁO CÁO ĐỐI CHIẾU ÁNH XẠ CHÂN SYMBOL ↔ FOOTPRINT ↔ MODULE THỰC TẾ (`FOOTPRINT_PIN_MAPPING_AUDIT.md`)

**Dự án**: THIẾT KẾ HỘP ĐEN AIoT THÔNG MINH PHÂN TÍCH VÀ GHI LẠI SỰ CỐ XE MÁY ĐIỆN  
**Project KiCad**: `D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1`  
**Thư viện Symbol Local**: `Presentation.kicad_sym`  
**Thư viện Footprint Local**: `AIOT_Blackbox_Local.pretty`  

---

## 1. TỔNG HỢP ĐỒNG BỘ SỐ CHÂN (`SYMBOL PIN NUMBER` = `FOOTPRINT PAD NUMBER` = `SILKSCREEN THỰC TẾ`)

Trong bước hoàn thiện Gate 1 bằng ảnh thực tế, **3 Symbol trong `Presentation.kicad_sym` và `AIOT_BLACKBOX_MAINBOARD_REV1.kicad_sch`** (`J1`, `U4`, `U5`) đã được cập nhật lại thuộc tính `(number "...")` để khớp 100% với thứ tự chân vật lý trên ảnh mà không làm thay đổi bất kỳ đường dây hay net nào trong schematic.

---

### 1.1. `U1` — `ESP32-S3-DevKitC-1 N16R8` (`Presentation:ESP32-S3-DevKitC-1`)
- **Ảnh đối chiếu**: `ESP32 N16R8\1794204039506_..._2dad8255752d7c0230db6d0f5b913e92.jpg`
- **Trạng thái Footprint**: `PENDING_MEASUREMENT` (chờ đo khoảng cách 2 hàng chân `22.86mm` vs `25.40mm`).
- **Bảng kiểm tra 12 chân đang kết nối trong Schematic + toàn bộ 44 chân**:

| Hàng chân trên Module | Thứ tự từ trên (Anten) xuống dưới (USB-C) | Số chân Symbol `U1` | Tên chân trên PCB `ESP32-S3` | Net trên Schematic (`filecodemain.cpp`) | Trạng thái |
| :--- | :---: | :---: | :--- | :--- | :---: |
| **Hàng Trái** | Chân 1..2 | `1`, `2` | `3V3`, `3V3` | `NC` (Không cấp chung với `3V3_SYS`) | `VERIFIED` |
| **Hàng Trái** | Chân 3 | `3` | `RST` | `NC` | `VERIFIED` |
| **Hàng Trái** | Chân 4..7 | `4`, `5`, `6`, `7` | `4`, `5`, `6`, `7` | `NC` (Chân dự phòng chưa gán) | `VERIFIED` |
| **Hàng Trái** | **Chân 8** | **`8`** | **`15` (`GPIO15`)** | **`SIM_RX_GPIO15`** (`UART1 RX` từ SIM `TXD`) | **`VERIFIED`** |
| **Hàng Trái** | **Chân 9** | **`9`** | **`16` (`GPIO16`)** | **`SIM_TX_GPIO16`** (`UART1 TX` tới SIM `RXD`) | **`VERIFIED`** |
| **Hàng Trái** | **Chân 10** | **`10`** | **`17` (`GPIO17`)** | **`GPS_TX_GPIO17`** (`UART2 RX` từ GPS `TXD`) | **`VERIFIED`** |
| **Hàng Trái** | **Chân 11** | **`11`** | **`18` (`GPIO18`)** | **`GPS_RX_GPIO18`** (`UART2 TX` tới GPS `RXD`) | **`VERIFIED`** |
| **Hàng Trái** | **Chân 12** | **`12`** | **`8` (`GPIO8`)** | **`I2C_SDA_GPIO8`** (`I2C SDA` chung OLED/MPU/RTC) | **`VERIFIED`** |
| **Hàng Trái** | Chân 13..14 | `13`, `14` | `3`, `46` | `NC` | `VERIFIED` |
| **Hàng Trái** | **Chân 15** | **`15`** | **`9` (`GPIO9`)** | **`I2C_SCL_GPIO9`** (`I2C SCL` chung OLED/MPU/RTC) | **`VERIFIED`** |
| **Hàng Trái** | **Chân 16** | **`16`** | **`10` (`GPIO10`)** | **`SD_CS_GPIO10`** (`MicroSD SPI CS`) | **`VERIFIED`** |
| **Hàng Trái** | **Chân 17** | **`17`** | **`11` (`GPIO11`)** | **`SPI_MOSI_GPIO11`** (`MicroSD SPI MOSI`) | **`VERIFIED`** |
| **Hàng Trái** | **Chân 18** | **`18`** | **`12` (`GPIO12`)** | **`SPI_SCK_GPIO12`** (`MicroSD SPI SCK`) | **`VERIFIED`** |
| **Hàng Trái** | **Chân 19** | **`19`** | **`13` (`GPIO13`)** | **`SPI_MISO_GPIO13`** (`MicroSD SPI MISO`) | **`VERIFIED`** |
| **Hàng Trái** | Chân 20 | `20` | `14` (`GPIO14`) | `NC` (Giải phóng khỏi xung đột cũ) | `VERIFIED` |
| **Hàng Trái** | **Chân 21** | **`21`** | **`5Vin` (`5V`)** | **`5V_SYS`** (Nguồn 5V cấp vào ESP32-S3) | **`VERIFIED`** |
| **Hàng Trái** | **Chân 22** | **`22`** | **`GND`** | **`GND`** | **`VERIFIED`** |
| **Hàng Phải** | Chân 23..44 | `23..44` | `GND, TX, RX, 1, 2, 42..19, GND, GND` | `Pin 23, 43, 44 = GND`, toàn bộ GPIO còn lại = `NC` | **`VERIFIED`** |

---

### 1.2. `U7` — `OLED 0.96" GM009605v4.3` (`AIOT_Blackbox_Local:OLED_0.96_GM009605v4.3_1x04_P2.54mm_SingleLayer`)

| Pad Footprint | Số chân Symbol `U7` | Silkscreen trên ảnh `OLED` | Net trên Schematic | Kiểu Pad PCB 1 lớp | Trạng thái |
| :---: | :---: | :--- | :--- | :--- | :---: |
| **Pad `1`** | Pin `1` | **`1: GND`** | `GND` | Rectangular `2.0 × 2.4 mm`, Drill `1.0 mm` | **`VERIFIED`** |
| **Pad `2`** | Pin `2` | **`2: VDD`** | `3V3_SYS` | Oval `2.0 × 2.4 mm`, Drill `1.0 mm` | **`VERIFIED`** |
| **Pad `3`** | Pin `3` | **`3: SCK`** | `I2C_SCL_GPIO9` | Oval `2.0 × 2.4 mm`, Drill `1.0 mm` | **`VERIFIED`** |
| **Pad `4`** | Pin `4` | **`4: SDA`** | `I2C_SDA_GPIO8` | Oval `2.0 × 2.4 mm`, Drill `1.0 mm` | **`VERIFIED`** |

---

### 1.3. `U2` — `MPU6050 GY-521` (`AIOT_Blackbox_Local:Module_GY-521_MPU6050_1x08_P2.54mm_SingleLayer`)

| Pad Footprint | Số chân Symbol `U2` | Silkscreen trên ảnh `GY-521` | Net trên Schematic | Kiểu Pad PCB 1 lớp | Trạng thái |
| :---: | :---: | :--- | :--- | :--- | :---: |
| **Pad `1`** | Pin `1` | **`VCC`** (Pad vuông) | `3V3_SYS` | Rectangular `2.0 × 2.4 mm`, Drill `1.0 mm` | **`VERIFIED`** |
| **Pad `2`** | Pin `2` | **`GND`** | `GND` | Oval `2.0 × 2.4 mm`, Drill `1.0 mm` | **`VERIFIED`** |
| **Pad `3`** | Pin `3` | **`SCL`** | `I2C_SCL_GPIO9` | Oval `2.0 × 2.4 mm`, Drill `1.0 mm` | **`VERIFIED`** |
| **Pad `4`** | Pin `4` | **`SDA`** | `I2C_SDA_GPIO8` | Oval `2.0 × 2.4 mm`, Drill `1.0 mm` | **`VERIFIED`** |
| **Pad `5`** | Pin `5` | **`XDA`** | `NC` | Oval `2.0 × 2.4 mm`, Drill `1.0 mm` | **`VERIFIED`** |
| **Pad `6`** | Pin `6` | **`XCL`** | `NC` | Oval `2.0 × 2.4 mm`, Drill `1.0 mm` | **`VERIFIED`** |
| **Pad `7`** | Pin `7` | **`AD0`** | `GND` (`0x68`) | Oval `2.0 × 2.4 mm`, Drill `1.0 mm` | **`VERIFIED`** |
| **Pad `8`** | Pin `8` | **`INT`** | `NC` | Oval `2.0 × 2.4 mm`, Drill `1.0 mm` | **`VERIFIED`** |

---

### 1.4. `U3` — `RTC DS3231 ZS-042` (`AIOT_Blackbox_Local:Module_DS3231_ZS042_1x06_P2.54mm_SingleLayer`)

| Pad Footprint | Số chân Symbol `U3` | Silkscreen trên ảnh `ZS-042` | Net trên Schematic | Kiểu Pad PCB 1 lớp | Trạng thái |
| :---: | :---: | :--- | :--- | :--- | :---: |
| **Pad `1`** | Pin `1` | **`32K`** (Pad vuông) | `NC` | Rectangular `2.0 × 2.4 mm`, Drill `1.0 mm` | **`VERIFIED`** |
| **Pad `2`** | Pin `2` | **`SQW`** | `NC` | Oval `2.0 × 2.4 mm`, Drill `1.0 mm` | **`VERIFIED`** |
| **Pad `3`** | Pin `3` | **`SCL`** | `I2C_SCL_GPIO9` | Oval `2.0 × 2.4 mm`, Drill `1.0 mm` | **`VERIFIED`** |
| **Pad `4`** | Pin `4` | **`SDA`** | `I2C_SDA_GPIO8` | Oval `2.0 × 2.4 mm`, Drill `1.0 mm` | **`VERIFIED`** |
| **Pad `5`** | Pin `5` | **`VCC`** | `3V3_SYS` | Oval `2.0 × 2.4 mm`, Drill `1.0 mm` | **`VERIFIED`** |
| **Pad `6`** | Pin `6` | **`GND`** | `GND` | Oval `2.0 × 2.4 mm`, Drill `1.0 mm` | **`VERIFIED`** |

---

### 1.5. `J1` — `MicroSD Card Adapter` (`AIOT_Blackbox_Local:Module_MicroSD_Adapter_1x06_P2.54mm_SingleLayer`)
*(Đã cập nhật lại Pin Number của Symbol `Presentation:MicroSD_SPI_Module` theo đúng ảnh thực tế)*

| Pad Footprint | Số chân Symbol `J1` (Mới) | Số chân cũ (Sai) | Silkscreen trên ảnh `MicroSD` | Net trên Schematic | Ghi chú kỹ thuật |
| :---: | :---: | :---: | :--- | :--- | :--- |
| **Pad `1`** | **Pin `1` (`CS`)** | `2` | **`CS`** | `SD_CS_GPIO10` (`GPIO10`) | **Đã đồng bộ khớp 100%** |
| **Pad `2`** | **Pin `2` (`SCK`)** | `4` | **`SCK`** | `SPI_SCK_GPIO12` (`GPIO12`) | **Đã đồng bộ khớp 100%** |
| **Pad `3`** | **Pin `3` (`MOSI`)** | `3` | **`MOSI`** | `SPI_MOSI_GPIO11` (`GPIO11`) | **Đã đồng bộ khớp 100%** |
| **Pad `4`** | **Pin `4` (`MISO`)** | `5` | **`MISO`** | `SPI_MISO_GPIO13` (`GPIO13`) | **Đã đồng bộ khớp 100%** |
| **Pad `5`** | **Pin `5` (`3V3`)** | `1` | **`VCC`** | `3V3_SYS` *(Cảnh báo `CONFLICT`: Module có LDO `AMS1117-3.3` cần `5V`)* | **Đã đồng bộ vị trí chân số 5** |
| **Pad `6`** | **Pin `6` (`GND`)** | `6` | **`GND`** | `GND` | **Đã đồng bộ khớp 100%** |

---

### 1.6. `U4` — `GPS NEO-M8N V2149` (`AIOT_Blackbox_Local:Conn_GPS_NEO-M8N_V2149_1x05_P2.54mm_SingleLayer`)
*(Đã cập nhật lại Pin Number của Symbol `Presentation:NEO-M8N_GNSS_Module` theo đúng Pad vuông số 1 trên ảnh thực tế)*

| Pad Footprint | Số chân Symbol `U4` (Mới) | Số chân cũ (Sai) | Silkscreen trên ảnh `GPS V2149` | Net trên Schematic | Ghi chú kỹ thuật |
| :---: | :---: | :---: | :--- | :--- | :--- |
| **Pad `1`** | **Pin `1` (`VCC`)** | `1` | **`VCC`** (Pad vuông) | `3V3_SYS` | **Đã đồng bộ khớp 100%** |
| **Pad `2`** | **Pin `2` (`GND`)** | `5` | **`GND`** | `GND` | **Đã đồng bộ khớp 100%** |
| **Pad `3`** | **Pin `3` (`TX`)** | `3` | **`TXD`** | `GPS_TX_GPIO17` (`ESP32 RX2 = GPIO17`) | **Đã đồng bộ khớp 100%** |
| **Pad `4`** | **Pin `4` (`RX`)** | `2` | **`RXD`** | `GPS_RX_GPIO18` (`ESP32 TX2 = GPIO18`) | **Đã đồng bộ khớp 100%** |
| **Pad `5`** | **Pin `5` (`PPS`)** | `4` | **`PPS`** | `NC` | **Đã đồng bộ khớp 100%** |

---

### 1.7. `U5` — `SIM 4G Breakout Header J6` (`AIOT_Blackbox_Local:Conn_SIM_Breakout_J6_1x05_P2.54mm_SingleLayer`)
*(Đã cập nhật lại Pin Number của Symbol `Presentation:MKE-M21_SIM7680C_Module` theo đúng hàng chân phải `J6` trên ảnh thực tế)*

| Pad Footprint | Số chân Symbol `U5` (Mới) | Số chân cũ | Silkscreen trên ảnh `SIM J6` | Net trên Schematic | Ghi chú kỹ thuật |
| :---: | :---: | :---: | :--- | :--- | :--- |
| **Pad `1`** | **Pin `1` (`VCC`)** | `1` | **`VCC`** | `SIM_PWR` (`NEEDS_VERIFICATION`) | **Đã đồng bộ khớp 100%** |
| **Pad `2`** | **Pin `2` (`PWRKEY`)** | `4` | **`RST`** | `NC` (Không nối) | Trên header thực tế là chân `RST` (để hở `NC`) |
| **Pad `3`** | **Pin `3` (`RX`)** | `2` | **`RXD`** | `SIM_TX_GPIO16` (`ESP32 TX1 = GPIO16`) | **Đã đồng bộ khớp 100%** |
| **Pad `4`** | **Pin `4` (`TX`)** | `3` | **`TXD`** | `SIM_RX_GPIO15` (`ESP32 RX1 = GPIO15`) | **Đã đồng bộ khớp 100%** |
| **Pad `5`** | **Pin `5` (`GND`)** | `6` | **`GND`** | `GND` | **Đã đồng bộ khớp 100%** |
| *(Không có pad)* | Pin `6` (`STATUS`), Pin `7` (`ANT`) | `5`, `7` | *(Không có trên J6)* | `NC` | `ANT` đã hàn lò xo trực tiếp trên module SIM |
