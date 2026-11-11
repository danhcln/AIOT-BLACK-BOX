# BÁO CÁO XÁC MINH BẰNG HÌNH ẢNH LINH KIỆN THỰC TẾ (`PHOTO_VERIFICATION_REPORT.md`)

**Dự án**: THIẾT KẾ HỘP ĐEN AIoT THÔNG MINH PHÂN TÍCH VÀ GHI LẠI SỰ CỐ XE MÁY ĐIỆN  
**Project KiCad**: `D:\ĐỒ ÁN 2\PCB_AIOT_BLACKBOX\AIOT_BLACKBOX_MAINBOARD_REV1`  
**Thư mục ảnh gốc**: `D:\ĐỒ ÁN 2\Hình ảnh linh kiện` (15 ảnh mặt trước/mặt sau)  
**Luật tham chiếu**: `D:\ĐỒ ÁN 2\.agents\rules\PCB_DESIGN_RULES_AIOT.md` (RULE 02, RULE 03, RULE 05, RULE 08, RULE 18, GATE 1)  

---

## 1. BẢNG TỔNG HỢP KẾT QUẢ XÁC MINH TỪ 15 ẢNH THỰC TẾ

| STT | Thư mục ảnh | Ref | Mã hiệu đọc được trên PCB / IC | Số chân & Thứ tự chân thực tế đọc từ ảnh | Đối chiếu Symbol KiCad (`Presentation.kicad_sym`) | Trạng thái Gate 1 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `ESP32 N16R8` (2 ảnh) | `U1` | Shield: `ESP32-S3-N16R8`, `FCC ID: 2AC7Z-ESP32S3N16R8`<br>PCB: `ESP32-S3`, `USB-OTG`, `COM`, `USB`, `IN-OUT`, `AMS1117-3.3` | **44 chân** (`2x22`, header đực màu vàng):<br>• **Hàng trái (Pin 1..22)**: `3V3, 3V3, RST, 4, 5, 6, 7, 15, 16, 17, 18, 8, 3, 46, 9, 10, 11, 12, 13, 14, 5Vin, GND`<br>• **Hàng phải (Pin 23..44)**: `GND, TX, RX, 1, 2, 42, 41, 40, 39, 38, 37, 36, 35, 0, 45, 48, 47, 21, 20, 19, GND, GND` | **KHỚP 100%** toàn bộ 44 chân (`1..44`) giữa ảnh phần cứng và Symbol `Presentation:ESP32-S3-DevKitC-1`.<br>Toàn bộ 10 GPIO active trong `filecodemain.cpp` + `5Vin` + `GND` đều nằm gọn trên **Hàng trái (`Pin 1..22`)**! | Pinout: **`VERIFIED`**<br>Row Pitch (`22.86mm` vs `25.40mm`): **`PENDING_MEASUREMENT`** (ảnh không có thước) |
| **2** | `OLED 0.96'inch` (3 ảnh) | `U7` | Mặt sau: **`GM009605v4.3`**<br>Kích thước in sẵn trên PCB: **`24.7x27x1.2`** (`24.7 × 27.0 × 1.2 mm`)<br>LDO `Q1`: `662K` (`XC6206-3.3V`), `R1/R2`: `103` (`10kΩ`), `I2C Address`: `0x3C` (`R3` hàn) | **4 chân** (`1x04`, đánh số `1..4` trên silkscreen mặt trước từ trái qua phải):<br>**`1: GND` — `2: VDD` — `3: SCK` — `4: SDA`** | **KHỚP 100%** với Symbol `Presentation:OLED_SSD1306_I2C` (`Pin 1=GND, 2=VDD, 3=SCK, 4=SDA`). | **`VERIFIED`** (Đủ cả Pinout + Kích thước cơ khí `24.7×27.0mm` in trên PCB) |
| **3** | `MPU6050` (2 ảnh) | `U2` | Mặt trước: `ITG/MPU6050`, trục tọa độ `X` (hướng về cạnh `INT`), `Y` (hướng về lỗ vít), LDO 5 chân, `222` (`2.2kΩ` pull-up)<br>Mặt sau: **`GY-521`** | **8 chân** (`1x08`, hàn header đực vuông góc 90°, tính từ Pad vuông số 1):<br>**`1: VCC` — `2: GND` — `3: SCL` — `4: SDA` — `5: XDA` — `6: XCL` — `7: AD0` — `8: INT`** | **KHỚP 100%** với Symbol `Presentation:MPU6050_Module` (`1=VCC, 2=GND, 3=SCL, 4=SDA, 5=XDA, 6=XCL, 7=AD0, 8=INT`). | Header `1x08 P2.54mm`: **`VERIFIED`**<br>Tâm lỗ vít M3 & bao ngoài: **`PENDING_MEASUREMENT`** |
| **4** | `RTC DS3231` (2 ảnh) | `U3` | Mặt trước: `B411` (`ZS-042`), IC `DS3231SN`, EEPROM `24C32N`, 2 mảng trở `472` (`4.7kΩ`)<br>Mặt sau: Khay pin cúc áo **`CR2032 3V`** | **6 chân** (`1x06`, hàn header đực vuông góc 90°, tính từ Pad vuông số 1 bên trái):<br>**`1: 32K` — `2: SQW` — `3: SCL` — `4: SDA` — `5: VCC` — `6: GND`** *(bỏ trống nhóm 4 lỗ daisy-chain bên phải)* | **KHỚP 100%** với Symbol `Presentation:DS3231_RTC_Module` (`1=32K, 2=SQW, 3=SCL, 4=SDA, 5=VCC, 6=GND`). | Header `1x06 P2.54mm`: **`VERIFIED`**<br>Tọa độ lỗ vít cơ khí: **`PENDING_MEASUREMENT`** |
| **5** | `Micro SD` (2 ảnh + 1 ảnh chụp chung với OLED) | `J1` | Mặt trước: **`MicroSD Card Adapter`**, LDO **`1117 3.3 BW053`** (`AMS1117-3.3`), IC đệm mức **`LVC125A`**, `R1..R4=103` (`10kΩ`), 4 lỗ vít góc M2 | **6 chân** (`1x06`, hàn header đực vuông góc 90°, từ trên xuống dưới ở mặt trước):<br>**`1: CS` — `2: SCK` — `3: MOSI` — `4: MISO` — `5: VCC` — `6: GND`** | **PHÁT HIỆN SAI LỆCH THỨ TỰ CHÂN & MÂU THUẪN ĐIỆN ÁP**:<br>1) Symbol cũ đánh số `1:3V3, 2:CS, 3:MOSI, 4:SCK, 5:MISO, 6:GND` $\rightarrow$ **Đã cập nhật lại Pin Number Symbol `J1`** thành `1:CS, 2:SCK, 3:MOSI, 4:MISO, 5:3V3(VCC), 6:GND`.<br>2) **`CONFLICT` Điện áp**: Module có LDO `AMS1117-3.3` nối từ chân `VCC`, thiết kế cho nguồn **`5V`** (`4.5V–5.5V`), trong khi schematic hiện cấp `3V3_SYS` (sụt áp qua LDO còn `~2.1V–2.3V`, dễ lỗi thẻ SD). | Header `1x06 P2.54mm`: **`VERIFIED`** (sau khi đồng bộ Pin Number)<br>Điện áp `VCC`: **`CONFLICT`** (`5V_SYS` vs `3V3_SYS`) |
| **6** | `GPS NEO M8N` (2 ảnh) | `U4` | Tem module: **`u-blox NEO-M8N-0-10`** (`86200049144`)<br>PCB: `GPS模块`, **`V2149`**, cổng Micro-USB `J3`, cổng SMA `J1` kèm anten rời + anten gốm `25×25mm` mặt sau | **5 chân** (`1x05`, tính từ Pad vuông số 1 bên trái mặt trước / bên phải mặt sau):<br>**`1: VCC` — `2: GND` — `3: TXD` — `4: RXD` — `5: PPS`** | **PHÁT HIỆN SAI LỆCH THỨ TỰ CHÂN SYMBOL**:<br>Symbol cũ đánh số `1:VCC, 2:RX, 3:TX, 4:PPS, 5:GND` $\rightarrow$ **Đã cập nhật lại Pin Number Symbol `U4`** thành `1:VCC, 2:GND, 3:TX, 4:RX, 5:PPS` (`6:ANT`) để khớp 100% với pad vuông số 1 trên module thực tế. | **`CONNECTOR_ONLY`** (`VERIFIED` cho đầu nối `1x05 P2.54mm`) |
| **7** | `Module Sim A7680C` (2 ảnh) | `U5` | Thư mục tên `Module Sim A7680C`, chữ khắc laser trên nắp shield SIMCom bị lóa sáng (`A7680C...`), trong khi tài liệu/code ghi `A7682S`.<br>Breakout màu xanh dương, tụ tantal `107A` (`100µF`), khay Nano-SIM mặt sau, anten lò xo hàn tại `ANT`. | **2 hàng chân 2 bên**:<br>• **Hàng phải `J6` (5 chân dưới chân `ANT`)**: **`1: VCC` — `2: RST` — `3: RXD` — `4: TXD` — `5: GND`**<br>• **Hàng trái (6 chân dưới `NET`)**: `RI, DTR, MICP, MICN, SPKP, SPKN` *(không dùng)*<br>*(Lưu ý: Trên header KHÔNG có chân `PWRKEY` hay `STATUS`, chỉ có chân `RST`)*. | **Đã cập nhật Pin Number Symbol `U5`** khớp với header `J6` (`1:VCC, 2:PWRKEY/RST[NC], 3:RX, 4:TX, 5:GND, 6:STATUS[NC], 7:ANT`).<br>• Mã module: **`MODEL_UNVERIFIED`** (`A7680C` vs `A7682S`).<br>• Điện áp `VCC`: Breakout chỉ có đi-ốt mặt sau + tụ tantal `107A`, không có cuộn cảm buck $\rightarrow$ **Giữ nguyên `SIM_PWR` độc lập (`NEEDS_VERIFICATION`)**. | **`CONNECTOR_ONLY`** (`VERIFIED` cho đầu nối `J6 1x05 P2.54mm`)<br>Model: **`MODEL_UNVERIFIED`**<br>Nguồn `SIM_PWR`: **`NEEDS_VERIFICATION`** |

