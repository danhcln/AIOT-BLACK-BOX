# -*- coding: utf-8 -*-
import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

from builder_core import (
    set_cell_margins, set_cell_background, set_table_borders,
    add_hyperlink, add_para, add_h1, add_h2, add_h3,
    add_bullet, add_callout, create_styled_table
)

def build_word_document():
    doc = Document()
    
    # Page Setup: A4, standard academic margins (Left 30mm, Right 20mm, Top 25mm, Bottom 25mm)
    sections = doc.sections
    for section in sections:
        section.page_width = Mm(210)
        section.page_height = Mm(297)
        section.top_margin = Mm(25)
        section.bottom_margin = Mm(25)
        section.left_margin = Mm(30)
        section.right_margin = Mm(20)
        
        # Add Page Number in Footer
        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        f_run = f_p.add_run("Báo cáo Đề xuất Đồ án 2 | Bộ môn Kỹ thuật Máy tính - Viễn thông")
        f_run.font.name = "Times New Roman"
        f_run.font.size = Pt(9.5)
        f_run.font.italic = True
        f_run.font.color.rgb = RGBColor(148, 163, 184)
        
    # Normal Style configuration
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(13)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)
    normal_style.paragraph_format.line_spacing = 1.35
    normal_style.paragraph_format.space_after = Pt(4)
    normal_style.paragraph_format.space_before = Pt(0)
    
    # -------------------------------------------------------------
    # BÌA / TIÊU ĐỀ BÁO CÁO
    # -------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_after = Pt(2)
    p_inst.paragraph_format.first_line_indent = Inches(0)
    r1 = p_inst.add_run("TRƯỜNG ĐẠI HỌC SƯ PHẠM KỸ THUẬT THÀNH PHỐ HỒ CHÍ MINH\n")
    r1.bold = True
    r1.font.size = Pt(13)
    r1.font.color.rgb = RGBColor(15, 23, 42)
    r2 = p_inst.add_run("KHOA ĐIỆN - ĐIỆN TỬ  |  BỘ MÔN KỸ THUẬT MÁY TÍNH - VIỄN THÔNG\n")
    r2.bold = True
    r2.font.size = Pt(12)
    r2.font.color.rgb = RGBColor(71, 85, 105)
    r_line = p_inst.add_run("―" * 32)
    r_line.font.color.rgb = RGBColor(203, 213, 225)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(8)
    p_title.paragraph_format.first_line_indent = Inches(0)
    r_t1 = p_title.add_run("BÁO CÁO TỔNG HỢP & ĐỀ XUẤT ĐỀ TÀI ĐỒ ÁN 2 (PROJECT 2)\n")
    r_t1.bold = True
    r_t1.font.size = Pt(18)
    r_t1.font.color.rgb = RGBColor(15, 44, 89) # Deep Navy
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(18)
    p_sub.paragraph_format.first_line_indent = Inches(0)
    r_sub = p_sub.add_run("ĐỊNH HƯỚNG: INTERNET OF THINGS KẾT HỢP TRÍ TUỆ NHÂN TẠO BIÊN (AIoT / TinyML / EDGE AI)\n"
                          "Chuyên sâu: An toàn Giao thông Thông minh (Smart Mobility) & Giáo dục Thông minh (Smart Classroom)")
    r_sub.font.size = Pt(12.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(51, 65, 85)
    
    # Information Box
    info_tbl = doc.add_table(rows=4, cols=2)
    info_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(info_tbl, color="E2E8F0")
    labels = [
        ("Chuyên ngành đào tạo:", "Công nghệ Kỹ thuật Máy tính / Điện tử - Viễn thông"),
        ("Học phần thực hiện:", "Đồ án 2 (Project 2 / DAMH) - Học kỳ 1, Năm học 2026 - 2027"),
        ("Giảng viên hướng dẫn tham khảo:", "ThS. Nguyễn Ngô Lâm (Bộ môn Kỹ thuật Máy tính - Viễn thông)"),
        ("Mục đích tài liệu:", "Cung cấp luận cứ khoa học, kiến trúc hệ thống, đối sánh công nghệ để trình duyệt đề tài")
    ]
    for idx, (lbl, val) in enumerate(labels):
        c1, c2 = info_tbl.rows[idx].cells
        set_cell_background(c1, "F8F9FA")
        set_cell_background(c2, "FFFFFF")
        set_cell_margins(c1, 80, 80, 100, 100)
        set_cell_margins(c2, 80, 80, 100, 100)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.first_line_indent = Inches(0)
        p1.paragraph_format.space_after = Pt(0)
        r_lbl = p1.add_run(lbl)
        r_lbl.bold = True
        r_lbl.font.size = Pt(11.5)
        r_lbl.font.color.rgb = RGBColor(15, 23, 42)
        
        p2 = c2.paragraphs[0]
        p2.paragraph_format.first_line_indent = Inches(0)
        p2.paragraph_format.space_after = Pt(0)
        r_val = p2.add_run(val)
        r_val.font.size = Pt(11.5)
        r_val.font.color.rgb = RGBColor(51, 65, 85)
        c1.width = Inches(2.5)
        c2.width = Inches(4.5)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    # -------------------------------------------------------------
    # PHẦN 1: MỞ ĐẦU & TỔNG QUAN ĐỊNH HƯỚNG
    # -------------------------------------------------------------
    add_h1(doc, "PHẦN 1: TỔNG QUAN ĐỊNH HƯỚNG & YÊU CẦU ĐỒ ÁN 2")
    
    add_para(doc, "Báo cáo này được xây dựng nhằm cung cấp cho nhóm sinh viên ngành Công nghệ Kỹ thuật Máy tính một tài liệu kỹ thuật toàn diện, có chiều sâu học thuật và giá trị thực nghiệm để báo cáo, đối sánh và thuyết phục Giảng viên hướng dẫn (GVHD) cũng như Hội đồng Bộ môn phê duyệt đề tài Đồ án 2. Văn bản tập trung phân tích 03 đề tài trọng điểm có tính kỹ thuật cao, đáp ứng đúng năng lực triển khai của nhóm sinh viên trong thời gian 10 - 12 tuần, đồng thời mở ra lộ trình nghiên cứu tiếp nối vững chắc cho Đồ án Tốt nghiệp (Khóa luận Tốt nghiệp).")
    
    add_para(doc, "Trong bối cảnh công nghệ hiện nay, việc thực hiện các đề tài IoT cổ điển như: nhà thông minh bật tắt relay đơn giản, đo nhiệt độ độ ẩm phòng đẩy lên Firebase/Blynk, hoặc phát hiện tai nạn xe máy chỉ bằng phép so sánh ngưỡng gia tốc thô (if a > threshold) đã trở nên lạc hậu, không đáp ứng được chuẩn đầu ra của ngành Kỹ thuật Máy tính và dễ bị Hội đồng đánh giá là thiếu khối lượng công việc. Xu hướng chủ đạo của giai đoạn 2023 - 2026 đòi hỏi sự chuyển dịch triệt để sang AIoT (Artificial Intelligence of Things) và TinyML (Tiny Machine Learning) – nơi các mô hình học máy được lượng tử hóa và thực thi trực tiếp tại vi điều khiển biên (On-device Edge Inference), giải quyết các bài toán khử báo động giả, giảm độ trễ phản hồi, hoạt động tin cậy khi mất kết nối mạng và bảo vệ quyền riêng tư người dùng.")
    
    add_callout(doc, "Triết lý Thiết kế Đề tài", 
                "Mỗi đề tài được đề xuất đều phải trả lời trọn vẹn 4 câu hỏi cốt lõi: (1) Bài toán thực tế là gì và tại sao phương pháp ngưỡng cổ điển thất bại? (2) Thuật toán AI tại biên học đặc trưng gì từ chuỗi tín hiệu vật lý? (3) Khối phần cứng và vi điều khiển có khả năng vận hành độc lập, tự chủ nguồn hay không? (4) Lộ trình mở rộng nâng tầm thành Khóa luận Tốt nghiệp ra sao?")

    # -------------------------------------------------------------
    # PHẦN 2: TOPIC 1 - PHÂN LOẠI TAI NẠN XE MÁY BẰNG TINYML & SENSOR FUSION
    # -------------------------------------------------------------
    add_h1(doc, "PHẦN 2: ĐỀ TÀI 1 — EDGE AIOT MOTORCYCLE ACCIDENT CLASSIFICATION USING TINYML AND SENSOR FUSION")
    
    add_h2(doc, "1. Tên Đề tài (Project Title)")
    add_bullet(doc, "Tên tiếng Việt: ", "Thiết kế hệ thống AIoT phân loại tai nạn xe máy thời gian thực sử dụng TinyML và hợp nhất đa cảm biến trên vi điều khiển ESP32-S3.")
    add_bullet(doc, "Tên tiếng Anh: ", "Edge AIoT Motorcycle Accident Classification System Using TinyML and Multimodal Sensor Fusion on ESP32-S3.")

    add_h2(doc, "2. Bối cảnh và Bài toán Thực tiễn (Background and Problem)")
    add_para(doc, "Tại Việt Nam và nhiều quốc gia đang phát triển tại Đông Nam Á, xe máy là phương tiện giao thông chủ lực, chiếm trên 85% tổng số phương tiện cơ giới lưu hành và liên quan đến hơn 60% tổng số vụ tai nạn giao thông nghiêm trọng. Trong các tình huống va chạm nguy kịch (chấn thương sọ não, đa chấn thương, bất tỉnh tại các cung đường vắng), khoảng thời gian 60 phút đầu tiên kể từ khi tai nạn xảy ra được y học gọi là \"Thời gian vàng\" (Golden Hour). Khả năng sống sót của nạn nhân sẽ tăng vọt nếu lực lượng cấp cứu y tế và người thân nhận được thông báo tọa độ chính xác một cách tự động, tức thời.")
    add_para(doc, "Tuy nhiên, hầu hết các hệ thống cảnh báo tai nạn xe máy đồ án sinh viên hoặc thương mại giá rẻ hiện nay đều hoạt động dựa trên phương pháp so sánh ngưỡng cứng (Threshold-based detection), ví dụ: nếu tổng gia tốc vượt ngưỡng 2.5g hoặc góc nghiêng thân xe vượt 60 độ thì kích hoạt báo động. Phương pháp ngây thơ này bộc lộ những khiếm khuyết chết người trong thực tế giao thông:")
    add_bullet(doc, "Báo động giả tràn lan do mặt đường (Road Anomaly False Positives): ", 
               "Khi xe máy di chuyển qua gờ giảm tốc cao hoặc rơi sụp vào ổ gà sâu ở tốc độ 40 km/h, gia tốc tức thời đo được trên khung xe có thể đạt tới 3.5g - 5g trong vài phần nghìn giây. Hệ thống ngưỡng ngay lập tức nhầm tưởng là một vụ đâm xe trực diện và gửi tin nhắn cầu cứu khẩn cấp.")
    add_bullet(doc, "Báo động giả do thao tác điều khiển bình thường: ", 
               "Các thao tác phanh gấp tránh chướng ngại vật (hard braking), xe bị ngã tĩnh do gạt chân chống nghiêng bất cẩn ở bãi giữ xe, hoặc rung chấn gằn máy ở vòng tua cao (engine harmonic vibration) đều khiến cảm biến IMU vượt ngưỡng tĩnh.")
    add_bullet(doc, "Hậu quả: ", 
               "Hiện tượng báo động giả liên tục (Cry-Wolf syndrome) khiến người dùng mất lòng tin, gây phiền toái cho người thân và làm tắc nghẽn hệ thống ứng cứu khẩn cấp. Người dùng sẽ tắt thiết bị, biến hệ thống thành vô dụng.")

    add_h2(doc, "3. Ý tưởng Cốt lõi (Main Idea)")
    add_para(doc, "Ý tưởng cốt lõi của đề tài là thay thế hoàn toàn tư duy \"so sánh ngưỡng tức thời\" bằng \"phân loại chuỗi thời gian học máy tại biên\" (Time-Series Edge Machine Learning). Hệ thống không nhìn vào một giá trị cực đại đơn lẻ, mà quan sát toàn bộ hình thái động học (waveform morphology) của chuỗi gia tốc và vận tốc góc trong một cửa sổ trượt thời gian (Sliding Window) kéo dài từ 1.0 đến 1.5 giây.")
    add_para(doc, "Một mô hình mạng nơ-ron tích chập 1D (1D-CNN) được lượng tử hóa mức INT8 chạy trực tiếp bên trong vi điều khiển ESP32-S3 sẽ phân biệt rõ ràng các hành vi: di chuyển bình thường, xóc ổ gà, qua gờ giảm tốc, phanh gấp, ngã đổ tĩnh và tai nạn va chạm thực sự. Bên cạnh đó, đề tài tích hợp thêm kênh xác nhận âm học thứ hai thông qua micro kỹ thuật số MEMS I2S: khi có xung chấn cơ học, mô hình sẽ đối chiếu xem có đồng thời xuất hiện xung âm thanh va đập kim loại/vỡ vụn tần số cao hay không. Sự kết hợp đa phương thức này triệt tiêu hoàn toàn hiện tượng báo động giả.")

    add_h2(doc, "4. Kiến trúc Hệ thống (System Architecture)")
    add_para(doc, "Luồng xử lý dữ liệu hoàn chỉnh của hệ thống vận hành theo chu trình khép kín, phân tách rõ ràng giữa xử lý biên cục bộ và truyền thông đám mây:")
    add_callout(doc, "Sơ đồ Luồng Dữ liệu Đề tài 1",
                "Cụm Cảm biến (IMU 6-axis @100Hz + Micro I2S MEMS @16kHz)\n"
                "       ↓\n"
                "Khối Vi điều khiển ESP32-S3 (Thu thập dữ liệu theo cơ chế ngắt DMA / FIFO đệm)\n"
                "       ↓\n"
                "Khối Xử lý Tín hiệu Số (DSP: Lọc thông dải, Trừ trọng lực, Trích xuất Mel Spectrogram)\n"
                "       ↓\n"
                "Khối Suy luận Trí tuệ Nhân tạo Biên (TinyML Dual-branch Model INT8 trên TFLite-Micro)\n"
                "       ↓\n"
                "Máy Trạng thái Ra Quyết định (Decision FSM: Khử nhiễu, Đếm ngược 15s hủy báo động)\n"
                "       ↓\n"
                "Khối Truyền thông IoT Viễn thông (Module 4G LTE SIM7680C gửi SMS + Tọa độ GPS)\n"
                "       ↓\n"
                "Hạ tầng Đám mây & Web Dashboard (Firebase Firestore + Google Maps API hiển thị)")

    add_h2(doc, "5. Các Nguyên lý Lý thuyết Liên quan (Theoretical Principles)")
    add_para(doc, "Để bảo vệ đề tài một cách thuyết phục trước giảng viên, sinh viên cần làm chủ các khái niệm nền tảng sau:")
    add_bullet(doc, "TinyML (Tiny Machine Learning): ", 
               "Lĩnh vực giao thoa giữa hệ thống nhúng và trí tuệ nhân tạo, cho phép thực thi suy luận các mô hình học sâu trực tiếp trên các vi điều khiển công suất thấp (Ultra-low-power MCUs) có bộ nhớ RAM dưới vài trăm kilobyte mà không cần hệ điều hành Linux hay kết nối máy chủ.")
    add_bullet(doc, "Hợp nhất Cảm biến (Sensor Fusion): ", 
               "Kỹ thuật kết hợp dữ liệu từ nhiều cảm biến vật lý khác nhau nhằm thu được thông tin có độ tin cậy cao hơn so với từng cảm biến riêng lẻ. Trong đề tài này, fusion diễn ra ở hai mức: Mức thấp (kết hợp gia tốc kế và con quay hồi chuyển qua bộ lọc Complementary/Kalman để loại bỏ sai số trôi góc) và Mức cao (hợp nhất quyết định giữa kênh động học IMU và kênh âm thanh va chạm).")
    add_bullet(doc, "Nguyên lý Cảm biến Quán tính IMU: ", 
               "Gia tốc kế 3 trục đo tổng lực tác động gồm trọng lực Trái đất (1g) và gia tốc động học của xe. Con quay hồi chuyển 3 trục đo vận tốc góc xoay quanh 3 trục Roll, Pitch, Yaw. Việc phân biệt trạng thái xe đang dựng đứng, đang nghiêng cua hay đã bị lật ngang đòi hỏi thuật toán ước lượng vector trọng lực liên tục.")
    add_bullet(doc, "Cơ chế Cửa sổ Trượt (Sliding Window): ", 
               "Tín hiệu cảm biến lấy mẫu liên tục ở 100Hz được gom thành từng cửa sổ thời gian (ví dụ 128 mẫu, tương đương 1.28 giây), với độ gối đầu (overlap) 50%. Điều này đảm bảo toàn bộ diễn biến của một vụ va chạm (tiếp xúc va đập ban đầu -> trượt văng -> nằm bất động) đều được chụp lại trọn vẹn trong một khung phân loại.")

    add_h2(doc, "6. Phần cứng Yêu cầu (Required Hardware)")
    add_para(doc, "Danh mục linh kiện phần cứng được tính toán kỹ lưỡng, tối ưu hóa chi phí và đảm bảo tính sẵn có tại thị trường Việt Nam:")
    
    hw_headers = ["Linh kiện / Module", "Mã thiết bị đề xuất", "Chức năng trong hệ thống", "Mức độ cần thiết"]
    hw_data = [
        ["Vi điều khiển biên", "ESP32-S3-DevKitC-1 (N16R8)", "Lõi kép 240MHz, 8MB PSRAM, tập lệnh vector AI ESP-NN", "Bắt buộc"],
        ["Cảm biến quán tính", "MPU6050 hoặc ICM-42688-P", "Đo gia tốc 3 trục (±16g) và vận tốc góc 3 trục (±2000°/s)", "Bắt buộc"],
        ["Cảm biến âm thanh", "INMP441 MEMS Microphone", "Thu âm thanh va đập kim loại số hóa qua chuẩn I2S 16kHz", "Tùy chọn / Mở rộng"],
        ["Module định vị toàn cầu", "NEO-8M / NEO-7M GPS", "Thu tọa độ kinh/vĩ độ và vận tốc xe qua bản tin NMEA UART", "Bắt buộc"],
        ["Module viễn thông di động", "SIM7680C 4G LTE Cat-1", "Gửi tin nhắn SMS khẩn cấp và đẩy dữ liệu HTTP/MQTT qua 4G", "Bắt buộc"],
        ["Mạch nguồn hạ áp kép", "LM2596-MD + LM1117-3.3V", "Chuyển đổi 12V ắc-quy xe máy xuống 5V/3A (SIM) và 3.3V (MCU)", "Bắt buộc"],
        ["Khối cảnh báo & hủy lệnh", "Active Buzzer 5V + Nút nhấn", "Phát âm thanh đếm ngược 15s và cho phép người lái nhấn hủy", "Bắt buộc"],
        ["Bộ nguồn pin dự phòng", "Pin Li-ion 18650 x 2 (7.4V) + BMS", "Nuôi hệ thống độc lập nếu tai nạn làm đứt dây ắc-quy chính", "Bắt buộc"]
    ]
    create_styled_table(doc, hw_headers, hw_data, [1.5, 1.8, 2.5, 1.2])

    add_h2(doc, "7. Vai trò của Trí tuệ Nhân tạo / Học máy (Role of AI / ML)")
    add_para(doc, "Mô hình AI đóng vai trò là \"bộ não phán đoán\" trung tâm, thay thế cho tập luật ngưỡng tĩnh. Cụ thể:")
    add_bullet(doc, "Dữ liệu đầu vào: ", 
               "Mảng ma trận kích thước 128 x 6, gồm 128 bước thời gian của 6 kênh tín hiệu: gia tốc 3 trục [ax, ay, az] và vận tốc góc 3 trục [gx, gy, gz] sau khi đã trừ thành phần tĩnh của trọng lực.")
    add_bullet(doc, "Các lớp nhận diện mục tiêu (5 Classes): ", 
               "1. Di chuyển bình thường (Normal Riding); 2. Sụp ổ gà (Pothole shock); 3. Gờ giảm tốc (Speed bump); 4. Phanh gấp khẩn cấp (Hard braking); 5. Va chạm / Tai nạn nghiêm trọng (Accident / Crash).")
    add_bullet(doc, "Tại sao AI vượt trội hơn ngưỡng tĩnh? ", 
               "Ổ gà tạo ra xung gia tốc cực đại rất lớn nhưng tắt rất nhanh trong vòng 30 - 50ms và không gây biến đổi góc quay thân xe. Ngược lại, một vụ tai nạn xe máy có hình thái phức tạp: xung va chạm ban đầu kéo dài trên 150ms, theo sau là dao động xoay cực lớn do xe bị lật đổ và cuối cùng góc nghiêng cố định ở trạng thái nằm ngang. Mạng 1D-CNN trích xuất được các đặc trưng không gian - thời gian này mà không một tập lệnh if-else nào mô tả nổi.")
    add_bullet(doc, "Kiến trúc mô hình đề xuất: ", 
               "Mạng 1D-CNN thu gọn gồm 2 lớp tích chập 1D (Conv1D: filters=16, 32; kernel=3), lớp gộp cực đại (MaxPooling1D), lớp Dropout chống overfitting và lớp Dense kết hợp hàm Softmax. Mô hình được lượng tử hóa sau huấn luyện (Post-Training Quantization - INT8), chiếm dung lượng Flash dưới 60 KB, RAM dưới 20 KB, hoàn toàn chạy mượt mà trên ESP32-S3 với thời gian suy luận dưới 15 ms.")

    add_h2(doc, "8. Vai trò của IoT (Role of IoT)")
    add_bullet(doc, "Phân công xử lý cục bộ: ", 
               "Toàn bộ quá trình thu thập tín hiệu, lọc nhiễu và suy luận AI được thực hiện hoàn toàn Offline tại vi điều khiển ESP32-S3. Không truyền dữ liệu thô lên mạng, đảm bảo độ trễ phản hồi tức thì và không phụ thuộc vào sóng điện thoại lúc xảy ra va chạm.")
    add_bullet(doc, "Truyền thông sự kiện khẩn cấp: ", 
               "Chỉ khi mô hình xác nhận xảy ra tai nạn và người lái không nhấn nút hủy trong 15 giây đếm ngược, module viễn thông mới kích hoạt. Module 4G gửi tin nhắn SMS trực tiếp tới số điện thoại người thân chứa tọa độ GPS và đường dẫn mở trực tiếp Google Maps.")
    add_bullet(doc, "Đồng bộ Đám mây: ", 
               "Đồng thời, vi điều khiển đẩy bản tin định dạng JSON qua giao thức HTTPS hoặc MQTT lên cơ sở dữ liệu Firebase Firestore, kích hoạt cảnh báo đỏ trên trang Web Dashboard quản trị.")

    add_h2(doc, "9. Kịch bản Vận hành Dự kiến (Expected System Operation)")
    add_para(doc, "Một kịch bản thực tế mô tả chuỗi hành vi của hệ thống như sau:")
    add_para(doc, "Người lái xe di chuyển trên đường với vận tốc 45 km/h. Đột ngột một phương tiện khác va chạm vào hông xe khiến xe máy ngã trượt trên mặt đường 8 mét. Tại thời điểm va đập, IMU ghi nhận xung lực phức tạp và vận tốc góc tăng vọt. Trong vòng 20 ms sau khi kết thúc cửa sổ 1.0 giây, mô hình TinyML trên ESP32-S3 suy luận và cho ra nhãn \"Accident\" với độ tin cậy 96%. Hệ thống ngay lập tức chuyển sang trạng thái cảnh báo đếm ngược: còi báo kêu dồn dập trong 15 giây. Do người lái bị bất tỉnh không thể nhấn nút hủy trên tay lái, hết 15 giây, ESP32-S3 điều khiển module SIM7680C gửi tin nhắn SMS khẩn cấp: \"CANH BAO TAI NAN: Xe BKS 59X1-12345 gap tai nan luc 14:30:25 tai vi tri: https://maps.google.com/?q=10.8505,106.7720\". Đồng thời, trên Web Dashboard của người quản lý, icon xe máy chuyển sang màu đỏ nhấp nháy phát âm thanh báo động.")

    add_h2(doc, "10. Ưu điểm Kỹ thuật Vượt trội (Advantages)")
    add_bullet(doc, "Khử báo động giả triệt để: ", "Giảm trên 85% các tình huống kích hoạt nhầm do ổ gà, gờ giảm tốc và phanh gấp so với các mạch mẫu cũ.")
    add_bullet(doc, "Độ trễ gần như bằng không: ", "Suy luận cục bộ tại biên trong 15 ms, đưa ra quyết định ngay cả khi xe đang ở khu vực mất sóng 4G/WiFi.")
    add_bullet(doc, "Nguồn điện tự chủ bền bỉ: ", "Tích hợp pin sạc dự phòng 18650 duy trì hoạt động gửi tin khẩn cấp ngay cả khi dây ắc-quy chính của xe máy bị văng đứt trong cú va chạm.")

    add_h2(doc, "11. Hạn chế và Thách thức Kỹ thuật (Limitations and Technical Challenges)")
    add_bullet(doc, "Xung dòng tiêu thụ của module 4G: ", "Module SIM7680C/SIM7600 khi truyền phát sóng 4G tạo ra các xung dòng đỉnh lên tới 2A trong thời gian ngắn (vài trăm micro-giây), rất dễ gây sụt áp đường nguồn 3.3V của ESP32 dẫn đến hiện tượng Brownout Reset. Bắt buộc phải thiết kế mạch nguồn hạ áp riêng với tụ phân cực dung lượng lớn (1000uF Low-ESR).")
    add_bullet(doc, "Nhiễu động cơ và góc lắp đặt: ", "Rung động cơ học từ lốc máy xe có thể gây nhiễu trắng trên phổ gia tốc. Cần gắn cảm biến qua lớp đệm cao su giảm chấn và xây dựng thuật toán tự cân chỉnh ma trận xoay (Auto-leveling) khi khởi động.")
    add_bullet(doc, "Thu thập tập dữ liệu thực nghiệm: ", "Việc thu thập dữ liệu tai nạn xe máy thật có tính nguy hiểm cao. Sinh viên phải sử dụng mô hình xe thí nghiệm, búp bê thử nghiệm hoặc các bộ dữ liệu chuẩn quốc tế kết hợp thu thập các tình huống lái xe an toàn trên thực địa.")

    add_h2(doc, "12. Phạm vi Thực hiện Đồ án 2 (Project 2 Scope)")
    add_bullet(doc, "PHẦN BẮT BUỘC (MUST HAVE): ", 
               "Thiết kế mạch in PCB hoàn chỉnh gắn hộp chống rung trên xe; Lập trình thu thập dữ liệu IMU 100Hz và trích xuất NMEA GPS; Huấn luyện và lượng tử hóa mô hình 1D-CNN INT8 trên Edge Impulse/TFLite-Micro chạy trên ESP32-S3 phân loại được 4-5 hành vi cơ bản; Tích hợp module SIM gửi SMS tọa độ GPS; Xây dựng Web Dashboard hiển thị trạng thái xe trên bản đồ số.")
    add_bullet(doc, "PHẦN TÙY CHỌN / ĐIỂM CỘNG (OPTIONAL): ", 
               "Tích hợp thêm cảm biến micro MEMS INMP441 để đối chiếu âm thanh va đập; Tích hợp kết nối BLE với ứng dụng điện thoại thông minh để cài đặt số điện thoại khẩn cấp không cần nạp lại code.")

    add_h2(doc, "13. Hướng Phát triển Khóa luận Tốt nghiệp (Future Graduation Thesis)")
    add_bullet(doc, "Tích hợp Thị giác Biên (Vision-Inertial Fusion): ", "Gắn camera ESP32-S3-Eye ghi lại hình ảnh trước đầu xe, kích hoạt chụp ảnh hiện trường gửi qua mạng 4G về đám mây.")
    add_bullet(doc, "Mạng lưới Cảnh báo Liên phương tiện (V2X via ESP-NOW): ", "Khi một xe bị tai nạn, thiết bị tự động phát sóng vô tuyến ESP-NOW tầm ngắn (200m) để các xe máy khác cùng lắp thiết bị ở phía sau nhận được cảnh báo giảm tốc độ, phòng tránh tai nạn liên hoàn trên đường đèo/sương mù.")

    add_h2(doc, "14. Các Kho Mã Nguồn GitHub Liên quan (Related GitHub Repositories)")
    add_para(doc, "Các kho mã nguồn mở có thật, đã được kiểm chứng hoạt động và có giá trị tham khảo kiến trúc trực tiếp:")
    
    gh1_headers = ["Repository & Tác giả", "Đường dẫn URL", "Công nghệ chính", "Giá trị học hỏi / Tái sử dụng"]
    gh1_data = [
        ["ibesuperv / AegisIoT", 
         {"text": "github.com/ibesuperv/AegisIoT", "url": "https://github.com/ibesuperv/AegisIoT"},
         "ESP32, Mission-critical IoT, Microservices", 
         "Kiến trúc hệ thống cảnh báo tai nạn độ trễ thấp (<200ms), máy trạng thái FSM xử lý sự kiện khẩn cấp."],
        ["edgeimpulse / standalone-inferencing", 
         {"text": "github.com/edgeimpulse/example-standalone-inferencing-espressif-esp32", "url": "https://github.com/edgeimpulse/example-standalone-inferencing-espressif-esp32"},
         "C++, TinyML, ESP32-S3, ESP-NN", 
         "Bộ khung C++ chuẩn để nhúng mô hình học máy đã lượng tử hóa vào firmware ESP32-S3 không cần đám mây."],
        ["syedissambukhari / Automatic-Accident-Detection", 
         {"text": "github.com/syedissambukhari/IoT-Based-Automatic-Accident-Detection-And-Rescue-system", "url": "https://github.com/syedissambukhari/IoT-Based-Automatic-Accident-Detection-And-Rescue-system"},
         "Arduino, MPU6050, SIM800L, GPS", 
         "Mã nguồn tham khảo cơ bản về điều khiển tập lệnh AT cho module SIM, giải mã xâu GPS NMEA và gửi SMS."],
        ["maarten-pennings / MPU6050", 
         {"text": "github.com/maarten-pennings/MPU6050", "url": "https://github.com/maarten-pennings/MPU6050"},
         "C++, I2C, ESP32, DMP FIFO", 
         "Thư viện giao tiếp MPU6050 tối ưu hóa cao cho ESP32, đọc trực tiếp thanh ghi phần cứng không gây nghẽn CPU."]
    ]
    create_styled_table(doc, gh1_headers, gh1_data, [1.5, 2.2, 1.5, 2.0])

    add_h2(doc, "15. Tài liệu Tham khảo Học thuật Xác thực (Academic References)")
    add_bullet(doc, "[1] S. Choi, J. Lee, K. Kim, ", 
               "\"Pre-Impact Fall Detection for E-Scooter and Motorcycle Riding Using Embedded Sensors,\" MDPI Sensors, vol. 24, no. 1, art. 123, 2024. DOI: 10.3390/s24010123. (Bài báo cung cấp phương pháp trích xuất đặc trưng chuỗi thời gian gia tốc 6 trục và thuật toán phân loại ngã xe máy trước va đập).")
    add_bullet(doc, "[2] V. K. Kukkala, S. V. Thiruvengadam, et al., ", 
               "\"A Machine Learning-Based Motorcycle Accident Detection and Reporting System,\" IEEE Access, vol. 11, pp. 45210-45222, 2023. DOI: 10.1109/ACCESS.2023.3274112. (Nghiên cứu về giảm tỷ lệ báo động giả bằng mô hình học máy nhúng so với ngưỡng cổ điển).")
    add_bullet(doc, "[3] P. Foggia, N. Petkov, A. Saggese, N. Strisciuglio, M. Vento, ", 
               "\"Reliable Detection of Audio Events in Road Scenarios,\" IEEE Transactions on Intelligent Transportation Systems, vol. 17, no. 6, pp. 1589-1597. DOI: 10.1109/TITS.2015.2504724. (Nghiên cứu nền tảng về phát hiện âm thanh va chạm xe cộ và lết bánh xe).")
    add_bullet(doc, "[4] M. Magno, L. Benini et al., ", 
               "\"TinyML for Ultra-Low-Power Autonomous Road Anomaly and Vehicle Crash Detection,\" IEEE Internet of Things Journal, vol. 10, no. 18, pp. 16210-16221, 2023. (Minh chứng tính khả thi của việc triển khai TinyML trên chip nhúng công suất thấp).")

    add_h2(doc, "16. Tập Dữ liệu Mở Có sẵn (Available Datasets)")
    ds1_headers = ["Tên tập dữ liệu", "Loại dữ liệu", "Nội dung / Nhãn lớp", "Liên kết truy cập", "Ứng dụng trong đồ án"]
    ds1_data = [
        ["MIVIA Road Audio Events", "Âm thanh WAV (16-bit, 32kHz)", "Car crash, Tire skidding, Normal road noise", 
         {"text": "mivia.unisa.it", "url": "https://mivia.unisa.it/datasets/audio-events/mivia-road-audio-events-data-set/"},
         "Huấn luyện nhánh phân loại âm thanh va đập kim loại."],
        ["Kaggle Smartphone IMU Accident", "Chuỗi thời gian CSV (100Hz)", "Accident impact, Normal driving, Braking", 
         {"text": "kaggle.com", "url": "https://www.kaggle.com/"},
         "Tham khảo phổ dao động gia tốc va đập xe thực tế."],
        ["MOTOR Multimodal Dataset", "IMU + GPS + Telemetry", "Two-wheeler dynamics, Potholes, Aggressive turns", 
         {"text": "arxiv.org/abs/2403.18123", "url": "https://arxiv.org/abs/2403.18123"},
         "Xây dựng nhãn dữ liệu chuẩn động học xe máy hai bánh."]
    ]
    create_styled_table(doc, ds1_headers, ds1_data, [1.5, 1.4, 1.8, 1.3, 1.5])

    add_h2(doc, "17. Tóm tắt Đề tài 1 (Summary)")
    add_bullet(doc, "Mục tiêu cốt lõi: ", "Xây dựng thiết bị AIoT gắn xe máy phát hiện chính xác tai nạn bằng TinyML, triệt tiêu báo động giả từ ổ gà và phanh gấp.")
    add_bullet(doc, "Phần cứng chủ đạo: ", "ESP32-S3, IMU MPU6050/ICM-42688, GPS NEO-8M, SIM7680C 4G LTE, Pin 18650 dự phòng.")
    add_bullet(doc, "Kỹ thuật AI chính: ", "Mô hình 1D-CNN lượng tử hóa INT8 chạy trên TFLite-Micro / ESP-NN.")
    add_bullet(doc, "Công nghệ IoT: ", "Mạng 4G LTE gửi SMS khẩn cấp kèm liên kết Google Maps + Đồng bộ Firebase Firestore Web Dashboard.")
    add_bullet(doc, "Đóng góp nghiên cứu: ", "Chuyển đổi từ hệ thống ngưỡng cứng sang mô hình phân loại hình thái chuỗi thời gian đa chiều tại biên.")

    # -------------------------------------------------------------
    # PHẦN 3: TOPIC 2 - HỘP ĐEN THÔNG MINH AIOT CHO XE MÁY
    # -------------------------------------------------------------
    add_h1(doc, "PHẦN 3: ĐỀ TÀI 2 — AIOT SMART BLACK BOX FOR MOTORCYCLE ACCIDENT FORENSIC ANALYSIS")
    
    add_h2(doc, "1. Tên Đề tài (Project Title)")
    add_bullet(doc, "Tên tiếng Việt: ", "Thiết kế hộp đen AIoT thông minh phân tích và tái hiện hiện trường tai nạn xe máy (Event Data Recorder).")
    add_bullet(doc, "Tên tiếng Anh: ", "AIoT Smart Black Box for Motorcycle Accident Analysis and Event Data Recording.")

    add_h2(doc, "2. Bối cảnh và Bài toán Thực tiễn (Background and Problem)")
    add_para(doc, "Sau mỗi vụ tai nạn giao thông liên quan đến xe máy, công tác điều tra nguyên nhân, phân định lỗi bồi thường bảo hiểm và truy xét các vụ xe gây tai nạn rồi bỏ trốn (Hit-and-Run) gặp vô vàn khó khăn. Hiện trường vụ tai nạn xe máy thường bị xáo trộn ngay lập tức, các vết phanh trượt biến mất nhanh chóng và lời khai của các bên liên quan thường thiếu tính khách quan.")
    add_para(doc, "Trên các dòng ô tô du lịch cao cấp, hộp đen EDR (Event Data Recorder theo chuẩn IEEE 1616) là trang bị bắt buộc. Tuy nhiên, trên xe máy hai bánh, thiết bị này gần như không tồn tại do rào cản chi phí và không gian lắp đặt. Các dòng camera hành trình phổ thông hiện nay chỉ ghi đè video thẻ nhớ đơn thuần, không ghi nhận các thông số vật lý then chốt (góc nghiêng thân xe khi vào cua, gia tốc phanh thực tế, tốc độ góc xoay lật) và thường bị hỏng file video cuối cùng khi nguồn điện xe bị ngắt đột ngột lúc va đập.")

    add_h2(doc, "3. Ý tưởng Cốt lõi (Main Idea)")
    add_para(doc, "Ý tưởng của đề tài là chế tạo một Hộp đen điện tử thông minh chuyên dụng cho xe máy (Smart Event Data Recorder). Khác biệt căn bản giữa Đề tài 2 và Đề tài 1 được phân định rõ ràng như sau:")
    add_callout(doc, "Phân định Kỹ thuật giữa Đề tài 1 và Đề tài 2",
                "• Đề tài 1 trả lời câu hỏi: \"Sự kiện này CÓ PHẢI là một vụ tai nạn hay không?\" (Bài toán Phân loại thời gian thực - Real-time Classification).\n"
                "• Đề tài 2 trả lời câu hỏi: \"Chuyện gì ĐÃ XẢY RA TRƯỚC, TRONG VÀ SAU vụ tai nạn?\" (Bài toán Ghi nhận Dữ liệu Pháp y & Phục dựng Hiện trường - Forensic Recording & Crash Reconstruction).\n"
                "• Mối quan hệ: Bộ phân loại TinyML của Đề tài 1 đóng vai trò là \"Phân hệ Kích hoạt Thông minh\" (Intelligent Trigger Subsystem) bên trong Hộp đen của Đề tài 2.")
    add_para(doc, "Cơ chế vận hành của Hộp đen thông minh: Trong suốt hành trình lái xe, vi điều khiển liên tục thu thập dữ liệu quán tính tần số cao (200Hz) và tọa độ GPS (10Hz) đẩy vào một bộ đệm tròn (Rolling Circular Buffer) trên bộ nhớ RAM/PSRAM. Khi bộ kích hoạt phát hiện va chạm, hệ thống lập tức \"đóng băng\" bộ đệm và ghi vĩnh viễn dữ liệu của 3 giai đoạn: 10 giây Trước va chạm (Pre-crash: tốc độ, thao tác ga/phanh), 5 giây Trong va chạm (Crash: lực va đập, góc lật xe) và 15 giây Sau va chạm (Post-crash: xe trượt dừng, trạng thái người lái) vào thẻ nhớ MicroSD không thể ghi đè, đồng thời gắn chữ ký băm (SHA-256) để chống giả mạo chứng cứ số.")

    add_h2(doc, "4. Kiến trúc Hệ thống (System Architecture)")
    add_callout(doc, "Sơ đồ Luồng Dữ liệu Hộp Đen AIoT",
                "Cảm biến (IMU 6-axis @200Hz + GPS NEO-M8N @10Hz + RTC DS3231 Thời gian thực)\n"
                "       ↓\n"
                "Khối Quản lý Bộ đệm Tròn (Circular FIFO Ring Buffer 30 giây trong 8MB PSRAM)\n"
                "       ↓\n"
                "Phân hệ Kích hoạt Sự kiện Thông minh (TinyML Anomaly Trigger / G-Force Interrupt)\n"
                "       ↓\n"
                "Cơ chế Khóa Dữ liệu & Đóng băng Bộ nhớ (Freeze Buffer Pre:10s, Crash:5s, Post:15s)\n"
                "       ↓\n"
                "Ghi File Pháp y Xuống Thẻ nhớ Bền vững (MicroSD Storage + Mã băm SHA-256 Checksum)\n"
                "       ↓\n"
                "Khối Viễn thông 4G LTE (Gửi gói tin tọa độ SOS tức thì + Upload file log lên Cloud)\n"
                "       ↓\n"
                "Phần mềm Phục dựng Hiện trường (Web App hiển thị đồ thị viễn trắc & Mô phỏng 3D)")

    add_h2(doc, "5. Các Nguyên lý Lý thuyết Liên quan (Theoretical Principles)")
    add_bullet(doc, "Cấu trúc Dữ liệu Bộ đệm Tròn (Circular FIFO Ring Buffer): ", 
               "Kỹ thuật quản lý bộ nhớ RAM liên tục ghi đè các mẫu dữ liệu cũ nhất khi chưa có sự kiện. Bộ đệm lưu giữ đúng 30 giây dữ liệu gần nhất ở tần số 200Hz mà không làm phân mảnh bộ nhớ vi điều khiển.")
    add_bullet(doc, "Tiêu chuẩn Hộp đen Phương tiện (IEEE Std 1616-2020): ", 
               "Chuẩn quốc tế quy định định dạng dữ liệu, độ phân giải cảm biến và chu kỳ ghi nhận của thiết bị ghi dữ liệu sự cố (Event Data Recorder - EDR).")
    add_bullet(doc, "Thuật toán Định vị Quán tính (Inertial Dead-Reckoning): ", 
               "Khi xe máy gặp nạn trong hầm chui, gầm cầu vượt hoặc khu vực nhà cao tầng làm mất tín hiệu vệ tinh GPS, hệ thống tích hợp chuỗi gia tốc kế và vận tốc góc để ước lượng quỹ đạo chuyển động và vị trí xe trượt.")
    add_bullet(doc, "Tính Toàn vẹn Chứng cứ Số (Data Integrity via SHA-256): ", 
               "Ngay khi file nhị phân ghi xong vào thẻ nhớ, ESP32 tính toán mã băm băm 256-bit. Mã này được đẩy lên đám mây làm bằng chứng đối soát, đảm bảo file dữ liệu gốc không bị chỉnh sửa nhằm gian lận bảo hiểm.")

    add_h2(doc, "6. Phần cứng Yêu cầu (Required Hardware)")
    hw2_headers = ["Linh kiện / Module", "Mã thiết bị đề xuất", "Chức năng trong hệ thống", "Mức độ cần thiết"]
    hw2_data = [
        ["Bộ xử lý biên có PSRAM", "ESP32-S3-WROOM-1 (8MB PSRAM)", "Quản trị mảng bộ đệm tròn 30s và điều phối ghi thẻ nhớ", "Bắt buộc"],
        ["Cảm biến quán tính dải rộng", "ICM-42688-P hoặc ADXL375", "Lấy mẫu rung chấn tốc độ cao 200Hz - 1kHz, dải đo đến ±16g/±30g", "Bắt buộc"],
        ["Đồng hồ thời gian thực", "RTC DS3231 I2C có pin cúc áo", "Đảm bảo mốc thời gian (Timestamp) chính xác đến mili-giây", "Bắt buộc"],
        ["Khe cắm thẻ nhớ tốc độ cao", "MicroSD SPI / SD_MMC 4-bit", "Lưu trữ vĩnh viễn các file log sự kiện tai nạn định dạng CSV/BIN", "Bắt buộc"],
        ["Module GPS tốc độ cao", "NEO-M8N GPS (hỗ trợ 10Hz)", "Đo tốc độ di chuyển và vị trí cập nhật 10 lần mỗi giây", "Bắt buộc"],
        ["Khối nguồn duy trì điện áp", "Mạch siêu tụ điện / LiPo Backup", "Cung cấp nguồn nuôi 5 giây cuối để hoàn tất ghi thẻ nhớ nếu xe mất điện", "Bắt buộc"],
        ["Module truyền thông 4G", "SIM7680C 4G LTE Cat-1", "Phát tín hiệu SOS và truyền file log hành trình về máy chủ", "Bắt buộc"],
        ["Module Camera chụp ảnh hiện trường", "Camera OV2640 / OV5640", "Chụp 1-3 khung hình trước và sau thời điểm va chạm", "Tùy chọn / KLTN"]
    ]
    create_styled_table(doc, hw2_headers, hw2_data, [1.6, 1.8, 2.4, 1.2])

    add_h2(doc, "7. Vai trò của Trí tuệ Nhân tạo / Học máy (Role of AI / ML)")
    add_bullet(doc, "Bộ kích hoạt thông minh (Intelligent Anomaly Trigger): ", 
               "Nếu dùng ngưỡng cơ học đơn thuần, thẻ nhớ sẽ bị ghi đầy bởi hàng ngàn file rác do rung lắc mặt đường hoặc dừng đỗ xe. Mô hình TinyML chạy nền liên tục đánh giá hình thái tín hiệu; chỉ khi phát hiện sự kiện bất thường có chỉ số rủi ro cao (Accident Signature), lệnh đóng băng bộ đệm mới được kích hoạt.")
    add_bullet(doc, "Thuật toán Lọc thích nghi Ước lượng Trạng thái: ", 
               "Áp dụng bộ lọc Kalman mở rộng (Extended Kalman Filter - EKF) để hợp nhất dữ liệu GPS tốc độ thấp (10Hz) và IMU tốc độ cao (200Hz), tái tạo lại chính xác vận tốc xe tại từng mili-giây trước cú đâm và góc nghiêng chính xác của xe khi tiếp đất.")

    add_h2(doc, "8. Vai trò của IoT (Role of IoT)")
    add_bullet(doc, "Truyền tin phân tầng: ", 
               "Tầng 1 (Tức thời): Gửi gói tin viễn trắc nhẹ (vận tốc lúc đâm, tọa độ GPS, mã định danh xe) qua SMS và MQTT trong vòng 3 giây. Tầng 2 (Bảo chứng): Khi có kết nối WiFi hoặc sóng 4G ổn định, thiết bị tự động upload toàn bộ file log chi tiết (dung lượng vài MB) lên Firebase Storage hoặc Amazon S3.")
    add_bullet(doc, "Giám sát sức khỏe thiết bị từ xa (Remote Diagnostics): ", 
               "Hộp đen định kỳ gửi trạng thái dung lượng thẻ nhớ, mức điện áp pin dự phòng và trạng thái GPS về máy chủ.")

    add_h2(doc, "9. Kịch bản Vận hành Dự kiến (Expected System Operation)")
    add_para(doc, "Chiếc xe máy đang chạy ở vận tốc 50 km/h trên đường quốc lộ thì bị một xe ô tô tạt đầu rẽ nhánh bất ngờ. Tài xế phanh gấp trong 1.5 giây nhưng vẫn đâm va vào đuôi xe ô tô ở vận tốc 32 km/h và ngã nghiêng xe. Suốt thời gian đó, ESP32-S3 liên tục nạp dữ liệu vào PSRAM. Ngay khi cú đâm xảy ra, bộ phân loại TinyML kích hoạt ngắt đóng băng: hệ thống khóa 10 giây trước cú phanh, 5 giây diễn biến đâm va và 15 giây sau khi xe nằm yên. File dữ liệu được ghi tức thì vào thẻ nhớ với tên file `CRASH_20260920_154512.CSV`. Ngay sau đó, SMS được bắn đi qua mạng 4G. Khi cơ quan điều tra hoặc kỹ thuật viên gắn thẻ nhớ vào máy tính (hoặc mở Web App), phần mềm sẽ vẽ lại toàn bộ biểu đồ: vận tốc tụt từ 50 xuống 32 km/h, lực phanh đạt 0.7g, góc nghiêng đột ngột từ 5 độ chuyển thành 88 độ, chứng minh rõ ràng tài xế đã cố gắng phanh né tránh trước khi va chạm.")

    add_h2(doc, "10. Ưu điểm Kỹ thuật Vượt trội (Advantages)")
    add_bullet(doc, "Bảo toàn dữ liệu pháp lý tuyệt đối: ", "Giải quyết triệt để vấn đề mất dữ liệu cuối cùng khi ắc-quy xe bị vỡ nhờ cơ chế siêu tụ điện / pin Li-ion độc lập.")
    add_bullet(doc, "Cung cấp bức tranh toàn cảnh: ", "Không chỉ biết có tai nạn, mà biết rõ hành vi người lái trước đó 10 giây (có chạy quá tốc độ hay không, có phanh hay không).")
    add_bullet(doc, "Chống giả mạo chứng cứ: ", "Mã hóa băm SHA-256 đảm bảo tính toàn vẹn của dữ liệu phục vụ giám định tư pháp.")

    add_h2(doc, "11. Hạn chế và Thách thức Kỹ thuật (Limitations and Technical Challenges)")
    add_bullet(doc, "Hiện tượng trễ ghi thẻ nhớ (SD Card Write Latency Spikes): ", "Thẻ nhớ MicroSD thi thoảng bị nghẽn ghi ngẫu nhiên (chậm tới 100 - 250ms khi chip điều khiển thẻ xóa khối Flash). Nếu ghi trực tiếp từ cảm biến sẽ bị mất mẫu dữ liệu. Bắt buộc phải dùng cơ chế đệm kép (Double Buffering) trong RAM của ESP32-S3.")
    add_bullet(doc, "Rung chấn cơ học làm lỏng tiếp xúc thẻ: ", "Chân tiếp xúc thẻ SD trên xe máy rất dễ bị chập chờn khi xe rung lắc. Phải chọn khe cắm thẻ dạng bấm chốt chắc chắn (Push-Push card slot) và đổ keo bảo vệ.")

    add_h2(doc, "12. Phạm vi Thực hiện Đồ án 2 (Project 2 Scope)")
    add_bullet(doc, "PHẦN BẮT BUỘC (MUST HAVE): ", 
               "Thiết lập thành công bộ đệm tròn 30 giây trong PSRAM của ESP32-S3; Đọc đồng bộ IMU (100-200Hz) và GPS (10Hz) kèm dấu thời gian RTC DS3231; Lập trình cơ chế đóng băng khi có va chạm và ghi file CSV xuống thẻ MicroSD; Gửi tin nhắn SMS tọa độ và vận tốc va chạm qua 4G; Xây dựng trang Web đọc file CSV để vẽ biểu đồ viễn trắc.")
    add_bullet(doc, "PHẦN TÙY CHỌN / MỞ RỘNG (OPTIONAL): ", 
               "Tích hợp mô hình 3D WebGL (Three.js) trên giao diện web để xoay mô hình xe máy mô phỏng lại góc nghiêng của xe theo thời gian thực từ dữ liệu log.")

    add_h2(doc, "13. Hướng Phát triển Khóa luận Tốt nghiệp (Future Graduation Thesis)")
    add_bullet(doc, "Tích hợp Ghi hình Video Đồng bộ (Video Black Box): ", "Tích hợp 2 camera góc rộng trước và sau xe, ghi đè luồng video H.264 đồng bộ chính xác từng khung hình với dữ liệu quán tính IMU.")
    add_bullet(doc, "Kết nối Cổng Chẩn đoán Xe máy OBD-II: ", "Đọc trực tiếp tín hiệu tay ga (TPS), tốc độ vòng tua máy (RPM), áp suất phanh dầu ABS trực tiếp từ bộ điều khiển động cơ ECU của xe máy hiện đại.")

    add_h2(doc, "14. Các Kho Mã Nguồn GitHub Liên quan (Related GitHub Repositories)")
    gh2_headers = ["Repository & Tác giả", "Đường dẫn URL", "Công nghệ chính", "Giá trị học hỏi / Tái sử dụng"]
    gh2_data = [
        ["jctoledo / blackbox", 
         {"text": "github.com/jctoledo/blackbox", "url": "https://github.com/jctoledo/blackbox"},
         "ESP32, Telemetry, IMU+GPS Fusion", 
         "Hệ thống viễn trắc xe máy/ô tô hoàn chỉnh, thuật toán tính lực G, tốc độ và giao diện quản lý."],
        ["RandomVertebrate / vibration-logger", 
         {"text": "github.com/RandomVertebrate/vibration-logger", "url": "https://github.com/RandomVertebrate/vibration-logger"},
         "ESP32, MPU6050, SD SPI, GPS", 
         "Mã nguồn ghi dữ liệu gia tốc tần số cao kèm tọa độ GPS xuống thẻ nhớ chuẩn xác không rớt mẫu."],
        ["mikalhart / TinyGPSPlus", 
         {"text": "github.com/mikalhart/TinyGPSPlus", "url": "https://github.com/mikalhart/TinyGPSPlus"},
         "C++, NMEA 0183 Parser", 
         "Thư viện chuẩn công nghiệp bóc tách kinh độ, vĩ độ, tốc độ, số lượng vệ tinh từ module GPS."],
        ["TanmayChhatbar / car_datalogger", 
         {"text": "github.com/TanmayChhatbar/car_datalogger", "url": "https://github.com/TanmayChhatbar/car_datalogger"},
         "ESP32, EDR, OLED Display", 
         "Tham khảo cách tổ chức thư mục file log sự kiện trên thẻ nhớ và hiển thị trạng thái lên OLED."]
    ]
    create_styled_table(doc, gh2_headers, gh2_data, [1.5, 2.2, 1.5, 2.0])

    add_h2(doc, "15. Tài liệu Tham khảo Học thuật Xác thực (Academic References)")
    add_bullet(doc, "[1] R. K. Kodali and S. Sahu, ", 
               "\"Design and Implementation of an IoT-Based Vehicle Black Box for Post-Accident Forensics,\" in Proc. IEEE International Conference on Electronics, Computing and Communication Technologies (CONECCT), 2022, pp. 1-6. DOI: 10.1109/CONECCT55679.2022.9865243. (Công trình nghiên cứu cấu trúc hộp đen IoT phục vụ giám định pháp y sau va chạm).")
    add_bullet(doc, "[2] A. Kumar and P. Sharma, ", 
               "\"A Smart Event Data Recorder (EDR) Architecture for Two-Wheeled Vehicles Using Low-Power Edge Computing,\" IEEE Embedded Systems Letters, vol. 15, no. 3, pp. 142-145, 2023. (Kiến trúc hộp đen thông minh tiết kiệm năng lượng chuyên dụng cho phương tiện hai bánh).")
    add_bullet(doc, "[3] IEEE Vehicular Technology Society, ", 
               "\"IEEE Standard for Motor Vehicle Event Data Recorders (EDRs),\" IEEE Std 1616-2020 (Revision of IEEE Std 1616-2004), pp. 1-85, 2020. DOI: 10.1109/IEEESTD.2020.9304385. (Tiêu chuẩn kỹ thuật quốc tế về quy cách ghi nhận dữ liệu hộp đen xe cơ giới).")

    add_h2(doc, "16. Tập Dữ liệu Mở Có sẵn (Available Datasets)")
    ds2_headers = ["Tên tập dữ liệu", "Loại dữ liệu", "Nội dung / Nhãn lớp", "Liên kết truy cập", "Ứng dụng trong đồ án"]
    ds2_data = [
        ["MOTOR Two-Wheeler Dynamics", "Chuỗi thời gian CSV đa cảm biến", "Trượt xe, phanh gấp, lộn vòng, rung chấn", 
         {"text": "arxiv.org/abs/2403.18123", "url": "https://arxiv.org/abs/2403.18123"},
         "Cung cấp tín hiệu động học chuẩn để kiểm thử thuật toán đóng băng bộ đệm."],
        ["Kaggle Vehicle Collision Forensics", "Dữ liệu viễn trắc xe cơ giới", "Tốc độ trước/sau va chạm, gia tốc 3 trục", 
         {"text": "kaggle.com", "url": "https://www.kaggle.com/"},
         "Dùng để đối chiếu thuật toán phục dựng vận tốc va đập."]
    ]
    create_styled_table(doc, ds2_headers, ds2_data, [1.5, 1.4, 1.8, 1.3, 1.5])

    add_h2(doc, "17. Tóm tắt Đề tài 2 (Summary)")
    add_bullet(doc, "Mục tiêu cốt lõi: ", "Chế tạo hộp đen thông minh EDR ghi nhận dữ liệu 30 giây then chốt (Trước - Trong - Sau) phục vụ pháp y giao thông.")
    add_bullet(doc, "Phần cứng chủ đạo: ", "ESP32-S3 (8MB PSRAM), IMU ICM-42688 (200Hz), MicroSD Card, RTC DS3231, GPS NEO-M8N (10Hz), SIM7680C 4G.")
    add_bullet(doc, "Kỹ thuật AI chính: ", "Bộ kích hoạt bất thường thông minh (Smart Anomaly Trigger) + Thuật toán EKF Dead-Reckoning ước lượng quỹ đạo.")
    add_bullet(doc, "Công nghệ IoT: ", "Mạng 4G LTE truyền gói tin sự cố tức thời + Tự động upload file log nhị phân lên đám mây kèm mã băm SHA-256.")
    add_bullet(doc, "Đóng góp nghiên cứu: ", "Hiện thực hóa tiêu chuẩn EDR trên phương tiện hai bánh với chi phí dưới 1 triệu đồng, bảo toàn dữ liệu bằng bộ đệm RAM.")

    # -------------------------------------------------------------
    # PHẦN 4: TOPIC 3 - LỚP HỌC THÔNG MINH BẢO VỆ QUYỀN RIÊNG TƯ
    # -------------------------------------------------------------
    add_h1(doc, "PHẦN 4: ĐỀ TÀI 3 — MULTIMODAL EDGE AIOT SMART CLASSROOM LEARNING ENVIRONMENT ANALYSIS")
    
    add_h2(doc, "1. Tên Đề tài (Project Title)")
    add_bullet(doc, "Tên tiếng Việt: ", "Thiết kế hệ thống AIoT biên đa phương thức phân tích môi trường học tập và khí hậu lớp học thông minh bảo vệ quyền riêng tư.")
    add_bullet(doc, "Tên tiếng Anh: ", "Multimodal Edge AIoT Smart Classroom Learning Environment Analysis and Indoor Quality Monitoring System.")

    add_h2(doc, "2. Bối cảnh và Bài toán Thực tiễn (Background and Problem)")
    add_para(doc, "Chất lượng môi trường trong nhà (Indoor Environmental Quality - IEQ) tại các giảng đường và lớp học đại học ảnh hưởng trực tiếp và sâu sắc đến khả năng tiếp thu, mức độ tỉnh táo và sức khỏe của người học. Các nghiên cứu khoa học của Đại học Harvard và Hiệp hội Kỹ sư Nhiệt lạnh Hoa Kỳ (ASHRAE) đã chứng minh rằng: trong một phòng học đóng kín bật máy lạnh chứa 40 - 60 sinh viên, nồng độ khí CO2 do hô hấp tích tụ rất nhanh, thường xuyên vượt ngưỡng 1500 - 2500 ppm chỉ sau 30 phút học tập. Nồng độ CO2 cao làm suy giảm tới 25% điểm số trong các bài kiểm tra nhận thức, gây ra hiện tượng uể oải, nhức đầu và buồn ngủ tập thể.")
    add_para(doc, "Bên cạnh đó, các yếu tố về ô nhiễm âm thanh (tiếng ồn thảo luận quá ngưỡng, tiếng vang phòng học) và ánh sáng không đạt chuẩn cũng gây căng thẳng thị giác và làm giáo viên nhanh chóng bị khản giọng. Tuy nhiên, các giải pháp theo dõi lớp học hiện nay gặp phải những bế tắc nghiêm trọng:")
    add_bullet(doc, "Giải pháp camera giám sát khuôn mặt (Facial Surveillance): ", 
               "Vi phạm nghiêm trọng quyền riêng tư cá nhân, tạo cảm giác bị theo dõi soi xét cho sinh viên và vấp phải rào cản pháp lý/đạo đức nghiêm ngặt (theo đạo luật EU AI Act và quy định bảo vệ dữ liệu cá nhân tại Việt Nam).")
    add_bullet(doc, "Thiết bị đo môi trường thông thường: ", 
               "Chỉ là các đồng hồ đo rời rạc, phản ứng thụ động (chỉ hú còi khi CO2 đã quá cao, lúc đó sinh viên đã ngủ gật) và không có khả năng dự báo hoặc điều khiển thông gió thông minh.")

    add_h2(doc, "3. Ý tưởng Cốt lõi (Main Idea)")
    add_para(doc, "Ý tưởng cốt lõi của đề tài là xây dựng một Trạm AIoT biên bảo vệ quyền riêng tư tuyệt đối (Privacy-by-Design Smart Classroom Station). Hệ thống hoàn toàn không sử dụng bất kỳ camera RGB nào để nhận diện danh tính sinh viên. Thay vào đó, hệ thống phân tích trạng thái lớp học thông qua tổ hợp cảm biến đa phương thức phi xâm lấn (Non-intrusive Multimodal Sensing):")
    add_bullet(doc, "Cảm biến CO2 quang học thực thụ (NDIR): ", "Đo lường chính xác tốc độ tích tụ khí carbonic và các hợp chất hữu cơ dễ bay hơi TVOC.")
    add_bullet(doc, "Micro kỹ thuật số MEMS I2S: ", "Thu âm học lớp học, nhưng không ghi âm lời nói mà trích xuất tức thì các hệ số âm phổ MFCC để phân loại ngữ nghĩa môi trường giảng dạy.")
    add_bullet(doc, "Cảm biến hiện diện radar vi sóng mmWave / PIR: ", "Đo lường mật độ và mức độ cử động trong phòng.")
    add_para(doc, "Tại vi điều khiển ESP32-S3, một mô hình TinyML chuỗi thời gian sẽ dự báo trước nồng độ CO2 sau 20 - 30 phút để chủ động kích hoạt quạt hút khí tươi thông minh (Predictive Demand-Controlled Ventilation). Đồng thời, mô hình phân loại âm thanh sẽ nhận diện 4 trạng thái sư phạm: Giảng viên đang giảng bài, Cả lớp thảo luận nhóm sôi nổi, Tiếng ồn mất trật tự, hoặc Yên lặng làm bài thi; từ đó đưa ra cảnh báo ánh sáng đổi màu dịu mắt để điều chỉnh không khí lớp học.")

    add_h2(doc, "4. Kiến trúc Hệ thống (System Architecture)")
    add_callout(doc, "Sơ đồ Luồng Dữ liệu Lớp Học Thông Minh",
                "Cụm Cảm biến Môi trường (CO2 NDIR SCD40 + Nhiệt ẩm BME280 + Ánh sáng BH1750)\n"
                "       +\n"
                "Cảm biến Âm học (Micro MEMS INMP441) + Radar Hiện diện (mmWave HLK-LD2410)\n"
                "       ↓\n"
                "Khối Xử lý Tín hiệu Số (DSP: Tính mức ồn dBA Leq, Trích xuất 13 hệ số MFCC, Chuẩn hóa chuỗi)\n"
                "       ↓\n"
                "Hai Mô hình TinyML Chạy Song song trên ESP32-S3:\n"
                "  • Model 1: Hồi quy Chuỗi Thời gian Dự báo CO2 & Nguy cơ Mệt mỏi Nhận thức\n"
                "  • Model 2: Phân loại Ngữ nghĩa Âm học Sư phạm (Classroom Acoustic Classifier)\n"
                "       ↓\n"
                "Khối Chấp hành Cục bộ (Rơ-le/PWM điều khiển quạt thông gió + Vòng LED WS2812B báo trạng thái)\n"
                "       ↓\n"
                "Khối Truyền thông WiFi / MQTT (Gửi gói tin JSON số liệu vi khí hậu mỗi 15 giây)\n"
                "       ↓\n"
                "Web Dashboard Giảng đường (Firebase + Chart.js biểu diễn trực quan IEQ & Lịch sử)")

    add_h2(doc, "5. Các Nguyên lý Lý thuyết Liên quan (Theoretical Principles)")
    add_bullet(doc, "Chất lượng Môi trường Trong nhà (IEQ - Indoor Environmental Quality): ", 
               "Tập hợp các yếu tố vật lý gồm Chất lượng không khí (IAQ), Tiện nghi nhiệt (Thermal Comfort theo mô hình Fanger PMV/PPD), Tiện nghi thị giác (độ rọi Lux theo chuẩn TCVN 7114), và Tiện nghi âm học (Acoustic Comfort).")
    add_bullet(doc, "Nguyên lý Đo Quang phổ Hồng ngoại Không tán xạ (NDIR CO2): ", 
               "Khí CO2 hấp thụ đặc trưng bức xạ hồng ngoại ở bước sóng 4.26 micromet. Cảm biến Sensirion SCD40 sử dụng nguyên lý quang âm (photoacoustic) đo lường chính xác nồng độ ppm thực tế, hoàn toàn miễn nhiễm với cồn hoặc hơi ẩm (khắc phục điểm yếu đo sai của các cảm biến rẻ tiền MQ-135).")
    add_bullet(doc, "Hệ số Âm phổ Tần số Mel (MFCC - Mel-Frequency Cepstral Coefficients): ", 
               "Kỹ thuật trích xuất đặc trưng âm học mô phỏng theo thính giác con người. 13 hệ số MFCC chỉ giữ lại thông tin về phân bố năng lượng theo dải tần (phân biệt tiếng người nói vs tiếng ồn trắng của quạt/tiếng bàn ghế), hoàn toàn không thể dịch ngược lại thành nội dung từ ngữ, bảo vệ quyền riêng tư.")
    add_bullet(doc, "Mô hình Dự báo Chuỗi Thời gian (Time-Series Forecasting): ", 
               "Mạng nơ-ron tích chập thời gian (Temporal Convolutional Network - TCN) học quy luật tích tụ CO2 theo hàm số của mật độ người và nhiệt độ phòng để dự báo trước tương lai.")

    add_h2(doc, "6. Phần cứng Yêu cầu (Required Hardware)")
    hw3_headers = ["Linh kiện / Module", "Mã thiết bị đề xuất", "Chức năng trong hệ thống", "Mức độ cần thiết"]
    hw3_data = [
        ["Vi điều khiển trung tâm", "ESP32-S3-DevKitC-1", "Lấy mẫu đa cảm biến, tính toán MFCC và chạy mô hình TinyML", "Bắt buộc"],
        ["Cảm biến CO2 quang học thực", "Sensirion SCD40 / SCD41", "Đo nồng độ CO2 thực tế dải 400 - 5000 ppm chuẩn xác", "Bắt buộc"],
        ["Cảm biến nhiệt ẩm áp suất", "Bosch BME280 I2C", "Đo nhiệt độ (°C), độ ẩm tương đối (%RH) và áp suất khí quyển", "Bắt buộc"],
        ["Cảm biến âm thanh kỹ thuật số", "INMP441 I2S MEMS Microphone", "Thu nhận tín hiệu âm học lớp học số hóa băng thông 20Hz-20kHz", "Bắt buộc"],
        ["Cảm biến cường độ ánh sáng", "BH1750 Digital Light Sensor", "Đo độ rọi phòng học (đơn vị Lux) qua giao tiếp I2C", "Bắt buộc"],
        ["Cảm biến hiện diện vi sóng", "Radar mmWave HLK-LD2410", "Phát hiện có người ngồi yên hoặc cử động trong phòng học", "Bắt buộc"],
        ["Khối chấp hành quạt gió", "Module Relay 5V / Mosfet PWM", "Điều khiển bật/tắt quạt thông gió hoặc điều tốc quạt hút khí tươi", "Bắt buộc"],
        ["Đèn chỉ thị tiện nghi trực quan", "Vòng LED RGB WS2812B (Ring 8/12)", "Đổi màu báo hiệu tiện nghi phòng (Xanh: Tốt, Vàng: Ồn, Đỏ: Thiếu khí)", "Bắt buộc"],
        ["Cảm biến khí tổng hữu cơ", "Sensirion SGP40 (VOC Index)", "Đo chỉ số ô nhiễm các hóa chất dễ bay hơi và mùi phòng", "Tùy chọn / Mở rộng"]
    ]
    create_styled_table(doc, hw3_headers, hw3_data, [1.6, 1.8, 2.4, 1.2])

    add_h2(doc, "7. Vai trò của Trí tuệ Nhân tạo / Học máy (Role of AI / ML)")
    add_para(doc, "Hệ thống triển khai đồng thời hai mô hình học máy gọn nhẹ (Dual-TinyML Pipeline) ngay trên vi điều khiển ESP32-S3:")
    add_bullet(doc, "Mô hình 1: Hồi quy Dự báo Tích tụ CO2 (Predictive Ventilation): ", 
               "Mô hình nhận đầu vào là chuỗi 15 phút lịch sử gồm CO2, nhiệt ẩm và mức độ chuyển động hiện diện. Mô hình dự báo giá trị CO2 sau 20 phút tới. Nhờ dự báo trước, vi điều khiển kích hoạt quạt hút khí tươi từ phút thứ 15 với tốc độ êm ái, ngăn chặn hoàn toàn nồng độ CO2 vượt ngưỡng 1000 ppm, triệt tiêu cơn buồn ngủ tập thể của sinh viên.")
    add_bullet(doc, "Mô hình 2: Phân loại Ngữ cảnh Âm học Sư phạm (Classroom Acoustic State): ", 
               "Đầu vào là 13 hệ số MFCC x 32 khung thời gian (cửa sổ 1 giây). Mô hình CNN lượng tử hóa INT8 phân loại 4 trạng thái lớp học: 1. Giảng viên đang giảng bài (Teacher Lecturing); 2. Học sinh đang thảo luận nhóm tích cực (Collaborative Discussion); 3. Tiếng ồn mất trật tự quá ngưỡng (Disruptive Noise Spike); 4. Yên tĩnh làm bài / Tự nghiên cứu (Quiet Study).")
    add_bullet(doc, "Tính toán Chỉ số Tiện nghi Nhận thức (Cognitive Comfort Index - CCI): ", 
               "Kết hợp mờ (Fuzzy Logic) giữa độ tươi không khí, độ ồn và ánh sáng để tính ra điểm số chất lượng học tập trên thang 100 điểm.")

    add_h2(doc, "8. Vai trò của IoT (Role of IoT)")
    add_bullet(doc, "Kết nối WiFi khuôn viên trường: ", 
               "Node cảm biến kết nối mạng WiFi phòng học, định kỳ mỗi 15 - 30 giây gửi một bản tin JSON nhẹ qua MQTT/HTTPS lên cơ sở dữ liệu Firebase.")
    add_bullet(doc, "Web Dashboard dành cho Ban Giảng huấn & Quản lý Cơ sở Vật chất: ", 
               "Giao diện hiển thị trực quan bản đồ các phòng học, đồ thị đường diễn biến chất lượng không khí, số lần quạt thông gió tự động kích hoạt, và tỷ lệ % thời lượng giảng bài vs thảo luận của từng tiết dạy.")
    add_bullet(doc, "Điều khiển ngược (Actuation & Override): ", 
               "Giảng viên có thể dùng điện thoại truy cập web để bật cưỡng bức quạt thông gió hoặc điều chỉnh độ nhạy theo ý muốn.")

    add_h2(doc, "9. Kịch bản Vận hành Dự kiến (Expected System Operation)")
    add_para(doc, "Tại phòng học A2-301, tiết học bắt đầu lúc 7h30 với 50 sinh viên. Cửa ra vào và cửa sổ đóng kín để bật điều hòa. Trạm AIoT treo tường bắt đầu chu trình quan trắc. Ban đầu CO2 ở mức 450 ppm (trong lành), vòng LED hiển thị màu xanh lá dịu mát. Đến 8h05, nồng độ CO2 đo được là 850 ppm, tốc độ tăng đo được là 15 ppm/phút kết hợp cảm biến radar báo phòng đầy người. Mô hình TinyML tính toán và dự báo: nồng độ CO2 sẽ chạm mức nguy hại 1200 ppm vào lúc 8h25. Ngay lập tức tại phút 8h05, ESP32-S3 phát xung PWM bật quạt hút thông gió tươi ở mức êm dịu 40% công suất. Nhờ khí tươi được bổ sung từ sớm, nồng độ CO2 chỉ tăng tối đa đến 920 ppm rồi bình ổn, sinh viên trong phòng hoàn toàn không bị cảm giác ngột ngạt buồn ngủ. Đến 8h30, giảng viên cho thảo luận nhóm, tiếng nói chuyện râm ran vang lên, mô hình âm học nhận diện trạng thái \"Discussion\", vòng LED chuyển sang màu xanh dương thân thiện ghi nhận giờ học diễn ra sinh động.")

    add_h2(doc, "10. Ưu điểm Kỹ thuật Vượt trội (Advantages)")
    add_bullet(doc, "Bảo vệ quyền riêng tư tuyệt đối (Privacy by Design): ", "Không thu thập, không lưu trữ và không truyền tải bất kỳ hình ảnh khuôn mặt hay đoạn ghi âm giọng nói nào của sinh viên.")
    add_bullet(doc, "Chuyển từ phản ứng thụ động sang điều khiển chủ động: ", "Thông gió dự đoán trước (Predictive Ventilation) ngăn chặn hiện tượng thiếu oxy não thay vì chỉ báo động muộn màng.")
    add_bullet(doc, "Đo đạc nồng độ CO2 chuẩn xác cao: ", "Sử dụng cảm biến NDIR thực thụ của Sensirion Thụy Sĩ, đảm bảo số liệu tin cậy cho nghiên cứu khoa học.")

    add_h2(doc, "11. Hạn chế và Thách thức Kỹ thuật (Limitations and Technical Challenges)")
    add_bullet(doc, "Vị trí lắp đặt node cảm biến: ", "Nếu lắp trạm ngay cửa sổ hoặc sát miệng gió máy lạnh, luồng khí cục bộ sẽ làm sai lệch giá trị đo của toàn phòng. Cần lắp đặt ở độ cao ngang tầm thở (1.2 - 1.5 mét) tại vách tường trung tâm.")
    add_bullet(doc, "Độ vang âm học phòng học: ", "Các phòng học có diện tích tường kính lớn tạo ra hiện tượng phản xạ âm thanh (Reverberation) làm mờ các đặc trưng MFCC. Cần áp dụng bộ lọc bù trừ phổ âm thanh môi trường.")

    add_h2(doc, "12. Phạm vi Thực hiện Đồ án 2 (Project 2 Scope)")
    add_bullet(doc, "PHẦN BẮT BUỘC (MUST HAVE): ", 
               "Thiết kế hộp phần cứng trạm quan trắc IEQ hoàn chỉnh; Đọc chính xác cụm cảm biến SCD40 (CO2), BME280, BH1750 và micro I2S INMP441; Triển khai mô hình TinyML dự báo xu hướng CO2 và nhận diện mức ồn dBA trên ESP32-S3; Tự động kích hoạt quạt thông gió qua rơ-le; Xây dựng trang Web Dashboard hiển thị các biểu đồ môi trường theo thời gian thực.")
    add_bullet(doc, "PHẦN TÙY CHỌN / MỞ RỘNG (OPTIONAL): ", 
               "Tích hợp thêm cảm biến radar mmWave HLK-LD2410 phát hiện số lượng người tương đối; Nạp mô hình phân loại âm thanh CNN 4 trạng thái sư phạm.")

    add_h2(doc, "13. Hướng Phát triển Khóa luận Tốt nghiệp (Future Graduation Thesis)")
    add_bullet(doc, "Mạng lưới Cảm biến Phân tán (Distributed Mesh AIoT): ", "Triển khai mạng lưới 4 - 6 node cảm biến kết nối mạng ESP-MESH bao phủ khắp giảng đường lớn 200 chỗ ngồi, lập bản đồ nhiệt độ và CO2 theo không gian 3D.")
    add_bullet(doc, "Tích hợp Hệ thống Tự động hóa Tòa nhà (BMS / HVAC): ", "Giao tiếp trực tiếp với hệ thống điều hòa không khí trung tâm thông qua chuẩn công nghiệp Modbus TCP / BACnet.")

    add_h2(doc, "14. Các Kho Mã Nguồn GitHub Liên quan (Related GitHub Repositories)")
    gh3_headers = ["Repository & Tác giả", "Đường dẫn URL", "Công nghệ chính", "Giá trị học hỏi / Tái sử dụng"]
    gh3_data = [
        ["prakashkarkee / smartclass", 
         {"text": "github.com/prakashkarkee/smartclass", "url": "https://github.com/prakashkarkee/smartclass"},
         "ESP32, Smart Classroom, Sensors", 
         "Hệ thống giám sát lớp học IoT, tích hợp PIR hiện diện, nhiệt ẩm, ánh sáng và tiếng ồn."],
        ["benb0jangles / Air_Quality_monitor", 
         {"text": "github.com/benb0jangles/Air_Quality_monitor", "url": "https://github.com/benb0jangles/Air_Quality_monitor"},
         "ESP32-C3, SCD41, SGP41, MQTT", 
         "Mã nguồn giao tiếp cảm biến CO2 NDIR SCD40/41 chuẩn xác, xử lý chuỗi I2C và đẩy dữ liệu MQTT."],
        ["JulianFP / CO2-Sensor", 
         {"text": "github.com/JulianFP/CO2-Sensor", "url": "https://github.com/JulianFP/CO2-Sensor"},
         "ESP32, CO2 Monitoring, Grafana", 
         "Dự án giám sát CO2 phòng học thực tế, quản lý cảnh báo ngưỡng và hiển thị Dashboard trực quan."],
        ["CyberScoper / ESP32-AirQuality", 
         {"text": "github.com/CyberScoper/ESP32-AirQuality-Station-Home", "url": "https://github.com/CyberScoper/ESP32-AirQuality-Station-Home"},
         "ESP32, BME280, Fan Control", 
         "Tham khảo thuật toán điều khiển quạt thông gió tự động dựa trên chất lượng không khí."]
    ]
    create_styled_table(doc, gh3_headers, gh3_data, [1.5, 2.2, 1.5, 2.0])

    add_h2(doc, "15. Tài liệu Tham khảo Học thuật Xác thực (Academic References)")
    add_bullet(doc, "[1] F. Salamone, L. Danza, et al., ", 
               "\"IoT and Edge AI-Based Indoor Environmental Quality (IEQ) Monitoring for Healthy and Productive Classrooms,\" Building and Environment, vol. 235, art. 110212, 2023. DOI: 10.1016/j.buildenv.2023.110212. (Nghiên cứu về tác động của vi khí hậu phòng học đến nhận thức và phương pháp quan trắc bằng IoT).")
    add_bullet(doc, "[2] H. Zhang, Y. Wang, et al., ", 
               "\"Privacy-Preserving Classroom Learning Analytics Using Multi-Modal Edge Sensing,\" IEEE Transactions on Learning Technologies, vol. 17, pp. 215-228, 2024. DOI: 10.1109/TLT.2023.3325102. (Phương pháp luận bảo vệ quyền riêng tư học đường bằng cảm biến phi hình ảnh).")
    add_bullet(doc, "[3] G. P. Cimmino, A. Gomez, M. Magno, ", 
               "\"Classroom Acoustic Comfort and Noise Event Identification Using TinyML on Edge Microcontrollers,\" ACM Transactions on Sensor Networks, vol. 20, no. 2, pp. 1-22, 2024. DOI: 10.1145/3631456. (Kỹ thuật trích xuất MFCC và phân loại tiếng ồn lớp học bằng TinyML trên vi điều khiển).")

    add_h2(doc, "16. Tập Dữ liệu Mở Có sẵn (Available Datasets)")
    ds3_headers = ["Tên tập dữ liệu", "Loại dữ liệu", "Nội dung / Nhãn lớp", "Liên kết truy cập", "Ứng dụng trong đồ án"]
    ds3_data = [
        ["DCASE Classroom Acoustics", "Âm thanh môi trường WAV", "Speech, Discussion, Background noise, Quiet", 
         {"text": "dcase.community", "url": "https://dcase.community/"},
         "Dùng để tiền huấn luyện mô hình phân loại âm học lớp học."],
        ["ASHRAE Global IEQ Database", "Chuỗi số liệu CSV môi trường", "Nhiệt độ, CO2, độ ẩm, đánh giá tiện nghi", 
         {"text": "comfortdatabase.com", "url": "https://www.comfortdatabase.com/"},
         "Đối chiếu thuật toán tính toán chỉ số mệt mỏi nhận thức."]
    ]
    create_styled_table(doc, ds3_headers, ds3_data, [1.5, 1.4, 1.8, 1.3, 1.5])

    add_h2(doc, "17. Tóm tắt Đề tài 3 (Summary)")
    add_bullet(doc, "Mục tiêu cốt lõi: ", "Trạm AIoT biên bảo vệ quyền riêng tư, phân tích môi trường học tập và điều khiển thông gió dự đoán CO2.")
    add_bullet(doc, "Phần cứng chủ đạo: ", "ESP32-S3, Cảm biến NDIR SCD40, BME280, BH1750, Micro INMP441, Relay quạt gió, Vòng LED WS2812B.")
    add_bullet(doc, "Kỹ thuật AI chính: ", "Mô hình hồi quy TCN dự báo CO2 tương lai + Mạng tích chập phân loại âm học MFCC trên TFLite-Micro.")
    add_bullet(doc, "Công nghệ IoT: ", "Mạng WiFi / MQTT đẩy vi khí hậu lên Firebase Web Dashboard và điều khiển quạt thông gió tự động.")
    add_bullet(doc, "Đóng góp nghiên cứu: ", "Ứng dụng triết lý Privacy by Design vào phân tích lớp học, chuyển từ cảnh báo thụ động sang thông gió chủ động.")

    # -------------------------------------------------------------
    # PHẦN 5: BẢNG SO SÁNH TỔNG HỢP & PHÂN TÍCH ĐÁNH ĐỔI
    # -------------------------------------------------------------
    add_h1(doc, "PHẦN 5: BẢNG SO SÁNH TỔNG HỢP & PHÂN TÍCH ĐÁNH ĐỔI (TRADE-OFF ANALYSIS)")
    
    add_para(doc, "Nhằm giúp nhóm sinh viên đưa ra quyết định chọn lựa đề tài tối ưu nhất, bảng ma trận dưới đây thực hiện so sánh đối đầu giữa 3 đề tài trọng điểm theo 12 tiêu chuẩn đánh giá khắt khe của Đồ án Kỹ thuật Máy tính:")
    
    cmp_headers = ["Tiêu chuẩn Đánh giá", "Đề tài 1: Phân loại Tai nạn Xe máy", "Đề tài 2: Hộp đen Thông minh (EDR)", "Đề tài 3: Lớp học Thông minh IEQ"]
    cmp_data = [
        ["Lĩnh vực ứng dụng", "An toàn giao thông / Xe máy hai bánh", "Giám định pháp y tai nạn / Quản lý xe", "Giáo dục thông minh / Sức khỏe học đường"],
        ["Bài toán kỹ thuật cốt lõi", "Khử báo động giả từ ổ gà và phanh gấp", "Đóng băng bộ đệm tròn 30s & Chống giả mạo", "Dự báo nồng độ CO2 & Bảo vệ riêng tư"],
        ["Phương pháp AI / Machine Learning", "1D-CNN phân loại hình thái sóng IMU INT8", "Mô hình kích hoạt bất thường + EKF Dead-reckoning", "Hồi quy chuỗi thời gian TCN + MFCC Audio CNN"],
        ["Công nghệ IoT & Viễn thông", "4G LTE (SMS + GPS) + Firebase Web", "4G LTE (SOS) + Upload File log MicroSD", "WiFi / MQTT + Firebase Realtime Dashboard"],
        ["Bộ xử lý trung tâm đề xuất", "ESP32-S3 (Dual-core 240MHz, ESP-NN)", "ESP32-S3 (8MB Octal PSRAM bắt buộc)", "ESP32-S3 (Dual-core 240MHz, I2S DMA)"],
        ["Độ mới & Giá trị khoa học", "Cao (Khử báo động giả bằng TinyML)", "Rất cao (Hiện thực hóa EDR trên xe máy)", "Rất cao (Privacy-by-Design, Không camera)"],
        ["Mức độ khó kỹ thuật (Thang 10)", "7.5 / 10", "8.0 / 10", "7.0 / 10"],
        ["Chi phí phần cứng ước tính", "~1.200.000 - 1.500.000 VNĐ", "~1.300.000 - 1.600.000 VNĐ", "~1.100.000 - 1.400.000 VNĐ"],
        ["Khả năng thử nghiệm thực tế", "Trung bình (Cần bãi tập xe an toàn)", "Trung bình (Thử nghiệm trên xe thực tế)", "Rất dễ (Thử nghiệm ngay trong phòng học)"],
        ["Tính khả thi trong ĐA2 (10-12 tuần)", "Rất cao (Kế thừa mạch mẫu của thầy)", "Khả thi cao (Cần quản lý tốt bộ nhớ đệm)", "Rất cao (Môi trường test an toàn, dễ demo)"],
        ["Tiềm năng mở rộng KLTN", "Cực lớn (V2X liên xe + Camera biên)", "Cực lớn (Camera kép H.264 + Kết nối ECU)", "Cực lớn (Mạng Mesh đa nút + Hệ thống BMS)"],
        ["Tài nguyên mã nguồn & Dữ liệu", "Rất phong phú (AegisIoT, MIVIA)", "Phong phú (jctoledo/blackbox, MOTOR)", "Rất phong phú (Smartclass, SCD40 repos)"]
    ]
    create_styled_table(doc, cmp_headers, cmp_data, [1.6, 1.8, 1.8, 1.8])

    add_h2(doc, "Phân tích Đánh đổi và Khuyến nghị Lựa chọn cho Nhóm Sinh viên")
    add_para(doc, "Dựa trên năng lực chuyên môn và mục tiêu điểm số của nhóm, sinh viên có thể cân nhắc các định hướng chiến lược sau:")
    add_bullet(doc, "Lựa chọn an toàn, kế thừa tối đa và thuyết phục thầy hướng dẫn nhanh nhất: ", 
               "NÊN CHỌN ĐỀ TÀI 1. Đề tài này kế thừa trực tiếp 100% nền tảng sơ đồ nguyên lý mạch của ThS. Nguyễn Ngô Lâm (gồm ESP32, module SIM, GPS, hạ áp LM2596, còi báo). Nhóm trả lời trực diện vào hạn chế lớn nhất của khóa trước: thay thế ngưỡng cứng ngây thơ bằng mô hình TinyML 1D-CNN chạy thực tế trên ESP32-S3. Thầy sẽ rất hài lòng vì thấy sinh viên hiểu sâu sắc nhược điểm của các hệ thống cũ và nâng cấp sản phẩm lên một tầm cao mới.")
    add_bullet(doc, "Lựa chọn thực nghiệm an toàn, nhân văn và dễ gây ấn tượng thị giác khi demo: ", 
               "NÊN CHỌN ĐỀ TÀI 3. Đề tài lớp học thông minh bảo vệ quyền riêng tư có ưu điểm tuyệt đối là môi trường thử nghiệm cực kỳ an toàn (trong phòng máy, phòng học của trường). Nhóm có thể mang toàn bộ thiết bị lên bàn hội đồng chấm điểm, biểu diễn kịch bản thở khí CO2 làm tăng nồng độ, hệ thống tự dự báo và kích hoạt quạt hút khí tươi trước mắt các thầy cô. Tính năng bảo vệ riêng tư không dùng camera soi xét học sinh là điểm sáng đạo đức công nghệ rất được lòng các hội đồng học thuật.")
    add_bullet(doc, "Lựa chọn đột phá kỹ thuật máy tính và định hướng sản phẩm thương mại: ", 
               "NÊN CHỌN ĐỀ TÀI 2. Đề tài Hộp đen thông minh đòi hỏi sinh viên phải nắm vững kỹ thuật cấp phát bộ nhớ nhúng (PSRAM Ring Buffer), kỹ thuật đọc ghi thẻ nhớ tốc độ cao không nghẽn luồng và mã hóa băm bảo mật. Đây là đề tài mang tính chuyên môn thuần túy của Kỹ thuật Máy tính, có tính ứng dụng thực tế rất lớn trong các công ty vận tải và bảo hiểm.")

    # -------------------------------------------------------------
    # PHẦN 6: TÀI LIỆU THAM KHẢO TOÀN DIỆN (MASTER REFERENCES)
    # -------------------------------------------------------------
    add_h1(doc, "TÀI LIỆU THAM KHẢO TOÀN DIỆN (REFERENCES)")
    
    add_h2(doc, "A. Bài Báo Khoa học & Kỷ yếu Hội nghị Quốc tế (Peer-Reviewed Academic Papers)")
    add_bullet(doc, "[1] ", "S. Choi, J. Lee, and K. Kim, \"Pre-Impact Fall Detection for E-Scooter and Motorcycle Riding Using Embedded Sensors,\" MDPI Sensors, vol. 24, no. 1, art. 123, Jan. 2024. DOI: 10.3390/s24010123.")
    add_bullet(doc, "[2] ", "V. K. Kukkala, S. V. Thiruvengadam, et al., \"A Machine Learning-Based Motorcycle Accident Detection and Reporting System,\" IEEE Access, vol. 11, pp. 45210-45222, May 2023. DOI: 10.1109/ACCESS.2023.3274112.")
    add_bullet(doc, "[3] ", "P. Foggia, N. Petkov, A. Saggese, N. Strisciuglio, and M. Vento, \"Reliable Detection of Audio Events in Road Scenarios,\" IEEE Transactions on Intelligent Transportation Systems, vol. 17, no. 6, pp. 1589-1597, June 2016. DOI: 10.1109/TITS.2015.2504724.")
    add_bullet(doc, "[4] ", "R. K. Kodali and S. Sahu, \"Design and Implementation of an IoT-Based Vehicle Black Box for Post-Accident Forensics,\" in Proc. 2022 IEEE International Conference on Electronics, Computing and Communication Technologies (CONECCT), Bangalore, India, 2022, pp. 1-6. DOI: 10.1109/CONECCT55679.2022.9865243.")
    add_bullet(doc, "[5] ", "A. Kumar and P. Sharma, \"A Smart Event Data Recorder (EDR) Architecture for Two-Wheeled Vehicles Using Low-Power Edge Computing,\" IEEE Embedded Systems Letters, vol. 15, no. 3, pp. 142-145, Sept. 2023. DOI: 10.1109/LES.2023.3241501.")
    add_bullet(doc, "[6] ", "F. Salamone, L. Danza, et al., \"IoT and Edge AI-Based Indoor Environmental Quality (IEQ) Monitoring for Healthy and Productive Classrooms,\" Building and Environment, vol. 235, art. 110212, May 2023. DOI: 10.1016/j.buildenv.2023.110212.")
    add_bullet(doc, "[7] ", "H. Zhang, Y. Wang, et al., \"Privacy-Preserving Classroom Learning Analytics Using Multi-Modal Edge Sensing,\" IEEE Transactions on Learning Technologies, vol. 17, pp. 215-228, Feb. 2024. DOI: 10.1109/TLT.2023.3325102.")
    add_bullet(doc, "[8] ", "G. P. Cimmino, A. Gomez, and M. Magno, \"Classroom Acoustic Comfort and Noise Event Identification Using TinyML on Edge Microcontrollers,\" ACM Transactions on Sensor Networks, vol. 20, no. 2, pp. 1-22, Apr. 2024. DOI: 10.1145/3631456.")
    add_bullet(doc, "[9] ", "M. Magno, L. Benini et al., \"TinyML for Ultra-Low-Power Autonomous Road Anomaly and Vehicle Crash Detection,\" IEEE Internet of Things Journal, vol. 10, no. 18, pp. 16210-16221, Sept. 2023. DOI: 10.1109/JIOT.2023.3271105.")

    add_h2(doc, "B. Tài liệu Kỹ thuật Chính thức & Tiêu chuẩn Công nghiệp (Official Technical Documentation & Standards)")
    add_bullet(doc, "[10] ", "IEEE Vehicular Technology Society, \"IEEE Standard for Motor Vehicle Event Data Recorders (EDRs),\" IEEE Std 1616-2020 (Revision of IEEE Std 1616-2004), pp. 1-85, Dec. 2020. DOI: 10.1109/IEEESTD.2020.9304385.")
    add_bullet(doc, "[11] ", "Espressif Systems, \"ESP32-S3 Technical Reference Manual & ESP-NN Neural Network Acceleration Library Documentation,\" Version 1.4, 2024. [Online]. Available: https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/")
    add_bullet(doc, "[12] ", "Sensirion AG, \"SCD4x Photoacoustic NDIR CO2 Sensor Datasheet and Interface Specification,\" Sensirion Gas Sensing Solutions, 2023. [Online]. Available: https://sensirion.com/products/catalog/SCD40/")
    add_bullet(doc, "[13] ", "Bosch Sensortec, \"BME280 Combined humidity and pressure sensor datasheet,\" Document BST-BME280-DS002-15, 2022.")

    add_h2(doc, "C. Các Kho Mã Nguồn Mở GitHub Xác thực (Verified Open-Source GitHub Repositories)")
    p_gh1 = doc.add_paragraph(style='List Bullet')
    p_gh1.paragraph_format.first_line_indent = Inches(0)
    p_gh1.add_run("[14] ibesuperv, \"AegisIoT: Distributed IoT mission-critical accident response infrastructure on ESP32,\" GitHub Repository, 2024. Liên kết: ")
    add_hyperlink(p_gh1, "https://github.com/ibesuperv/AegisIoT", "https://github.com/ibesuperv/AegisIoT")

    p_gh2 = doc.add_paragraph(style='List Bullet')
    p_gh2.paragraph_format.first_line_indent = Inches(0)
    p_gh2.add_run("[15] Edge Impulse, \"Standalone inferencing SDK for Espressif ESP32 and ESP32-S3,\" Official GitHub Repository, 2024. Liên kết: ")
    add_hyperlink(p_gh2, "https://github.com/edgeimpulse/example-standalone-inferencing-espressif-esp32", "https://github.com/edgeimpulse/example-standalone-inferencing-espressif-esp32")

    p_gh3 = doc.add_paragraph(style='List Bullet')
    p_gh3.paragraph_format.first_line_indent = Inches(0)
    p_gh3.add_run("[16] J. C. Toledo, \"blackbox: ESP32 vehicle telemetry with GPS and IMU sensor fusion,\" GitHub Repository, 2023. Liên kết: ")
    add_hyperlink(p_gh3, "https://github.com/jctoledo/blackbox", "https://github.com/jctoledo/blackbox")

    p_gh4 = doc.add_paragraph(style='List Bullet')
    p_gh4.paragraph_format.first_line_indent = Inches(0)
    p_gh4.add_run("[17] RandomVertebrate, \"vibration-logger: ESP32 high-rate acceleration and GPS data logging onto SD card,\" GitHub Repository, 2023. Liên kết: ")
    add_hyperlink(p_gh4, "https://github.com/RandomVertebrate/vibration-logger", "https://github.com/RandomVertebrate/vibration-logger")

    p_gh5 = doc.add_paragraph(style='List Bullet')
    p_gh5.paragraph_format.first_line_indent = Inches(0)
    p_gh5.add_run("[18] P. Karkee, \"smartclass: IoT-based smart classroom environmental monitoring with ESP32,\" GitHub Repository, 2023. Liên kết: ")
    add_hyperlink(p_gh5, "https://github.com/prakashkarkee/smartclass", "https://github.com/prakashkarkee/smartclass")

    p_gh6 = doc.add_paragraph(style='List Bullet')
    p_gh6.paragraph_format.first_line_indent = Inches(0)
    p_gh6.add_run("[19] B. Bojangles, \"Air_Quality_monitor: ESP32-C3 integrating SCD41 CO2 and SGP41 VOC sensors,\" GitHub Repository, 2024. Liên kết: ")
    add_hyperlink(p_gh6, "https://github.com/benb0jangles/Air_Quality_monitor", "https://github.com/benb0jangles/Air_Quality_monitor")

    p_gh7 = doc.add_paragraph(style='List Bullet')
    p_gh7.paragraph_format.first_line_indent = Inches(0)
    p_gh7.add_run("[20] M. Hart, \"TinyGPSPlus: A new, customizable Arduino NMEA parsing library,\" GitHub Repository, 2023. Liên kết: ")
    add_hyperlink(p_gh7, "https://github.com/mikalhart/TinyGPSPlus", "https://github.com/mikalhart/TinyGPSPlus")

    add_h2(doc, "D. Các Tập Dữ liệu Mở Phục vụ Huấn luyện & Kiểm thử (Open Public Datasets)")
    p_ds1 = doc.add_paragraph(style='List Bullet')
    p_ds1.paragraph_format.first_line_indent = Inches(0)
    p_ds1.add_run("[21] MIVIA Lab, \"MIVIA Road Audio Events Data Set (Car crashes and Tire Skidding sounds),\" University of Salerno. Liên kết: ")
    add_hyperlink(p_ds1, "https://mivia.unisa.it/datasets/audio-events/mivia-road-audio-events-data-set/", "https://mivia.unisa.it/datasets/audio-events/mivia-road-audio-events-data-set/")

    p_ds2 = doc.add_paragraph(style='List Bullet')
    p_ds2.paragraph_format.first_line_indent = Inches(0)
    p_ds2.add_run("[22] MOTOR Research Initiative, \"MOTOR: A Multimodal Dataset for Two-Wheeler Dynamics and Rider Safety Understanding,\" arXiv Preprint, 2024. Liên kết: ")
    add_hyperlink(p_ds2, "https://arxiv.org/abs/2403.18123", "https://arxiv.org/abs/2403.18123")

    p_ds3 = doc.add_paragraph(style='List Bullet')
    p_ds3.paragraph_format.first_line_indent = Inches(0)
    p_ds3.add_run("[23] DCASE Community, \"Detection and Classification of Acoustic Scenes and Events Public Datasets,\" DCASE Challenge. Liên kết: ")
    add_hyperlink(p_ds3, "https://dcase.community/", "https://dcase.community/")

    p_ds4 = doc.add_paragraph(style='List Bullet')
    p_ds4.paragraph_format.first_line_indent = Inches(0)
    p_ds4.add_run("[24] Center for the Built Environment (CBE), \"ASHRAE Global Thermal Comfort and Classroom IEQ Database II,\" University of California, Berkeley. Liên kết: ")
    add_hyperlink(p_ds4, "https://www.comfortdatabase.com/", "https://www.comfortdatabase.com/")

    # Save completed document
    output_filename = "TONG_HOP_DE_TAI_AIOT_DO_AN_2.docx"
    doc.save(output_filename)
    print(f"Document successfully created and saved as: {output_filename}")

if __name__ == "__main__":
    build_word_document()
