# -*- coding: utf-8 -*-
"""
Module ch3_sec31.py: Section 3.1 content generator.
"""

import os
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from build_chapter3_full import (
    add_p, add_bullet, add_h1, add_h2, add_h3, add_figure, add_table_with_caption
)

def add_section_3_1(doc, assets_dir):
    # -------------------------------------------------------------------------
    # CHƯƠNG 3
    # -------------------------------------------------------------------------
    add_h1(doc, "CHƯƠNG 3: THIẾT KẾ VÀ XÂY DỰNG HỆ THỐNG")
    
    add_p(doc, 
          "Chương 3 tập trung trình bày toàn diện quá trình nghiên cứu, tính toán, lựa chọn giải pháp công nghệ "
          "và xây dựng kiến trúc phần cứng cũng như thuật toán cho đề tài “Thiết kế hộp đen AIoT thông minh phân tích "
          "và ghi lại sự cố xe máy điện”. Dựa trên những yêu cầu kỹ thuật thực tế của phương tiện giao thông hai bánh, "
          "chương này sẽ phân tích cụ thể sơ đồ khối chức năng, mô tả nguyên lý vận hành tổng thể, thực hiện đối sánh "
          "kỹ thuật để lựa chọn linh kiện tối ưu cho từng khối, thiết kế sơ đồ nguyên lý tích hợp hoàn chỉnh và xây dựng "
          "thuật toán phân tích sự cố tại biên (Edge Computing) đảm bảo tính thời gian thực, độ tin cậy và an toàn thông tin.")
          
    # -------------------------------------------------------------------------
    # 3.1 YÊU CẦU VÀ SƠ ĐỒ KHỐI HỆ THỐNG
    # -------------------------------------------------------------------------
    add_h2(doc, "3.1 YÊU CẦU VÀ SƠ ĐỒ KHỐI HỆ THỐNG")
    
    # 3.1.1 Yêu cầu của hệ thống
    add_h3(doc, "3.1.1 Yêu cầu của hệ thống")
    
    add_p(doc, 
          "Xe máy điện (Electric Motorcycle / E-Scooter) đang trở thành phương tiện giao thông cá nhân phổ biến hàng đầu "
          "tại Việt Nam và nhiều quốc gia nhờ ưu điểm thân thiện với môi trường và tiết kiệm chi phí năng lượng. Tuy nhiên, "
          "đặc tính động học của phương tiện hai bánh vốn tiềm ẩn độ mất ổn định cao hơn rất nhiều so với ô tô bốn bánh. "
          "Các tình huống mất lái, trượt ngã, va chạm trực diện hoặc tông đuôi thường diễn ra chỉ trong vài phần trăm giây. "
          "Hơn nữa, người điều khiển xe máy điện dễ bị chấn thương nặng hoặc bất tỉnh sau tai nạn, dẫn đến mất khả năng tự gọi "
          "cứu hộ. Xuất phát từ thực tiễn cấp bách đó, hệ thống hộp đen AIoT thông minh cần phải đáp ứng đầy đủ các yêu cầu "
          "kỹ thuật khắt khe sau:")
          
    add_p(doc, "", bold_prefix="a) Yêu cầu chức năng (Functional Requirements):")
    
    add_bullet(doc, "Thu thập dữ liệu chuyển động quán tính liên tục: ",
               "Hệ thống phải thu thập dữ liệu gia tốc 3 trục (ax, ay, az) và vận tốc góc 3 trục (gx, gy, gz) ở tần số cao "
               "(tối thiểu 100 Hz) với độ phân giải cao nhằm nắm bắt trọn vẹn diễn biến động học của xe ngay trước, trong và sau sự cố.")
               
    add_bullet(doc, "Định vị vị trí địa lý chính xác: ",
               "Xác định tọa độ kinh độ (Longitude), vĩ độ (Latitude), độ cao và tốc độ di chuyển thực tế của xe thông qua "
               "hệ thống vệ tinh định vị toàn cầu GNSS với tần số cập nhật dữ liệu đạt 10 Hz.")
               
    add_bullet(doc, "Cung cấp thời gian thực tuyệt đối: ",
               "Đồng bộ tem thời gian thực (Timestamp) chính xác đến từng giây (năm, tháng, ngày, giờ, phút, giây) từ khối RTC "
               "chuyên dụng có bù nhiệt, đảm bảo tính pháp lý và độc lập hoàn toàn với sóng viễn thông.")
               
    add_bullet(doc, "Phân tích và phát hiện sự cố tại biên (Edge Processing): ",
               "Sử dụng thuật toán học máy biên (TinyML) kết hợp phân tích ngưỡng động lực học để phân loại chính xác các trạng "
               "thái sự cố (va chạm trực diện/đuôi, ngã lật xe, trượt rê trên đường) và phân biệt với các rung chấn bình thường "
               "(như xe đi qua gờ giảm tốc, ổ gà).")
               
    add_bullet(doc, "Cơ chế đệm vòng và lưu trữ dữ liệu an toàn: ",
               "Hệ thống duy trì bộ đệm vòng (circular FIFO buffer) lưu trữ liên tục 30 giây dữ liệu (15 giây trước sự cố và "
               "15 giây sau sự cố). Dữ liệu này được tự động ghi cố định vào thẻ nhớ MicroSD theo định dạng tệp tin nhị phân/CSV "
               "chuẩn và khóa lại kèm mã băm SHA-256 để chống can thiệp, phục vụ công tác giám định pháp y và bảo hiểm.")
               
    add_bullet(doc, "Cảnh báo đa cấp và tương tác người dùng: ",
               "Khi phát hiện sự cố, hệ thống phát cảnh báo tại chỗ bằng còi Piezo âm lượng lớn (> 85 dB) kết hợp đèn LED trạng thái "
               "và hiển thị đồng hồ đếm ngược 15 giây trên màn hình OLED. Người lái có thể nhấn nút CANCEL để chủ động hủy báo động "
               "nếu sự cố nhẹ hoặc va quẹt ngoài ý muốn.")
               
    add_bullet(doc, "Truyền thông khẩn cấp không dây: ",
               "Nếu hết thời gian đếm ngược 15 giây mà không có thao tác hủy từ người dùng, hệ thống lập tức kích hoạt module 4G LTE "
               "gửi tin nhắn SMS khẩn cấp chứa tọa độ Google Maps đến số điện thoại người thân/cứu hộ, đồng thời truyền bản tin "
               "telemetry lên máy chủ IoT qua giao thức MQTT/HTTP.")
               
    add_bullet(doc, "Quản lý nguồn và vận hành độc lập: ",
               "Hệ thống vận hành bằng nguồn pin Li-ion 18650 tích hợp, có mạch giám sát điện áp pin thời gian thực và hỗ trợ "
               "cổng sạc tiêu chuẩn USB-C để nạp lại năng lượng.")

    add_p(doc, "", bold_prefix="b) Yêu cầu phi chức năng (Non-Functional Requirements):")
    
    add_bullet(doc, "Độ ổn định và kháng nhiễu công nghiệp: ",
               "Thiết bị phải chịu được rung lắc cơ học mạnh, dằn xóc liên tục và nhiệt độ môi trường khắc nghiệt khi xe di chuyển ngoài trời.")
               
    add_bullet(doc, "Độ trễ xử lý cực thấp: ",
               "Thời gian từ khi xảy ra va chạm đến khi kích hoạt còi cảnh báo tại chỗ phải dưới 100 ms; thời gian gửi tin nhắn khẩn cấp "
               "không quá 5 giây sau khi hết thời gian đếm ngược.")
               
    add_bullet(doc, "An toàn năng lượng và phân tách miền nguồn: ",
               "Thiết kế các đường nguồn 5V_SYS và 3V3_SYS độc lập, có tụ lọc ổn định nhằm ngăn chặn hoàn toàn hiện tượng sụt áp tức thời "
               "(Brownout Reset) khi module 4G phát sóng công suất cao hoặc thẻ nhớ thực hiện lệnh ghi ngẫu nhiên.")
               
    add_bullet(doc, "Kích thước nhỏ gọn: ",
               "Kích thước mạch và vỏ hộp được tối ưu hóa để lắp đặt kín đáo, an toàn bên trong thân hoặc cốp xe máy điện.")

    # 3.1.2 Sơ đồ khối hệ thống và chức năng của từng khối
    add_h3(doc, "3.1.2 Sơ đồ khối hệ thống và chức năng của từng khối")
    
    add_p(doc, 
          "Dựa trên các yêu cầu phân tích ở trên, hệ thống hộp đen AIoT thông minh được xây dựng theo kiến trúc phân tầng "
          "module hóa cao, bao gồm 10 khối chức năng chính được liên kết chặt chẽ thông qua các chuẩn giao tiếp tiêu chuẩn công nghiệp "
          "(I2C, SPI, UART, GPIO). Sơ đồ khối chức năng hoàn chỉnh của hệ thống được minh họa chi tiết trong Hình 3.1 dưới đây:")
          
    fig1_path = os.path.join(assets_dir, "H3_1_so_do_khoi_he_thong.png")
    add_figure(doc, fig1_path, "Hình 3.1: Sơ đồ khối chức năng của hệ thống hộp đen AIoT xe máy điện", width_inches=6.0)
    
    add_p(doc, "Chức năng chi tiết và vai trò kỹ thuật của từng khối trong hệ thống được xác định như sau:")
    
    add_bullet(doc, "1. Khối xử lý trung tâm (Central Processing Unit): ",
               "Đóng vai trò là 'bộ não' điều phối toàn bộ hoạt động của thiết bị. Khối sử dụng vi điều khiển ESP32-S3-DevKitC-1 N16R8 "
               "với lõi kép 32-bit Xtensa LX7 xung nhịp 240 MHz, tích hợp 16 MB Flash và 8 MB Octal PSRAM. Vi điều khiển đảm nhiệm "
               "thu thập dữ liệu cảm biến đa luồng, duy trì bộ đệm vòng FIFO 30 giây trong PSRAM, chạy mô hình học máy biên TinyML "
               "nhận diện sự cố, điều khiển các khối ngoại vi và xử lý giao thức viễn thông.")
               
    add_bullet(doc, "2. Khối cảm biến quán tính (Inertial Measurement Unit - IMU): ",
               "Sử dụng module GY-521 tích hợp IC MPU6050 bao gồm 3 trục gia tốc kế (Accelerometer) và 3 trục con quay hồi chuyển "
               "(Gyroscope) 16-bit. Khối đo đạc liên tục các biến thiên gia tốc va đập và vận tốc góc quay thân xe, gửi về vi điều khiển "
               "qua bus I2C (tần số 400 kHz) kết hợp chân ngắt phần cứng IMU_INT để báo hiệu khi có sự kiện vượt ngưỡng.")
               
    add_bullet(doc, "3. Khối đồng hồ thời gian thực (Real-Time Clock - RTC): ",
               "Sử dụng module DS3231 tích hợp bộ dao động thạch anh bù nhiệt độ (TCXO) có độ chính xác cao (sai số dưới 1 phút/năm). "
               "Khối cung cấp mốc thời gian tuyệt đối chính xác cho các bản ghi hộp đen, đồng thời tích hợp pin cúc áo CR2032 dự phòng "
               "giúp mạch RTC duy trì thời gian liên tục ngay cả khi hệ thống bị ngắt toàn bộ nguồn điện.")
               
    add_bullet(doc, "4. Khối định vị GPS (GNSS Module): ",
               "Sử dụng module định vị cao cấp NEO-M8N của u-blox, hỗ trợ đồng thời nhiều hệ thống vệ tinh định vị (GPS, GLONASS, "
               "Galileo, BeiDou). Khối có nhiệm vụ giải mã vị trí địa lý (kinh độ, vĩ độ, độ cao) và vận tốc di chuyển thực tế, truyền về "
               "ESP32-S3 qua giao tiếp UART và cung cấp xung thời gian chuẩn PPS (Pulse Per Second) cho hệ thống.")
               
    add_bullet(doc, "5. Khối lưu trữ cục bộ (Local Storage): ",
               "Sử dụng module thẻ nhớ MicroSD giao tiếp qua chuẩn bus SPI tốc độ cao. Khối lưu giữ các bản ghi tệp tin nhị phân "
               "và nhật ký hành trình hộp đen độc lập với mạng Internet, đảm bảo dữ liệu quan trọng không bao giờ bị mất mát khi xe "
               "đi vào vùng mất sóng di động.")
               
    add_bullet(doc, "6. Khối truyền thông 4G LTE: ",
               "Sử dụng module công nghiệp MKE-M21 tích hợp chip SIM7680C chuẩn LTE Cat-1. Khối đảm nhận việc gửi tin nhắn SMS "
               "chứa liên kết tọa độ vị trí sự cố đến người thân/trung tâm cứu hộ và truyền các gói tin dữ liệu giám sát từ xa "
               "lên nền tảng đám mây IoT qua giao thức MQTT/HTTP.")
               
    add_bullet(doc, "7. Khối hiển thị (Display Block): ",
               "Sử dụng màn hình OLED 0.96 inch độ phân giải 128x64 điểm ảnh chuẩn giao tiếp I2C. Màn hình hiển thị trạng thái vận hành, "
               "tốc độ xe, số lượng vệ tinh GPS kết nối, cường độ sóng 4G, mức pin và trực quan hóa đồng hồ đếm ngược 15 giây khi xảy ra sự cố.")
               
    add_bullet(doc, "8. Khối cảnh báo tại chỗ (Warning Block): ",
               "Bao gồm còi báo Piezo 5V âm lượng lớn được điều khiển qua transistor NPN 2SC1815 và đèn LED báo hiệu trạng thái (Status LED). "
               "Khối có nhiệm vụ phát tín hiệu âm thanh và ánh sáng mạnh mẽ nhằm thu hút sự trợ giúp của người đi đường xung quanh hiện trường tai nạn.")
               
    add_bullet(doc, "9. Khối nút nhấn (User Input Block): ",
               "Bao gồm nút bấm CANCEL tích hợp mạch lọc RC phần cứng chống rung phím (Debounce). Nút nhấn cho phép người lái chủ động "
               "xác nhận tình trạng an toàn và hủy bỏ quá trình báo động khẩn cấp trong trường hợp sự cố va quẹt nhẹ.")
               
    add_bullet(doc, "10. Khối nguồn (Power Management Block): ",
               "Bao gồm nguồn pin Li-ion 18650 tích hợp (VBAT) là nguồn năng lượng vận hành chính; cổng sạc ngoài USB-C (VBUS); các mạch "
               "chuyển đổi và phân phối nguồn tạo ra hai đường điện áp hệ thống riêng biệt: 5V_SYS (cấp cho ESP32 DevKit, còi Buzzer) và "
               "3V3_SYS (cấp cho các cảm biến và mạch logic); cùng mạch cầu phân áp đo điện áp pin đưa về chân GPIO1 (ADC_VBAT_SENSE).")
               
    add_p(doc, 
          "Mối quan hệ phối hợp, chuẩn giao tiếp và linh kiện cụ thể của 10 khối chức năng được tổng hợp một cách khoa học "
          "trong Bảng 3.1 dưới đây:")
          
    # Bảng 3.1
    tbl1_headers = ["STT", "Khối chức năng", "Linh kiện / Module lựa chọn", "Giao tiếp phần cứng", "Nhiệm vụ chính trong hệ thống"]
    tbl1_data = [
        ["1", "Khối xử lý trung tâm", "ESP32-S3-DevKitC-1 N16R8", "GPIO, I2C, SPI, UART", "Thu thập dữ liệu, chạy TinyML, điều phối toàn hệ thống"],
        ["2", "Khối cảm biến quán tính", "GY-521 (MPU6050 6-DoF)", "I2C0 (0x69) + INT", "Đo gia tốc 3 trục (ax,ay,az) và vận tốc góc 3 trục (gx,gy,gz)"],
        ["3", "Khối thời gian thực", "DS3231 RTC Module", "I2C0 (0x68)", "Cung cấp thời gian thực chính xác bù nhiệt, tem dữ liệu hộp đen"],
        ["4", "Khối định vị GPS", "NEO-M8N GNSS Module", "UART1 + PPS", "Xác định tọa độ địa lý, độ cao, vận tốc thực và đồng bộ thời gian"],
        ["5", "Khối lưu trữ cục bộ", "MicroSD Card SPI Module", "SPI Bus", "Ghi dữ liệu đệm sự cố và nhật ký hành trình an toàn, chống mất mát"],
        ["6", "Khối truyền thông 4G", "MKE-M21 (SIM7680C 4G Cat-1)", "UART2 + PWRKEY + STATUS", "Phát tin nhắn SMS khẩn cấp và truyền telemetry lên IoT Server"],
        ["7", "Khối hiển thị", "OLED 0.96 inch SSD1306", "I2C0 (0x3C)", "Hiển thị trạng thái hệ thống, vận tốc, vệ tinh, sóng 4G và đếm ngược"],
        ["8", "Khối cảnh báo", "Piezo Buzzer 5V + LED Status", "GPIO15 (Driver NPN), GPIO7", "Phát âm thanh còi hú báo động tại chỗ và đèn chớp định kỳ/khẩn cấp"],
        ["9", "Khối nút nhấn", "Nút nhấn cơ khí + Mạch lọc RC", "GPIO6 (Ngắt ngoài)", "Cho phép người lái bấm hủy báo động giả trong vòng 15 giây"],
        ["10", "Khối nguồn", "Pin 18650, USB-C, Cầu phân áp", "VBAT, VBUS, 5V_SYS, 3V3_SYS", "Cung cấp năng lượng liên tục, sạc pin và đo điện áp pin qua ADC1"]
    ]
    add_table_with_caption(doc, "Bảng 3.1: Tổng hợp chức năng, linh kiện lựa chọn và giao thức kết nối của các khối",
                           tbl1_headers, tbl1_data, col_widths=[0.6, 1.6, 1.8, 1.4, 2.2])

    # 3.1.3 Hoạt động của hệ thống
    add_h3(doc, "3.1.3 Hoạt động của hệ thống")
    
    add_p(doc, 
          "Quá trình vận hành của hệ thống hộp đen AIoT thông minh trên xe máy điện được thiết kế theo một chu trình khép kín, "
          "phân chia thành các giai đoạn rõ ràng nhằm đảm bảo tính toàn vẹn dữ liệu, phản ứng tức thời với tai nạn và tối ưu hóa "
          "năng lượng tiêu thụ. Luồng hoạt động chính của hệ thống diễn ra tuần tự qua các bước sau:")
          
    add_p(doc, "", bold_prefix="Bước 1: Khởi động và tự kiểm tra phần cứng (Power-On Self-Test - POST):")
    add_p(doc, 
          "Khi người dùng bật khóa xe hoặc hệ thống được cấp nguồn từ pin 18650, vi điều khiển ESP32-S3 khởi động, thiết lập cấu hình "
          "các chân GPIO đóng băng theo thiết kế. Hệ thống khởi tạo bus I2C ở tốc độ 400 kHz, bus SPI ở tốc độ 20 MHz và hai cổng UART "
          "phần cứng. ESP32-S3 tiến hành kiểm tra sự hiện diện của MPU6050 (đọc thanh ghi WHO_AM_I = 0x68), nạp hệ số bù sai số (Offset), "
          "đọc thời gian từ DS3231, khởi tạo thẻ nhớ MicroSD (kiểm tra định dạng FAT32), bật nguồn module SIM7680C qua chân PWRKEY "
          "và lắng nghe dữ liệu NMEA từ module NEO-M8N. Kết quả kiểm tra phần cứng được cập nhật trực quan lên màn hình OLED. "
          "Đèn LED STATUS nháy sáng báo hiệu hệ thống đã sẵn sàng làm việc.")
          
    add_p(doc, "", bold_prefix="Bước 2: Chu trình giám sát bình thường (Normal Monitoring Loop):")
    add_p(doc, 
          "Trong trạng thái xe di chuyển bình thường trên đường, hệ thống vận hành theo cơ chế đa tác vụ (Multitasking) thời gian thực:")
    add_bullet(doc, "Thu thập dữ liệu quán tính: ", 
               "Ngắt timer định kỳ kích hoạt đọc dữ liệu gia tốc (ax, ay, az) và vận tốc góc (gx, gy, gz) từ MPU6050 ở tần số 100 Hz (chu kỳ 10 ms).")
    add_bullet(doc, "Thu thập dữ liệu định vị: ", 
               "Cổng UART1 tiếp nhận và bóc tách các câu bản tin NMEA ($GNRMC, $GNGGA) từ NEO-M8N ở tần số 10 Hz để lấy tọa độ, tốc độ và hướng di chuyển.")
    add_bullet(doc, "Cập nhật thời gian và điện áp: ", 
               "Mỗi 1 giây, hệ thống đọc lại tem thời gian từ DS3231 và đo điện áp pin qua chân ADC_VBAT_SENSE (GPIO1).")
    add_bullet(doc, "Ghi đệm vòng FIFO liên tục trong PSRAM: ", 
               "Mỗi gói dữ liệu bao gồm [Timestamp, ax, ay, az, gx, gy, gz, Latitude, Longitude, Speed, VBAT] được đẩy vào một hàng đợi "
               "vòng tròn (Circular Buffer) dung lượng 30 giây được phân bổ trên bộ nhớ ngoài 8 MB PSRAM. Khi bộ đệm đầy, các mẫu dữ liệu "
               "cũ nhất sẽ tự động bị ghi đè bởi mẫu dữ liệu mới nhất.")
    add_bullet(doc, "Cập nhật hiển thị: ", 
               "Màn hình OLED làm mới thông số xe (tốc độ km/h, số lượng vệ tinh bắt được, dung lượng pin còn lại) với chu kỳ 500 ms.")

    add_p(doc, "", bold_prefix="Bước 3: Phân tích sự cố tại biên (Edge Incident Analysis):")
    add_p(doc, 
          "Mỗi cửa sổ dữ liệu IMU trượt (Sliding Window kích thước 100 mẫu = 1 giây) được đưa vào mô hình học máy biên TinyML "
          "kết hợp các điều kiện lọc ngưỡng thích nghi. Thuật toán liên tục tính toán độ lớn gia tốc tổng hợp SVM (Signal Vector Magnitude), "
          "góc nghiêng thân xe (Roll/Pitch) qua bộ lọc bù Complementary Filter và độ biến thiên vận tốc góc. Nếu các giá trị tính toán "
          "vẫn nằm trong giới hạn động học cho phép của xe máy hai bánh, hệ thống đánh giá xe ở trạng thái C0 (Bình thường) hoặc C4 "
          "(Rung chấn mặt đường) và duy trì chu trình giám sát.")

    add_p(doc, "", bold_prefix="Bước 4: Nhận diện sự cố và kích hoạt cảnh báo tại chỗ (Incident Trigger):")
    add_p(doc, 
          "Khi thuật toán phát hiện các dấu hiệu tai nạn nghiêm trọng (C1: Va chạm trực diện/đuôi với gia tốc va đập đột biến vượt ngưỡng "
          "G-force; C2: Xe bị ngã nghiêng một góc vượt quá 65 độ và nằm im trên mặt đường; C3: Xe bị trượt rê văng xa với vận tốc góc lớn), "
          "hệ thống lập tức chuyển sang chế độ Khẩn cấp (Emergency Pre-Alert Mode):")
    add_bullet(doc, "Khóa bộ đệm vòng: ", 
               "Lập tức đánh dấu thời điểm xảy ra sự cố t0, bảo toàn dữ liệu 15 giây trước va chạm và tiếp tục thu thập thêm 15 giây dữ liệu "
               "ngay sau va chạm để hình thành tệp sự cố hộp đen trọn vẹn 30 giây.")
    add_bullet(doc, "Cảnh báo âm thanh và ánh sáng: ", 
               "Vi điều khiển phát tín hiệu mức cao ra chân GPIO15 để kích hoạt còi Piezo kêu dồn dập (tần số ngắt quãng 2 Hz, âm lượng > 85 dB), "
               "đồng thời nhấp nháy đèn LED STATUS ở tần số cao nhằm gây sự chú ý mạnh mẽ.")
    add_bullet(doc, "Hiển thị đếm ngược trên OLED: ", 
               "Màn hình OLED chuyển sang giao diện cảnh báo nguy hiểm với dòng chữ: 'CANH BAO VA CHAM! NHAN CANCEL TRONG 15s' kèm đồng hồ đếm lùi trực quan.")

    add_p(doc, "", bold_prefix="Bước 5: Xử lý tương tác người dùng và phân nhánh quyết định:")
    add_p(doc, 
          "Trong khoảng thời gian cửa sổ đếm ngược 15 giây, hệ thống liên tục quét trạng thái chân nút nhấn CANCEL (GPIO6):")
    add_bullet(doc, "Trường hợp A (Người lái nhấn CANCEL trong vòng 15 giây): ", 
               "Hệ thống xác định đây là sự cố nhẹ, người điều khiển vẫn hoàn toàn tỉnh táo và tự chủ được tình huống hoặc chỉ là va chạm "
               "ngoài ý muốn không cần cứu hộ y tế. ESP32-S3 lập tức tắt còi báo động, tắt đèn chớp, hiển thị thông báo 'DA HUY CANH BAO', "
               "ghi một bản ghi nhật ký sự kiện 'Incident Cancelled by User' vào thẻ nhớ MicroSD và đưa hệ thống quay trở lại chu trình giám sát bình thường.")
    add_bullet(doc, "Trường hợp B (Hết 15 giây không có thao tác nhấn CANCEL): ", 
               "Hệ thống xác nhận tai nạn là cực kỳ nghiêm trọng, người lái xe có nguy cơ đã bất tỉnh hoặc gặp chấn thương nặng không thể thao tác. "
               "Thiết bị lập tức thực thi chuỗi hành động cứu hộ khẩn cấp:")
    add_bullet(doc, "  • Đóng băng và ghi thẻ nhớ: ", 
               "Toàn bộ 30 giây dữ liệu hộp đen (3000 mẫu IMU, 300 mẫu GPS) được trích xuất từ PSRAM, đóng gói thành tệp tin nhị phân chuẩn "
               "trên thẻ MicroSD, tạo mã băm mật mã SHA-256 gắn vào cuối tệp tin để bảo vệ tính toàn vẹn chứng cứ số.")
    add_bullet(doc, "  • Phát tin nhắn SMS khẩn cấp: ", 
               "ESP32-S3 gửi tập lệnh AT qua UART2 điều khiển module SIM7680C phát tin nhắn SMS cứu nạn tự động đến các số điện thoại người thân "
               "và cơ quan y tế đã cấu hình trước. Nội dung SMS bao gồm: Thời gian tai nạn, Loại sự cố, Vận tốc va chạm và một đường dẫn Google Maps "
               "trực tiếp (dạng: https://maps.google.com/?q=<Latitude>,<Longitude>) giúp lực lượng cứu hộ dễ dàng bấm mở chỉ đường tức thì.")
    add_bullet(doc, "  • Truyền dữ liệu lên Cloud Server: ", 
               "Module 4G kích hoạt kết nối dữ liệu mạng không dây, gửi gói tin telemetry định dạng JSON lên máy chủ IoT qua giao thức MQTT/HTTP "
               "để lưu trữ vào cơ sở dữ liệu và hiển thị lên bản đồ giám sát giao thông trực tuyến.")
    add_bullet(doc, "  • Duy trì báo động tại hiện trường: ", 
               "Còi Piezo tiếp tục phát tín hiệu ngắt quãng và cập nhật định vị định kỳ cho đến khi có sự can thiệp trực tiếp của nhân viên cứu nạn.")
               
    print("Section 3.1 built successfully.")