---

## 2. PHÂN TÍCH CHI TIẾT TỪNG MODULE & BẰNG CHỨNG ẢNH

### 2.1. Module 1: `ESP32 N16R8` (`U1`)
- **File ảnh đã kiểm tra**:
  1. Mặt trước: `D:\ĐỒ ÁN 2\Hình ảnh linh kiện\ESP32 N16R8\1794204039475_198069978360956581_1780654779979847084_84491fa379081b485b62d44112a8bbd7.jpg`
  2. Mặt sau: `D:\ĐỒ ÁN 2\Hình ảnh linh kiện\ESP32 N16R8\1794204039506_198069978360956581_1780654779979847084_2dad8255752d7c0230db6d0f5b913e92.jpg`
- **Đặc điểm nhận diện**:
  - Module Wi-Fi/BLE trên board là **`ESP32-S3-WROOM-1` bản `N16R8`** (16MB Flash, 8MB Octal PSRAM, anten PCB meander ở đỉnh trên).
  - Board phát triển kiểu **YD-ESP32-S3 / DevKitC-1 clone** có 2 cổng USB Type-C ở cạnh dưới (`COM` qua chip nạp UART và `USB` native OTG), nút nhấn `RST` (trái) và `BOOT` (phải), LED địa chỉ `RGB`, jumper hàn `IN-OUT`, IC nguồn `AMS1117-3.3` và tụ tantal vàng `226A`.
  - Hai hàng header đực màu vàng **`2 × 22 = 44 chân`** cắm xuống dưới.
