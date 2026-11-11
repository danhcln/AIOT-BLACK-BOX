# TÀI LIỆU DATASHEET VÀ THÔNG SỐ KỸ THUẬT LINH KIỆN HỘP ĐEN AIoT

Thư mục này quản lý toàn bộ danh mục thông số kỹ thuật (Datasheet), tài liệu hướng dẫn thiết kế phần cứng (Hardware Integration Manual) và tập lệnh điều khiển AT/I2C/SPI chính hãng của các khối linh kiện thuộc đồ án Hộp đen AIoT.

Để tối ưu dung lượng repository và tuân thủ bản quyền phân phối tài liệu của các nhà sản xuất bán dẫn, các file PDF gốc được lưu trữ cục bộ tại máy thiết kế và được lập chỉ mục tra cứu trực tiếp tại hai bảng tính:
- [`DATASHEET_INDEX.csv`](./DATASHEET_INDEX.csv): Bảng tra cứu định dạng CSV chuẩn hóa quốc tế.
- [`DATASHEET_INDEX.xlsx`](./DATASHEET_INDEX.xlsx): Bảng tính Excel có màu định dạng và bộ lọc tra cứu theo khối chức năng.

---

## Danh mục liên kết trực tiếp tới tài liệu chính hãng của nhà sản xuất

