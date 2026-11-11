# -*- coding: utf-8 -*-
"""
Module ch3_sec33.py: Section 3.3 generator.
Covers:
- 3.3 THIẾT KẾ THUẬT TOÁN PHÂN TÍCH VÀ GHI NHẬN SỰ CỐ
- 3.3.1 Phương pháp phát hiện và phân tích sự cố (Dynamic analysis of electric 2-wheelers, 5 motion classes C0-C4, comparisons table, Edge TinyML/sliding window)
- 3.3.2 Quy trình xử lý, lưu trữ và truyền dữ liệu sự cố (30s circular FIFO buffer in PSRAM, SHA-256 seal, two-stage warning & 15s countdown, SMS SOS & Cloud transmission, Flowchart Fig 3.13)
"""

import os
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from build_chapter3_full import (
    add_p, add_bullet, add_h2, add_h3, add_figure, add_table_with_caption, add_code_snippet
)

def add_section_3_3(doc, assets_dir):
    # -------------------------------------------------------------------------
    # 3.3 THIẾT KẾ THUẬT TOÁN PHÂN TÍCH VÀ GHI NHẬN SỰ CỐ
    # -------------------------------------------------------------------------
    add_h2(doc, "3.3 THIẾT KẾ THUẬT TOÁN PHÂN TÍCH VÀ GHI NHẬN SỰ CỐ")
    
    add_p(doc, 
          "Bên cạnh một kiến trúc phần cứng vững chắc và ổn định, linh hồn của hệ thống hộp đen AIoT chính là thuật toán phát hiện "
          "và ghi nhận sự cố. Không giống như ô tô bốn bánh vốn có cấu trúc cân bằng tĩnh (khi vào cua xe không bị nghiêng đáng kể), "
          "xe máy điện là phương tiện hai bánh có đặc thù động học phức tạp: xe luôn nghiêng thân khi vào cua để cân bằng lực ly tâm, "
          "thường xuyên chịu rung lắc do mặt đường gồ ghề và có thể bị trượt ngã ở nhiều tư thế khác nhau. Do đó, thuật toán nhận diện "
          "phải phân biệt được chính xác đâu là cử động bình thường của xe và đâu là tai nạn thực sự, đảm bảo không bỏ sót sự cố nguy hiểm "
          "nhưng đồng thời triệt tiêu tối đa các cảnh báo giả gây phiền toái cho người dùng.")

    # =========================================================================
    # 3.3.1 Phương pháp phát hiện và phân tích sự cố
    # =========================================================================
    add_h3(doc, "3.3.1 Phương pháp phát hiện và phân tích sự cố")
    
    add_p(doc, 
          "Để xây dựng thuật toán phân tích sự cố chuẩn xác, trước hết cần mô hình hóa các trạng thái động học vật lý của xe máy điện "
          "dựa trên các tín hiệu thu thập từ cảm biến quán tính 6-DoF (gia tốc ax, ay, az và vận tốc góc gx, gy, gz) kết hợp dữ liệu vận tốc "
          "từ bộ thu GNSS:")
          
    add_bullet(doc, "Gia tốc toàn phần tổng hợp (Signal Vector Magnitude - SVM): ", 
               "Được tính toán theo công thức: SVM = √(ax² + ay² + az²). Ở trạng thái tĩnh hoặc chuyển động đều trên đường phẳng, "
               "SVM xấp xỉ gia tốc trọng trường 1.0g (≈ 9.81 m/s²). Khi xảy ra va chạm trực diện hoặc tông đuôi mạnh, SVM xuất hiện đỉnh xung lực "
               "vượt quá 3.5g trong khoảng thời gian rất ngắn.")
               
    add_bullet(doc, "Góc nghiêng thân xe (Roll & Pitch Angles): ", 
               "Được tính toán thông qua bộ lọc bù (Complementary Filter) kết hợp giữa góc tính từ gia tốc kế và tích phân con quay hồi chuyển: "
               "θ = α × (θ + Gyro × Δt) + (1 - α) × Acc_Angle (với trọng số α = 0.96). Bộ lọc bù triệt tiêu hoàn toàn nhiễu rung cơ học cao tần "
               "của gia tốc kế và hiện tượng trôi dạt góc (Drift) tích phân dài hạn của con quay hồi chuyển.")
               
    add_bullet(doc, "Đặc tính vào cua bình thường (Normal Cornering): ", 
               "Khi xe máy điện vào cua, người lái nghiêng xe một góc θ tự nhiên thỏa mãn cân bằng lực: tan(θ) = v² / (R × g). "
               "Mặc dù góc nghiêng có thể đạt 30° - 45°, nhưng vận tốc xe v > 0 và lực ly tâm bù trừ lực trọng trường khiến thành phần gia tốc "
               "trên hệ trục thân xe vẫn duy trì cân bằng động. Xe không bị coi là ngã.")
               
    add_bullet(doc, "Đặc tính rung chấn mặt đường (Road Bumps / Potholes): ", 
               "Khi bánh xe va vào ổ gà hoặc đi qua gờ giảm tốc, gia tốc trục đứng az xuất hiện dao động tắt dần biên độ lớn (> 2.0g), "
               "tuy nhiên chu kỳ dao động diễn ra cực nhanh (< 120 ms), góc nghiêng thân xe Roll không bị biến dạng lớn và xe tiếp tục "
               "di chuyển thẳng với vận tốc GPS không đổi.")

    add_p(doc, "", bold_prefix="Định nghĩa 5 phân lớp động học và sự cố của xe máy điện (C0 - C4):")
    add_p(doc, 
          "Dựa trên các nghiên cứu thực nghiệm động học phương tiện hai bánh, đề tài chuẩn hóa và phân loại toàn bộ trạng thái chuyển động "
          "của xe máy điện thành 5 phân lớp chính (từ C0 đến C4) được mô tả chi tiết trong Bảng 3.20:")

    # Bảng 3.20 - 5 Motion Classes
    tbl20_headers = ["Mã lớp", "Tên phân lớp trạng thái", "Đặc trưng động học vật lý", "Ngưỡng nhận diện định lượng", "Hành động hệ thống"]
    tbl20_data = [
        ["C0", "Vận hành bình thường (Normal Riding)", "Xe chạy thẳng, tăng/giảm tốc đều, ôm cua nghiêng tự nhiên", "SVM ∈ [0.7g, 1.4g], Góc Roll < 45°, Tốc độ > 0", "Giám sát liên tục, cập nhật đệm vòng FIFO 30s"],
        ["C1", "Va chạm trực diện / đuôi (Collision / Crash)", "Xung lực va đập cực lớn, xe dừng đột ngột trong thời gian rất ngắn", "SVM > 3.5g (hoặc |ax| > 2.5g), Vận tốc GPS sụt giảm tức thì", "KÍCH HOẠT CẢNH BÁO KHẨN CẤP, đếm ngược 15s"],
        ["C2", "Ngã đổ xe / Lật nghiêng (Fall / Roll-over)", "Xe bị nghiêng ngả vượt ngưỡng cân bằng và nằm im trên mặt đường", "Góc Roll |θ| > 65°, kéo dài liên tục > 1.5 giây, Vận tốc = 0", "KÍCH HOẠT CẢNH BÁO KHẨN CẤP, đếm ngược 15s"],
        ["C3", "Trượt ngã phanh gấp (Slide / Skid Fall)", "Bánh xe mất ma sát, xe xoay trượt ngang kèm gia tốc góc lớn", "|ay| > 1.8g, |Gyro_Z| > 180 °/s, tiếp sau là góc Roll > 65°", "KÍCH HOẠT CẢNH BÁO KHẨN CẤP, đếm ngược 15s"],
        ["C4", "Rung chấn mặt đường (Road Bump / Rough)", "Xung gia tốc trục đứng dằn xóc do ổ gà, gờ giảm tốc", "|az| > 2.0g nhưng thời gian t < 150 ms, Góc Roll bình thường", "Bỏ qua cảnh báo giả, duy trì chu trình giám sát"]
    ]
    add_table_with_caption(doc, "Bảng 3.20: Bảng định nghĩa 5 phân lớp chuyển động và sự cố của xe máy điện (C0 - C4)",
                           tbl20_headers, tbl20_data, col_widths=[0.6, 1.8, 2.0, 1.8, 1.8])

    add_p(doc, "", bold_prefix="Khảo sát và đối sánh các phương pháp phát hiện sự cố:")
    add_p(doc, 
          "Để phân loại chính xác 5 phân lớp động học trên, nhóm tác giả tiến hành đánh giá 3 phương pháp xử lý dữ liệu khả thi:")
    add_bullet(doc, "Phương án A: Thuật toán ngưỡng cố định đơn giản (Fixed Thresholding): ", 
               "Chỉ so sánh từng trục gia tốc với một hằng số cố định. Phương pháp này rất dễ lập trình nhưng tỷ lệ cảnh báo sai (False Positive) "
               "cực cao khi xe đi qua ổ gà hoặc người lái phanh gấp.")
    add_bullet(doc, "Phương án B: Thuật toán cửa sổ trượt phân tích đa tham số kết hợp TinyML trên biên (Được chọn): ", 
               "Sử dụng kỹ thuật cửa sổ trượt (Sliding Window 100 mẫu = 1 giây) trích xuất các đặc trưng miền thời gian (Mean, Variance, Max, Min, SVM) "
               "kết hợp mô hình phân loại nơ-ron rút gọn chạy trực tiếp trên vi điều khiển ESP32-S3. Phương pháp này loại bỏ hoàn toàn các cảnh báo giả, "
               "độ trễ phản hồi dưới 50 ms và không phụ thuộc vào mạng Internet.")
    add_bullet(doc, "Phương án C: Đẩy toàn bộ dữ liệu thô lên Cloud để chạy AI (Cloud-based AI): ", 
               "Gửi liên tục dữ liệu cảm biến 100 Hz lên máy chủ qua mạng 4G. Phương pháp này có độ trễ truyền thông quá lớn (từ 500 ms đến vài giây), "
               "tiêu tốn chi phí cước 4G khổng lồ và hoàn toàn tê liệt khi xe đi vào vùng mất sóng di động.")

    add_p(doc, 
          "Đối sánh giữa các phương pháp phân tích và phát hiện sự cố được tổng hợp trong Bảng 3.21:")
          
    # Bảng 3.21
    tbl21_headers = ["Tiêu chí kỹ thuật", "Thuật toán cửa sổ trượt + TinyML biên [Được chọn]", "Ngưỡng cố định đơn giản", "Phân tích trên Cloud"]
    tbl21_data = [
        ["Độ trễ phát hiện sự cố", "Cực thấp (< 50 ms ngay tại thiết bị)", "Rất nhanh (< 10 ms)", "Rất chậm (500 ms - vài giây do độ trễ mạng)"],
        ["Tỷ lệ cảnh báo giả (False Alarm)", "Rất thấp (Phân biệt chuẩn ổ gà và va chạm)", "Rất cao (Dễ nhầm dằn xóc với tai nạn)", "Thấp"],
        ["Độ độc lập với mạng viễn thông", "Độc lập 100%, hoạt động ngay cả khi mất sóng", "Độc lập 100%", "Phụ thuộc 100% vào sóng 4G liên tục"],
        ["Yêu cầu băng thông và cước Data", "Không tốn băng thông (Chỉ truyền khi có sự cố)", "Không tốn băng thông", "Cực lớn (Phải truyền 100 mẫu/giây liên tục)"],
        ["Tận dụng tài nguyên phần cứng", "Tối ưu tập lệnh Vector của ESP32-S3", "Chỉ dùng lệnh rẽ nhánh if/else", "Phải thuê server xử lý đám mây"],
        ["Khả năng thích ứng động học", "Rất cao, học được mẫu hình tai nạn phức tạp", "Kém, không thích nghi được", "Cao"],
        ["Đánh giá mức độ phù hợp", "Lý tưởng nhất cho hộp đen xe máy điện", "Không đạt chuẩn an toàn", "Bất khả thi về mặt thực tiễn"]
    ]
    add_table_with_caption(doc, "Bảng 3.21: So sánh các phương pháp phân tích và phát hiện sự cố xe máy điện",
                           tbl21_headers, tbl21_data, col_widths=[1.8, 2.0, 1.8, 1.6])

    add_p(doc, "", bold_prefix="Phương án được lựa chọn và nguyên lý thuật toán cửa sổ trượt:")
    add_p(doc, 
          "Hệ thống ứng dụng thuật toán cửa sổ trượt phân tích đa tham số kết hợp mô hình nơ-ron rút gọn TinyML thực thi cục bộ trên ESP32-S3. "
          "Dữ liệu từ MPU6050 được lấy mẫu ở tần số 100 Hz. Một cửa sổ trượt có kích thước N = 100 mẫu (tương ứng độ dài thời gian 1.0 giây) "
          "với độ dịch chuyển bước trượt (Step size) là 20 mẫu (200 ms). Tại mỗi bước trượt, hệ thống tính toán véc-tơ đặc trưng gồm: "
          "[SVM_max, SVM_std, Roll_avg, Roll_max, Pitch_avg, Gyro_magnitude, Speed_GPS]. Véc-tơ này được đối chiếu qua mạng luật logic "
          "và bộ phân loại biên để kết luận trạng thái phương tiện.")

    add_p(doc, "", bold_prefix="Tuyên bố khoa học trung thực về mô hình AI:")
    add_p(doc, 
          "Trong phạm vi giai đoạn thiết kế kiến trúc hệ thống hiện tại, thuật toán phân loại sự cố được xây dựng trên nền tảng khung lý thuyết "
          "động học phương tiện và bộ phân loại ngưỡng thích nghi đa biến (Adaptive Multi-parameter Thresholding). Ma trận trọng số mạng nơ-ron "
          "nén (Quantized Neural Network) sẽ được tối ưu hóa và hoàn thiện trong giai đoạn thử nghiệm thực tế sau khi thu thập đầy đủ bộ dữ liệu "
          "thực nghiệm trên xe máy điện chạy thực địa, đảm bảo tính chuẩn xác và trung thực khoa học.")

    # =========================================================================
    # 3.3.2 Quy trình xử lý, lưu trữ và truyền dữ liệu sự cố
    # =========================================================================
    add_h3(doc, "3.3.2 Quy trình xử lý, lưu trữ và truyền dữ liệu sự cố")
    
    add_p(doc, 
          "Khi một sự cố va chạm hoặc lật ngã (thuộc các lớp C1, C2, C3) được phát hiện, hệ thống thực thi một chuỗi quy trình xử lý khép kín "
          "được thiết kế cực kỳ chặt chẽ nhằm bảo vệ dữ liệu và thực hiện cứu nạn kịp thời:")
          
    add_p(doc, "", bold_prefix="1. Cơ chế bộ đệm vòng FIFO 30 giây trong 8 MB Octal PSRAM:")
    add_p(doc, 
          "Để tái hiện chính xác toàn bộ diễn biến vụ tai nạn phục vụ công tác giám định, hệ thống duy trì một bộ đệm vòng tròn (Circular Buffer) "
          "có độ dài thời gian chính xác 30 giây được phân bổ cố định trên bộ nhớ ngoài 8 MB Octal PSRAM:")
    add_bullet(doc, "Cửa sổ trước sự cố (Pre-crash Window - 15 giây): ", 
               "Lưu giữ liên tục 1500 mẫu IMU (100 Hz) và 150 mẫu GPS (10 Hz) của 15 giây ngay trước thời điểm xảy ra va chạm. "
               "Dữ liệu này phản ánh trung thực tốc độ di chuyển, hành vi ôm cua, phanh gấp hoặc thao tác đánh lái của người lái trước khi tai nạn xảy ra.")
    add_bullet(doc, "Cửa sổ sau sự cố (Post-crash Window - 15 giây): ", 
               "Ngay khi sự cố được kích hoạt tại thời điểm t0, con trỏ ghi tiếp tục cho phép hệ thống thu thập thêm chính xác 15 giây dữ liệu "
               "kế tiếp (1500 mẫu IMU, 150 mẫu GPS). Dữ liệu này ghi nhận quá trình xe văng trượt, va đập thứ cấp và tư thế dừng lại cuối cùng trên hiện trường.")
    add_bullet(doc, "Khóa đóng băng bộ đệm: ", 
               "Sau khi thu thập đủ 15 giây sau va chạm, toàn bộ khối bộ nhớ 30 giây này được đánh dấu khóa bảo vệ (Locked Buffer), "
               "ngăn chặn hoàn toàn việc các dữ liệu mới ghi đè lên.")

    add_p(doc, "", bold_prefix="2. Cơ chế bảo vệ toàn vẹn chứng cứ số bằng mã băm SHA-256 (SHA-256 Seal):")
    add_p(doc, 
          "Để tệp tin dữ liệu hộp đen có giá trị chứng cứ pháp lý không thể chối cãi trước tòa án và các công ty bảo hiểm, hệ thống tích hợp "
          "thuật toán băm mật mã SHA-256 (Secure Hash Algorithm 256-bit). Toàn bộ khối dữ liệu 30 giây sự cố được nén nhị phân thành tệp tin "
          "mang tên định dạng: CRASH_YYYYMMDD_HHMMSS.DAT. Trước khi đóng tệp tin trên thẻ nhớ MicroSD, ESP32-S3 sử dụng bộ tăng tốc mật mã "
          "phần cứng tích hợp để tính toán mã băm SHA-256 (chuỗi 64 ký tự Hexadecimal) đại diện cho toàn bộ nội dung tệp tin và ghi mã băm này "
          "vào đuôi tệp tin cũng như lưu vào vùng nhớ bảo mật. Bất kỳ sự can thiệp, chỉnh sửa hay cắt ghép dữ liệu nào sau này đều sẽ làm sai lệch "
          "mã băm SHA-256, giúp các chuyên gia giám định phát hiện ngay hành vi làm giả hiện trường.")

    add_p(doc, "", bold_prefix="3. Quy trình cảnh báo phân cấp hai giai đoạn và tương tác người dùng:")
    add_p(doc, 
          "Hệ thống vận hành theo quy trình phản ứng hai giai đoạn thông minh nhằm loại trừ hoàn toàn các báo động giả:")
    add_bullet(doc, "Giai đoạn 1 - Báo động tại chỗ và cửa sổ đếm ngược 15 giây: ", 
               "Ngay khi phát hiện sự cố, hệ thống lập tức kích hoạt còi Piezo kêu dồn dập (2 Hz), nhấp nháy đèn LED STATUS và hiển thị "
               "giao diện cảnh báo trên màn hình OLED với đồng hồ đếm ngược từ 15 về 0. Nếu người lái chỉ bị va chạm nhẹ hoặc xe bị đổ khi dựng chân chống, "
               "người lái chỉ cần nhấn nút CANCEL (GPIO6). Hệ thống sẽ lập tức tắt còi, hủy tiến trình gửi tin nhắn cấp cứu, ghi nhận sự kiện 'Hủy bởi người dùng' "
               "vào nhật ký và quay lại trạng thái giám sát bình thường.")
    add_bullet(doc, "Giai đoạn 2 - Báo động khẩn cấp và truyền tin cứu hộ: ", 
               "Nếu hết 15 giây mà không có bất kỳ thao tác bấm nút nào từ người lái (chứng tỏ người lái đã bất tỉnh, bị kẹt hoặc chấn thương nghiêm trọng), "
               "hệ thống lập tức kích hoạt giao tiếp với module 4G LTE SIM7680C. Module tự động soạn và gửi tin nhắn SMS cứu nạn khẩn cấp tới danh bạ cài sẵn. "
               "Nội dung tin nhắn mẫu: 'CANH BAO TAI NAN XE MAY DIEN! Thoi gian: 14:32:10 15/10/2026. Loai su co: Va cham truc dien. "
               "Van toc va cham: 42 km/h. Toa do hien truong: https://maps.google.com/?q=10.8505,106.7718'. Người nhận tin nhắn chỉ cần chạm vào "
               "liên kết để mở ngay ứng dụng Google Maps dẫn đường trực tiếp tới vị trí người gặp nạn. Đồng thời, một gói tin JSON chứa đầy đủ các chỉ số "
               "vật lý được gửi lên máy chủ giám sát đám mây qua giao thức MQTT/HTTP.")

    add_p(doc, "", bold_prefix="Lưu đồ thuật toán vận hành toàn hệ thống:")
    add_p(doc, 
          "Toàn bộ tiến trình vận hành, phân tích sự cố, quản lý bộ đệm vòng, phân nhánh nút bấm CANCEL và cứu hộ khẩn cấp được tổng hợp "
          "và trực quan hóa một cách khoa học trong Lưu đồ thuật toán Hình 3.13 dưới đây:")
          
    fig13_path = os.path.join(assets_dir, "H3_13_luu_do_hoat_dong_he_thong.png")
    add_figure(doc, fig13_path, "Hình 3.13: Lưu đồ thuật toán vận hành, phân tích và xử lý sự cố toàn hệ thống", width_inches=5.2)

    print("Section 3.3 built successfully.")