- **Đối chiếu thứ tự 44 chân (từ trên anten xuống dưới cổng USB-C, nhìn từ mặt trước)**:
  - **Hàng bên trái (tương ứng Pin `1..22` của Symbol `U1`)**:
    `1: 3V3` | `2: 3V3` | `3: RST` | `4: 4` | `5: 5` | `6: 6` | `7: 7` | `8: 15` | `9: 16` | `10: 17` | `11: 18` | `12: 8` | `13: 3` | `14: 46` | `15: 9` | `16: 10` | `17: 11` | `18: 12` | `19: 13` | `20: 14` | `21: 5Vin` | `22: GND`.
  - **Hàng bên phải (tương ứng Pin `23..44` của Symbol `U1`)**:
    `23: GND` | `24: TX` | `25: RX` | `26: 1` | `27: 2` | `28: 42` | `29: 41` | `30: 40` | `31: 39` | `32: 38` | `33: 37` | `34: 36` | `35: 35` | `36: 0` | `37: 45` | `38: 48` | `39: 47` | `40: 21` | `41: 20` | `42: 19` | `43: GND` | `44: GND`.
- **Phát hiện cực kỳ có lợi cho PCB 1 lớp (`B.Cu`)**:
  - Tất cả **10 chân GPIO đang hoạt động trong `filecodemain.cpp`** (`GPIO8, GPIO9, GPIO10, GPIO11, GPIO12, GPIO13, GPIO15, GPIO16, GPIO17, GPIO18`) cùng với chân cấp nguồn **`5Vin` (Pin 21)** và **`GND` (Pin 22)** đều nằm hoàn toàn ở **cùng một hàng chân bên trái (`Pin 8..22`)**!
  - Hàng chân bên phải (`Pin 23..44`) không có bất kỳ tín hiệu nào đang dùng trong firmware ngoài `GND`. Nhờ vậy, khi đi dây PCB 1 lớp ở Gate 3, toàn bộ đường mạch từ `ESP32-S3` thoát ra từ một phía duy nhất, giảm tối đa giao cắt!