| STT | Khối linh kiện | Mã linh kiện thực tế | Tiêu đề tài liệu | Nhà sản xuất | Đường dẫn trực tiếp chính hãng (Official URL) |
|---|---|---|---|---|---|
| 01 | **ESP32-S3** | ESP32-S3 / DevKitC-1 N16R8 | ESP32-S3 Series Datasheet | Espressif Systems | [Tải về](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf) |
| 02 | **ESP32-S3** | ESP32-S3 / DevKitC-1 N16R8 | ESP32-S3 Technical Reference Manual | Espressif Systems | [Tải về](https://www.espressif.com/sites/default/files/documentation/esp32-s3_technical_reference_manual_en.pdf) |
| 03 | **ESP32-S3** | ESP32-S3-WROOM-1 N16R8 | ESP32-S3-WROOM-1 Module Datasheet | Espressif Systems | [Tải về](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf) |
| 04 | **MPU-6050** | MPU-6050 / GY-521 Breakout | MPU-6000/6050 Product Specification | InvenSense / TDK | [Tải về](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf) |
| 05 | **MPU-6050** | MPU-6050 / GY-521 Breakout | MPU-6000/6050 Register Map & Descriptions | InvenSense / TDK | [Tải về](https://cdn.sparkfun.com/datasheets/Sensors/Accelerometers/RM-MPU-6000A.pdf) |
| 06 | **MPU-6050** | MPU-6050 / GY-521 Breakout | MPU-6000/6050 Evaluation Board User Guide | InvenSense / TDK | [Tải về](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/3984/MPU-6000_6050_EvalBrd_UG.pdf) |
| 07 | **DS3231** | DS3231 RTC / ZS-042 | DS3231 Extremely Accurate I2C RTC Datasheet | Maxim Integrated / ADI | [Tải về](https://www.analog.com/media/en/technical-documentation/data-sheets/ds3231.pdf) |
| 08 | **DS3231** | DS3231 RTC / ZS-042 | Adafruit DS3231 Precision RTC Hardware Guide | Adafruit Industries | [Tải về](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-ds3231-precision-rtc-breakout.pdf) |
| 09 | **DS3231** | DS3231 RTC / ZS-042 | Waveshare Pico-RTC-DS3231 Schematic Reference | Waveshare Electronics | [Tải về](https://files.waveshare.com/upload/0/08/Pico-RTC-DS3231_Sch.pdf) |
| 10 | **NEO-M8N** | u-blox NEO-M8N GNSS | NEO-M8 Series Concurrent GNSS Data Sheet | u-blox AG | [Tải về](https://content.u-blox.com/sites/default/files/NEO-M8-FW3_DataSheet_UBX-15031086.pdf) |
| 11 | **NEO-M8N** | u-blox NEO-M8N GNSS | u-blox 8 / M8 Receiver Description & Protocol | u-blox AG | [Tải về](https://content.u-blox.com/sites/default/files/products/documents/u-blox8-M8_ReceiverDescrProtSpec_UBX-13003221.pdf) |
| 12 | **NEO-M8N** | u-blox NEO-M8N GNSS | NEO-8Q / NEO-M8 Hardware Integration Manual | u-blox AG | [Tải về](https://content.u-blox.com/sites/default/files/NEO-8Q-NEO-M8-FW3_HIM_UBX-15029985.pdf) |
| 13 | **4G LTE** | MKE-M21 (SIM7680C/A7680C) | Mạch MKE-M21 SIM7680C 4G Technical Manual | MakerEdu Vietnam | [Tải về](https://github.com/makereduvn/MKE-M21-SIM7680C-4G-MODULE) |
| 14 | **4G LTE** | SIMCom A7680C Series | SIMCom A7680C Hardware Design Manual | SIMCom Wireless Solutions | [Tải về](https://www.simcom.com/) |
| 15 | **4G LTE** | SIMCom A7680C / A7600 | SIMCom A7600 Series AT Command Manual | SIMCom Wireless Solutions | [Tải về](https://files.waveshare.com/upload/d/dd/A7600_Series_AT_Command_Manual_V1.01.pdf) |
| 16 | **MicroSD** | MicroSD Storage SPI | SD Physical Layer Simplified Specification v6.00 | SD Association (SDA) | [Tải về](https://academy.cba.mit.edu/classes/networking_communications/SD/SD.pdf) |
| 17 | **MicroSD** | MicroSD Storage SPI | Adafruit MicroSD SPI Card Breakout Hardware Guide | Adafruit Industries | [Tải về](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-microsd-spi-sdio.pdf) |
| 18 | **MicroSD** | MicroSD Storage SPI | Waveshare Micro SD Board Circuit Schematic | Waveshare Electronics | [Tải về](https://files.waveshare.com/upload/8/83/Micro-SD-Storage-Board-Schematic.pdf) |
| 19 | **OLED** | 0.96 inch 128x64 SSD1306 | SSD1306 Dot Matrix OLED Driver Controller | Solomon Systech | [Tải về](https://files.waveshare.com/upload/e/ec/SDD1306-30pin.pdf) |
| 20 | **OLED** | 0.96 inch 128x64 SSD1306 | Waveshare 0.96-inch OLED Module User Manual | Waveshare Electronics | [Tải về](https://files.waveshare.com/upload/7/71/0.96inch-OLED-UserManual.pdf) |
| 21 | **OLED** | 0.96 inch 128x64 SSD1306 | Waveshare 0.96-inch OLED Module Schematic | Waveshare Electronics | [Tải về](https://files.waveshare.com/upload/d/dc/0.96inch-OLED-Schematic.pdf) |
| 22 | **Buzzer** | 5V Active Piezo Buzzer | CPE-163 5V Piezo Audio Indicator Specification | Same Sky / CUI Devices | [Tải về](https://www.sameskydevices.com/product/resource/cpe-163.pdf) |
| 23 | **Buzzer** | 5V Active Piezo Buzzer | Murata Piezoelectric Sound Components Manual | Murata Manufacturing | [Tải về](https://www.murata.com/~/media/webrenewal/support/library/catalog/products/sound/p15e.ashx) |
| 24 | **Buzzer** | 5V Active Piezo Buzzer | Sonitron Standard Piezo Audio Indicator Manual | Sonitron N.V. | [Tải về](https://www.sonitron.be/wp-content/uploads/2019/07/SMB-series.pdf) |
| 25 | **2SC1815** | Transistor NPN TO-92 | Toshiba 2SC1815 Silicon Epitaxial Transistor | Toshiba Corporation | [Tải về](https://akizukidenshi.com/goodsaffix/2sc1815.pdf) |
| 26 | **2SC1815** | Transistor NPN TO-92 | Central Semiconductor 2SC1815 Specification | Central Semiconductor | [Tải về](https://my.centralsemi.com/datasheets/2SC1815.PDF) |
| 27 | **2SC1815** | Transistor NPN TO-92 | Youfeng Microelectronics 2SC1815 TO-92 Spec | Youfeng Micro / LCSC | [Tải về](https://datasheet.lcsc.com/datasheet/pdf/5472637d014a36df83e77b0ea431f59e.pdf?productCode=C22459218) |
| 28 | **Pin 18650** | 18650 Li-ion 3.7V | Sony/Murata US18650VTC6 3000mAh Technical Spec | Sony / Murata | [Tải về](https://enerpower.de/wp-content/uploads/2016/10/Specification-US18650VTC6.pdf) |
| 29 | **Pin 18650** | 18650 Li-ion 3.7V | Panasonic Lithium Battery Technical Handbook | Panasonic Energy | [Tải về](https://energy.panasonic.com/dam/master/pdf/eu/material/Panasonic_Lithium_Handbook.pdf) |
| 30 | **Pin 18650** | 18650 Li-ion 3.7V | Samsung SDI INR18650-25R Specification | Samsung SDI | [Tải về](https://docs.telitpower.com/pdf/li-ion/INR18650-25R.pdf) |
