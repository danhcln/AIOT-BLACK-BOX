# -*- coding: utf-8 -*-
"""
Module ch3_sec32_p3.py: Section 3.2 Part 3 generator.
Covers:
- 3.2.7 Khối hiển thị (OLED 0.96 inch, comparisons, specs table, schematic crop)
- 3.2.8 Khối cảnh báo (Piezo Buzzer + LED Status, comparisons, schematic crop)
- 3.2.9 Khối nút nhấn (CANCEL button + RC filter, comparisons, schematic crop)
- 3.2.10 Khối nguồn (New Power Architecture: VBAT 18650 primary, USB-C VBUS charging, 5V_SYS & 3V3_SYS separate rails, ESP32 as load, ADC_VBAT_SENSE divider, schematic crop)
- 3.2.11 Sơ đồ nguyên lý toàn hệ thống (REV8 Full schematic integration analysis)
"""

import os
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from build_chapter3_full import (
    add_p, add_bullet, add_h3, add_figure, add_table_with_caption
)

def add_section_3_2_part3(doc, assets_dir):
    # =========================================================================
    # 3.2.7 Khối hiển thị
    # =========================================================================
    add_h3(doc, "3.2.7 Khối hiển thị")
    
    add_p(doc, 
          "Khối hiển thị đóng vai trò là giao diện tương tác trực quan (Human-Machine Interface - HMI) tại chỗ của hộp đen, "
          "giúp người sử dụng xe máy điện theo dõi tức thời trạng thái làm việc của toàn bộ hệ thống. Trong quá trình vận hành bình thường, "
          "màn hình hiển thị các thông số quan trọng bao gồm: tốc độ di chuyển thực tế (km/h), số lượng vệ tinh GPS kết nối, tình trạng "
          "sóng 4G LTE, mức điện áp pin còn lại và trạng thái thẻ nhớ. Đặc biệt, khi phát hiện sự cố va chạm, màn hình đóng vai trò thông báo "
          "khẩn cấp và trực quan hóa đồng hồ đếm ngược 15 giây cho phép người lái biết rõ thời gian còn lại để bấm hủy. "
          "Các phương án màn hình hiển thị được khảo sát gồm:")
          
    add_p(doc, "", bold_prefix="Phương án 1: Sử dụng màn hình OLED 0.96 inch SSD1306 giao tiếp I2C (Được chọn):")
    add_p(doc, 
          "Màn hình OLED 0.96 inch đơn sắc sử dụng chip điều khiển SSD1306, độ phân giải 128x64 điểm ảnh, giao tiếp qua bus I2C.")
    add_bullet(doc, "Ưu điểm: ", 
               "Công nghệ phát quang hữu cơ tự thân (OLED) mang lại độ tương phản cực kỳ sắc nét, góc nhìn rộng vượt trội (> 160 độ), "
               "cho phép người lái quan sát rõ ràng nội dung ngay cả dưới ánh nắng gắt ban ngày hay trong đêm tối; tiêu thụ năng lượng "
               "cực thấp (trung bình chỉ khoảng 15 mA, các pixel màu đen tắt hoàn toàn giúp tiết kiệm năng lượng pin); độ phân giải đồ họa "
               "128x64 điểm ảnh cho phép vẽ thanh đếm ngược (Progress Bar) và các biểu tượng trực quan; kích thước siêu nhỏ gọn (27x27 mm) "
               "rất dễ lắp đặt lên mặt đồng hồ hoặc ghi-đông xe máy; DÙNG CHUNG BUS I2C0 (chân GPIO8, GPIO9) với MPU6050 và DS3231 "
               "mà không tốn thêm bất kỳ chân GPIO nào của vi điều khiển.")
    add_bullet(doc, "Nhược điểm: ", 
               "Kích thước hiển thị 0.96 inch nhỏ gọn nên chỉ phù hợp bố trí các thông tin xúc tích, cô đọng.")

    add_p(doc, "", bold_prefix="Phương án 2: Sử dụng màn hình ký tự LCD 16x2 giao tiếp I2C:")
    add_p(doc, 
          "Màn hình tinh thể lỏng truyền thống hiển thị 2 dòng, mỗi dòng 16 ký tự chữ số, tích hợp mạch chuyển đổi I2C PCF8574.")
    add_bullet(doc, "Ưu điểm: ", 
               "Giá thành rất rẻ, dễ lập trình ký tự chữ cơ bản.")
    add_bullet(doc, "Nhược điểm: ", 
               "Kích thước rất cồng kềnh (khoảng 80x36 mm), rất khó bố trí thẩm mỹ trên ghi-đông xe máy; chỉ hiển thị được ký tự ASCII thô, "
               "hoàn toàn không vẽ được đồ họa, icon vệ tinh, vạch pin hay thanh tiến trình đếm ngược; góc nhìn rất hẹp, độ tương phản kém, "
               "bị lóa và rất khó đọc khi xe di chuyển dưới ánh sáng mặt trời ngoài trời; đèn nền tiêu thụ dòng liên tục khá lớn (~30-50 mA).")

    add_p(doc, "", bold_prefix="Phương án 3: Sử dụng màn hình màu TFT LCD 2.4 inch SPI (IL9341):")
    add_p(doc, 
          "Màn hình màu TFT kích thước lớn 2.4 inch, độ phân giải 320x240 điểm ảnh, giao tiếp qua chuẩn SPI.")
    add_bullet(doc, "Ưu điểm: ", 
               "Hiển thị màu sắc sống động, kích thước màn hình lớn, giao diện bắt mắt.")
    add_bullet(doc, "Nhược điểm: ", 
               "Tiêu thụ dòng điện rất lớn (đèn nền ăn dòng từ 80 mA đến 150 mA liên tục), làm cạn kiệt nhanh chóng pin dự phòng của hộp đen; "
               "chiếm dụng thêm 4 đến 5 chân GPIO tốc độ cao trên vi điều khiển cho giao tiếp SPI; kích thước lớn khó chế tạo vỏ bảo vệ chống nước cho xe máy.")

    add_p(doc, 
          "Các chỉ tiêu đối sánh kỹ thuật giữa 3 phương án màn hình hiển thị được tổng hợp trong Bảng 3.15:")
          
    # Bảng 3.15
    tbl15_headers = ["Tiêu chí kỹ thuật", "OLED 0.96 inch I2C [Được chọn]", "LCD 16x2 I2C", "TFT LCD 2.4 inch SPI"]
    tbl15_data = [
        ["Công nghệ hiển thị", "OLED phát quang hữu cơ tự thân", "Tinh thể lỏng LCD phản xạ + Đèn nền", "Màn hình màu TFT LCD"],
        ["Độ phân giải", "128x64 Điểm ảnh đồ họa", "16 Cột x 2 Dòng ký tự chữ", "320x240 Điểm ảnh màu"],
        ["Khả năng quan sát ngoài trời", "Rất tốt (Độ tương phản cực cao)", "Kém (Bị lóa dưới ánh nắng gắt)", "Trung bình (Cần tăng sáng đèn nền)"],
        ["Góc nhìn hiển thị", "Rộng xuất sắc (> 160 độ)", "Hẹp (Chỉ nhìn rõ góc thẳng)", "Khá (~120 độ)"],
        ["Mức tiêu thụ dòng điện", "Rất thấp (~10 - 15 mA)", "Trung bình (~35 - 50 mA)", "Rất cao (~90 - 150 mA)"],
        ["Giao diện truyền thông", "I2C (Dùng chung bus I2C0)", "I2C (Bus I2C0)", "SPI (Tốn thêm 4-5 chân GPIO)"],
        ["Kích thước vật lý", "Rất nhỏ gọn (27 x 27 mm)", "Cồng kềnh (80 x 36 mm)", "Lớn (75 x 50 mm)"],
        ["Khả năng vẽ thanh đếm ngược", "Rất linh hoạt, vẽ thanh tiến trình", "Không hỗ trợ (Chỉ đếm số thô)", "Rất đẹp nhưng tốn tài nguyên"],
        ["Mức độ phù hợp xe máy", "Tối ưu và thẩm mỹ nhất", "Thô kệch, không phù hợp xe", "Tiêu tốn năng lượng quá mức"]
    ]
    add_table_with_caption(doc, "Bảng 3.15: So sánh các phương án màn hình hiển thị trạng thái",
                           tbl15_headers, tbl15_data, col_widths=[1.8, 2.0, 1.8, 1.6])

    add_p(doc, "", bold_prefix="Phương án được lựa chọn: Màn hình OLED 0.96 inch SSD1306 I2C:")
    add_p(doc, 
          "Màn hình OLED 0.96 inch SSD1306 được lựa chọn chính thức nhờ sự vượt trội về độ tương phản, khả năng tiết kiệm năng lượng "
          "và khả năng dùng chung bus I2C giúp tiết kiệm chân vi điều khiển. Thông số kỹ thuật chi tiết của module OLED được thể hiện trong Bảng 3.16:")

    # Bảng 3.16
    tbl16_headers = ["Thông số kỹ thuật", "Giá trị thiết kế / Đặc tính kỹ thuật", "Ghi chú ứng dụng"]
    tbl16_data = [
        ["IC điều khiển hiển thị", "SSD1306 (Solomon Systech)", "Hỗ trợ bộ đệm khung hình đồ họa 128x64 bit"],
        ["Kích thước màn hình", "0.96 inch đường chéo (Vùng hiển thị 21.74 x 10.86 mm)", "Kích thước bo mạch module: 27 x 27 mm"],
        ["Độ phân giải hiển thị", "128 x 64 Pixels (Đơn sắc Trắng hoặc Xanh dương)", "Hiển thị chữ, thông số và đồ họa mượt mà"],
        ["Điện áp hoạt động", "3.3V DC (Cấp từ đường nguồn 3V3_SYS)", "Phù hợp trực tiếp mức logic của ESP32-S3"],
        ["Giao tiếp phần cứng", "I2C (Chân SDA, SCK)", "Sử dụng chung bus I2C0 với MPU6050 và DS3231"],
        ["Địa chỉ I2C của màn hình", "0x3C (Chuẩn nhà sản xuất)", "Không xung đột với 0x68 (DS3231) và 0x69 (MPU6050)"],
        ["Chân header vật lý", "GND, VDD, SCK, SDA (4 chân vật lý)", "Chân SCK trên module chính là chân xung I2C SCL"]
    ]
    add_table_with_caption(doc, "Bảng 3.16: Thông số kỹ thuật chi tiết của module OLED 0.96 inch I2C",
                           tbl16_headers, tbl16_data, col_widths=[2.0, 2.8, 2.4])

    add_p(doc, "", bold_prefix="Kết nối phần cứng trên sơ đồ nguyên lý REV8:")
    add_p(doc, 
          "Module OLED 0.96 inch trong thiết kế REV8 có 4 chân header vật lý được đấu nối trực tiếp vào hệ thống:")
    add_bullet(doc, "Chân VDD & GND: ", "Chân VDD nối vào đường nguồn logic 3V3_SYS, chân GND nối vào mặt phẳng mass chung.")
    add_bullet(doc, "Chân dữ liệu SDA: ", "Nối trực tiếp vào đường bus I2C0_SDA (chân GPIO8 của vi điều khiển ESP32-S3).")
    add_bullet(doc, "Chân xung nhịp SCK: ", 
               "Nối trực tiếp vào đường bus I2C0_SCL (chân GPIO9 của vi điều khiển ESP32-S3). Lưu ý: Trên bo mạch module OLED thương mại, "
               "chân xung nhịp I2C thường được in nhãn là 'SCK', tuy nhiên trong giao thức I2C đây chính là đường tín hiệu SCL.")

    add_p(doc, 
          "Sơ đồ nguyên lý khối hiển thị màn hình OLED 0.96 inch I2C trích xuất từ bản vẽ thiết kế REV8 được thể hiện trong Hình 3.8:")
          
    fig8_path = os.path.join(assets_dir, "H3_8_oled_block.png")
    add_figure(doc, fig8_path, "Hình 3.8: Sơ đồ nguyên lý khối hiển thị màn hình OLED 0.96 inch I2C", width_inches=3.8)

    # =========================================================================
    # 3.2.8 Khối cảnh báo
    # =========================================================================
    add_h3(doc, "3.2.8 Khối cảnh báo")
    
    add_p(doc, 
          "Khối cảnh báo có nhiệm vụ phát tín hiệu âm thanh và ánh sáng mạnh mẽ tại hiện trường tai nạn. Vai trò của khối này gồm hai mục tiêu: "
          "Thứ nhất, nhắc nhở người lái xe biết rằng hệ thống vừa ghi nhận một sự kiện va chạm và đang trong quá trình đếm ngược 15 giây "
          "(để người lái bấm nút hủy nếu còn tỉnh táo và không có nguy hiểm); Thứ hai, nếu hết 15 giây mà không có thao tác hủy, khối sẽ phát "
          "âm thanh báo động liên tục âm lượng lớn để thu hút sự chú ý của người đi đường xung quanh đến ứng cứu nạn nhân. "
          "Các phương án thiết kế mạch cảnh báo gồm:")
          
    add_p(doc, "", bold_prefix="Phương án 1: Còi báo Piezo 5V tích cực lái bằng Transistor NPN 2SC1815 + LED chỉ thị (Được chọn):")
    add_p(doc, 
          "Sử dụng còi báo gốm áp điện (Active Piezo Buzzer 5V) tích hợp sẵn mạch dao động nội bên trong, được đóng ngắt công suất thông qua "
          "transistor chuyển mạch NPN 2SC1815 kết hợp điện trở hạn dòng bazơ 1kΩ, đi kèm đèn LED báo trạng thái lái qua điện trở 330Ω.")
    add_bullet(doc, "Ưu điểm: ", 
               "Tạo ra âm thanh cảnh báo the thé có tần số cao đặc trưng (~2.3 kHz - 4 kHz), đây là dải tần tai người nhạy cảm nhất, "
               "đảm bảo xuyên qua tiếng ồn động cơ và giao thông đường phố; âm lượng lớn (> 85 dB tại khoảng cách 10 cm); mạch lái transistor "
               "2SC1815 cách ly tuyệt đối dòng tải của còi khỏi chân GPIO15 của ESP32-S3, bảo vệ vi điều khiển không bị quá tải dòng điện; "
               "còi Piezo có bản chất điện dung (Capacitive transducer), hoàn toàn không sinh ra sức điện động cảm ứng ngược (Back-EMF) "
               "như loa cuộn dây từ tính, do đó không đòi hỏi đi-ốt dập xung ngược phức tạp; độ bền cơ học cao, chống rung lắc xe máy; chi phí thấp.")
    add_bullet(doc, "Nhược điểm: ", "Âm thanh cố định một dải tần số đơn điệu.")

    add_p(doc, "", bold_prefix="Phương án 2: Sử dụng loa thụ động (Passive Speaker) điều khiển PWM:")
    add_p(doc, 
          "Sử dụng loa điện động nhỏ phát các nốt nhạc giai điệu thông qua xung PWM của vi điều khiển.")
    add_bullet(doc, "Ưu điểm: ", "Có thể phát nhiều âm sắc và giai điệu nhạc khác nhau.")
    add_bullet(doc, "Nhược điểm: ", 
               "Âm lượng rất nhỏ trong không gian đường phố ồn ào; màng loa mỏng dễ bị rách, ngấm nước khi đi mưa; cuộn dây loa từ tính "
               "sinh xung cảm ứng lớn đòi hỏi mạch bảo vệ phức tạp; tiêu tốn liên tục tài nguyên bộ định thời (Timer PWM) của CPU.")

    add_p(doc, "", bold_prefix="Phương án 3: Sử dụng module phát âm thanh giọng nói (DFPlayer Mini / MP3):")
    add_p(doc, 
          "Sử dụng module giải mã âm thanh số MP3 phát các câu cảnh báo bằng giọng nói (ví dụ: 'Cảnh báo va chạm, xin hãy giúp đỡ!').")
    add_bullet(doc, "Ưu điểm: ", "Nội dung cảnh báo rõ ràng bằng ngôn ngữ con người.")
    add_bullet(doc, "Nhược điểm: ", 
               "Mạch cồng kềnh, cần thẻ nhớ micro riêng cho module MP3; độ trễ phát âm thanh lớn (phải đợi khởi động giải mã file MP3); "
               "công suất phát loa nhỏ không nghe rõ ngoài đường; tiêu thụ dòng điện lớn; mạch dễ lỗi khi xảy ra chấn động cơ học mạnh.")

    add_p(doc, 
          "Đối sánh giữa các giải pháp mạch cảnh báo tại chỗ được trình bày trong Bảng 3.17:")
          
    # Bảng 3.17
    tbl17_headers = ["Tiêu chí kỹ thuật", "Còi Piezo 5V + Transistor 2SC1815 [Được chọn]", "Loa thụ động PWM", "Module phát âm thanh MP3"]
    tbl17_data = [
        ["Cường độ âm thanh (dB)", "Rất lớn (> 85 dB tại 10 cm, xuyên ồn)", "Nhỏ (< 70 dB, dễ bị át tiếng)", "Trung bình (~75 dB)"],
        ["Đặc tính âm thanh", "Tần số cao đanh thép (2.3 - 4 kHz)", "Âm sắc đa dạng theo xung PWM", "Giọng nói tiếng Việt phát từ file MP3"],
        ["Mức độ gây chú ý tai nạn", "Cực kỳ hiệu quả ngay tức thì", "Kém hiệu quả khi đi đường phố", "Khá nhưng độ trễ cao"],
        ["Độ an toàn cho vi điều khiển", "Cách ly tuyệt đối qua NPN 2SC1815", "Dễ gây xung cảm ứng ngược", "Cách ly qua giao tiếp UART"],
        ["Độ bền rung xóc xe máy", "Rất cao (Không có màng rung cơ học)", "Dễ rách màng loa khi rung xóc", "Trung bình (Nhiều linh kiện rời)"],
        ["Tài nguyên vi điều khiển", "Chỉ cần 1 chân Digital IO xuất mức 0/1", "Phải chiếm dụng 1 kênh Hardware PWM", "Chiếm dụng 1 cổng UART nối tiếp"],
        ["Đánh giá mức độ phù hợp", "Tối ưu nhất cho cảnh báo cấp cứu", "Không đạt yêu cầu âm lượng", "Phức tạp hóa không cần thiết"]
    ]
    add_table_with_caption(doc, "Bảng 3.17: So sánh các phương án thiết kế khối cảnh báo tại chỗ",
                           tbl17_headers, tbl17_data, col_widths=[1.8, 2.0, 1.8, 1.6])

    add_p(doc, "", bold_prefix="Phương án được lựa chọn và tính toán kết nối phần cứng:")
    add_p(doc, 
          "Mạch cảnh báo kết hợp Còi Piezo 5V tích cực lái bằng transistor NPN 2SC1815 và đèn LED trạng thái được chọn chính thức. "
          "Thiết kế mạch chi tiết như sau:")
    add_bullet(doc, "Mạch điều khiển còi Buzzer (BUZZER_CTRL - GPIO15): ", 
               "Tín hiệu điều khiển từ chân GPIO15 của ESP32-S3 đi qua điện trở bazơ R_B = 1kΩ nối vào cực Bazơ (B) của transistor NPN 2SC1815. "
               "Cực Phát (Emitter - E) của transistor nối trực tiếp xuống mass (GND). Cực Thu (Collector - C) nối vào cực âm (-) của còi Piezo. "
               "Cực dương (+) của còi Piezo được nối lên đường nguồn công suất 5V_SYS. Khi GPIO15 xuất mức cao (3.3V), dòng bazơ I_B đạt xấp xỉ "
               "(3.3V - 0.7V) / 1kΩ = 2.6 mA, đưa transistor 2SC1815 vào trạng thái bão hòa hoàn toàn (Saturation Mode, V_CE_sat < 0.2V), "
               "cấp trọn vẹn điện áp xấp xỉ 4.8V cho còi Piezo phát âm thanh cực đại. Khi GPIO15 ở mức thấp (0V), transistor khóa hoàn toàn, còi tắt.")
    add_bullet(doc, "Mạch đèn LED chỉ thị trạng thái (LED_STATUS - GPIO7): ", 
               "Chân GPIO7 nối tiếp qua điện trở hạn dòng R_LED = 330Ω vào cực Anot của đèn LED màu, cực Catot nối xuống GND. "
               "Dòng định mức qua LED đạt khoảng (3.3V - 2.0V) / 330Ω ≈ 4 mA, đảm bảo LED phát sáng rõ nét nhưng hoàn toàn an toàn cho chân IO của vi điều khiển.")

    add_p(doc, 
          "Sơ đồ nguyên lý khối cảnh báo còi Piezo 5V và LED chỉ thị trích xuất từ bản vẽ thiết kế REV8 được thể hiện trong Hình 3.9:")
          
    fig9_path = os.path.join(assets_dir, "H3_9_warning_block.png")
    add_figure(doc, fig9_path, "Hình 3.9: Sơ đồ nguyên lý khối cảnh báo còi Piezo 5V và LED chỉ thị", width_inches=4.2)

    # =========================================================================
    # 3.2.9 Khối nút nhấn
    # =========================================================================
    add_h3(doc, "3.2.9 Khối nút nhấn")
    
    add_p(doc, 
          "Khối nút nhấn giữ vai trò là kênh phản hồi trực tiếp của người điều khiển xe (Human Feedback Interface). Trong điều kiện di chuyển "
          "thực tế tại Việt Nam, xe máy điện có thể gặp phải các tình huống va quẹt nhẹ, xe bị đổ khi đang dắt ở bãi đỗ hoặc sụp ổ gà sâu "
          "khiến gia tốc tăng vọt làm kích hoạt cảnh báo sự cố. Khi đó, nút nhấn CANCEL cho phép người lái chủ động bấm xác nhận tình trạng "
          "bản thân vẫn an toàn, lập tức hủy chu trình đếm ngược, ngăn chặn việc thiết bị tự động gửi tin nhắn cấp cứu giả (False Alarm) "
          "làm hoang mang người thân và lãng phí nguồn lực cứu hộ. Các phương án thiết kế nút nhấn gồm:")
          
    add_p(doc, "", bold_prefix="Phương án 1: Nút nhấn cơ khí tích hợp mạch lọc RC phần cứng chống dội phím (Được chọn):")
    add_p(doc, 
          "Sử dụng nút nhấn hành trình cơ khí (Tactile Pushbutton) loại thường mở (Normally Open), được trang bị điện trở kéo lên ngoài 10kΩ "
          "nối lên 3V3_SYS và tụ gốm dập nhiễu 100nF mắc song song xuống GND.")
    add_bullet(doc, "Ưu điểm: ", 
               "Phản hồi xúc giác (Tactile Click) rõ ràng, giúp người lái xe cảm nhận dứt khoát thao tác bấm ngay cả khi đang đeo găng tay bảo hộ xe máy; "
               "mạch lọc RC phần cứng (R = 10kΩ, C = 100nF) tạo ra hằng số thời gian τ = R × C = 10kΩ × 100nF = 1.0 ms, dập tắt triệt để các xung gai "
               "nhiễu điện áp và hiện tượng rung cơ học (Contact Bouncing) ngay tại tầng vật lý trước khi tín hiệu đi vào chân vi điều khiển; "
               "độ tin cậy cơ học cao, kháng nhiễu tĩnh điện vượt trội.")
    add_bullet(doc, "Nhược điểm: ", "Cần thêm 2 linh kiện thụ động (trở 10k và tụ 100nF) trên bo mạch.")

    add_p(doc, "", bold_prefix="Phương án 2: Sử dụng nút bấm cảm ứng điện dung (Capacitive Touch):")
    add_p(doc, 
          "Sử dụng phím cảm ứng điện dung không có tiếp điểm chuyển động cơ khí.")
    add_bullet(doc, "Ưu điểm: ", "Hình thức hiện đại, bề mặt phẳng dễ làm kín chống nước.")
    add_bullet(doc, "Nhược điểm: ", 
               "Rất kém tin cậy trên xe máy điện; khi người lái đeo găng tay da hoặc khi trời mưa nước bám trên bề mặt cảm ứng, phím bấm sẽ bị liệt "
               "hoặc kích hoạt chạm giả liên tục; hoàn toàn không có cảm giác bấm vật lý trong lúc người lái đang bối rối sau va chạm.")

    add_p(doc, "", bold_prefix="Phương án 3: Nút nhấn thả nổi, lọc chống dội hoàn toàn bằng phần mềm:")
    add_p(doc, 
          "Chỉ sử dụng nút nhấn nối thẳng vào chân IO và sử dụng trở kéo nội (Internal Pull-up) của vi điều khiển, lọc dội bằng code trễ.")
    add_bullet(doc, "Ưu điểm: ", "Tiết kiệm linh kiện ngoài.")
    add_bullet(doc, "Nhược điểm: ", 
               "Trở kéo nội của ESP32 có giá trị khá lớn (~45kΩ), rất nhạy cảm với xung nhiễu điện từ trường phát ra từ động cơ điện xe máy; "
               "dễ gây ra các ngắt giả (Spurious Interrupts) làm treo hoặc sai lệch logic của máy trạng thái khẩn cấp.")

    add_p(doc, 
          "Các giải pháp thiết kế nút nhấn được đối sánh kỹ thuật trong Bảng 3.18:")
          
    # Bảng 3.18
    tbl18_headers = ["Tiêu chí kỹ thuật", "Nút cơ khí + Mạch lọc RC [Được chọn]", "Phím cảm ứng điện dung", "Nút thường lọc bằng phần mềm"]
    tbl18_data = [
        ["Cảm giác phản hồi xúc giác", "Rõ ràng (Click cơ khí dứt khoát)", "Không có phản hồi lực", "Có phản hồi cơ học"],
        ["Khả năng bấm khi đeo găng tay", "Hoạt động hoàn hảo", "Bị liệt, không nhận diện được", "Hoạt động được"],
        ["Khả năng chống dội phím (Bounce)", "Triệt tiêu 100% bằng phần cứng lọc RC", "Không có dội phím", "Phải tốn thời gian trễ phần mềm"],
        ["Kháng nhiễu động cơ xe máy", "Rất cao (Nhờ tụ 100nF dập xung gai)", "Dễ bị kích hoạt giả do tĩnh điện", "Dễ bắt nhiễu do trở kéo nội lớn"],
        ["Độ ổn định khi trời mưa ướt", "Hoàn toàn ổn định", "Dễ bị chạm liên tục do giọt nước", "Ổn định"],
        ["Mức độ phù hợp xe máy điện", "Tối ưu và tin cậy tuyệt đối", "Kém tin cậy trong môi trường xe", "Dễ phát sinh ngắt giả"]
    ]
    add_table_with_caption(doc, "Bảng 3.18: So sánh các phương án thiết kế nút nhấn CANCEL / Khẩn cấp",
                           tbl18_headers, tbl18_data, col_widths=[1.8, 2.0, 1.8, 1.6])

    add_p(doc, "", bold_prefix="Phương án được lựa chọn và kết nối phần cứng:")
    add_p(doc, 
          "Phương án nút nhấn cơ khí có mạch lọc RC phần cứng được chọn chính thức. Trên sơ đồ nguyên lý bản vẽ REV8, kết nối phần cứng "
          "được thiết kế chuẩn mực như sau:")
    add_bullet(doc, "Đường tín hiệu CANCEL: ", "Nối trực tiếp vào chân GPIO6 của vi điều khiển ESP32-S3 (chân hỗ trợ ngắt cạnh xuống Falling Edge).")
    add_bullet(doc, "Điện trở kéo lên (R_PULL = 10kΩ): ", "Nối từ chân CANCEL lên đường nguồn logic 3V3_SYS, đảm bảo khi không bấm nút, chân GPIO6 luôn ở mức cao (3.3V) ổn định.")
    add_bullet(doc, "Tụ điện dập nhiễu (C_FILTER = 100nF): ", "Nối song song từ chân CANCEL xuống mass (GND), tạo mạch tích phân RC hấp thụ toàn bộ xung nhiễu quá độ.")
    add_bullet(doc, "Tiếp điểm nút bấm SW1: ", "Một đầu nối vào chân CANCEL, đầu còn lại nối trực tiếp xuống mass (GND). Khi người dùng nhấn nút, đường tín hiệu được kéo thẳng xuống 0V dứt khoát.")

    add_p(doc, 
          "Sơ đồ nguyên lý khối nút nhấn CANCEL / xác nhận sự cố trích xuất từ bản vẽ thiết kế REV8 được thể hiện trong Hình 3.10:")
          
    fig10_path = os.path.join(assets_dir, "H3_10_cancel_button_block.png")
    add_figure(doc, fig10_path, "Hình 3.10: Sơ đồ nguyên lý khối nút nhấn CANCEL / xác nhận sự cố", width_inches=3.5)

    # =========================================================================
    # 3.2.10 Khối nguồn
    # =========================================================================
    add_h3(doc, "3.2.10 Khối nguồn")
    
    add_p(doc, 
          "Khối nguồn đóng vai trò huyết mạch sống còn, quyết định tính ổn định liên tục và khả năng sống sót của thiết bị hộp đen "
          "khi phương tiện gặp sự cố. Trong các vụ tai nạn giao thông xe máy điện, hệ thống điện chính của xe (khối pin lực 48V-72V) thường bị "
          "bảo vệ ngắt cầu dao tự động (BMS Trip) hoặc đường dây điện bị đứt gãy do va đập biến dạng. Nếu hộp đen phụ thuộc trực tiếp vào "
          "nguồn điện xe, thiết bị sẽ lập tức mất điện ngay lúc va chạm, dẫn đến không thể ghi dữ liệu và không thể gửi tin nhắn cứu hộ. "
          "Do đó, kiến trúc nguồn của hệ thống được xây dựng dựa trên các nguyên lý an toàn độc lập sau:")
          
    add_p(doc, "", bold_prefix="Kiến trúc nguồn điện được phê duyệt chính thức (Approved System Power Architecture):")
    add_bullet(doc, "NGUỒN NĂNG LƯỢNG VẬN HÀNH CHÍNH (PRIMARY OPERATING POWER SOURCE): ", 
               "Là khối Pin Li-ion 18650 tích hợp bên trong hộp đen (đường nguồn ký hiệu VBAT, điện áp danh định 3.7V, khi nạp đầy đạt 4.2V, "
               "ngưỡng ngắt an toàn 3.0V). Pin Li-ion 18650 cung cấp năng lượng liên tục và hoàn toàn độc lập cho toàn bộ bo mạch, "
               "đảm bảo hệ thống duy trì hoạt động bình thường ngay cả khi ắc quy chính của xe máy điện bị ngắt hoặc phá hủy.")
    add_bullet(doc, "NGUỒN SẠC NGOÀI / ĐẦU VÀO NGOẠI VI (EXTERNAL INPUT / CHARGING SOURCE): ", 
               "Là cổng kết nối tiêu chuẩn công nghiệp USB-C (đường nguồn ký hiệu VBUS, điện áp danh định 5V). Cổng USB-C đóng vai trò "
               "duy nhất là nguồn cấp điện bên ngoài để sạc lại cho pin Li-ion 18650 thông qua mạch quản lý sạc, KHÔNG PHẢI là nguồn năng lượng "
               "vận hành trực tiếp chính của hệ thống.")
    add_bullet(doc, "DÒNG CHẢY NĂNG LƯỢNG CHUẨN CỦA HỆ THỐNG: ", 
               "USB-C / VBUS (Nguồn sạc ngoài 5V) → MẠCH QUẢN LÝ SẠC VÀ BẢO VỆ PIN → PIN 18650 / VBAT (Nguồn vận hành chính) → "
               "MẠCH BIẾN ĐỔI VÀ PHÂN PHỐI NGUỒN HỆ THỐNG → CÁC ĐƯỜNG NGUỒN RIÊNG BIỆT (5V_SYS & 3V3_SYS).")

    add_p(doc, "", bold_prefix="Nguyên tắc phân tách các miền nguồn hệ thống (Separate System Power Rails):")
    add_p(doc, 
          "Để đảm bảo an toàn điện và độ ổn định cao nhất, hệ thống phân định rõ ràng các miền nguồn độc lập:")
    add_bullet(doc, "Đường nguồn 5V_SYS: ", 
               "Đường nguồn 5V của hệ thống, cấp nguồn cho đầu vào VIN của bo mạch vi điều khiển ESP32-S3-DevKitC-1 và mạch còi cảnh báo Piezo 5V. "
               "Tên miền mạng chính thức của dự án là 5V_SYS (tuyệt đối không gộp chung với VBUS và không đổi tên thành +5V).")
    add_bullet(doc, "Đường nguồn 3V3_SYS: ", 
               "Đường nguồn điện áp thấp 3.3V chuyên dụng cấp cho toàn bộ các cảm biến và mạch logic ngoại vi (MPU6050, DS3231, OLED, MicroSD).")
    add_bullet(doc, "Đường mass chung (GND): ", "Mặt phẳng hồi tiếp điện áp chung toàn hệ thống.")

    add_p(doc, "", bold_prefix="Luận chứng khoa học: Tuyệt đối không lấy nguồn từ chân 3V3 của ESP32 DevKit nuôi ngoại vi:")
    add_p(doc, 
          "Trong nhiều thiết kế nghiệp dư, người thiết kế thường lấy chân 3.3V từ bo mạch vi điều khiển để cấp nguồn cho tất cả cảm biến và module. "
          "Đối với thiết bị hộp đen AIoT, ĐÂY LÀ MỘT SAI LẦM KỸ THUẬT NGHIÊM TRỌNG vì các lý do khoa học sau:")
    add_bullet(doc, "Giới hạn tản nhiệt của IC ổn áp LDO onboard: ", 
               "IC ổn áp 3.3V (thường là dòng AMS1117-3.3 hoặc SGM2211) tích hợp trên bo ESP32 DevKit có diện tích đồng tản nhiệt cực nhỏ. "
               "Bản thân chip ESP32-S3 lõi kép khi chạy ở 240 MHz kèm PSRAM đã tiêu thụ dòng điện xấp xỉ 100 - 150 mA.")
    add_bullet(doc, "Hiện tượng sụt áp Brownout Reset: ", 
               "Khi module thẻ nhớ MicroSD thực hiện ghi ngẫu nhiên từng khối hoặc module 4G phát sóng, các xung dòng đỉnh ngắn hạn (Peak Currents) "
               "có thể vượt quá khả năng đáp ứng tức thời của LDO onboard trên bo DevKit. Hiện tượng này làm đường 3.3V bị sụt áp đột ngột xuống dưới 2.8V, "
               "kích hoạt mạch giám sát điện áp thấp Brownout Detector bên trong ESP32-S3, làm vi điều khiển bị Reset tức tưởi ngay thời điểm quan trọng nhất, "
               "gây mất mát dữ liệu sự cố hộp đen. Do đó, hệ thống bắt buộc phải thiết kế đường nguồn 3V3_SYS độc lập, coi ESP32-S3 và các module "
               "là CÁC TẢI TIÊU THỤ (LOADS) độc lập của hệ thống nguồn.")

    add_p(doc, "", bold_prefix="Mạch giám sát điện áp pin Li-ion 18650 (ADC_VBAT_SENSE):")
    add_p(doc, 
          "Để theo dõi dung lượng pin và cảnh báo pin yếu, hệ thống tích hợp mạch cầu phân áp chính xác kết nối từ cực dương pin VBAT "
          "về chân GPIO1 (ADC1_CH0) của ESP32-S3. Mạch bao gồm:")
    add_bullet(doc, "Cầu phân áp tỷ lệ 1:2: ", 
               "Gồm điện trở trên R_TOP = 100kΩ (sai số 1%) nối từ VBAT xuống nút ADC_VBAT_SENSE và điện trở dưới R_BOT = 100kΩ (sai số 1%) "
               "nối từ nút ADC_VBAT_SENSE xuống GND. Khi pin Li-ion ở điện áp đầy 4.2V, điện áp đưa vào chân GPIO1 là: "
               "V_ADC = VBAT × [R_BOT / (R_TOP + R_BOT)] = 4.2V × [100k / 200k] = 2.10V. Mức điện áp 2.10V này nằm hoàn toàn bên trong "
               "dải đo tuyến tính an toàn và chính xác của bộ biến đổi ADC ESP32-S3 (dải đo chuẩn 0V - 3.1V khi cấu hình suy hao 11dB).")
    add_bullet(doc, "Tụ gốm lọc nhiễu tần số cao (C_ADC = 100nF): ", 
               "Mắc song song với điện trở dưới R_BOT nối xuống GND. Tụ 100nF tạo thành bộ lọc thông thấp (Low-Pass Filter) có tần số cắt "
               "f_c = 1 / (2π × R_eq × C) ≈ 31.8 Hz (với R_eq = 100k || 100k = 50kΩ), triệt tiêu hoàn toàn các gai nhiễu cao tần sinh ra "
               "từ môi trường xung quanh, giúp kết quả đọc ADC cực kỳ ổn định và mượt mà.")

    add_p(doc, "", bold_prefix="Tuyên bố kỹ thuật về linh kiện chuyển đổi nguồn rời:")
    add_p(doc, 
          "Theo định hướng kiến trúc chuẩn xác của đề tài, các linh kiện chuyển đổi DC-DC rời cụ thể (IC sạc pin, IC Buck/Boost hạ áp/nâng áp) "
          "ở cấp độ chip linh kiện rời hiện CHƯA ĐÓNG BĂNG MÃ HIỆU LINH KIỆN CỐ ĐỊNH mà sẽ được đo đạc, kiểm chứng và lựa chọn dứt khoát "
          "dựa trên kết quả đo dòng tiêu thụ đỉnh thực tế của phần cứng hoàn chỉnh trong giai đoạn thi công. Báo cáo không tự tiện bịa đặt "
          "mã hiệu IC, hiệu suất chuyển đổi hay thời gian dùng pin khi chưa có kết quả đo đạc thực nghiệm.")

    add_p(doc, 
          "Các miền nguồn và tải tiêu thụ dự kiến trong hệ thống được phân định rõ ràng trong Bảng 3.19:")
          
    # Bảng 3.19
    tbl19_headers = ["Miền nguồn mạng", "Bản chất năng lượng", "Mức điện áp danh định", "Tải tiêu thụ / Chức năng kết nối chính"]
    tbl19_data = [
        ["VBUS", "Nguồn ngoài / Sạc", "5.0V DC (±5%)", "Cổng sạc USB-C cấp nguồn cho mạch nạp pin Li-ion"],
        ["VBAT", "Nguồn vận hành chính", "3.7V - 4.2V DC", "Pin Li-ion 18650 tích hợp, cấp năng lượng cho mạch biến đổi nguồn"],
        ["5V_SYS", "Đường nguồn hệ thống", "5.0V DC ổn định", "Cấp cho chân VIN/5V của ESP32-S3 DevKit, cấp còi cảnh báo Piezo 5V"],
        ["3V3_SYS", "Đường nguồn logic", "3.3V DC ổn định", "Cấp cho cảm biến MPU6050, DS3231, OLED 0.96 inch, thẻ nhớ MicroSD"],
        ["GND", "Mass hệ thống", "0V Reference", "Mặt phẳng mass chung hồi tiếp tín hiệu và dòng công suất"],
        ["ADC_VBAT_SENSE", "Kênh đo lường", "1.5V - 2.1V (Tỷ lệ 1/2 VBAT)", "Ngõ vào chân GPIO1 (ADC1_CH0) của ESP32-S3 đo điện áp pin"]
    ]
    add_table_with_caption(doc, "Bảng 3.19: Phân định các miền nguồn và tải tiêu thụ dự kiến trong hệ thống",
                           tbl19_headers, tbl19_data, col_widths=[1.5, 1.8, 1.6, 2.3])

    add_p(doc, 
          "Sơ đồ nguyên lý khối quản lý nguồn và mạch phân áp đo điện áp pin trích xuất từ bản vẽ thiết kế REV8 được thể hiện trong Hình 3.11:")
          
    fig11_path = os.path.join(assets_dir, "H3_11_power_block.png")
    add_figure(doc, fig11_path, "Hình 3.11: Sơ đồ nguyên lý khối quản lý nguồn và mạch phân áp đo điện áp pin", width_inches=5.2)

    # =========================================================================
    # 3.2.11 Sơ đồ nguyên lý toàn hệ thống
    # =========================================================================
    add_h3(doc, "3.2.11 Sơ đồ nguyên lý toàn hệ thống")
    
    add_p(doc, 
          "Trên cơ sở hoàn thiện thiết kế chi tiết cho từng khối chức năng riêng lẻ, toàn bộ hệ thống hộp đen AIoT thông minh "
          "được tích hợp và liên kết đồng bộ trên một bản vẽ sơ đồ nguyên lý tổng thể duy nhất theo tiêu chuẩn bản vẽ công nghiệp REV8 "
          "(AIOT_BLACKBOX_PRESENTATION_A4_REV8_FINAL).")
          
    add_p(doc, 
          "Bản vẽ REV8 tuân thủ nghiêm ngặt các quy tắc thiết kế phần cứng và quy tắc bản vẽ mạch điện tử (SCHEMATIC_DRAWING_RULES.md):")
    add_bullet(doc, "Bố cục trực quan theo dòng tín hiệu: ", 
               "Khối vi điều khiển trung tâm ESP32-S3 được bố trí ở vị trí trung tâm; các khối cảm biến đầu vào (MPU6050, DS3231, GNSS, Nút nhấn) "
               "được bố trí tuần tự phía bên trái; các khối chấp hành đầu ra và lưu trữ (MicroSD, OLED, 4G LTE, Cảnh báo) được bố trí khoa học phía bên phải; "
               "khối nguồn và mạch phân áp đo pin được quy hoạch gọn gàng ở góc dưới.")
    add_bullet(doc, "Quy chuẩn độ cao chân nguồn và mass: ", 
               "Toàn bộ các nhãn nguồn dương (5V_SYS, 3V3_SYS, VBAT, VBUS) đều xuất phát từ đỉnh trên của các khối và hướng lên trên; "
               "toàn bộ các điểm nối mass (GND) đều xuất phát từ đáy dưới của các linh kiện và hướng thẳng xuống mặt phẳng mass chung, "
               "tuyệt đối không có hiện tượng chéo dây hay đảo ngược chiều nguồn.")
    add_bullet(doc, "Bảo toàn các chân hở No-Connect: ", 
               "Tất cả các chân header vật lý thực tế trên các module nhưng không sử dụng trong mạch (chân 32K, SQW trên DS3231; "
               "chân XDA, XCL trên MPU6050) đều được giữ nguyên hiển thị và gắn cờ No-Connect (dấu chéo đỏ) theo đúng chuẩn KiCad, "
               "không tự ý xóa bỏ chân thực tế của linh kiện.")

    add_p(doc, 
          "Sơ đồ nguyên lý toàn hệ thống hộp đen AIoT xe máy điện bản vẽ REV8 được minh họa hoàn chỉnh trong Hình 3.12 dưới đây:")
          
    fig12_path = os.path.join(assets_dir, "H3_12_full_schematic.png")
    add_figure(doc, fig12_path, "Hình 3.12: Sơ đồ nguyên lý toàn hệ thống hộp đen AIoT xe máy điện (Bản vẽ REV8)", width_inches=6.2)

    print("Section 3.2 Part 3 built successfully.")