- **Lý do giữ `PENDING_MEASUREMENT` cho khoảng cách 2 hàng chân (Row Pitch)**:
  - Ảnh chụp `ESP32 N16R8` không kèm thước đo. Board clone YD-ESP32-S3 có nhựa đen USB-OTG ở mặt dưới thường có khoảng cách 2 hàng chân là **`25.40 mm` (1000 mil / 1.0 inch)** hoặc **`22.86 mm` (900 mil)**. Sai lệch `2.54 mm` sẽ làm **không thể cắm vừa DevKit vào 2 hàng socket cái trên PCB**. Do đó tuyệt đối tuân thủ Mục 4: giữ trạng thái **`PENDING_MEASUREMENT`** cho đến khi đo bằng thước kẹp thực tế.

---

### 2.2. Module 2: `OLED 0.96'inch` (`U7`)
- **File ảnh đã kiểm tra**:
  1. `D:\ĐỒ ÁN 2\Hình ảnh linh kiện\OLED 0.96'inch\1794204268899_198069978360956581_1780654779979847084_a4cbb1a4889d772097392fc372944adc.jpg`
  2. `D:\ĐỒ ÁN 2\Hình ảnh linh kiện\OLED 0.96'inch\1794204268914_198069978360956581_1780654779979847084_6ea5164c1a8d3554c625e8bc03efef54.jpg`
  3. `D:\ĐỒ ÁN 2\Hình ảnh linh kiện\OLED 0.96'inch\1794204268929_198069978360956581_1780654779979847084_ea720cbb8a783cfe2d809b200c19561e.jpg`
- **Bằng chứng xác minh 100% (`VERIFIED`)**:
  - Mã PCB mặt sau: **`GM009605v4.3`**.
  - Kích thước cơ khí được nhà sản xuất in trực tiếp trên silkscreen mặt sau: **`24.7x27x1.2`** (Cao `24.7 mm` × Rộng `27.0 mm` × Dày PCB `1.2 mm`).
  - Thứ tự 4 chân in rõ cả số `1, 2, 3, 4` và tên chân ở mặt trước: **`1: GND` — `2: VDD` — `3: SCK` — `4: SDA`** (hoàn toàn trùng khớp với Symbol `U7`).
  - Mặt sau có IC ổn áp LDO 3.3V `Q1` (`662K` = `XC6206P332MR`) và cặp điện trở kéo lên I2C `R1, R2` (`103` = `10kΩ`), địa chỉ I2C chọn `0x3C` (hàn trở `R3`, để trống `R4`), khớp với `OLED_ADDR = 0x3C` trong `filecodemain.cpp`.

---

### 2.3. Module 3: `MPU6050` (`U2` — `GY-521`)
- **File ảnh đã kiểm tra**:
  1. Mặt trước: `D:\ĐỒ ÁN 2\Hình ảnh linh kiện\MPU6050\1794204268975_198069978360956581_1780654779979847084_6830228556ea5344f5f55aee9fc06483.jpg`
  2. Mặt sau: `D:\ĐỒ ÁN 2\Hình ảnh linh kiện\MPU6050\1794204268990_198069978360956581_1780654779979847084_6488ca57a043a4d16110cabf69387bfb.jpg`
