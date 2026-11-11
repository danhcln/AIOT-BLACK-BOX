# -*- coding: utf-8 -*-
"""
Module ch3_sec32_p1.py: Section 3.2 Part 1 generator.
Covers:
- 3.2 Introduction
- 3.2.1 Khối xử lý trung tâm (ESP32-S3-DevKitC-1 N16R8, comparisons, Frozen GPIO table, schematic crop)
- 3.2.2 Khối cảm biến quán tính (GY-521 / MPU6050, comparisons, specs table, schematic crop)
- 3.2.3 Khối đồng hồ thời gian thực (DS3231 RTC, comparisons, specs table, schematic crop)
"""

import os
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from build_chapter3_full import (
    add_p, add_bullet, add_h2, add_h3, add_figure, add_table_with_caption, add_code_snippet
)

def add_section_3_2_part1(doc, assets_dir):
    # -------------------------------------------------------------------------
    # 3.2 THIẾT KẾ HỆ THỐNG
    # -------------------------------------------------------------------------
    add_h2(doc, "3.2 THIẾT KẾ HỆ THỐNG")
    
    add_p(doc, 
          "Phần này trình bày chi tiết quá trình thiết kế kỹ thuật cho từng khối chức năng cấu thành hệ thống hộp đen AIoT. "
          "Với phương châm thiết kế công nghiệp, đảm bảo độ tin cậy cao và tối ưu hóa chi phí sản xuất, mỗi khối chức năng "
          "đều được nhóm tác giả tiến hành khảo sát đa chiều, đề xuất từ 2 đến 3 phương án khả thi, phân tích sâu sắc ưu và nhược "
          "điểm, xây dựng bảng đối sánh kỹ thuật minh bạch trước khi đưa ra phương án lựa chọn tối ưu nhất cho ứng dụng giám sát "
          "và ghi nhận sự cố xe máy điện.")

    # =========================================================================
    # 3.2.1 Khối xử lý trung tâm
    # =========================================================================
    add_h3(doc, "3.2.1 Khối xử lý trung tâm")
    
    add_p(doc, 
          "Khối xử lý trung tâm đóng vai trò hạt nhân chỉ huy, quyết định trực tiếp đến hiệu năng, độ trễ và khả năng mở rộng "
          "của toàn bộ hệ thống hộp đen. Vi điều khiển trung tâm phải đồng thời thực hiện đa tác vụ thời gian thực: tiếp nhận luồng dữ "
          "liệu quán tính tần số cao (100 Hz), bóc tách dữ liệu vệ tinh GNSS (10 Hz), duy trì bộ đệm vòng 30 giây dữ liệu trong bộ nhớ, "
          "thực thi thuật toán học máy biên (TinyML) nhận diện sự cố, quản lý đọc/ghi thẻ nhớ SPI MicroSD, điều khiển hiển thị OLED, "
          "tương tác nút nhấn, kích hoạt còi cảnh báo và giao tiếp tập lệnh AT với module 4G LTE. Các phương án vi điều khiển được cân nhắc gồm:")
          
    add_p(doc, "", bold_prefix="Phương án 1: Sử dụng vi điều khiển ESP32-S3-DevKitC-1 N16R8 (Espressif Systems):")
    add_p(doc, 
          "ESP32-S3 là dòng vi điều khiển SoC lõi kép 32-bit Xtensa LX7 thế hệ mới, hoạt động ở tần số xung nhịp lên tới 240 MHz. "
          "Phiên bản N16R8 được tích hợp sẵn 16 MB Quad SPI Flash và 8 MB Octal SPI PSRAM, hỗ trợ tập lệnh mở rộng xử lý vector "
          "(Vector Instructions) tối ưu cho các thuật toán học máy biên (TinyML/DSP).")
    add_bullet(doc, "Ưu điểm: ", 
               "Tốc độ xử lý vượt trội (240 MHz lõi kép); bộ nhớ cực lớn với 8 MB PSRAM ngoài cho phép cấp phát các bộ đệm vòng FIFO "
               "chứa hàng nghìn mẫu cảm biến đa chiều mà không sợ tràn RAM; tích hợp tập lệnh tăng tốc AI; hỗ trợ 45 chân GPIO với "
               "khả năng cấu hình ma trận chân (GPIO Matrix) cực kỳ linh hoạt; tích hợp sẵn 3 UART, 2 I2C, 4 SPI, USB-OTG/JTAG native; "
               "hệ sinh thái phát triển mạnh mẽ (ESP-IDF, Arduino Framework).")
    add_bullet(doc, "Nhược điểm: ", 
               "Mức tiêu thụ dòng đỉnh khi kích hoạt các bộ phát vô tuyến RF nội cao hơn dòng vi điều khiển truyền thống (tuy nhiên "
               "trong đề tài này hệ thống dùng module 4G rời nên vi điều khiển chỉ tập trung xử lý thuật toán và giao tiếp ngoại vi).")

    add_p(doc, "", bold_prefix="Phương án 2: Sử dụng vi điều khiển ESP32-WROOM-32D (Classic ESP32):")
    add_p(doc, 
          "Dòng vi điều khiển thế hệ trước rất phổ biến trong các ứng dụng IoT, sử dụng lõi kép Xtensa LX6 xung nhịp 240 MHz, "
          "tích hợp 520 KB SRAM nội và 4 MB Flash.")
    add_bullet(doc, "Ưu điểm: ", 
               "Giá thành rẻ, sẵn có trên thị trường, cộng đồng hỗ trợ rất lớn, thư viện ngoại vi phong phú.")
    add_bullet(doc, "Nhược điểm: ", 
               "Không có bộ nhớ mở rộng PSRAM (chỉ có 520 KB SRAM nội, trong đó vùng nhớ khả dụng cho ứng dụng chỉ khoảng 320 KB), "
               "rất dễ bị tràn bộ nhớ (Heap exhaustion) khi vừa duy trì bộ đệm FIFO dữ liệu sự cố vừa nạp các thư viện nặng như FATFS, "
               "TinyML và giao thức truyền thông; không có tập lệnh vector tăng tốc AI; số lượng chân GPIO khả dụng ít hơn ESP32-S3.")

    add_p(doc, "", bold_prefix="Phương án 3: Sử dụng vi điều khiển STM32F401 / STM32F411 (Black Pill - ARM Cortex-M4):")
    add_p(doc, 
          "Dòng vi điều khiển 32-bit dựa trên kiến trúc ARM Cortex-M4 của STMicroelectronics, tích hợp bộ xử lý dấu phẩy động phần cứng (FPU), "
          "xung nhịp 84 MHz - 100 MHz, 512 KB Flash và 128 KB SRAM.")
    add_bullet(doc, "Ưu điểm: ", 
               "Độ bền công nghiệp cao, tiêu thụ điện năng thấp, hoạt động ổn định trong môi trường nhiễu điện từ mạnh, phần cứng FPU xử lý phép toán số thực nhanh.")
    add_bullet(doc, "Nhược điểm: ", 
               "Bộ nhớ SRAM rất hạn chế (128 KB), hoàn toàn không đủ dung lượng để duy trì bộ đệm sự cố 30 giây độ phân giải cao; tốc độ xung nhịp "
               "thấp hơn nhiều so với ESP32-S3; cấu hình giao tiếp phức tạp, thời gian phát triển phần mềm lâu; giá thành bo mạch và linh kiện phụ trợ cao hơn.")

    add_p(doc, 
          "Các tiêu chí kỹ thuật cốt lõi đối sánh giữa 3 phương án vi điều khiển được thể hiện trong Bảng 3.2:")
          
    # Bảng 3.2
    tbl2_headers = ["Tiêu chí so sánh", "ESP32-S3 N16R8 (Được chọn)", "ESP32-WROOM-32D", "STM32F411 (Black Pill)"]
    tbl2_data = [
        ["Kiến trúc CPU", "Xtensa 32-bit LX7 Lõi kép", "Xtensa 32-bit LX6 Lõi kép", "ARM 32-bit Cortex-M4 + FPU"],
        ["Tần số xung nhịp", "240 MHz", "240 MHz", "100 MHz"],
        ["Bộ nhớ Flash", "16 MB (Quad SPI)", "4 MB (SPI)", "512 KB (Nội)"],
        ["Bộ nhớ SRAM nội", "512 KB SRAM", "520 KB SRAM", "128 KB SRAM"],
        ["Bộ nhớ ngoài PSRAM", "8 MB (Octal SPI cực nhanh)", "Không tích hợp", "Không tích hợp"],
        ["Tập lệnh tăng tốc AI", "Có (Vector Instructions)", "Không hỗ trợ", "Chỉ có tập lệnh DSP cơ bản"],
        ["Số chân GPIO khả dụng", "45 chân IO linh hoạt", "34 chân (bị hạn chế chân Input-only)", "32 chân IO"],
        ["Giao diện ngoại vi", "3x UART, 2x I2C, 4x SPI, USB Native", "3x UART, 2x I2C, 3x SPI", "3x USART, 3x I2C, 5x SPI, USB OTG"],
        ["Khả năng đệm 30s sự cố", "Rất tốt (cấp phát PSRAM thoải mái)", "Hạn chế (nguy cơ tràn Heap)", "Không khả thi (SRAM quá nhỏ)"],
        ["Mức độ phù hợp đề tài", "Tối ưu nhất cho AIoT hộp đen", "Trung bình", "Kém phù hợp"]
    ]
    add_table_with_caption(doc, "Bảng 3.2: So sánh các phương án vi điều khiển cho khối xử lý trung tâm",
                           tbl2_headers, tbl2_data, col_widths=[1.8, 1.8, 1.5, 1.5])

    add_p(doc, "", bold_prefix="Phương án được lựa chọn: ESP32-S3-DevKitC-1 N16R8:")
    add_p(doc, 
          "Vi điều khiển ESP32-S3-DevKitC-1 N16R8 được lựa chọn chính thức cho hệ thống hộp đen AIoT vì đáp ứng hoàn hảo các yêu cầu cốt lõi:")
    add_bullet(doc, "Dung lượng bộ nhớ khổng lồ: ", 
               "Với 8 MB PSRAM tốc độ cao, hệ thống thoải mái cấp phát các mảng đệm vòng (Ring Buffers) lưu giữ 3000 mẫu dữ liệu IMU "
               "và 300 mẫu dữ liệu GPS cùng lúc mà chỉ chiếm dưới 2% dung lượng PSRAM khả dụng, loại bỏ hoàn toàn nguy cơ sập hệ thống do tràn bộ nhớ.")
    add_bullet(doc, "Khả năng tăng tốc học máy biên (TinyML): ", 
               "Tập lệnh xử lý vector của lõi Xtensa LX7 cho phép thực thi mô hình phân loại cử động và nhận diện sự cố ngay tại biên "
               "với độ trễ chỉ vài phần nghìn giây, giúp phát hiện tai nạn gần như tức thời.")
    add_bullet(doc, "Số lượng chân GPIO dồi dào: ", 
               "Cho phép kết nối độc lập toàn bộ các module ngoại vi (IMU, RTC, OLED, SD, GPS, 4G LTE, Buzzer, LED, Button, ADC) "
               "mà không cần sử dụng bất kỳ IC mở rộng chân nào, giúp sơ đồ mạch gọn gàng và tăng độ tin cậy phần cứng.")

    add_p(doc, "", bold_prefix="Bảng phân công chân kết nối GPIO đóng băng (Frozen GPIO Mapping):")
    add_p(doc, 
          "Để đảm bảo tính chuẩn xác tuyệt đối giữa thiết kế sơ đồ nguyên lý bản vẽ REV8 và mã nguồn nhúng của hệ thống, "
          "toàn bộ 17 tín hiệu phần cứng được phân công và cố định nghiêm ngặt vào các chân GPIO của ESP32-S3 như trình bày trong Bảng 3.3:")

    # Bảng 3.3 - Frozen GPIO Mapping
    tbl3_headers = ["STT", "Chân ESP32-S3", "Tên tín hiệu mạng", "Chế độ IO", "Khối phần cứng kết nối", "Chức năng chi tiết trong mạch"]
    tbl3_data = [
        ["1", "GPIO1", "ADC_VBAT_SENSE", "Analog Input", "Khối nguồn", "Đo điện áp pin Li-ion 18650 qua cầu phân áp 100k/100k + tụ 100nF"],
        ["2", "GPIO8", "I2C0_SDA", "Open-Drain / Bi-Dir", "MPU6050, DS3231, OLED", "Đường truyền dữ liệu bus I2C0 (Kéo trở 4.7k lên 3V3_SYS)"],
        ["3", "GPIO9", "I2C0_SCL", "Open-Drain / Output", "MPU6050, DS3231, OLED", "Đường xung nhịp bus I2C0 400kHz (Kéo trở 4.7k lên 3V3_SYS)"],
        ["4", "GPIO10", "IMU_INT", "Digital Input (Pull-up)", "Khối cảm biến MPU6050", "Tín hiệu ngắt phần cứng khi gia tốc vượt ngưỡng va chạm"],
        ["5", "GPIO14", "SD_CS", "Digital Output", "Khối thẻ nhớ MicroSD", "Tín hiệu chọn chip (Chip Select) giao tiếp bus SPI"],
        ["6", "GPIO11", "SPI_MOSI", "Digital Output", "Khối thẻ nhớ MicroSD", "Đường truyền dữ liệu nối tiếp từ vi điều khiển sang thẻ nhớ"],
        ["7", "GPIO12", "SPI_SCK", "Digital Output", "Khối thẻ nhớ MicroSD", "Đường xung nhịp đồng bộ giao tiếp bus SPI (20 MHz)"],
        ["8", "GPIO13", "SPI_MISO", "Digital Input", "Khối thẻ nhớ MicroSD", "Đường nhận dữ liệu nối tiếp từ thẻ nhớ về vi điều khiển"],
        ["9", "GPIO17", "GNSS_TXD", "Digital Output (UART1)", "Khối GPS (NEO-M8N)", "Đường truyền lệnh cấu hình từ ESP32 sang chân RX NEO-M8N"],
        ["10", "GPIO18", "GNSS_RXD", "Digital Input (UART1)", "Khối GPS (NEO-M8N)", "Đường nhận bản tin NMEA từ chân TX NEO-M8N về ESP32"],
        ["11", "GPIO21", "GNSS_PPS", "Digital Input (Interrupt)", "Khối GPS (NEO-M8N)", "Xung đồng bộ thời gian chuẩn 1Hz (Pulse Per Second)"],
        ["12", "GPIO43", "4G_TXD", "Digital Output (UART2)", "Khối 4G LTE (SIM7680C)", "Đường truyền tập lệnh AT từ ESP32 sang chân RX SIM7680C"],
        ["13", "GPIO44", "4G_RXD", "Digital Input (UART2)", "Khối 4G LTE (SIM7680C)", "Đường nhận dữ liệu phản hồi từ chân TX SIM7680C về ESP32"],
        ["14", "GPIO4", "4G_PWRKEY", "Digital Output", "Khối 4G LTE (SIM7680C)", "Kích xung mức thấp bật/tắt nguồn module 4G SIM7680C"],
        ["15", "GPIO5", "4G_STATUS", "Digital Input", "Khối 4G LTE (SIM7680C)", "Đọc mức logic trạng thái hoạt động của module 4G"],
        ["16", "GPIO6", "CANCEL", "Digital Input (Interrupt)", "Khối nút nhấn", "Ngắt nút nhấn hủy sự cố, trở kéo 10k lên 3V3 + tụ lọc 100nF"],
        ["17", "GPIO7", "LED_STATUS", "Digital Output", "Khối cảnh báo", "Điều khiển đèn LED chỉ thị trạng thái qua điện trở 330 ohm"],
        ["18", "GPIO15", "BUZZER_CTRL", "Digital Output", "Khối cảnh báo", "Điều khiển còi Piezo 5V qua điện trở bazơ 1k và NPN 2SC1815"]
    ]
    add_table_with_caption(doc, "Bảng 3.3: Bảng phân công chân kết nối GPIO của vi điều khiển ESP32-S3-DevKitC-1 N16R8",
                           tbl3_headers, tbl3_data, col_widths=[0.5, 1.2, 1.5, 1.4, 1.5, 2.5])

    add_p(doc, 
          "Sơ đồ nguyên lý kết nối chi tiết của khối xử lý trung tâm ESP32-S3-DevKitC-1 N16R8 trích xuất từ bản vẽ thiết kế REV8 "
          "được thể hiện trong Hình 3.2:")
          
    fig2_path = os.path.join(assets_dir, "H3_2_esp32_block.png")
    add_figure(doc, fig2_path, "Hình 3.2: Sơ đồ nguyên lý khối vi điều khiển ESP32-S3-DevKitC-1 N16R8", width_inches=4.8)

    # =========================================================================
    # 3.2.2 Khối cảm biến quán tính
    # =========================================================================
    add_h3(doc, "3.2.2 Khối cảm biến quán tính")
    
    add_p(doc, 
          "Khối cảm biến quán tính (IMU) là thành phần thu nhận tín hiệu vật lý quan trọng nhất của hộp đen, quyết định trực tiếp "
          "khả năng phát hiện và phân tích tai nạn giao thông. Khi xe máy điện di chuyển, các lực tác động cơ học như phanh gấp, "
          "ôm cua, rung xóc do ổ gà, va quẹt hay lật ngã đều tạo ra các biến thiên đặc trưng về gia tốc dài và tốc độ quay góc. "
          "Để thực hiện nhiệm vụ này, các phương án cảm biến quán tính được khảo sát gồm:")
          
    add_p(doc, "", bold_prefix="Phương án 1: Sử dụng module GY-521 tích hợp IC MPU6050 (InvenSense / TDK):")
    add_p(doc, 
          "MPU6050 là cảm biến chuyển động 6 bậc tự do (6-DoF) tích hợp nguyên khối một cảm biến gia tốc 3 trục (MEMS Accelerometer) "
          "và một con quay hồi chuyển 3 trục (MEMS Gyroscope) cùng bộ vi xử lý chuyển động kỹ thuật số phần cứng (DMP - Digital Motion Processor).")
    add_bullet(doc, "Ưu điểm: ", 
               "Tích hợp đồng thời cả gia tốc và vận tốc góc trong một chip duy nhất; dải đo gia tốc có thể lập trình lên tới ±16g và "
               "vận tốc góc ±2000 °/s đáp ứng hoàn hảo dải động học va chạm xe máy; tích hợp sẵn bộ đệm phần cứng FIFO 1024 bytes cho phép "
               "vi điều khiển đọc mẻ (Burst read) giảm tải ngắt CPU; hỗ trợ chân ngắt phần cứng INT; giá thành rất rẻ và phổ biến rộng rãi.")
    add_bullet(doc, "Nhược điểm: ", 
               "Không tích hợp sẵn cảm biến từ trường (La bàn số Magnetometer), tuy nhiên đối với việc phân tích tai nạn xe máy, "
               "dữ liệu gia tốc và góc nghiêng Roll/Pitch từ 6-DoF là hoàn toàn đầy đủ và đáng tin cậy.")

    add_p(doc, "", bold_prefix="Phương án 2: Sử dụng cảm biến gia tốc 3 trục ADXL345 (Analog Devices):")
    add_p(doc, 
          "ADXL345 là cảm biến gia tốc 3 trục độc lập độ phân giải cao (13-bit) dải đo ±16g, giao tiếp qua I2C hoặc SPI.")
    add_bullet(doc, "Ưu điểm: ", 
               "Tiêu thụ dòng điện cực thấp (dưới 30 µA), độ bền công nghiệp cao, hỗ trợ nhiều chế độ ngắt phần cứng (Tap, Double Tap, Free Fall).")
    add_bullet(doc, "Nhược điểm: ", 
               "Chỉ có 3 trục gia tốc kế, hoàn toàn thiếu 3 trục con quay hồi chuyển (Gyroscope). Do đó hệ thống không thể tính toán chính xác "
               "góc nghiêng động khi xe đang ôm cua ở tốc độ cao (bị ảnh hưởng bởi lực ly tâm) và không đo được vận tốc góc quay khi xe bị trượt ngã.")

    add_p(doc, "", bold_prefix="Phương án 3: Sử dụng cảm biến định hướng tuyệt đối 9-DoF BNO055 (Bosch Sensortec):")
    add_p(doc, 
          "BNO055 là cảm biến SiP (System in Package) 9 trục tích hợp Accelerometer, Gyroscope, Magnetometer và bộ xử lý ARM Cortex-M0 chạy thuật toán hợp nhất dữ liệu (Sensor Fusion) xuất trực tiếp góc Euler và Quaternion.")
    add_bullet(doc, "Ưu điểm: ", 
               "Độ chính xác rất cao, tự động lọc trôi dạt và bù nhiệt, vi điều khiển không cần tính toán góc nghiêng.")
    add_bullet(doc, "Nhược điểm: ", 
               "Giá thành rất đắt (cao gấp 6 - 8 lần MPU6050); từ kế dễ bị méo mó từ trường nghiêm trọng bởi khung kim loại và động cơ điện công suất lớn của xe máy; nguồn cung cấp trên thị trường không ổn định.")

    add_p(doc, 
          "Các thông số kỹ thuật cốt lõi so sánh giữa các phương án cảm biến quán tính được trình bày trong Bảng 3.4:")
          
    # Bảng 3.4
    tbl4_headers = ["Tiêu chí kỹ thuật", "GY-521 (MPU6050) [Được chọn]", "ADXL345", "BNO055"]
    tbl4_data = [
        ["Số bậc tự do (DoF)", "6-DoF (3 trục Gia tốc + 3 trục Con quay)", "3-DoF (Chỉ có 3 trục Gia tốc)", "9-DoF (Gia tốc + Con quay + Từ kế)"],
        ["Dải đo gia tốc", "±2g, ±4g, ±8g, ±16g", "±2g, ±4g, ±8g, ±16g", "±2g, ±4g, ±8g, ±16g"],
        ["Dải đo vận tốc góc", "±250, ±500, ±1000, ±2000 °/s", "Không có", "±125, ±250, ±500, ±1000, ±2000 °/s"],
        ["Độ phân giải ADC", "16-bit cho mỗi trục", "13-bit", "16-bit (Gia tốc & Con quay)"],
        ["Bộ đệm phần cứng (FIFO)", "1024 Bytes", "32 Mẫu (Level FIFO)", "Không hỗ trợ FIFO người dùng"],
        ["Chuẩn giao tiếp", "I2C (Fast Mode 400 kHz)", "I2C / SPI", "I2C / UART"],
        ["Tác động của từ trường xe", "Hoàn toàn miễn nhiễm", "Hoàn toàn miễn nhiễm", "Dễ bị sai lệch góc do động cơ xe điện"],
        ["Chi phí linh kiện", "Thấp (~30.000 VNĐ)", "Trung bình (~55.000 VNĐ)", "Rất cao (~220.000 VNĐ)"],
        ["Đánh giá mức độ phù hợp", "Tối ưu và tin cậy nhất", "Thiếu trục đo góc quay", "Không cần thiết, giá quá cao"]
    ]
    add_table_with_caption(doc, "Bảng 3.4: So sánh các phương án cảm biến quán tính cho khối IMU",
                           tbl4_headers, tbl4_data, col_widths=[1.8, 2.0, 1.6, 1.8])

    add_p(doc, "", bold_prefix="Phương án được lựa chọn: Module GY-521 (MPU6050):")
    add_p(doc, 
          "Module GY-521 tích hợp IC MPU6050 được lựa chọn nhờ sự cân bằng hoàn hảo giữa tính năng kỹ thuật, độ tin cậy và giá thành. "
          "Dải đo ±16g và ±2000 °/s đáp ứng hoàn hảo yêu cầu đo đạc va chạm xung lực lớn trên xe máy. Các thông số kỹ thuật chi tiết của "
          "module được tổng hợp trong Bảng 3.5:")

    # Bảng 3.5
    tbl5_headers = ["Thông số kỹ thuật", "Giá trị thiết kế / Đặc tính kỹ thuật", "Ghi chú ứng dụng"]
    tbl5_data = [
        ["IC cảm biến chính", "MPU6050 (InvenSense / TDK)", "Cảm biến chuyển động MEMS 6-DoF nguyên khối"],
        ["Điện áp hoạt động module", "3.3V - 5.0V (Tích hợp LDO 3.3V onboard)", "Hệ thống cấp nguồn chuẩn từ đường 3V3_SYS"],
        ["Giao diện truyền thông", "I2C (Chân SCL, SDA), tốc độ tối đa 400 kHz", "Nối chung bus I2C0 với DS3231 và OLED"],
        ["Cấu hình địa chỉ I2C", "0x69 (Khi chân AD0 nối lên mức cao 3.3V)", "Tránh xung đột địa chỉ 0x68 với DS3231 RTC"],
        ["Chân ngắt phần cứng", "Chân INT nối về GPIO10 của ESP32-S3", "Báo ngắt chuyển động / ngắt dữ liệu sẵn sàng"],
        ["Tần số lấy mẫu dữ liệu", "100 Hz (Cấu hình bộ lọc thông thấp DLPF)", "Đảm bảo ghi nhận trọn vẹn đỉnh va chạm"],
        ["Các chân không sử dụng", "XDA (Auxiliary SDA), XCL (Auxiliary SCL)", "Để hở mạch (No-Connect) theo chuẩn REV8"]
    ]
    add_table_with_caption(doc, "Bảng 3.5: Thông số kỹ thuật chi tiết của cảm biến MPU6050 (GY-521)",
                           tbl5_headers, tbl5_data, col_widths=[2.0, 2.8, 2.4])

    add_p(doc, "", bold_prefix="Kết nối phần cứng và giải pháp chống xung đột địa chỉ I2C:")
    add_p(doc, 
          "Trên sơ đồ nguyên lý bản vẽ REV8, module GY-521 có 8 chân header vật lý. Các kết nối được thiết kế cụ thể như sau:")
    add_bullet(doc, "Chân nguồn VCC & GND: ", "Chân VCC được cấp từ nguồn 3V3_SYS đã qua lọc nhiễu, chân GND nối vào mặt phẳng mass chung.")
    add_bullet(doc, "Bus giao tiếp I2C: ", "Chân SCL nối vào GPIO9 (I2C0_SCL), chân SDA nối vào GPIO8 (I2C0_SDA). Bus I2C được kéo lên nguồn 3V3_SYS thông qua hai điện trở pull-up R1, R2 có giá trị 4.7kΩ.")
    add_bullet(doc, "Giải pháp xung đột địa chỉ (AD0 Pin): ", 
               "Mặc định khi chân AD0 nối đất (GND), MPU6050 có địa chỉ I2C là 0x68. Tuy nhiên, địa chỉ 0x68 này trùng hoàn toàn với "
               "địa chỉ I2C cố định của IC thời gian thực DS3231. Để giải quyết triệt để vấn đề xung đột địa chỉ trên cùng một đường bus I2C, "
               "thiết kế REV8 đã nối cố định chân AD0 của MPU6050 lên đường nguồn 3V3_SYS. Nhờ đó, địa chỉ I2C của MPU6050 chuyển thành 0x69, "
               "giúp vi điều khiển giao tiếp độc lập, tin cậy tuyệt đối với cả hai thiết bị.")
    add_bullet(doc, "Chân ngắt INT: ", "Nối trực tiếp vào GPIO10 (IMU_INT) của vi điều khiển, cho phép đánh thức hệ thống hoặc kích hoạt lấy mẫu khẩn cấp.")
    add_bullet(doc, "Các chân phụ XDA, XCL: ", "Để hở hoàn toàn (No-Connect) vì hệ thống không sử dụng thêm cảm biến từ kế phụ trợ.")

    add_p(doc, 
          "Sơ đồ nguyên lý khối cảm biến quán tính GY-521 (MPU6050) trích xuất từ bản vẽ thiết kế REV8 được thể hiện trong Hình 3.3:")
          
    fig3_path = os.path.join(assets_dir, "H3_3_mpu6050_block.png")
    add_figure(doc, fig3_path, "Hình 3.3: Sơ đồ nguyên lý khối cảm biến quán tính GY-521 (MPU6050)", width_inches=4.5)

    # =========================================================================
    # 3.2.3 Khối đồng hồ thời gian thực
    # =========================================================================
    add_h3(doc, "3.2.3 Khối đồng hồ thời gian thực")
    
    add_p(doc, 
          "Đối với một thiết bị hộp đen ghi nhận sự cố, tính xác thực về mặt thời gian (Forensic Timestamp) có ý nghĩa quyết định "
          "về giá trị pháp lý trong điều tra tai nạn và khiếu nại bảo hiểm. Thời gian ghi nhận sự cố phải là thời gian thực tuyệt đối "
          "(năm, tháng, ngày, giờ, phút, giây) và không bị sai lệch khi xe đi vào vùng hầm, mất sóng vệ tinh GPS hay mất sóng mạng 4G. "
          "Các phương án thiết kế khối thời gian thực được xem xét bao gồm:")
          
    add_p(doc, "", bold_prefix="Phương án 1: Sử dụng module RTC DS3231 có bù nhiệt độ TCXO (Maxim Integrated):")
    add_p(doc, 
          "DS3231 là IC đồng hồ thời gian thực tích hợp sẵn bộ dao động thạch anh bù nhiệt độ (TCXO - Temperature Compensated Crystal Oscillator) "
          "và cảm biến nhiệt độ bên trong chip nguyên khối.")
    add_bullet(doc, "Ưu điểm: ", 
               "Độ chính xác cực cao (sai số danh định chỉ ±2 ppm trong dải nhiệt độ từ 0°C đến +40°C, tương đương sai số chưa tới 1 phút "
               "trong suốt 1 năm hoạt động liên tục ngoài trời); tích hợp khe gắn pin cúc áo CR2032 dự phòng trên bo mạch giúp duy trì thời gian "
               "liên tục từ 3 đến 5 năm ngay cả khi mất toàn bộ nguồn điện chính; giao tiếp I2C chuẩn; độ tin cậy tuyệt đối.")
    add_bullet(doc, "Nhược điểm: ", 
               "Giá thành cao hơn dòng DS1307 cơ bản (tuy nhiên hoàn toàn xứng đáng với yêu cầu của thiết bị hộp đen).")

    add_p(doc, "", bold_prefix="Phương án 2: Sử dụng module RTC DS1307 truyền thống:")
    add_p(doc, 
          "DS1307 là IC thời gian thực kinh điển sử dụng thạch anh dao động 32.768 kHz gắn ngoài.")
    add_bullet(doc, "Ưu điểm: ", 
               "Giá thành rất rẻ, mạch đơn giản, dễ tìm mua.")
    add_bullet(doc, "Nhược điểm: ", 
               "Độ trôi thời gian rất lớn khi nhiệt độ môi trường thay đổi. Do thạch anh ngoài không có mạch bù nhiệt, trong điều kiện xe máy "
               "hoạt động ngoài trời (nắng gắt mùa hè nhiệt độ lên tới 50°C hoặc đêm lạnh), thời gian của DS1307 có thể bị sai lệch từ vài phút "
               "đến hàng chục phút mỗi tháng, làm mất giá trị bằng chứng pháp lý của dữ liệu hộp đen.")

    add_p(doc, "", bold_prefix="Phương án 3: Sử dụng bộ đếm RTC nội tích hợp trong ESP32-S3:")
    add_p(doc, 
          "ESP32-S3 có tích hợp bộ đếm RTC nội và có thể đồng bộ thời gian từ máy chủ NTP (Network Time Protocol) qua Wi-Fi/4G.")
    add_bullet(doc, "Ưu điểm: ", 
               "Không tốn thêm chi phí linh kiện phần cứng, tiết kiệm diện tích mạch in.")
    add_bullet(doc, "Nhược điểm: ", 
               "Độ chính xác của bộ dao động RC nội rất kém (sai lệch lớn theo nhiệt độ); phụ thuộc hoàn toàn vào kết nối mạng Internet để "
               "đồng bộ lại thời gian sau mỗi lần tắt/bật nguồn; nếu xe đi vào vùng không có sóng 4G/GPS khi khởi động, hệ thống sẽ hoàn toàn "
               "mất mốc thời gian thực, dẫn đến tệp tin sự cố bị gán nhãn thời gian sai (như năm 1970).")

    add_p(doc, 
          "Các chỉ tiêu kỹ thuật đối sánh giữa các giải pháp RTC được tổng hợp trong Bảng 3.6:")
          
    # Bảng 3.6
    tbl6_headers = ["Tiêu chí kỹ thuật", "Module DS3231 [Được chọn]", "Module DS1307", "RTC nội ESP32-S3"]
    tbl6_data = [
        ["Công nghệ dao động", "Thạch anh bù nhiệt độ nội (TCXO)", "Thạch anh 32.768 kHz rời ngoài", "Bộ dao động RC nội / Thạch anh ngoài"],
        ["Độ chính xác / Sai số", "Cực cao: ±2 ppm (Sai lệch < 1 phút/năm)", "Kém: ±20 - 50 ppm (Sai lệch 2-5 phút/tháng)", "Rất kém nếu không có đồng bộ mạng liên tục"],
        ["Ảnh hưởng của nhiệt độ", "Tự động bù nhiệt độ từ 0°C đến +40°C", "Trôi dạt nghiêm trọng theo thời tiết", "Trôi dạt mạnh theo nhiệt độ chip"],
        ["Pin nuôi nguồn dự phòng", "Pin cúc áo CR2032 onboard trên module", "Pin cúc áo CR2032", "Không có (Mất thời gian khi ngắt nguồn)"],
        ["Độ độc lập với mạng", "Độc lập hoàn toàn, tức thời khi bật nguồn", "Độc lập với mạng", "Phụ thuộc hoàn toàn vào sóng 4G/NTP"],
        ["Giao diện truyền thông", "I2C (Địa chỉ cố định 0x68)", "I2C (Địa chỉ cố định 0x68)", "Thanh ghi nội của vi điều khiển"],
        ["Mức độ phù hợp đề tài", "Hoàn hảo nhất cho hộp đen an toàn", "Không đạt yêu cầu pháp lý", "Không khả thi cho thiết bị độc lập"]
    ]
    add_table_with_caption(doc, "Bảng 3.6: So sánh các phương án đồng hồ thời gian thực cho khối RTC",
                           tbl6_headers, tbl6_data, col_widths=[1.8, 2.0, 1.8, 1.6])

    add_p(doc, "", bold_prefix="Phương án được lựa chọn: Module DS3231 RTC:")
    add_p(doc, 
          "Module DS3231 được lựa chọn chính thức nhằm đảm bảo tính toàn vẹn và giá trị pháp lý tuyệt đối cho các bản ghi sự cố hộp đen. "
          "Thông số kỹ thuật chi tiết của module DS3231 được tổng hợp trong Bảng 3.7:")

    # Bảng 3.7
    tbl7_headers = ["Thông số kỹ thuật", "Giá trị thiết kế / Đặc tính kỹ thuật", "Ghi chú ứng dụng"]
    tbl7_data = [
        ["IC thời gian thực", "DS3231SN / DS3231M (Maxim Integrated)", "Tích hợp sẵn TCXO và cảm biến nhiệt độ bên trong"],
        ["Độ chính xác thời gian", "±2 ppm từ 0°C đến +40°C; ±3.5 ppm từ -40°C đến +85°C", "Tương đương sai số danh định dưới 1 phút mỗi năm"],
        ["Điện áp hoạt động logic", "3.3V DC (Cấp từ đường nguồn 3V3_SYS)", "Đồng bộ chuẩn logic 3.3V với ESP32-S3"],
        ["Pin nuôi nguồn dự phòng", "Pin Lithium Cell CR2032 (3V / 220 mAh)", "Đế pin tích hợp onboard trên bo mạch module"],
        ["Dòng tiêu thụ chế độ pin", "Chỉ khoảng 1.0 µA - 3.0 µA khi mất nguồn chính", "Đảm bảo duy trì thời gian từ 3 đến 5 năm liên tục"],
        ["Giao diện truyền thông", "I2C (Bus I2C0), tốc độ truyền 400 kHz", "Dùng chung chân GPIO8 (SDA) và GPIO9 (SCL)"],
        ["Địa chỉ I2C cố định", "0x68 (Chuẩn công nghiệp của dòng DS3231)", "Không bị trùng do MPU6050 đã chuyển sang 0x69"],
        ["Chân không kết nối", "32K (Xung ra 32.768kHz) và SQW (Ngắt vuông)", "Để hở mạch (No-Connect) theo thiết kế REV8"]
    ]
    add_table_with_caption(doc, "Bảng 3.7: Thông số kỹ thuật chi tiết của module DS3231 RTC",
                           tbl7_headers, tbl7_data, col_widths=[2.0, 2.8, 2.4])

    add_p(doc, "", bold_prefix="Kết nối phần cứng khối RTC trên sơ đồ nguyên lý REV8:")
    add_p(doc, 
          "Module DS3231 sử dụng trong đề tài có hàng header vật lý gồm 6 chân: 32K, SQW, SCL, SDA, VCC, GND. Cần đặc biệt lưu ý "
          "rằng đế pin cúc áo CR2032 đã được tích hợp gắn trực tiếp trên mặt lưng của bo mạch module, hoàn toàn không có chân header "
          "VBAT rời đưa ra ngoài. Kết nối mạch điện của khối RTC được thiết kế chuẩn xác như sau:")
    add_bullet(doc, "Chân nguồn VCC & GND: ", "Chân VCC nối vào đường nguồn logic 3V3_SYS, chân GND nối vào mass chung hệ thống.")
    add_bullet(doc, "Bus giao diện I2C: ", "Chân SCL nối vào GPIO9 (I2C0_SCL), chân SDA nối vào GPIO8 (I2C0_SDA). Module sử dụng chung trở kéo pull-up 4.7kΩ có sẵn trên bus I2C0.")
    add_bullet(doc, "Các chân 32K và SQW: ", "Do hệ thống không cần xuất xung nhịp thạch anh 32.768 kHz ra ngoài và cũng không sử dụng ngắt báo thức (Alarm interrupt), hai chân 32K và SQW được giữ nguyên trạng thái để hở mạch (No-Connect), đảm bảo độ an toàn cao nhất.")

    add_p(doc, 
          "Sơ đồ nguyên lý khối đồng hồ thời gian thực DS3231 RTC trích xuất từ bản vẽ thiết kế REV8 được thể hiện trong Hình 3.4:")
          
    fig4_path = os.path.join(assets_dir, "H3_4_ds3231_block.png")
    add_figure(doc, fig4_path, "Hình 3.4: Sơ đồ nguyên lý khối đồng hồ thời gian thực DS3231 RTC", width_inches=4.5)

    print("Section 3.2 Part 1 built successfully.")
