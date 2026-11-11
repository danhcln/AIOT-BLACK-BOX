# -*- coding: utf-8 -*-
"""
Module ch3_sec32_p2.py: Section 3.2 Part 2 generator.
Covers:
- 3.2.4 Khối GPS (NEO-M8N GNSS, comparisons, specs table, schematic crop)
- 3.2.5 Khối lưu trữ (MicroSD SPI Module, comparisons, specs table, schematic crop)
- 3.2.6 Khối 4G LTE (MKE-M21 / SIM7680C, comparisons, AT commands table, specs table, schematic crop)
"""

import os
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from build_chapter3_full import (
    add_p, add_bullet, add_h3, add_figure, add_table_with_caption, add_code_snippet
)

def add_section_3_2_part2(doc, assets_dir):
    # =========================================================================
    # 3.2.4 Khối GPS
    # =========================================================================
    add_h3(doc, "3.2.4 Khối GPS")
    
    add_p(doc, 
          "Để thực hiện chức năng định vị vị trí xe khi xảy ra tai nạn và cung cấp dữ liệu vận tốc, hướng di chuyển phục vụ phân tích "
          "nguyên nhân sự cố, hộp đen thông minh bắt buộc phải tích hợp khối thu tín hiệu định vị vệ tinh toàn cầu (GNSS). Khối này có nhiệm vụ "
          "giải mã liên tục tọa độ kinh độ (Longitude), vĩ độ (Latitude), độ cao (Altitude), tốc độ mặt đất (Ground Speed) và búp sóng thời gian chuẩn. "
          "Các phương án module định vị được nghiên cứu và khảo sát gồm:")
          
    add_p(doc, "", bold_prefix="Phương án 1: Sử dụng module định vị đa băng tần NEO-M8N GNSS (u-blox - Thụy Sĩ):")
    add_p(doc, 
          "NEO-M8N là module định vị vệ tinh cao cấp thuộc thế hệ thứ 8 của hãng u-blox danh tiếng, sở hữu động cơ thu 72 kênh và "
          "khả năng thu nhận đồng thời nhiều hệ thống vệ tinh định vị độc lập (Concurrent GNSS): GPS (Mỹ), GLONASS (Nga), BeiDou (Trung Quốc) "
          "và Galileo (Châu Âu).")
    add_bullet(doc, "Ưu điểm: ", 
               "Khả năng bắt sóng vệ tinh vượt trội trong môi trường đô thị phức tạp (nhiều nhà cao tầng, đường hầm, cầu vượt, tán cây rậm rạp) "
               "nhờ thu đồng thời đa hệ thống vệ tinh; độ nhạy thu tín hiệu cực cao (-167 dBm khi bám vết); tốc độ cập nhật tọa độ nhanh lên tới 10 Hz; "
               "thời gian chốt vị trí lần đầu (TTFF) rất ngắn; tích hợp thạch anh bù nhiệt độ (TCXO) và bộ nhớ Flash nội lưu cấu hình; "
               "cung cấp chân xung thời gian chuẩn 1 Hz (PPS - Pulse Per Second) với độ chính xác nanogiây giúp đồng bộ nhịp dữ liệu hộp đen.")
    add_bullet(doc, "Nhược điểm: ", 
               "Giá thành cao hơn các dòng GPS cơ bản đời cũ, tuy nhiên hoàn toàn tương xứng với độ tin cậy của thiết bị an toàn phương tiện.")

    add_p(doc, "", bold_prefix="Phương án 2: Sử dụng module GPS NEO-6M (u-blox thế hệ cũ):")
    add_p(doc, 
          "NEO-6M là dòng module GPS thế hệ thứ 6 của u-blox ra đời từ nhiều năm trước, có 50 kênh thu và chỉ bắt được duy nhất một hệ thống vệ tinh GPS (Mỹ).")
    add_bullet(doc, "Ưu điểm: ", 
               "Giá thành rẻ, rất phổ biến, dễ tích hợp với các bo mạch Arduino.")
    add_bullet(doc, "Nhược điểm: ", 
               "Chỉ hỗ trợ đơn hệ thống vệ tinh GPS; độ nhạy thu thấp (-161 dBm); tốc độ cập nhật tối đa chỉ 5 Hz; thời gian chốt vị trí rất lâu "
               "(khi khởi động nguội mất từ 1 đến 3 phút); dễ bị mất tín hiệu hoàn toàn khi xe chạy vào các tuyến phố có nhà cao tầng hoặc tán cây dày đặc; "
               "độ trễ lớn không đáp ứng tốt yêu cầu định vị sự cố xe máy.")

    add_p(doc, "", bold_prefix="Phương án 3: Sử dụng module ATGM336H (Zhongke Microelectronics):")
    add_p(doc, 
          "ATGM336H là module định vị chi phí thấp của Trung Quốc, hỗ trợ hệ thống GPS và BDS (Bắc Đẩu).")
    add_bullet(doc, "Ưu điểm: ", 
               "Kích thước rất nhỏ gọn, giá thành thấp, tiêu thụ dòng điện thấp.")
    add_bullet(doc, "Nhược điểm: ", 
               "Khả năng lọc nhiễu vô tuyến và độ ổn định kém hơn u-blox; độ chính xác định vị dao động lớn; chất lượng linh kiện trên các bản mạch "
               "thương mại không đồng đều; tài liệu kỹ thuật và hỗ trợ cấu hình sâu từ hãng sản xuất hạn chế hơn nhiều so với u-blox.")

    add_p(doc, 
          "Các chỉ tiêu kỹ thuật cốt lõi so sánh giữa 3 phương án module định vị được thể hiện trong Bảng 3.8:")
          
    # Bảng 3.8
    tbl8_headers = ["Tiêu chí kỹ thuật", "NEO-M8N GNSS [Được chọn]", "NEO-6M GPS", "ATGM336H"]
    tbl8_data = [
        ["Hãng sản xuất / Xuất xứ", "u-blox (Thụy Sĩ)", "u-blox (Thụy Sĩ)", "Zhongke Microelectronics (TQ)"],
        ["Số kênh thu vệ tinh", "72 kênh đa vệ tinh đồng thời", "50 kênh đơn vệ tinh", "32 kênh"],
        ["Hệ thống vệ tinh hỗ trợ", "GPS/QZSS, GLONASS, BeiDou, Galileo", "Chỉ duy nhất GPS (Mỹ)", "GPS, BeiDou (BDS)"],
        ["Độ nhạy thu (Tracking)", "Cực cao: -167 dBm", "Trung bình: -161 dBm", "Khá: -162 dBm"],
        ["Tốc độ cập nhật tối đa", "10 Hz (100 ms mỗi chu kỳ)", "5 Hz (200 ms mỗi chu kỳ)", "10 Hz"],
        ["Thời gian chốt vị trí nguội (Cold TTFF)", "Nhanh: ~26 giây", "Chậm: ~35 - 60 giây", "Khá: ~32 giây"],
        ["Bộ dao động tích hợp", "TCXO (Thạch anh bù nhiệt độ cao cấp)", "Thạch anh thông thường (Crystal)", "Thạch anh thông thường"],
        ["Xung chuẩn thời gian PPS", "Có (Độ chính xác nano giây)", "Có", "Có"],
        ["Khả năng bám sóng đô thị", "Vượt trội trong hẻm sâu, nhà cao tầng", "Dễ mất tín hiệu ở đô thị", "Trung bình"],
        ["Mức độ phù hợp hộp đen", "Lý tưởng nhất cho xe máy điện", "Đã lỗi thời, không khuyến nghị", "Kém tin cậy hơn u-blox"]
    ]
    add_table_with_caption(doc, "Bảng 3.8: So sánh các phương án module định vị cho khối GPS",
                           tbl8_headers, tbl8_data, col_widths=[1.8, 2.0, 1.8, 1.6])

    add_p(doc, "", bold_prefix="Phương án được lựa chọn: Module NEO-M8N GNSS:")
    add_p(doc, 
          "Module NEO-M8N của hãng u-blox được lựa chọn dứt khoát làm thiết bị định vị tiêu chuẩn cho đề tài. Việc thu nhận đồng thời "
          "cả GPS và GLONASS cho phép thiết bị luôn 'nhìn thấy' từ 14 đến 22 vệ tinh cùng lúc (thay vì chỉ 4-7 vệ tinh như module cũ), "
          "đảm bảo cung cấp tọa độ tai nạn chính xác tới từng số nhà ngay giữa trung tâm thành phố. Thông số kỹ thuật chi tiết của "
          "module NEO-M8N được trình bày trong Bảng 3.9:")

    # Bảng 3.9
    tbl9_headers = ["Thông số kỹ thuật", "Giá trị thiết kế / Đặc tính kỹ thuật", "Ghi chú ứng dụng"]
    tbl9_data = [
        ["Động cơ định vị", "u-blox M8 engine (72 kênh)", "Hỗ trợ định vị vệ tinh đồng thời đa hệ thống"],
        ["Điện áp hoạt động bo mạch", "3.3V - 5.0V DC (Tích hợp mạch ổn áp nội)", "Hệ thống cấp nguồn an toàn từ đường nguồn hệ thống"],
        ["Giao diện truyền thông", "UART nối tiếp (Asynchronous Serial)", "Tốc độ baud mặc định 9600 bps (có thể nâng 115200)"],
        ["Định dạng dữ liệu xuất", "Giao thức chuẩn NMEA 0183 ($GNRMC, $GNGGA)", "Cung cấp tọa độ, vận tốc km/h và thời gian UTC"],
        ["Anten thu sóng tích hợp", "Anten gốm tích cực Ceramic Patch 25x25mm", "Có mạch khuếch đại nhiễu thấp (LNA) tích hợp"],
        ["Chân kết nối phần cứng", "VCC, GND, TX, RX, PPS", "Exposed header vật lý chuẩn trên module"],
        ["Chân xung thời gian PPS", "Xung vuông 1 Hz (Độ rộng xung 100 ms)", "Nối về chân ngắt GPIO21 của ESP32-S3"]
    ]
    add_table_with_caption(doc, "Bảng 3.9: Thông số kỹ thuật chi tiết của module định vị NEO-M8N GNSS",
                           tbl9_headers, tbl9_data, col_widths=[2.0, 2.8, 2.4])

    add_p(doc, "", bold_prefix="Kết nối phần cứng khối GPS trên sơ đồ nguyên lý REV8:")
    add_p(doc, 
          "Module NEO-M8N được giao tiếp trực tiếp với bộ điều khiển UART1 phần cứng của ESP32-S3 và một chân ngắt ngoài đồng bộ:")
    add_bullet(doc, "Chân nhận dữ liệu vi điều khiển (GNSS_RXD - GPIO18): ", 
               "Nối trực tiếp từ chân TX của module NEO-M8N sang chân GPIO18 của ESP32-S3 để tiếp nhận liên tục các câu bản tin NMEA.")
    add_bullet(doc, "Chân truyền dữ liệu vi điều khiển (GNSS_TXD - GPIO17): ", 
               "Nối từ chân GPIO17 của ESP32-S3 sang chân RX của module NEO-M8N để truyền các tập lệnh cấu hình nhị phân UBX "
               "(như lệnh tăng tần số cập nhật tọa độ lên 10 Hz, lọc các bản tin không cần thiết).")
    add_bullet(doc, "Chân xung thời gian chuẩn (GNSS_PPS - GPIO21): ", 
               "Nối từ chân PPS của NEO-M8N sang chân GPIO21 của ESP32-S3. Xung PPS xuất hiện chính xác ở đầu mỗi giây, kích hoạt ngắt phần cứng "
               "giúp hệ thống đồng bộ hóa mốc lấy mẫu cảm biến IMU trùng khớp tuyệt đối với thời gian vệ tinh toàn cầu.")
    add_bullet(doc, "Nguồn cấp: ", "Được cấp nguồn từ đường nguồn hệ thống thích hợp và nối mass chung GND.")

    add_p(doc, 
          "Sơ đồ nguyên lý khối định vị GPS (NEO-M8N GNSS) trích xuất từ bản vẽ thiết kế REV8 được thể hiện trong Hình 3.5:")
          
    fig5_path = os.path.join(assets_dir, "H3_5_gnss_block.png")
    add_figure(doc, fig5_path, "Hình 3.5: Sơ đồ nguyên lý khối định vị GPS (NEO-M8N GNSS)", width_inches=4.5)

    # =========================================================================
    # 3.2.5 Khối lưu trữ
    # =========================================================================
    add_h3(doc, "3.2.5 Khối lưu trữ")
    
    add_p(doc, 
          "Bản chất cốt lõi của một hệ thống hộp đen (Black Box / Event Data Recorder - EDR) là phải lưu trữ an toàn, toàn vẹn và bất biến "
          "mọi dữ liệu động học của phương tiện trước, trong và sau thời điểm xảy ra sự cố. Đặc biệt, trong các vụ tai nạn giao thông nghiêm trọng "
          "xảy ra tại các vùng đèo dốc, hầm đường bộ hoặc vùng sâu vùng xa không có sóng di động 4G, khả năng lưu trữ cục bộ độc lập là phòng tuyến "
          "duy nhất bảo vệ dữ liệu phục vụ điều tra. Các phương án thiết kế khối lưu trữ gồm:")
          
    add_p(doc, "", bold_prefix="Phương án 1: Sử dụng module thẻ nhớ MicroSD giao tiếp qua bus SPI (Được chọn):")
    add_p(doc, 
          "Sử dụng thẻ nhớ MicroSD thông qua khe cắm thẻ MicroSD chuẩn giao tiếp nối tiếp SPI tốc độ cao.")
    add_bullet(doc, "Ưu điểm: ", 
               "Dung lượng lưu trữ cực lớn (từ 8 GB đến 32 GB), cho phép ghi dữ liệu nhật ký liên tục trong nhiều tháng; định dạng hệ thống tệp tin "
               "FAT32 tiêu chuẩn quốc tế; thẻ nhớ có thể tháo rời dễ dàng để cắm trực tiếp vào máy tính của cơ quan chức năng, công ty bảo hiểm "
               "hoặc chuyên gia giám định để trích xuất dữ liệu phân tích ngoại tuyến (Offline Forensic Examination) mà không cần tháo cả thiết bị; "
               "tốc độ truyền dữ liệu SPI nhanh (lên tới 20 MHz trên ESP32-S3); chi phí thẻ nhớ rất rẻ và dễ dàng thay thế.")
    add_bullet(doc, "Nhược điểm: ", 
               "Cần cơ cấu khe cắm cơ khí vững chắc chống rung lắc; cần quản lý bộ đệm ghi để tránh làm giảm tuổi thọ bộ nhớ Flash của thẻ nhớ.")

    add_p(doc, "", bold_prefix="Phương án 2: Sử dụng chip nhớ EEPROM / SPI NOR Flash hàn cố định trên bo mạch:")
    add_p(doc, 
          "Sử dụng các chip nhớ bán dẫn thể rắn (như W25Q128 16MB SPI Flash hoặc AT24C512 EEPROM) hàn chết trực tiếp lên mạch in PCB.")
    add_bullet(doc, "Ưu điểm: ", 
               "Không có tiếp điểm cơ khí, độ bền chống rung xóc cơ học tuyệt đối, tiêu thụ điện năng thấp.")
    add_bullet(doc, "Nhược điểm: ", 
               "Dung lượng bộ nhớ rất nhỏ (chỉ từ vài kilobyte đến vài megabyte), không đủ dung lượng để ghi lưu nhật ký hành trình dài ngày; "
               "khi xảy ra sự cố, để trích xuất dữ liệu bắt buộc phải kết nối máy tính qua cổng cáp hoặc tháo chip khỏi bo mạch, gây cản trở và "
               "phức tạp hóa quy trình điều tra hiện trường.")

    add_p(doc, "", bold_prefix="Phương án 3: Giải pháp chỉ lưu trữ dữ liệu trực tiếp trên máy chủ đám mây (Cloud-only):")
    add_p(doc, 
          "Hệ thống không trang bị bộ nhớ vật lý cục bộ mà truyền toàn bộ dữ liệu cảm biến trực tiếp lên máy chủ đám mây qua mạng 4G.")
    add_bullet(doc, "Ưu điểm: ", 
               "Giảm thiểu kích thước phần cứng, dữ liệu được đồng bộ hóa tức thì lên máy chủ trung tâm.")
    add_bullet(doc, "Nhược điểm: ", 
               "Cực kỳ nguy hiểm và vi phạm nguyên lý cơ bản của hộp đen an toàn; nếu xe gặp tai nạn tại khu vực mất sóng di động, vùng phủ sóng yếu "
               "hoặc anten 4G bị va đập gãy hỏng trong lúc va chạm, toàn bộ dữ liệu sự cố sẽ biến mất vĩnh viễn và không thể khôi phục; "
               "tiêu tốn băng thông và chi phí cước dữ liệu di động rất lớn.")

    add_p(doc, 
          "Các chỉ tiêu đối sánh kỹ thuật giữa các giải pháp lưu trữ dữ liệu được thể hiện trong Bảng 3.10:")
          
    # Bảng 3.10
    tbl10_headers = ["Tiêu chí kỹ thuật", "Thẻ nhớ MicroSD SPI [Được chọn]", "Chip nhớ Flash/EEPROM hàn bo", "Chỉ lưu trữ trên Cloud"]
    tbl10_data = [
        ["Dung lượng lưu trữ", "Rất lớn (8 GB - 32 GB)", "Rất nhỏ (vài MB đến vài chục MB)", "Không giới hạn (Phía Server)"],
        ["Độ độc lập với mạng 4G", "Độc lập 100%, ghi liên tục", "Độc lập 100%", "Phụ thuộc 100% vào mạng viễn thông"],
        ["Khả năng trích xuất pháp y", "Dễ dàng tháo thẻ cắm vào PC", "Phải cắm cáp mạch hoặc giải hàn", "Phải truy cập tài khoản Web/Server"],
        ["Hệ thống tệp tin", "FAT32 / CSV / Nhị phân chuẩn", "Raw Memory / Tự quản lý phân vùng", "JSON / Database trên Server"],
        ["Tốc độ ghi dữ liệu", "Cao (Bus SPI 20 MHz)", "Trung bình", "Bị giới hạn bởi độ trễ mạng di động"],
        ["Khả năng lưu nhật ký dài", "Hàng tháng liên tục", "Chỉ vài giờ", "Tốn chi phí cước Data 4G liên tục"],
        ["Mức độ phù hợp hộp đen", "Tối ưu nhất cho điều tra tai nạn", "Kém linh hoạt", "Không khả thi cho thiết bị an toàn"]
    ]
    add_table_with_caption(doc, "Bảng 3.10: So sánh các phương án lưu trữ dữ liệu sự cố",
                           tbl10_headers, tbl10_data, col_widths=[1.8, 2.0, 1.8, 1.6])

    add_p(doc, "", bold_prefix="Phương án được lựa chọn: Module thẻ nhớ MicroSD giao tiếp SPI:")
    add_p(doc, 
          "Module thẻ nhớ MicroSD sử dụng chuẩn giao tiếp SPI được chọn làm giải pháp lưu trữ chính thức cho hệ thống. Thông số kỹ thuật "
          "và phân công chân giao tiếp được trình bày chi tiết trong Bảng 3.11:")

    # Bảng 3.11
    tbl11_headers = ["Tên chân module", "Kết nối vi điều khiển", "Tên tín hiệu mạng", "Chức năng chi tiết trong giao tiếp SPI"]
    tbl11_data = [
        ["CS", "GPIO14", "SD_CS", "Chân chọn chip (Chip Select), tích cực mức thấp (Active Low)"],
        ["MOSI", "GPIO11", "SPI_MOSI", "Dữ liệu ra từ vi điều khiển sang thẻ nhớ (Master Out Slave In)"],
        ["SCK", "GPIO12", "SPI_SCK", "Đường xung nhịp đồng bộ giao tiếp SPI tốc độ cao (20 MHz)"],
        ["MISO", "GPIO13", "SPI_MISO", "Dữ liệu nối tiếp từ thẻ nhớ truyền về vi điều khiển (Master In Slave Out)"],
        ["VCC", "Đường nguồn logic", "3V3_SYS / 5V_SYS", "Cấp nguồn hoạt động cho thẻ nhớ (có tụ gốm 100nF lọc nguồn)"],
        ["GND", "Mass hệ thống", "GND", "Nối vào mặt phẳng mass chung của mạch"]
    ]
    add_table_with_caption(doc, "Bảng 3.11: Thông số kỹ thuật và chân giao tiếp của module thẻ nhớ MicroSD SPI",
                           tbl11_headers, tbl11_data, col_widths=[1.5, 1.6, 1.5, 2.6])

    add_p(doc, "", bold_prefix="Cơ chế đệm RAM bảo vệ thẻ nhớ và cấu trúc tệp tin:")
    add_p(doc, 
          "Việc ghi liên tục dữ liệu cảm biến tần số 100 Hz trực tiếp vào thẻ nhớ Flash có thể làm chậm tốc độ CPU do độ trễ ghi khối (Block latency) "
          "và làm giảm tuổi thọ thẻ nhớ. Để khắc phục triệt để nhược điểm này, hệ thống áp dụng kỹ thuật đệm kép (Double Buffering): "
          "Dữ liệu 100 Hz được tích lũy vào một khối đệm RAM 512 bytes trong PSRAM. Chỉ khi khối đệm đầy (tương đương 1 chu kỳ ghi khối ngành chuẩn), "
          "lệnh ghi một mẻ duy nhất mới được kích hoạt xuống thẻ nhớ SPI, sau đó thực hiện lệnh giải phóng bộ đệm (Flush) để đảm bảo dữ liệu "
          "được ghi thực sự vào tế bào nhớ vật lý mà không bị kẹt trong bộ đệm tạm thời.")

    add_p(doc, 
          "Sơ đồ nguyên lý khối lưu trữ thẻ nhớ MicroSD SPI trích xuất từ bản vẽ thiết kế REV8 được thể hiện trong Hình 3.6:")
          
    fig6_path = os.path.join(assets_dir, "H3_6_microsd_block.png")
    add_figure(doc, fig6_path, "Hình 3.6: Sơ đồ nguyên lý khối lưu trữ thẻ nhớ MicroSD SPI", width_inches=4.5)

    # =========================================================================
    # 3.2.6 Khối 4G LTE
    # =========================================================================
    add_h3(doc, "3.2.6 Khối 4G LTE")
    
    add_p(doc, 
          "Khối truyền thông 4G LTE đảm nhiệm vai trò kết nối cứu nạn sống còn của hệ thống hộp đen AIoT. Sau khi thuật toán nhận diện "
          "xác nhận xảy ra tai nạn nghiêm trọng và người lái không nhấn nút hủy trong thời gian đếm ngược 15 giây, thiết bị phải lập tức "
          "phát đi tín hiệu cấp cứu không dây mang theo thông tin tọa độ vị trí hiện trường đến người thân và hệ thống điều hành giao thông thông minh. "
          "Các phương án công nghệ truyền thông không dây được phân tích gồm:")
          
    add_p(doc, "", bold_prefix="Phương án 1: Sử dụng module công nghiệp MKE-M21 tích hợp IC SIM7680C 4G LTE Cat-1 (Được chọn):")
    add_p(doc, 
          "SIM7680C là dòng chip truyền thông không dây 4G LTE Cat-1 thế hệ mới của hãng SIMCom, được thiết kế chuyên biệt cho các thiết bị IoT di động.")
    add_bullet(doc, "Ưu điểm: ", 
               "Tương thích hoàn toàn với tất cả các nhà mạng viễn thông tại Việt Nam (Viettel, Vinaphone, Mobifone); tốc độ truyền dữ liệu đạt "
               "chuẩn Cat-1 (Downlink 10 Mbps, Uplink 5 Mbps), độ trễ thấp; hỗ trợ đầy đủ tính năng gửi/nhận tin nhắn SMS và các giao thức mạng "
               "TCP/IP, HTTP, MQTT; kích thước bo mạch siêu nhỏ gọn; mức tiêu thụ năng lượng thấp hơn nhiều so với dòng module 4G Cat-4 (như SIM7600); "
               "tích hợp giao tiếp UART chuẩn công nghiệp với các chân điều khiển phần cứng chuyên dụng (PWRKEY, STATUS).")
    add_bullet(doc, "Nhược điểm: ", 
               "Tương tự như mọi thiết bị viễn thông vô tuyến, module có thể xuất hiện các xung dòng đỉnh ngắn hạn khi phát sóng RF, "
               "đòi hỏi thiết kế mạch nguồn phải có giải pháp lọc ổn áp đường nguồn riêng biệt.")

    add_p(doc, "", bold_prefix="Phương án 2: Sử dụng module 2G SIM800L (GSM / GPRS):")
    add_p(doc, 
          "SIM800L là module truyền thông 2G kinh điển đã từng được sử dụng phổ biến trong các dự án sinh viên trước đây.")
    add_bullet(doc, "Ưu điểm: ", 
               "Giá thành rất rẻ, kích thước nhỏ.")
    add_bullet(doc, "Nhược điểm nghiêm trọng: ", 
               "TẠI VIỆT NAM, BỘ THÔNG TIN VÀ TRUYỀN THÔNG ĐÃ CHÍNH THỨC TẮT HOÀN TOÀN SÓNG 2G TỪ THÁNG 10/2024. Do đó, các module chỉ hỗ trợ "
               "2G như SIM800L hiện nay đã hoàn toàn mất khả năng bắt sóng, không thể gửi tin nhắn SMS hay kết nối mạng dữ liệu. Việc lựa chọn "
               "SIM800L ở thời điểm hiện tại là hoàn toàn sai lầm về mặt kỹ thuật và không thể vận hành thực tế.")

    add_p(doc, "", bold_prefix="Phương án 3: Giải pháp chỉ sử dụng kết nối nội bộ Wi-Fi và Bluetooth:")
    add_p(doc, 
          "Chỉ tận dụng kết nối Wi-Fi/BLE sẵn có trên chip ESP32-S3 mà không trang bị thêm module mạng di động viễn thông.")
    add_bullet(doc, "Ưu điểm: ", 
               "Không tốn thêm chi phí module viễn thông và thẻ SIM.")
    add_bullet(doc, "Nhược điểm: ", 
               "Bán kính kết nối cực ngắn (dưới 50 mét); xe máy điện di chuyển liên tục trên đường giao thông công cộng hoàn toàn không thể có mạng "
               "Wi-Fi cố định để kết nối; nếu người lái gặp tai nạn giữa đường, hệ thống hoàn toàn cô lập và không thể gửi bất kỳ tín hiệu cấp cứu nào "
               "ra bên ngoài, làm mất đi giá trị cốt lõi của một hệ thống an toàn thông minh.")

    add_p(doc, 
          "Các giải pháp truyền thông không dây từ xa được đối sánh toàn diện trong Bảng 3.12:")
          
    # Bảng 3.12
    tbl12_headers = ["Tiêu chí kỹ thuật", "Module MKE-M21 (SIM7680C 4G) [Được chọn]", "Module SIM800L (2G)", "Wi-Fi / Bluetooth nội bộ"]
    tbl12_data = [
        ["Thế hệ mạng di động", "4G LTE Cat-1 (Băng tần B1/B3/B5/B8)", "2G GSM / GPRS (900/1800 MHz)", "Không có mạng di động"],
        ["Tình trạng sóng tại Việt Nam", "Hoạt động ổn định, phủ sóng toàn quốc", "ĐÃ BỊ TẮT SÓNG HOÀN TOÀN (10/2024)", "Không áp dụng"],
        ["Khả năng gửi SMS cấp cứu", "Gửi tức thì trong 1-3 giây", "Không hoạt động do mất sóng", "Không hỗ trợ"],
        ["Truyền dữ liệu lên Cloud", "MQTT / HTTP qua mạng di động 4G", "Không hoạt động", "Chỉ gửi được khi có trạm phát Wi-Fi"],
        ["Vùng hoạt động phương tiện", "Bất kỳ đâu trên toàn quốc có sóng di động", "Không hoạt động", "Bán kính hạn hẹp dưới 50m"],
        ["Tốc độ truyền dữ liệu", "Down: 10 Mbps, Up: 5 Mbps", "Tối đa 85.6 kbps", "54 Mbps (Chỉ trong mạng nội bộ)"],
        ["Tính thực tiễn của đề tài", "Đạt chuẩn công nghiệp hiện đại", "Không thể sử dụng thực tế", "Kém thực tế cho phương tiện di chuyển"]
    ]
    add_table_with_caption(doc, "Bảng 3.12: So sánh các giải pháp truyền thông không dây từ xa",
                           tbl12_headers, tbl12_data, col_widths=[1.8, 2.0, 1.8, 1.6])

    add_p(doc, "", bold_prefix="Phương án được lựa chọn: Module MKE-M21 (SIM7680C 4G LTE Cat-1):")
    add_p(doc, 
          "Module công nghiệp MKE-M21 tích hợp IC SIM7680C là lựa chọn chuẩn xác, vừa đón đầu công nghệ viễn thông 4G hiện đại, "
          "vừa đảm bảo khả năng hoạt động lâu dài cho sản phẩm. Thông số kỹ thuật chi tiết của module SIM7680C được tổng hợp trong Bảng 3.13:")

    # Bảng 3.13
    tbl13_headers = ["Thông số kỹ thuật", "Giá trị thiết kế / Đặc tính kỹ thuật", "Ghi chú ứng dụng"]
    tbl13_data = [
        ["IC xử lý trung tâm", "SIMCom SIM7680C LTE Cat-1", "Tối ưu hóa chuyên biệt cho thiết bị IoT di động"],
        ["Băng tần LTE hỗ trợ", "FDD-LTE: B1/B3/B5/B8; TDD-LTE: B34/B38/B39/B40/B41", "Tương thích 100% các nhà mạng Viettel, Vina, Mobi"],
        ["Giao diện truyền thông", "UART nối tiếp (Chuẩn mức logic 3.3V)", "Giao tiếp với bộ UART2 của ESP32-S3"],
        ["Tốc độ baud UART", "Mặc định 115200 bps", "Đảm bảo truyền nhận tập lệnh AT phản hồi cực nhanh"],
        ["Chân điều khiển nguồn", "4G_PWRKEY nối về chân GPIO4", "Kích xung mức thấp 1.5s để khởi động/tắt module"],
        ["Chân đọc trạng thái", "4G_STATUS nối về chân GPIO5", "Mức cao = Module đang hoạt động; Mức thấp = Module tắt"],
        ["Tích hợp khe cắm SIM", "Khe Nano SIM chuẩn công nghiệp dạng khay trượt", "Lắp đặt chắc chắn, chống rung lắc trên xe máy"]
    ]
    add_table_with_caption(doc, "Bảng 3.13: Thông số kỹ thuật chi tiết của module 4G LTE MKE-M21 (SIM7680C)",
                           tbl13_headers, tbl13_data, col_widths=[2.0, 2.8, 2.4])

    add_p(doc, "", bold_prefix="Tập lệnh AT điều khiển quan trọng của module SIM7680C:")
    add_p(doc, 
          "Vi điều khiển ESP32-S3 tương tác toàn bộ với SIM7680C thông qua tập lệnh AT tiêu chuẩn mở rộng của SIMCom. "
          "Bảng 3.14 liệt kê các lệnh AT cốt lõi được lập trình trong firmware để thực thi gửi tin nhắn SMS cứu hộ và truyền dữ liệu đám mây:")

    # Bảng 3.14
    tbl14_headers = ["Lệnh AT", "Chức năng điều khiển", "Cú pháp thực thi", "Phản hồi mong đợi"]
    tbl14_data = [
        ["AT", "Kiểm tra kết nối và độ sẵn sàng của module", "AT\\r\\n", "OK"],
        ["ATE0", "Tắt chế độ phản hồi vọng lệnh (Echo off)", "ATE0\\r\\n", "OK"],
        ["AT+CPIN?", "Kiểm tra tình trạng nhận dạng của thẻ SIM", "AT+CPIN?\\r\\n", "+CPIN: READY"],
        ["AT+CSQ", "Đo cường độ tín hiệu sóng di động (RSSI)", "AT+CSQ\\r\\n", "+CSQ: <rssi>,<ber>"],
        ["AT+CREG?", "Kiểm tra trạng thái đăng ký vào mạng di động", "AT+CREG?\\r\\n", "+CREG: 0,1 (Đã đăng ký)"],
        ["AT+CMGF=1", "Cấu hình chế độ tin nhắn văn bản (Text Mode)", "AT+CMGF=1\\r\\n", "OK"],
        ["AT+CMGS", "Gửi tin nhắn SMS cứu hộ đến số khẩn cấp", "AT+CMGS=\\\"<Phone_Number>\\\"\\r\\n", "> [Nhập nội dung + Ctrl+Z]"],
        ["AT+CGATT=1", "Kích hoạt dịch vụ truyền dữ liệu gói GPRS/LTE", "AT+CGATT=1\\r\\n", "OK"],
        ["AT+CSTT", "Cấu hình APN mạng di động (v-internet, m3-world)", "AT+CSTT=\\\"<APN>\\\"\\r\\n", "OK"],
        ["AT+CIICR", "Kích hoạt kết nối không dây và cấp phát IP", "AT+CIICR\\r\\n", "OK"]
    ]
    add_table_with_caption(doc, "Bảng 3.14: Tập lệnh AT cơ bản điều khiển module 4G LTE SIM7680C",
                           tbl14_headers, tbl14_data, col_widths=[1.5, 2.3, 2.2, 1.5])

    add_p(doc, "", bold_prefix="Kết nối phần cứng trên sơ đồ nguyên lý REV8:")
    add_p(doc, 
          "Trên bản vẽ sơ đồ nguyên lý chuẩn REV8, khối 4G LTE được đấu nối mạch điện chính xác như sau:")
    add_bullet(doc, "Tín hiệu UART2: ", 
               "Chân 4G_TXD (GPIO43 của ESP32-S3) nối sang chân RX của SIM7680C; chân 4G_RXD (GPIO44 của ESP32-S3) nối sang chân TX của SIM7680C.")
    add_bullet(doc, "Tín hiệu điều khiển nguồn 4G_PWRKEY: ", 
               "Nối từ chân GPIO4 sang chân PWRKEY của SIM7680C. Khi cần khởi động module, vi điều khiển kéo chân GPIO4 xuống mức thấp (GND) "
               "trong thời gian 1.5 giây rồi đưa về mức cao để bật nguồn theo đúng trình tự khởi động của datasheet SIMCom.")
    add_bullet(doc, "Tín hiệu trạng thái 4G_STATUS: ", 
               "Nối từ chân STATUS của SIM7680C về chân GPIO5 của ESP32-S3, cho phép vi điều khiển giám sát tức thì module đang thức hay ngủ.")
    add_bullet(doc, "Đường nguồn cấp: ", 
               "Module được cấp nguồn ổn định, có dự phòng tụ hóa dung lượng lớn để gánh các xung dòng phát RF của anten.")

    add_p(doc, 
          "Sơ đồ nguyên lý khối truyền thông không dây 4G LTE (MKE-M21 / SIM7680C) trích xuất từ bản vẽ thiết kế REV8 được thể hiện trong Hình 3.7:")
          
    fig7_path = os.path.join(assets_dir, "H3_7_4g_lte_block.png")
    add_figure(doc, fig7_path, "Hình 3.7: Sơ đồ nguyên lý khối truyền thông không dây 4G LTE (MKE-M21 / SIM7680C)", width_inches=4.5)

    print("Section 3.2 Part 2 built successfully.")