- **Bằng chứng xác minh**:
  - Mặt sau in **`GY-521`**, mặt trước in **`ITG/MPU6050`** kèm mũi tên hệ trục tọa độ **`X` (hướng sang trái về phía chân `INT`)** và **`Y` (hướng xuống dưới về phía 2 lỗ bắt vít)**.
  - Hàng chân `1x08` (`P2.54mm`) đã được hàn sẵn **header đực bẻ góc 90° (right-angle)** hướng ra ngoài biên board. Nếu cắm trực tiếp vào socket cái đứng `1x08` trên PCB chính thì board `GY-521` sẽ dựng đứng vuông góc 90° với mặt PCB chính (làm đổi trục `Z` thành phương ngang!). Để lắp phẳng (`BOARD_MOUNT` song song mặt PCB chính) đúng trục gia tốc xe máy điện, cần hàn lại header đực thẳng đứng hoặc dùng cáp/đầu nối.
  - Thứ tự chân từ Pad vuông số 1: **`1: VCC` — `2: GND` — `3: SCL` — `4: SDA` — `5: XDA` — `6: XCL` — `7: AD0` — `8: INT`** (khớp 100% với Symbol `U2`).
  - Điện trở pull-up I2C trên module là **`222` (`2.2kΩ`)** nối sẵn lên `3.3V`.

---

### 2.4. Module 4: `RTC DS3231` (`U3` — `ZS-042`)
- **File ảnh đã kiểm tra**:
  1. Mặt trước: `D:\ĐỒ ÁN 2\Hình ảnh linh kiện\RTC DS3231\1794204268944_198069978360956581_1780654779979847084_1146cfef14d6c6eac4ae8ccd0c8b5d56.jpg`
  2. Mặt sau: `D:\ĐỒ ÁN 2\Hình ảnh linh kiện\RTC DS3231\1794204268960_198069978360956581_1780654779979847084_a6eada72e50465773b889ff922c9d38f.jpg`
- **Bằng chứng xác minh**:
  - Module RTC `ZS-042` (`B411`) dùng IC chính hãng `DS3231SN` (SOIC-16) + EEPROM `AT24C32N`.
  - Mặt sau đang lắp viên pin **Lithium `CR2032 3V` (pin KHÔNG sạc)** trong khay giữ pin. Trên mặt trước có mạch sạc trickle-charge nhỏ (đi-ốt đỏ + trở `201`) nối từ `VCC`. Việc schematic cấp **`3V3_SYS`** cho `U3` (thay vì `5V`) giúp giảm dòng nạp ngược vào pin `CR2032`, nhưng khuyến nghị gỡ bỏ trở `201` hoặc đi-ốt nạp trên module `ZS-042` khi vận hành lâu dài với pin `CR2032`.
  - Hàng chân `1x06` (`P2.54mm`) hàn header đực bẻ góc 90°, thứ tự từ Pad vuông số 1: **`1: 32K` — `2: SQW` — `3: SCL` — `4: SDA` — `5: VCC` — `6: GND`** (khớp 100% với Symbol `U3`).

---

### 2.5. Module 5: `Micro SD` (`J1` — `MicroSD Card Adapter`) — CẢNH BÁO QUAN TRỌNG
- **File ảnh đã kiểm tra**:
  1. Mặt sau: `D:\ĐỒ ÁN 2\Hình ảnh linh kiện\Micro SD\1794204268869_198069978360956581_1780654779979847084_d16ec021c362c70c68833202e3bf4670.jpg`
  2. Mặt trước: `D:\ĐỒ ÁN 2\Hình ảnh linh kiện\Micro SD\1794204268884_198069978360956581_1780654779979847084_3c29c5070fa32b94e95acbb08c00777d.jpg`
  3. Ảnh chụp chung với OLED: `D:\ĐỒ ÁN 2\Hình ảnh linh kiện\OLED 0.96'inch\1794204268899_198069978360956581_1780654779979847084_a4cbb1a4889d772097392fc372944adc.jpg`
- **Phát hiện 1 — Sai lệch thứ tự chân Symbol `J1` (Đã sửa trong Gate 1)**:
  - Trên module thực tế, thứ tự 6 chân dọc theo cạnh phải (từ trên xuống dưới khi nhìn mặt trước) là:
    **`1: CS` — `2: SCK` — `3: MOSI` — `4: MISO` — `5: VCC` — `6: GND`**.
  - Trong Symbol `Presentation:MicroSD_SPI_Module` cũ, thứ tự đánh số chân là `1:3V3, 2:CS, 3:MOSI, 4:SCK, 5:MISO, 6:GND`. Nếu giữ nguyên số chân cũ để xuất sang PCB, chân nguồn sẽ bị nối nhầm vào chân `CS` và làm đảo lộn các đường SPI (`SCK`, `MISO`)!
  - **Biện pháp đã thực hiện**: Đã cập nhật lại `(number "...")` của Symbol `Presentation:MicroSD_SPI_Module` trong `Presentation.kicad_sym` và `AIOT_BLACKBOX_MAINBOARD_REV1.kicad_sch` thành **`1:CS, 2:SCK, 3:MOSI, 4:MISO, 5:3V3(VCC), 6:GND`** đồng bộ 100% với Footprint `Module_MicroSD_Adapter_1x06_P2.54mm_SingleLayer`.
- **Phát hiện 2 — Mâu thuẫn điện áp cấp nguồn (`CONFLICT`)**:
  - Ảnh mặt trước `3c29c5070fa32b94e95acbb08c00777d.jpg` cho thấy rõ module có IC ổn áp **`AMS1117-3.3` (`1117 3.3 BW053`)** và IC đệm mức logic **`74LVC125A` (`LVC125A`)**.
  - Chân `VCC` (Pin 5) của module đi vào chân `VIN` của `AMS1117-3.3` (có sụt áp dropout `~1.1V`). Do đó, chân `VCC` của module này được thiết kế để nhận nguồn **`5V` (`5V_SYS`)**, sau đó `AMS1117-3.3` hạ xuống `3.3V` cấp cho thẻ MicroSD và `74LVC125A`!
  - Hiện tại trên schematic, chân `Pin 5` của `J1` đang nối vào **`3V3_SYS`**. Nếu cấp `3.3V` vào đầu vào `AMS1117-3.3`, điện áp sau LDO chỉ còn `~2.2V`, dưới ngưỡng hoạt động chuẩn (`2.7V–3.6V`) của thẻ nhớ MicroSD!
  - **Tuân thủ nguyên tắc không tự ý đổi kiến trúc nguồn**: Giữ nguyên net `3V3_SYS` trong schematic hiện tại nhưng đánh dấu **`CONFLICT`** và khuyến nghị bạn phê duyệt chuyển chân `VCC` của `J1` sang **`5V_SYS`** (hoặc bố trí jumper 3 chân chọn `5V_SYS / 3V3_SYS`) trước khi sang Gate 2.

---

### 2.6. Module 6: `GPS NEO M8N` (`U4` — `u-blox NEO-M8N-0-10`, PCB `V2149`)
- **File ảnh đã kiểm tra**:
  1. Mặt trước: `D:\ĐỒ ÁN 2\Hình ảnh linh kiện\GPS NEO M8N\1794204268827_198069978360956581_1780654779979847084_13499ca1a093d5e4344c19664af661a5.jpg`
  2. Mặt sau: `D:\ĐỒ ÁN 2\Hình ảnh linh kiện\GPS NEO M8N\1794204268849_198069978360956581_1780654779979847084_8fe2db746e8583bb0eceebefd6db6e5f.jpg`
- **Phát hiện sai lệch thứ tự chân Symbol `U4` (Đã sửa trong Gate 1)**:
  - Trên PCB `V2149`, hàng 5 lỗ hàn (`1x05 P2.54mm`) có **Pad số 1 hình vuông** nằm ở ngoài cùng bên trái (mặt trước) / bên phải (mặt sau).
  - Thứ tự in rõ trên silkscreen mặt sau (`8fe2db746e8583bb0eceebefd6db6e5f.jpg`) từ Pad vuông số 1 là:
    **`1: VCC` — `2: GND` — `3: TXD` — `4: RXD` — `5: PPS`**.
  - Trong Symbol `Presentation:NEO-M8N_GNSS_Module` cũ, các chân đang đánh số `1:VCC, 2:RX, 3:TX, 4:PPS, 5:GND` (lệch chân `2:GND`, `4:RX`, `5:PPS`).
  - **Biện pháp đã thực hiện**: Đã cập nhật lại `(number "...")` của Symbol `U4` thành **`1:VCC, 2:GND, 3:TX, 4:RX, 5:PPS` (`6:ANT`)** khớp 100% với Footprint `Conn_GPS_NEO-M8N_V2149_1x05_P2.54mm_SingleLayer`.
- **Kiểu lắp (`CONNECTOR_ONLY`)**:
  - Mặt sau module GPS gắn khối **anten gốm patch `25 × 25 mm`** dày và mặt trước có đầu vặn SMA + dây cáp đồng trục nối ra anten thanh rời. Vì vậy phân loại **`CONNECTOR_ONLY`** (dùng header/socket hoặc cáp 5 sợi `P2.54mm` trên PCB chính và cố định module GPS ở nắp trên hộp đen hướng lên trời) là hợp lý và tối ưu nhất.

---

### 2.7. Module 7: `Module Sim A7680C` (`U5`)
- **File ảnh đã kiểm tra**:
  1. Mặt trước: `D:\ĐỒ ÁN 2\Hình ảnh linh kiện\Module Sim A7680C\1794204134409_198069978360956581_1780654779979847084_e48892d98332388c5f711227cc6e4e73.jpg`
  2. Mặt sau: `D:\ĐỒ ÁN 2\Hình ảnh linh kiện\Module Sim A7680C\1794204134494_198069978360956581_1780654779979847084_fdb304df868a2ad6c707d7a224855f0c.jpg`
- **Phân tích mã model (`MODEL_UNVERIFIED`)**:
  - Tên thư mục ảnh do người dùng cung cấp là `Module Sim A7680C`. Trên nắp kim loại của module SIMCom (`e48892d98332388c5f711227cc6e4e73.jpg`), dòng chữ khắc laser bị ánh sáng phản chiếu làm mờ nhưng vẫn nhận diện được các nét đầu kiểu `A7680C...` và kiểu đóng gói LCC có 12 pad cạnh trên/dưới × 8 pad cạnh trái/phải, trong khi chú thích trong `filecodemain.cpp` ghi `SIM A7682S`.
  - Theo đúng quy định tại Mục 9, đánh dấu mã phần cứng là **`MODEL_UNVERIFIED` (`A7680C` vs `A7682S`)** và không tự khẳng định hai mã này là một.
- **Xác minh thứ tự chân đầu nối `J6` (`CONNECTOR_ONLY` — `VERIFIED`)**:
  - Ảnh mặt sau `fdb304df868a2ad6c707d7a224855f0c.jpg` cho thấy rõ 2 hàng chân dọc hai bên:
    - **Cạnh phải (`J6`)**: Phía trên cùng là lỗ hàn `ANT` (đã hàn anten lò xo xoắn đồng), ngay bên dưới là **5 chân header `P2.54mm`** theo thứ tự từ trên xuống dưới:
      **`1: VCC` — `2: RST` — `3: RXD` — `4: TXD` — `5: GND`**.
    - **Cạnh trái**: Phía trên cùng là lỗ `NET` (bỏ trống), bên dưới là 6 chân phụ `RI, DTR, MICP, MICN, SPKP, SPKN` (không hàn, không dùng trong hệ thống).
  - **Điểm lưu ý quan trọng**: Breakout thực tế **chỉ đưa chân `RST` ra header `J6` (Pin 2)**, hoàn toàn **không có chân `PWRKEY` và `STATUS`** trên rào chân (mạch tự khởi động auto-boot bằng tụ/transistor đã tích hợp sẵn trên breakout). Trong firmware `filecodemain.cpp` cũng chỉ dùng `TXD`, `RXD` và để trống `PWRKEY/STATUS` (`NC`), nên hoàn toàn tương thích!
  - **Đã cập nhật Pin Number Symbol `U5`** thành `1:VCC, 2:PWRKEY(RST-NC), 3:RX, 4:TX, 5:GND, 6:STATUS(NC), 7:ANT` khớp với đầu nối 5 chân `Conn_SIM_Breakout_J6_1x05_P2.54mm_SingleLayer`.
- **Trạng thái nguồn `SIM_PWR` (`NEEDS_VERIFICATION`)**:
  - Quan sát mặt trước và mặt sau breakout chỉ thấy 1 tụ tantal vàng `107A` (`100µF 10V`), 3 transistor SOT-23 dịch mức UART và 1 đi-ốt SMD nhỏ ở mặt sau để hạ áp nhẹ từ `5V` xuống `~4.2V–4.3V`. Vì cần xác nhận chắc chắn thông số đi-ốt hạ áp trên thực tế trước khi đóng nguồn `5V_SYS`, đường **`SIM_PWR` tiếp tục giữ nguyên trạng thái cô lập qua connector `J3` (`NEEDS_VERIFICATION`)**.

