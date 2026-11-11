# -*- coding: utf-8 -*-
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

def build_excel_report():
    wb = openpyxl.Workbook()
    # Remove default sheet
    default_sheet = wb.active
    wb.remove(default_sheet)

    # Styles
    font_family = "Segoe UI"
    
    title_font = Font(name=font_family, size=15, bold=True, color="1B365D")
    subtitle_font = Font(name=font_family, size=11, italic=True, color="475569")
    h2_font = Font(name=font_family, size=12, bold=True, color="1B365D")
    
    header_font = Font(name=font_family, size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    
    category_font = Font(name=font_family, size=11, bold=True, color="0F2C59")
    category_fill = PatternFill(start_color="E2E8F0", end_color="E2E8F0", fill_type="solid")
    
    total_font = Font(name=font_family, size=11, bold=True, color="0F172A")
    total_fill = PatternFill(start_color="CBD5E1", end_color="CBD5E1", fill_type="solid")
    
    highlight_total_font = Font(name=font_family, size=11, bold=True, color="991B1B")
    highlight_total_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
    
    contingency_font = Font(name=font_family, size=11, bold=True, color="92400E")
    contingency_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
    
    data_font = Font(name=font_family, size=10.5, color="1E293B")
    link_font = Font(name=font_family, size=10.5, color="0284C7", underline="single")
    bold_data_font = Font(name=font_family, size=10.5, bold=True, color="1E293B")
    
    mand_font = Font(name=font_family, size=10, bold=True, color="166534")
    mand_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
    
    opt_font = Font(name=font_family, size=10, bold=True, color="854D0E")
    opt_fill = PatternFill(start_color="FEF9C3", end_color="FEF9C3", fill_type="solid")
    
    zebra_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    
    thin_gray = Side(style='thin', color="D0D5DD")
    border_all = Border(left=thin_gray, right=thin_gray, top=thin_gray, bottom=thin_gray)
    double_bottom = Border(left=thin_gray, right=thin_gray, top=thin_gray, bottom=Side(style='double', color="1B365D"))
    
    currency_fmt = '#,##0 "₫"'
    date_fmt = 'DD/MM/YYYY'
    
    # -------------------------------------------------------------
    # SHEET 1: TONG_QUAN
    # -------------------------------------------------------------
    ws1 = wb.create_sheet(title="TONG_QUAN")
    ws1.views.sheetView[0].showGridLines = True
    
    ws1.cell(row=2, column=2, value="DỰ TOÁN CHI PHÍ & BẢNG BÓC TÁCH LINH KIỆN (BOM)").font = title_font
    ws1.cell(row=3, column=2, value="Đề tài: Hộp đen AIoT thông minh phân tích và tái hiện hiện trường tai nạn xe máy").font = subtitle_font
    ws1.cell(row=4, column=2, value="Thời điểm khảo sát giá: Tháng 09/2026 | Nguồn dữ liệu: Hshop, ThegioiIC, Nshop, Dientu360, Shopee").font = subtitle_font
    
    # Block 1: Summary of Cost Levels
    ws1.cell(row=6, column=2, value="1. TỔNG HỢP CÁC MỨC NGÂN SÁCH DỰ ÁN").font = h2_font
    
    summary_headers = ["Mức cấu hình", "Mô tả phạm vi kỹ thuật", "Chi phí phần cứng", "Dự phòng (10%)", "Tổng ngân sách"]
    for col_idx, h in enumerate(summary_headers, start=2):
        cell = ws1.cell(row=7, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_all
        
    cost_levels_data = [
        ("Cấu hình A: Tối thiểu (Minimum Prototype)", "Chạy demo trên bàn Lab (ESP32-S3 + IMU + GPS + MicroSD + WiFi)", "='CAU_HINH_CHI_PHI'!E27", "=D8*0.1", "=D8+E8"),
        ("Cấu hình B: Khuyến nghị (Recommended ĐA2)", "Bản hoàn chỉnh nộp ĐA2 (Mức A + RTC DS3231 + SIM 4G + LM2596 + Pin Li-ion + Hộp ABS)", "='CAU_HINH_CHI_PHI'!F27", "=D9*0.1", "=D9+E9"),
        ("Cấu hình C: Khóa luận Tốt nghiệp (KLTN)", "Bản mở rộng KLTN (Mức B + Micro I2S + IMU ICM-42688 + Camera + Gia công PCB)", "='CAU_HINH_CHI_PHI'!G27", "=D10*0.1", "=D10+E10"),
    ]
    
    for row_idx, row in enumerate(cost_levels_data, start=8):
        ws1.cell(row=row_idx, column=2, value=row[0]).font = bold_data_font
        ws1.cell(row=row_idx, column=3, value=row[1]).font = data_font
        
        c_hw = ws1.cell(row=row_idx, column=4, value=row[2])
        c_hw.font = bold_data_font
        c_hw.number_format = currency_fmt
        c_hw.alignment = Alignment(horizontal="right")
        
        c_ctg = ws1.cell(row=row_idx, column=5, value=row[3])
        c_ctg.font = data_font
        c_ctg.number_format = currency_fmt
        c_ctg.alignment = Alignment(horizontal="right")
        
        c_tot = ws1.cell(row=row_idx, column=6, value=row[4])
        c_tot.font = highlight_total_font if row_idx == 9 else bold_data_font
        c_tot.fill = highlight_total_fill if row_idx == 9 else white_fill
        c_tot.number_format = currency_fmt
        c_tot.alignment = Alignment(horizontal="right")
        
        for c in range(2, 7):
            ws1.cell(row=row_idx, column=c).border = border_all
            
    # Block 2: Breakdown by Category for Recommended Project 2
    ws1.cell(row=12, column=2, value="2. CƠ CẤU CHI PHÍ CẤU HÌNH KHUYẾN NGHỊ ĐỒ ÁN 2 (THEO NHÓM LINH KIỆN)").font = h2_font
    
    cat_headers = ["STT", "Nhóm linh kiện", "Thành phần đại diện", "Chi phí ước tính", "Tỷ trọng (%)"]
    for col_idx, h in enumerate(cat_headers, start=2):
        cell = ws1.cell(row=13, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_all
        
    cat_breakdown = [
        (1, "Vi điều khiển (Microcontroller)", "ESP32-S3-DevKitC-1 N16R8 (8MB PSRAM)", "='BOM_DA2'!L6"),
        (2, "Cảm biến chuyển động (Sensors)", "IMU MPU6050 (GY-521)", "='BOM_DA2'!L7"),
        (3, "Định vị toàn cầu (GPS)", "Module GPS NEO-6M kèm anten gốm", "='BOM_DA2'!L8"),
        (4, "Lưu trữ dữ liệu (Storage)", "Module đọc thẻ SPI + Thẻ MicroSD 32GB SanDisk", "='BOM_DA2'!L9+'BOM_DA2'!L10"),
        (5, "Đồng hồ thời gian thực (RTC)", "Module RTC DS3231 kèm pin cúc áo", "='BOM_DA2'!L11"),
        (6, "Khối nguồn điện (Power System)", "Hạ áp LM2596 + Pin Li-ion 18650 + Mạch sạc TP4056", "='BOM_DA2'!L12+'BOM_DA2'!L13+'BOM_DA2'!L14"),
        (7, "Truyền thông viễn thông (IoT)", "Module 4G LTE SIM7680C + SIM 4G Viettel IoT", "='BOM_DA2'!L15+'BOM_DA2'!L16"),
        (8, "Phụ kiện lắp ráp (Accessories)", "Breadboard, Dây cắm, Cáp Type-C, Còi, Nút, Hộp ABS, Proto PCB", "='BOM_DA2'!L17+'BOM_DA2'!L18+'BOM_DA2'!L19+'BOM_DA2'!L20+'BOM_DA2'!L21+'BOM_DA2'!L22"),
    ]
    
    for idx, row in enumerate(cat_breakdown, start=14):
        ws1.cell(row=idx, column=2, value=row[0]).alignment = Alignment(horizontal="center")
        ws1.cell(row=idx, column=3, value=row[1]).font = bold_data_font
        ws1.cell(row=idx, column=4, value=row[2]).font = data_font
        
        c_val = ws1.cell(row=idx, column=5, value=row[3])
        c_val.font = bold_data_font
        c_val.number_format = currency_fmt
        c_val.alignment = Alignment(horizontal="right")
        
        c_pct = ws1.cell(row=idx, column=6, value=f"=E{idx}/E22")
        c_pct.font = data_font
        c_pct.number_format = "0.0%"
        c_pct.alignment = Alignment(horizontal="right")
        
        for c in range(2, 7):
            ws1.cell(row=idx, column=c).border = border_all
            
    # Total Category Row
    ws1.cell(row=22, column=2, value="").border = double_bottom
    ws1.cell(row=22, column=3, value="TỔNG CHI PHÍ PHẦN CỨNG ĐA2").font = total_font
    ws1.cell(row=22, column=4, value="17 Hạng mục hoàn chỉnh").font = total_font
    
    c_tot_cat = ws1.cell(row=22, column=5, value="=SUM(E14:E21)")
    c_tot_cat.font = total_font
    c_tot_cat.fill = total_fill
    c_tot_cat.number_format = currency_fmt
    c_tot_cat.alignment = Alignment(horizontal="right")
    
    c_tot_pct = ws1.cell(row=22, column=6, value="=SUM(F14:F21)")
    c_tot_pct.font = total_font
    c_tot_pct.fill = total_fill
    c_tot_pct.number_format = "0.0%"
    c_tot_pct.alignment = Alignment(horizontal="right")
    
    for c in range(2, 7):
        ws1.cell(row=22, column=c).border = double_bottom
        
    # Block 3: Purchasing Recommendations
    # Block 3: Linh kien nen mua truoc (Phase 1)
    ws1.cell(row=24, column=2, value="3. LINH KIỆN NÊN MUA TRƯỚC (BẮT BUỘC ĐỂ KHỞI ĐỘNG DỰ ÁN)").font = h2_font
    
    first_buy_headers = ["STT", "Linh kiện ưu tiên mua trước", "Model khuyến nghị", "Đơn giá", "Lý do bắt buộc phải mua trước để bắt đầu dự án"]
    for col_idx, h in enumerate(first_buy_headers, start=2):
        cell = ws1.cell(row=25, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_all
        
    first_buy_data = [
        (1, "Bo mạch vi điều khiển ESP32-S3", "ESP32-S3-DevKitC-1 N16R8", 185000, 
         "Bộ não trung tâm; cần mua đầu tiên để cài toolchain PlatformIO, kiểm tra 8MB PSRAM và dựng khung đa luồng FreeRTOS."),
        (2, "Cảm biến quán tính IMU 6 trục", "MPU6050 (GY-521)", 75000, 
         "Thu thập dữ liệu rung chấn, va chạm, lật góc để tạo tập dữ liệu huấn luyện mô hình TinyML trên Edge Impulse."),
        (3, "Mạch đọc thẻ MicroSD", "MicroSD SPI Module", 20000, 
         "Xây dựng hệ thống tệp FATFS trên giao tiếp SPI và kiểm thử chức năng lưu trữ file log nhị phân/CSV."),
        (4, "Thẻ nhớ MicroSD 32GB Class 10", "SanDisk Ultra 32GB A1", 85000, 
         "Cần có cùng mạch đọc để kiểm tra độ trễ ghi thực tế (write latency); thẻ kém chất lượng sẽ làm tràn circular buffer."),
        (5, "Module định vị GPS", "GY-NEO6MV2 kèm anten gốm", 135000, 
         "Lập trình ngắt UART nhận bản tin NMEA, bóc tách tọa độ kinh vĩ độ và tốc độ xe phục vụ định vị hiện trường."),
        (6, "Phụ kiện thử nghiệm cơ bản", "Breadboard, Dây cắm, Cáp Type-C", 101000, 
         "Dụng cụ cắm mạch và nạp code/debug Serial Monitor; không thể bắt đầu lập trình nếu thiếu các phụ kiện này.")
    ]
    
    for idx, r in enumerate(first_buy_data, start=26):
        ws1.cell(row=idx, column=2, value=r[0]).alignment = Alignment(horizontal="center")
        ws1.cell(row=idx, column=3, value=r[1]).font = bold_data_font
        ws1.cell(row=idx, column=4, value=r[2]).font = data_font
        
        c_pr = ws1.cell(row=idx, column=5, value=r[3])
        c_pr.font = bold_data_font
        c_pr.number_format = currency_fmt
        c_pr.alignment = Alignment(horizontal="right")
        
        c_rs = ws1.cell(row=idx, column=6, value=r[4])
        c_rs.font = data_font
        c_rs.alignment = Alignment(wrap_text=True)
        
        for c in range(2, 7):
            ws1.cell(row=idx, column=c).border = border_all
            
    # Total for first buy
    tot_fb_row = 26 + len(first_buy_data)
    ws1.cell(row=tot_fb_row, column=2, value="").border = double_bottom
    ws1.cell(row=tot_fb_row, column=3, value="TỔNG CHI PHÍ ĐỢT 1 (KHỞI ĐỘNG LAB)").font = total_font
    ws1.cell(row=tot_fb_row, column=4, value="6 Hạng mục thiết yếu").font = total_font
    c_tot_fb = ws1.cell(row=tot_fb_row, column=5, value=f"=SUM(E26:E{tot_fb_row-1})")
    c_tot_fb.font = total_font
    c_tot_fb.fill = total_fill
    c_tot_fb.number_format = currency_fmt
    c_tot_fb.alignment = Alignment(horizontal="right")
    ws1.cell(row=tot_fb_row, column=6, value="Chỉ cần ~601.000 ₫ là hoàn thành được 80% phần mềm & AI của ĐA2").font = bold_data_font
    for c in range(2, 7):
        ws1.cell(row=tot_fb_row, column=c).border = double_bottom

    # Block 4: Linh kien chua can mua ngay
    start_not_yet = tot_fb_row + 2
    ws1.cell(row=start_not_yet, column=2, value="4. LINH KIỆN CHƯA CẦN MUA NGAY (TRÁNH LÃNG PHÍ NGÂN SÁCH BAN ĐẦU)").font = h2_font
    
    not_yet_headers = ["STT", "Linh kiện chưa cần mua ngay", "Chi phí (VNĐ)", "Thời điểm nên mua", "Lý do chưa cần mua trong giai đoạn đầu"]
    for col_idx, h in enumerate(not_yet_headers, start=2):
        cell = ws1.cell(row=start_not_yet+1, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_all
        
    not_yet_data = [
        (1, "Module 4G LTE SIM7680C", 245000, "Tuần 5 - Tuần 7", 
         "Chưa cần mua ở tuần đầu; chỉ mua khi thuật toán AI và lưu trữ SD đã hoạt động trơn tru trên bàn Lab."),
        (2, "SIM 4G IoT duy trì kết nối", 50000, "Tuần 6 - Tuần 7", 
         "Mua cùng module 4G; nếu mua sớm sẽ bị trôi ngày cước thuê bao di động lãng phí trong thời gian viết code."),
        (3, "Mạch hạ áp LM2596 & Pin Li-ion 18650", 87000, "Tuần 7 - Tuần 8", 
         "Chỉ cần khi lắp mạch lên xe máy thật; giai đoạn phát triển Lab dùng trực tiếp nguồn 5V qua cáp Type-C máy tính."),
        (4, "Hộp bảo vệ nhựa ABS IP65", 45000, "Tuần 8 (Hoàn thiện)", 
         "Chỉ mua khi đã cố định kích thước cụm linh kiện; mua sớm dễ bị chật hoặc khoét lỗ sai vị trí cổng cắm."),
        (5, "Micro INMP441, Camera OV2640, PCB JLCPCB", 440000, "Khóa luận Tốt nghiệp", 
         "Thuộc phạm vi nâng cấp KLTN (âm thanh va đập & chụp ảnh hiện trường); Đồ án 2 không bắt buộc để tránh quá tải.")
    ]
    
    for idx, r in enumerate(not_yet_data, start=start_not_yet+2):
        ws1.cell(row=idx, column=2, value=r[0]).alignment = Alignment(horizontal="center")
        ws1.cell(row=idx, column=3, value=r[1]).font = bold_data_font
        
        c_pr = ws1.cell(row=idx, column=4, value=r[2])
        c_pr.font = bold_data_font
        c_pr.number_format = currency_fmt
        c_pr.alignment = Alignment(horizontal="right")
        
        ws1.cell(row=idx, column=5, value=r[3]).alignment = Alignment(horizontal="center")
        
        c_rs = ws1.cell(row=idx, column=6, value=r[4])
        c_rs.font = data_font
        c_rs.alignment = Alignment(wrap_text=True)
        
        for c in range(2, 7):
            ws1.cell(row=idx, column=c).border = border_all
            
    # Auto-fit columns for Sheet 1
    ws1.column_dimensions['B'].width = 8
    ws1.column_dimensions['C'].width = 36
    ws1.column_dimensions['D'].width = 28
    ws1.column_dimensions['E'].width = 20
    ws1.column_dimensions['F'].width = 46

    # -------------------------------------------------------------
    # SHEET 2: BOM_DA2
    # -------------------------------------------------------------
    ws2 = wb.create_sheet(title="BOM_DA2")
    ws2.views.sheetView[0].showGridLines = True
    
    ws2.cell(row=2, column=2, value="BẢNG BÓC TÁCH LINH KIỆN MUA SẮM ĐỒ ÁN 2 (BOM - BILL OF MATERIALS)").font = title_font
    ws2.cell(row=3, column=2, value="Cấu hình khuyến nghị chính thức cho mẫu thử nghiệm Đồ án 2").font = subtitle_font
    
    bom_cols = [
        "STT", "Nhóm linh kiện", "Tên linh kiện", "Model đề xuất", "Thông số chính", 
        "Mục đích sử dụng", "Phân loại", "Số lượng", "Giá thấp nhất", "Giá cao nhất", 
        "Giá lựa chọn", "Thành tiền", "Nơi bán", "Tên shop", "Link sản phẩm", "Ngày kiểm tra", "Ghi chú"
    ]
    
    for c_idx, h in enumerate(bom_cols, start=1):
        cell = ws2.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border_all
        
    bom_raw_data = [
        # Vi điều khiển
        (1, "Vi điều khiển", "Bo mạch ESP32-S3", "ESP32-S3-DevKitC-1 N16R8", "Xtensa Dual-core 240MHz, 16MB Flash, 8MB PSRAM", 
         "Bộ xử lý trung tâm, chạy TinyML 1D-CNN, đệm tròn RAM", "Bắt buộc", 1, 160000, 255000, 185000, 
         "ThegioiIC", "Thế Giới IC", "https://thegioiic.com/esp32-s3-devkitc-1-n8", "20/09/2026", "Bắt buộc bản có 8MB PSRAM để chứa buffer 30s"),
         
        # Cảm biến
        (2, "Cảm biến", "Cảm biến quán tính IMU", "MPU6050 (GY-521)", "Gia tốc 3 trục ±16g, Con quay hồi chuyển ±2000°/s", 
         "Đo lực va đập, rung chấn và góc lật nghiêng xe", "Bắt buộc", 1, 55000, 85000, 75000, 
         "Hshop.vn", "Hshop TP.HCM", "https://hshop.vn/products/mach-cam-bien-gia-toc-mpu-6050-gy-521", "20/09/2026", "Cảm biến tiêu chuẩn, thư viện C++ phong phú"),
         
        # GPS
        (3, "GPS", "Module định vị GPS", "GY-NEO6MV2 / NEO-6M", "Bắt sóng GPS vệ tinh, ngõ ra UART 9600 bps kèm anten gốm", 
         "Ghi nhận tọa độ tai nạn và tốc độ di chuyển", "Bắt buộc", 1, 110000, 155000, 135000, 
         "Dientu360", "Điện Tử 360", "https://dientu360.com/module-gps-neo-6m", "20/09/2026", "Kèm sẵn anten gốm thụ động"),
         
        # Lưu trữ
        (4, "Lưu trữ", "Mạch đọc thẻ MicroSD", "MicroSD SPI Module", "Giao tiếp SPI 5V/3.3V, hỗ trợ thẻ nhớ dung lượng đến 32GB", 
         "Giao tiếp phần cứng giữa ESP32 và thẻ nhớ", "Bắt buộc", 1, 12000, 35000, 20000, 
         "ThegioiIC", "Thế Giới IC", "https://thegioiic.com", "20/09/2026", "Hỗ trợ điện áp 3.3V/5V có trở đệm"),
         
        (5, "Lưu trữ", "Thẻ nhớ MicroSD", "SanDisk Ultra 32GB Class 10", "Chuẩn A1/U1, tốc độ đọc 100MB/s, chống sốc/nhiệt", 
         "Lưu trữ vĩnh viễn file log CSV 30 giây tai nạn", "Bắt buộc", 1, 75000, 95000, 85000, 
         "Shopee Mall", "SanDisk Official", "https://shopee.vn", "20/09/2026", "Bắt buộc Class 10 chính hãng tránh nghẽn ghi"),
         
        # Đồng hồ thời gian thực
        (6, "Thời gian thực", "Module RTC DS3231", "DS3231 I2C AT24C32", "Đồng hồ thạch anh bù nhiệt sai số <2ppm, kèm pin CR2032", 
         "Giữ mốc giờ chính xác khi xe mất GPS hoặc tắt máy", "Khuyến nghị", 1, 50000, 70000, 60000, 
         "ThegioiIC", "Thế Giới IC", "https://thegioiic.com", "20/09/2026", "Kèm pin nuôi độc lập"),
         
        # Nguồn
        (7, "Nguồn điện", "Mạch hạ áp DC-DC", "LM2596S Buck 3A", "Điện áp vào 4-35V, ra 5V/3A ổn định hiệu suất cao", 
         "Hạ áp từ ắc-quy 12V xe máy nuôi toàn bộ mạch", "Bắt buộc", 1, 20000, 35000, 25000, 
         "Hshop.vn", "Hshop TP.HCM", "https://hshop.vn", "20/09/2026", "Tụ lọc Low-ESR chống sụt áp"),
         
        (8, "Nguồn điện", "Pin Li-ion dự phòng", "Cell pin 18650 2000mAh", "Pin sạc Li-ion 3.7V dung lượng 2000mAh", 
         "Nguồn nuôi khẩn cấp 30 giây khi ắc-quy xe bị đứt", "Khuyến nghị", 1, 45000, 65000, 50000, 
         "Nshopvn", "Nshop", "https://nshopvn.com", "20/09/2026", "Duy trì ghi file khi mất nguồn chính"),
         
        (9, "Nguồn điện", "Mạch sạc pin Li-ion", "TP4056 Type-C Protection", "Sạc pin Li-ion 1A tích hợp ngắt khi quá xả <2.5V", 
         "Tự động sạc pin dự phòng khi xe nổ máy", "Khuyến nghị", 1, 10000, 15000, 12000, 
         "Hshop.vn", "Hshop TP.HCM", "https://hshop.vn", "20/09/2026", "Bản có 2 IC bảo vệ quá tải"),
         
        # Giao tiếp IoT
        (10, "Giao tiếp IoT", "Module 4G LTE Cat-1", "MKE-M21 SIM7680C", "Giao tiếp UART AT command, hỗ trợ SMS, VoLTE, TCP/MQTT", 
         "Gửi tin nhắn SMS khẩn cấp chứa link Google Maps", "Khuyến nghị", 1, 220000, 260000, 245000, 
         "Hshop.vn", "Hshop TP.HCM", "https://hshop.vn/products/mach-mke-m21-sim7680c-4g-sms-call-module", "20/09/2026", "Module 4G chuẩn, sóng 2G đã bị cắt ở VN"),
         
        (11, "Giao tiếp IoT", "SIM 4G IoT Viettel/Vina", "Gói cước IoT Data/SMS", "Sim 4G duy trì 6 tháng gửi tin nhắn cảnh báo", 
         "Duy trì kết nối viễn thông di động ngoài đường", "Khuyến nghị", 1, 40000, 60000, 50000, 
         "Đại lý Viettel", "Viettel Store", "https://vietteltelecom.vn", "20/09/2026", "Cần kích hoạt dịch vụ VoLTE/SMS"),
         
        # Phụ kiện
        (12, "Phụ kiện", "Bo cắm thử nghiệm", "Breadboard MB-102", "Bo mạch cắm lỗ thử nghiệm 830 điểm cắm", 
         "Cắm nối linh kiện thử nghiệm trên bàn Lab", "Bắt buộc", 1, 30000, 45000, 35000, 
         "Hshop.vn", "Hshop TP.HCM", "https://hshop.vn", "20/09/2026", "Dùng cho giai đoạn nghiên cứu"),
         
        (13, "Phụ kiện", "Dây cắm Jumper", "Tép dây 20cm Đực-Cái, Đực-Đực", "Dây đồng bọc nhựa 40 sợi dài 20cm", 
         "Kết nối các chân tín hiệu giữa các module", "Bắt buộc", 2, 15000, 25000, 18000, 
         "Hshop.vn", "Hshop TP.HCM", "https://hshop.vn", "20/09/2026", "2 tép gồm 1 tép Đ-C và 1 tép Đ-Đ"),
         
        (14, "Phụ kiện", "Cáp nạp Type-C", "Cáp USB Type-C 1m", "Lõi đồng truyền dữ liệu tốc độ cao và cấp nguồn", 
         "Nạp code chương trình và debug với máy tính", "Bắt buộc", 1, 25000, 40000, 30000, 
         "Shopee", "Phụ kiện số", "https://shopee.vn", "20/09/2026", "Bắt buộc cáp có truyền data"),
         
        (15, "Phụ kiện", "Khối cảnh báo tại chỗ", "Buzzer 5V + Nút nhấn 12mm", "Còi chíp báo động âm lượng 85dB + Nút nhấn hủy", 
         "Phát còi đếm ngược 15s và cho người lái bấm hủy", "Bắt buộc", 1, 15000, 25000, 20000, 
         "ThegioiIC", "Thế Giới IC", "https://thegioiic.com", "20/09/2026", "Còi active 5V kêu to rõ"),
         
        (16, "Phụ kiện", "Hộp bảo vệ chống sốc", "Hộp nhựa ABS IP65 100x68x50", "Nhựa ABS đúc có gioăng cao su chống nước bụi", 
         "Đóng gói hệ thống chắc chắn gắn lên sườn xe máy", "Khuyến nghị", 1, 35000, 55000, 45000, 
         "ThegioiIC", "Thế Giới IC", "https://thegioiic.com", "20/09/2026", "Bảo vệ mạch khi xe rung lắc dằn xóc"),
         
        (17, "Phụ kiện", "Bo hàn đa năng (Proto)", "Phíp đồng đục lỗ 7x9 cm", "Phíp thủy tinh FR4 hai mặt mạ thiếc", 
         "Hàn cố định các module trước ngày bảo vệ đồ án", "Khuyến nghị", 2, 10000, 15000, 12000, 
         "Nshopvn", "Nshop", "https://nshopvn.com", "20/09/2026", "Gắn chắc chắn hơn breadboard cắm dây")
    ]
    
    start_r = 6
    for idx, r_data in enumerate(bom_raw_data, start=start_r):
        row_num = idx
        bg = zebra_fill if idx % 2 == 1 else white_fill
        
        # Values
        ws2.cell(row=row_num, column=1, value=r_data[0]).alignment = Alignment(horizontal="center")
        ws2.cell(row=row_num, column=2, value=r_data[1]).font = bold_data_font
        ws2.cell(row=row_num, column=3, value=r_data[2]).font = bold_data_font
        ws2.cell(row=row_num, column=4, value=r_data[3]).font = data_font
        ws2.cell(row=row_num, column=5, value=r_data[4]).font = data_font
        ws2.cell(row=row_num, column=6, value=r_data[5]).font = data_font
        
        # Classification tag
        c_tag = ws2.cell(row=row_num, column=7, value=r_data[6])
        if r_data[6] == "Bắt buộc":
            c_tag.font = mand_font
            c_tag.fill = mand_fill
        else:
            c_tag.font = opt_font
            c_tag.fill = opt_fill
        c_tag.alignment = Alignment(horizontal="center")
        
        # Quantity
        ws2.cell(row=row_num, column=8, value=r_data[7]).alignment = Alignment(horizontal="center")
        
        # Prices
        c_min = ws2.cell(row=row_num, column=9, value=r_data[8])
        c_min.number_format = currency_fmt
        c_min.alignment = Alignment(horizontal="right")
        
        c_max = ws2.cell(row=row_num, column=10, value=r_data[9])
        c_max.number_format = currency_fmt
        c_max.alignment = Alignment(horizontal="right")
        
        c_sel = ws2.cell(row=row_num, column=11, value=r_data[10])
        c_sel.font = bold_data_font
        c_sel.number_format = currency_fmt
        c_sel.alignment = Alignment(horizontal="right")
        
        # Formula for Subtotal: =H{row} * K{row}
        c_sub = ws2.cell(row=row_num, column=12, value=f"=H{row_num}*K{row_num}")
        c_sub.font = bold_data_font
        c_sub.number_format = currency_fmt
        c_sub.alignment = Alignment(horizontal="right")
        
        ws2.cell(row=row_num, column=13, value=r_data[11])
        ws2.cell(row=row_num, column=14, value=r_data[12])
        
        # Hyperlink
        c_link = ws2.cell(row=row_num, column=15, value="Xem sản phẩm")
        c_link.hyperlink = r_data[13]
        c_link.font = link_font
        c_link.alignment = Alignment(horizontal="center")
        
        ws2.cell(row=row_num, column=16, value=r_data[14]).alignment = Alignment(horizontal="center")
        ws2.cell(row=row_num, column=17, value=r_data[15])
        
        for c in range(1, 18):
            if c != 7:  # keep tag color
                ws2.cell(row=row_num, column=c).fill = bg
            ws2.cell(row=row_num, column=c).border = border_all
            
    end_r = start_r + len(bom_raw_data) - 1
    
    # Subtotal Row
    tot_row = end_r + 1
    ws2.cell(row=tot_row, column=1, value="")
    ws2.cell(row=tot_row, column=2, value="TỔNG CỘNG PHẦN CỨNG").font = total_font
    for c in range(3, 8):
        ws2.cell(row=tot_row, column=c, value="")
    ws2.cell(row=tot_row, column=8, value=f"=SUM(H{start_r}:H{end_r})").alignment = Alignment(horizontal="center")
    ws2.cell(row=tot_row, column=8).font = total_font
    ws2.cell(row=tot_row, column=9, value=f"=SUM(I{start_r}:I{end_r})").number_format = currency_fmt
    ws2.cell(row=tot_row, column=10, value=f"=SUM(J{start_r}:J{end_r})").number_format = currency_fmt
    ws2.cell(row=tot_row, column=11, value="")
    
    c_tot_sum = ws2.cell(row=tot_row, column=12, value=f"=SUM(L{start_r}:L{end_r})")
    c_tot_sum.font = total_font
    c_tot_sum.number_format = currency_fmt
    c_tot_sum.alignment = Alignment(horizontal="right")
    
    for c in range(1, 18):
        ws2.cell(row=tot_row, column=c).fill = total_fill
        ws2.cell(row=tot_row, column=c).border = border_all
        
    # Contingency 10% Row
    ctg_row = tot_row + 1
    ws2.cell(row=ctg_row, column=2, value="DỰ PHÒNG RỦI RO (10%)").font = contingency_font
    ws2.cell(row=ctg_row, column=3, value="Hỏng hóc, đứt cáp, thay linh kiện, sai lệch giá").font = contingency_font
    c_ctg_val = ws2.cell(row=ctg_row, column=12, value=f"=L{tot_row}*0.1")
    c_ctg_val.font = contingency_font
    c_ctg_val.number_format = currency_fmt
    c_ctg_val.alignment = Alignment(horizontal="right")
    
    for c in range(1, 18):
        ws2.cell(row=ctg_row, column=c).fill = contingency_fill
        ws2.cell(row=ctg_row, column=c).border = border_all
        
    # Final Recommended Purchasing Budget Row
    fin_row = ctg_row + 1
    ws2.cell(row=fin_row, column=2, value="TỔNG DỰ TOÁN MUA SẮM KHUYẾN NGHỊ").font = highlight_total_font
    ws2.cell(row=fin_row, column=3, value="Đã bao gồm 10% chi phí dự phòng").font = highlight_total_font
    c_fin_val = ws2.cell(row=fin_row, column=12, value=f"=L{tot_row}+L{ctg_row}")
    c_fin_val.font = highlight_total_font
    c_fin_val.number_format = currency_fmt
    c_fin_val.alignment = Alignment(horizontal="right")
    
    for c in range(1, 18):
        ws2.cell(row=fin_row, column=c).fill = highlight_total_fill
        ws2.cell(row=fin_row, column=c).border = double_bottom
        
    # Set column widths for BOM_DA2
    col_widths_bom = {
        'A': 6, 'B': 16, 'C': 25, 'D': 25, 'E': 35, 'F': 32, 'G': 14, 
        'H': 10, 'I': 15, 'J': 15, 'K': 15, 'L': 16, 'M': 16, 'N': 16, 'O': 16, 'P': 14, 'Q': 35
    }
    for col_l, w in col_widths_bom.items():
        ws2.column_dimensions[col_l].width = w
        
    ws2.freeze_panes = "C6"
    ws2.auto_filter.ref = f"A5:Q{end_r}"

    # -------------------------------------------------------------
    # SHEET 3: SO_SANH_GIA
    # -------------------------------------------------------------
    ws3 = wb.create_sheet(title="SO_SANH_GIA")
    ws3.views.sheetView[0].showGridLines = True
    
    ws3.cell(row=2, column=2, value="ĐỐI SÁNH GIÁ CẢ TỪ CÁC ĐƠN VỊ CUNG CẤP TẠI VIỆT NAM").font = title_font
    ws3.cell(row=3, column=2, value="So sánh giá giữa Hshop, ThegioiIC, Nshop, Dientu360 và Shopee Mall").font = subtitle_font
    
    ss_cols = [
        "Linh kiện cốt lõi", "Model đề xuất", 
        "Nhà cung cấp 1", "Giá NCC 1", "Link NCC 1",
        "Nhà cung cấp 2", "Giá NCC 2", "Link NCC 2",
        "Nhà cung cấp 3", "Giá NCC 3", "Link NCC 3",
        "Nơi chọn mua", "Giá chọn mua", "Lý do lựa chọn đơn vị"
    ]
    
    for c_idx, h in enumerate(ss_cols, start=1):
        cell = ws3.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border_all
        
    ss_raw_data = [
        ("ESP32-S3 DevKit", "ESP32-S3-DevKitC-1 N16R8",
         "ThegioiIC", 185000, "https://thegioiic.com/esp32-s3-devkitc-1-n8",
         "Hshop.vn (MKE-K01)", 255000, "https://hshop.vn/products/mach-phat-trien-mke-k01-esp32-s3-dev-kit",
         "Nshop (S3 UNO)", 195000, "https://nshopvn.com",
         "ThegioiIC", 185000, "Bản chuẩn N16R8 có 8MB PSRAM giá hợp lý nhất, hàng sẵn TP.HCM"),
         
        ("Cảm biến IMU 6 trục", "MPU6050 (GY-521)",
         "Hshop.vn", 85000, "https://hshop.vn/products/mach-cam-bien-gia-toc-mpu-6050-gy-521",
         "ThegioiIC", 62000, "https://thegioiic.com",
         "Nshop", 67000, "https://nshopvn.com",
         "ThegioiIC / Hshop", 75000, "Linh kiện nguyên vỉ, IC chuẩn không bị lỗi thanh ghi I2C"),
         
        ("Module định vị GPS", "NEO-6M V2 kèm anten",
         "Dientu360", 155000, "https://dientu360.com/module-gps-neo-6m",
         "Nshop", 145000, "https://nshopvn.com",
         "ThegioiIC", 98040, "https://thegioiic.com",
         "Dientu360 / Nshop", 135000, "Còn sẵn hàng kèm anten gốm thụ động, bảo hành đổi trả"),
         
        ("Mạch đọc thẻ MicroSD", "MicroSD SPI Module",
         "ThegioiIC", 37620, "https://thegioiic.com",
         "Nshop (4AP3)", 12000, "https://nshopvn.com",
         "Hshop.vn", 25000, "https://hshop.vn",
         "Nshop / ThegioiIC", 20000, "Mạch ra chân SPI chuẩn có IC đệm chuyển mức 5V sang 3.3V"),
         
        ("Thẻ nhớ MicroSD", "SanDisk Ultra 32GB Class 10",
         "Shopee Mall (SanDisk)", 85000, "https://shopee.vn",
         "CellphoneS", 90000, "https://cellphones.com.vn",
         "Thegioididong", 95000, "https://thegioididong.com",
         "Shopee Mall SanDisk", 85000, "Chính hãng tem Dầu Khí / Synnex FPT, tốc độ ghi ổn định Class 10"),
         
        ("Đồng hồ RTC", "DS3231 I2C AT24C32",
         "ThegioiIC", 70670, "https://thegioiic.com",
         "Hshop.vn", 65000, "https://hshop.vn",
         "Nshop", 55000, "https://nshopvn.com",
         "Hshop / ThegioiIC", 60000, "Có sẵn pin cúc áo CR2032 và thạch anh bù nhiệt độ chính xác cao"),
         
        ("Mạch hạ áp DC-DC", "LM2596S Buck 3A",
         "Hshop.vn", 20000, "https://hshop.vn",
         "ThegioiIC", 18000, "https://thegioiic.com",
         "Nshop", 22000, "https://nshopvn.com",
         "Hshop.vn", 25000, "Mạch hạ áp kinh điển, chịu dòng xung tốt, linh kiện dán chuẩn"),
         
        ("Module 4G LTE", "SIM7680C 4G Cat-1 (MKE-M21)",
         "Hshop.vn (MKE-M21)", 245000, "https://hshop.vn/products/mach-mke-m21-sim7680c-4g-sms-call-module",
         "Shopee (Breakout)", 235000, "https://shopee.vn",
         "ThegioiIC (SIM7600)", 380000, "https://thegioiic.com",
         "Hshop.vn", 245000, "Module thiết kế chuẩn tương thích mẫu của Thầy, hỗ trợ kỹ thuật tốt")
    ]
    
    start_ss_r = 6
    for idx, r in enumerate(ss_raw_data, start=start_ss_r):
        row_num = idx
        bg = zebra_fill if idx % 2 == 1 else white_fill
        
        ws3.cell(row=row_num, column=1, value=r[0]).font = bold_data_font
        ws3.cell(row=row_num, column=2, value=r[1]).font = data_font
        
        # Seller 1
        ws3.cell(row=row_num, column=3, value=r[2])
        c1 = ws3.cell(row=row_num, column=4, value=r[3])
        c1.number_format = currency_fmt
        c1.alignment = Alignment(horizontal="right")
        clink1 = ws3.cell(row=row_num, column=5, value="Link")
        clink1.hyperlink = r[4]
        clink1.font = link_font
        clink1.alignment = Alignment(horizontal="center")
        
        # Seller 2
        ws3.cell(row=row_num, column=6, value=r[5])
        c2 = ws3.cell(row=row_num, column=7, value=r[6])
        c2.number_format = currency_fmt
        c2.alignment = Alignment(horizontal="right")
        clink2 = ws3.cell(row=row_num, column=8, value="Link")
        clink2.hyperlink = r[7]
        clink2.font = link_font
        clink2.alignment = Alignment(horizontal="center")
        
        # Seller 3
        ws3.cell(row=row_num, column=9, value=r[8])
        c3 = ws3.cell(row=row_num, column=10, value=r[9])
        c3.number_format = currency_fmt
        c3.alignment = Alignment(horizontal="right")
        clink3 = ws3.cell(row=row_num, column=11, value="Link")
        clink3.hyperlink = r[10]
        clink3.font = link_font
        clink3.alignment = Alignment(horizontal="center")
        
        # Selected
        ws3.cell(row=row_num, column=12, value=r[11]).font = bold_data_font
        c_sel = ws3.cell(row=row_num, column=13, value=r[12])
        c_sel.font = bold_data_font
        c_sel.number_format = currency_fmt
        c_sel.alignment = Alignment(horizontal="right")
        ws3.cell(row=row_num, column=14, value=r[13]).font = data_font
        
        for c in range(1, 15):
            ws3.cell(row=row_num, column=c).fill = bg
            ws3.cell(row=row_num, column=c).border = border_all
            
    end_ss_r = start_ss_r + len(ss_raw_data) - 1
    
    col_widths_ss = {
        'A': 20, 'B': 25, 'C': 16, 'D': 15, 'E': 8, 
        'F': 18, 'G': 15, 'H': 8, 'I': 18, 'J': 15, 'K': 8, 
        'L': 18, 'M': 16, 'N': 38
    }
    for col_l, w in col_widths_ss.items():
        ws3.column_dimensions[col_l].width = w
        
    ws3.freeze_panes = "C6"
    ws3.auto_filter.ref = f"A5:N{end_ss_r}"

    # -------------------------------------------------------------
    # SHEET 4: CAU_HINH_CHI_PHI
    # -------------------------------------------------------------
    ws4 = wb.create_sheet(title="CAU_HINH_CHI_PHI")
    ws4.views.sheetView[0].showGridLines = True
    
    ws4.cell(row=2, column=2, value="SO SÁNH 3 MỨC CẤU HÌNH PHẦN CỨNG CHI TIẾT").font = title_font
    ws4.cell(row=3, column=2, value="Bảng đối chiếu linh kiện xuất hiện trong từng phiên bản phát triển").font = subtitle_font
    
    ch_cols = [
        "STT", "Tên linh kiện / Module", "Model đề xuất", "Đơn giá ước tính", 
        "Cấu hình A: Tối thiểu (Lab)", "Cấu hình B: Khuyến nghị (ĐA2)", "Cấu hình C: Khóa luận (KLTN)", "Ghi chú vai trò"
    ]
    
    for c_idx, h in enumerate(ch_cols, start=1):
        cell = ws4.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border_all
        
    cfg_table_data = [
        (1, "Bo mạch vi điều khiển", "ESP32-S3 DevKit N16R8", 185000, "='BOM_DA2'!K6", "='BOM_DA2'!K6", "='BOM_DA2'!K6", "Bộ não trung tâm chạy TinyML"),
        (2, "Cảm biến quán tính IMU", "MPU6050 (GY-521)", 75000, "='BOM_DA2'!K7", "='BOM_DA2'!K7", 0, "Cảm biến đo rung lắc va đập ĐA2"),
        (3, "Cảm biến IMU cao cấp", "ICM-42688-P", 135000, 0, 0, 135000, "Nâng cấp chống rung động cơ KLTN"),
        (4, "Module định vị GPS", "NEO-6M kèm anten gốm", 135000, "='BOM_DA2'!K8", "='BOM_DA2'!K8", "='BOM_DA2'!K8", "Đo tốc độ và kinh vĩ độ tai nạn"),
        (5, "Mạch đọc thẻ MicroSD", "MicroSD SPI Module", 20000, "='BOM_DA2'!K9", "='BOM_DA2'!K9", "='BOM_DA2'!K9", "Giao tiếp thẻ nhớ SPI"),
        (6, "Thẻ nhớ MicroSD 32GB", "SanDisk Ultra Class 10", 85000, "='BOM_DA2'!K10", "='BOM_DA2'!K10", "='BOM_DA2'!K10", "Lưu file log 30 giây tai nạn"),
        (7, "Đồng hồ RTC DS3231", "DS3231 I2C kèm pin", 60000, 0, "='BOM_DA2'!K11", "='BOM_DA2'!K11", "Mốc giờ chuẩn khi mất GPS"),
        (8, "Mạch hạ áp LM2596", "LM2596S Buck 3A", 25000, 0, "='BOM_DA2'!K12", "='BOM_DA2'!K12", "Hạ áp 12V ắc-quy xe máy"),
        (9, "Pin Li-ion dự phòng", "Cell 18650 2000mAh", 50000, 0, "='BOM_DA2'!K13", "='BOM_DA2'!K13", "Nuôi nguồn khi ắc-quy đứt dây"),
        (10, "Mạch sạc pin TP4056", "TP4056 Type-C Protection", 12000, 0, "='BOM_DA2'!K14", "='BOM_DA2'!K14", "Sạc tự động cho pin 18650"),
        (11, "Module 4G LTE Viễn thông", "SIM7680C (MKE-M21)", 245000, 0, "='BOM_DA2'!K15", "='BOM_DA2'!K15", "Gửi tin nhắn SMS tọa độ khẩn cấp"),
        (12, "SIM 4G IoT duy trì", "Sim Viettel/Vina IoT", 50000, 0, "='BOM_DA2'!K16", "='BOM_DA2'!K16", "Duy trì kết nối mạng di động"),
        (13, "Breadboard thử nghiệm", "MB-102 830 lỗ", 35000, "='BOM_DA2'!K17", "='BOM_DA2'!K17", 0, "Cắm dây thử nghiệm bàn Lab"),
        (14, "Dây cắm Jumper (2 tép)", "Dây 20cm Đ-C và Đ-Đ", 36000, "='BOM_DA2'!L18", "='BOM_DA2'!L18", 18000, "Nối mạch tín hiệu"),
        (15, "Cáp nạp Type-C", "USB Type-C 1m", 30000, "='BOM_DA2'!K19", "='BOM_DA2'!K19", "='BOM_DA2'!K19", "Nạp code và cấp nguồn Lab"),
        (16, "Còi Buzzer + Nút bấm", "Buzzer 5V + Nút nhấn", 20000, "='BOM_DA2'!K20", "='BOM_DA2'!K20", "='BOM_DA2'!K20", "Khối cảnh báo và nút hủy"),
        (17, "Hộp nhựa bảo vệ ABS", "Hộp chống sốc IP65", 45000, 0, "='BOM_DA2'!K21", "='BOM_DA2'!K21", "Đóng hộp gắn cố định đuôi xe"),
        (18, "Bo mạch hàn đa năng", "Phíp đồng đục lỗ 7x9cm", 24000, 0, "='BOM_DA2'!L22", 0, "Hàn cố định linh kiện ĐA2"),
        (19, "Micro MEMS I2S", "INMP441 Digital Mic", 45000, 0, 0, 45000, "Thu âm va đập kim loại (KLTN)"),
        (20, "Module Camera hiện trường", "ESP32-CAM / OV2640", 110000, 0, 0, 110000, "Chụp ảnh hiện trường tai nạn (KLTN)"),
        (21, "Gia công mạch in PCB", "PCB 2 lớp JLCPCB (lô 5 cái)", 150000, 0, 0, 150000, "Mạch in chuyên nghiệp cho KLTN")
    ]
    
    start_cfg_r = 6
    for idx, r in enumerate(cfg_table_data, start=start_cfg_r):
        row_num = idx
        bg = zebra_fill if idx % 2 == 1 else white_fill
        
        ws4.cell(row=row_num, column=1, value=r[0]).alignment = Alignment(horizontal="center")
        ws4.cell(row=row_num, column=2, value=r[1]).font = bold_data_font
        ws4.cell(row=row_num, column=3, value=r[2]).font = data_font
        
        c_price = ws4.cell(row=row_num, column=4, value=r[3])
        c_price.number_format = currency_fmt
        c_price.alignment = Alignment(horizontal="right")
        
        # Config A
        cA = ws4.cell(row=row_num, column=5, value=r[4])
        cA.number_format = currency_fmt
        cA.alignment = Alignment(horizontal="right")
        
        # Config B
        cB = ws4.cell(row=row_num, column=6, value=r[5])
        cB.number_format = currency_fmt
        cB.alignment = Alignment(horizontal="right")
        
        # Config C
        cC = ws4.cell(row=row_num, column=7, value=r[6])
        cC.number_format = currency_fmt
        cC.alignment = Alignment(horizontal="right")
        
        ws4.cell(row=row_num, column=8, value=r[7]).font = data_font
        
        for c in range(1, 9):
            ws4.cell(row=row_num, column=c).fill = bg
            ws4.cell(row=row_num, column=c).border = border_all
            
    end_cfg_r = start_cfg_r + len(cfg_table_data) - 1
    
    # Total row for CAU_HINH_CHI_PHI
    tot_cfg_row = end_cfg_r + 1
    ws4.cell(row=tot_cfg_row, column=1, value="")
    ws4.cell(row=tot_cfg_row, column=2, value="TỔNG CHI PHÍ PHẦN CỨNG").font = total_font
    ws4.cell(row=tot_cfg_row, column=3, value="").font = total_font
    ws4.cell(row=tot_cfg_row, column=4, value="").font = total_font
    
    c_tot_A = ws4.cell(row=tot_cfg_row, column=5, value=f"=SUM(E{start_cfg_r}:E{end_cfg_r})")
    c_tot_A.font = total_font
    c_tot_A.number_format = currency_fmt
    c_tot_A.alignment = Alignment(horizontal="right")
    
    c_tot_B = ws4.cell(row=tot_cfg_row, column=6, value=f"=SUM(F{start_cfg_r}:F{end_cfg_r})")
    c_tot_B.font = highlight_total_font
    c_tot_B.fill = highlight_total_fill
    c_tot_B.number_format = currency_fmt
    c_tot_B.alignment = Alignment(horizontal="right")
    
    c_tot_C = ws4.cell(row=tot_cfg_row, column=7, value=f"=SUM(G{start_cfg_r}:G{end_cfg_r})")
    c_tot_C.font = total_font
    c_tot_C.number_format = currency_fmt
    c_tot_C.alignment = Alignment(horizontal="right")
    
    ws4.cell(row=tot_cfg_row, column=8, value="").font = total_font
    
    for c in range(1, 9):
        if c != 6:
            ws4.cell(row=tot_cfg_row, column=c).fill = total_fill
        ws4.cell(row=tot_cfg_row, column=c).border = double_bottom
        
    col_widths_cfg = {'A': 6, 'B': 24, 'C': 26, 'D': 16, 'E': 20, 'F': 20, 'G': 20, 'H': 32}
    for col_l, w in col_widths_cfg.items():
        ws4.column_dimensions[col_l].width = w
        
    ws4.freeze_panes = "D6"

    # -------------------------------------------------------------
    # SHEET 5: LINH_KIEN_TUY_CHON
    # -------------------------------------------------------------
    ws5 = wb.create_sheet(title="LINH_KIEN_TUY_CHON")
    ws5.views.sheetView[0].showGridLines = True
    
    ws5.cell(row=2, column=2, value="DANH MỤC LINH KIỆN MỞ RỘNG & TÙY CHỌN (OPTIONAL UPGRADES)").font = title_font
    ws5.cell(row=3, column=2, value="Các module nâng cấp cho Khóa luận Tốt nghiệp hoặc khi có thêm kinh phí").font = subtitle_font
    
    opt_cols = [
        "STT", "Tên linh kiện", "Model đề xuất", "Mục đích sử dụng", 
        "Đơn giá ước tính", "Mức độ ưu tiên", "Thời điểm nên mua", "Nơi bán đề xuất", "Link tham khảo"
    ]
    
    for c_idx, h in enumerate(opt_cols, start=1):
        cell = ws5.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_all
        
    opt_raw_data = [
        (1, "Micro MEMS I2S", "INMP441 Digital Microphone", "Thu âm tiếng đâm va kim loại, tiếng kính vỡ để đối chiếu kép với IMU", 
         45000, "MEDIUM", "Khóa luận Tốt nghiệp", "Hshop.vn", "https://hshop.vn"),
         
        (2, "Cảm biến IMU công nghiệp", "ICM-42688-P 6-axis", "Độ trôi nhiệt siêu thấp, chống rung cơ học xe máy chuyên dụng", 
         135000, "MEDIUM", "Khóa luận Tốt nghiệp", "ThegioiIC", "https://thegioiic.com"),
         
        (3, "Module Camera hiện trường", "ESP32-CAM / OV2640", "Chụp 1-3 bức ảnh hiện trường va chạm trước và sau cú đâm", 
         110000, "HIGH", "Khóa luận Tốt nghiệp", "Nshopvn", "https://nshopvn.com"),
         
        (4, "Màn hình OLED 0.96 inch", "OLED SSD1306 I2C 128x64", "Hiển thị tốc độ xe, số vệ tinh GPS và trạng thái hộp đen tại chỗ", 
         65000, "LOW", "Mua sau nếu thích", "Hshop.vn", "https://hshop.vn"),
         
        (5, "Gia công mạch in PCB", "PCB 2 lớp mạ thiếc JLCPCB", "Thiết kế bo mạch nguyên khối gắn linh kiện dán, đóng hộp chuyên nghiệp", 
         150000, "HIGH", "Khóa luận Tốt nghiệp", "JLCPCB / Kim Sơn", "https://jlcpcb.com"),
         
        (6, "Cổng giao tiếp chẩn đoán ECU", "Module MCP2515 CAN-bus", "Giao tiếp cổng OBD-II xe máy đọc tay ga, vòng tua máy RPM, phanh ABS", 
         45000, "LOW", "Khóa luận Tốt nghiệp", "ThegioiIC", "https://thegioiic.com"),
         
        (7, "Máy tính biên thị giác sâu", "Raspberry Pi Zero 2W", "Nếu muốn chạy mô hình YOLOv8 nhận diện biển số xe gây tai nạn", 
         480000, "LOW", "Khóa luận Tốt nghiệp", "Cybershop / Hshop", "https://hshop.vn")
    ]
    
    start_opt_r = 6
    for idx, r in enumerate(opt_raw_data, start=start_opt_r):
        row_num = idx
        bg = zebra_fill if idx % 2 == 1 else white_fill
        
        ws5.cell(row=row_num, column=1, value=r[0]).alignment = Alignment(horizontal="center")
        ws5.cell(row=row_num, column=2, value=r[1]).font = bold_data_font
        ws5.cell(row=row_num, column=3, value=r[2]).font = data_font
        ws5.cell(row=row_num, column=4, value=r[3]).font = data_font
        
        c_price = ws5.cell(row=row_num, column=5, value=r[4])
        c_price.number_format = currency_fmt
        c_price.alignment = Alignment(horizontal="right")
        
        # Priority
        c_prio = ws5.cell(row=row_num, column=6, value=r[5])
        if r[5] == "HIGH":
            c_prio.font = Font(name=font_family, size=10, bold=True, color="991B1B")
            c_prio.fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
        elif r[5] == "MEDIUM":
            c_prio.font = Font(name=font_family, size=10, bold=True, color="854D0E")
            c_prio.fill = PatternFill(start_color="FEF9C3", end_color="FEF9C3", fill_type="solid")
        else:
            c_prio.font = Font(name=font_family, size=10, color="475569")
            c_prio.fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
        c_prio.alignment = Alignment(horizontal="center")
        
        ws5.cell(row=row_num, column=7, value=r[6]).alignment = Alignment(horizontal="center")
        ws5.cell(row=row_num, column=8, value=r[7])
        
        clink = ws5.cell(row=row_num, column=9, value="Xem linh kiện")
        clink.hyperlink = r[8]
        clink.font = link_font
        clink.alignment = Alignment(horizontal="center")
        
        for c in range(1, 10):
            if c != 6:
                ws5.cell(row=row_num, column=c).fill = bg
            ws5.cell(row=row_num, column=c).border = border_all
            
    col_widths_opt = {'A': 6, 'B': 22, 'C': 25, 'D': 38, 'E': 16, 'F': 16, 'G': 20, 'H': 18, 'I': 16}
    for col_l, w in col_widths_opt.items():
        ws5.column_dimensions[col_l].width = w
        
    ws5.freeze_panes = "C6"

    # -------------------------------------------------------------
    # SHEET 6: NGUON_GIA
    # -------------------------------------------------------------
    ws6 = wb.create_sheet(title="NGUON_GIA")
    ws6.views.sheetView[0].showGridLines = True
    
    ws6.cell(row=2, column=2, value="NHẬT KÝ KIỂM CHỨNG NGUỒN GIÁ & LIÊN KẾT THẬT (PRICE LOG)").font = title_font
    ws6.cell(row=3, column=2, value="Toàn bộ báo giá được khảo sát từ các cửa hàng linh kiện có pháp nhân tại Việt Nam").font = subtitle_font
    
    log_cols = [
        "Mã nguồn (ID)", "Nền tảng / Đơn vị", "Tên cửa hàng", "Tên sản phẩm niêm yết", 
        "Model / Biến thể", "Giá niêm yết", "Đường dẫn URL xác thực", "Ngày kiểm tra", "Trạng thái", "Ghi chú kỹ thuật"
    ]
    
    for c_idx, h in enumerate(log_cols, start=1):
        cell = ws6.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_all
        
    source_log_data = [
        ("SRC-01", "Website B2C", "Hshop.vn", "Mạch MKE-K01 ESP32-S3 Dev Kit", "ESP32-S3 N16R8", 255000, 
         "https://hshop.vn/products/mach-phat-trien-mke-k01-esp32-s3-dev-kit", "20/09/2026", "VERIFIED", "Bản thiết kế tương thích chân ESP32-S3 DevKitC-1"),
         
        ("SRC-02", "Website B2B/B2C", "Thegioiic.com", "ESP32-S3-DevKitC-1-N8", "ESP32-S3-WROOM-1", 185000, 
         "https://thegioiic.com/esp32-s3-devkitc-1-n8", "20/09/2026", "VERIFIED", "Có sẵn hàng tại kho TP.HCM, giá chưa VAT"),
         
        ("SRC-03", "Website B2C", "Hshop.vn", "Mạch cảm biến gia tốc MPU-6050 (GY-521)", "GY-521 MPU6050", 85000, 
         "https://hshop.vn/products/mach-cam-bien-gia-toc-mpu-6050-gy-521", "20/09/2026", "VERIFIED", "Module nguyên seal kèm hàng rào chân thẳng/chân cong"),
         
        ("SRC-04", "Website B2C", "Dientu360.com", "Module GPS NEO-6M", "NEO-6M V2", 155000, 
         "https://dientu360.com/module-gps-neo-6m", "20/09/2026", "VERIFIED", "Kèm anten gốm 25x25mm và pin backup"),
         
        ("SRC-05", "Website B2B/B2C", "Thegioiic.com", "Mạch Đọc Thẻ Nhớ MicroSD, SD 2 Trong 1", "SPI MicroSD", 37620, 
         "https://thegioiic.com", "20/09/2026", "VERIFIED", "Hỗ trợ điện áp 3.3V và 5V ổn định"),
         
        ("SRC-06", "Sàn TMĐT", "Shopee Mall SanDisk", "Thẻ nhớ SanDisk Ultra microSDHC 32GB", "SanDisk 32GB A1", 85000, 
         "https://shopee.vn", "20/09/2026", "VERIFIED", "Chính hãng Synnex FPT / Dầu Khí, Class 10"),
         
        ("SRC-07", "Website B2B/B2C", "Thegioiic.com", "DS3231 Mạch Thời Gian Thực Có IC Nhớ", "DS3231 + AT24C32", 70670, 
         "https://thegioiic.com", "20/09/2026", "VERIFIED", "Có thạch anh bù nhiệt độ, kèm pin CR2032"),
         
        ("SRC-08", "Website B2C", "Hshop.vn", "Mạch giảm áp DC-DC Buck LM2596S 3A", "LM2596S", 20000, 
         "https://hshop.vn", "20/09/2026", "VERIFIED", "Chịu dòng đỉnh 3A, phù hợp hạ áp 12V xe máy"),
         
        ("SRC-09", "Website B2C", "Hshop.vn", "Mạch MKE-M21 SIM7680C 4G SMS/CALL Module", "SIM7680C 4G Cat-1", 245000, 
         "https://hshop.vn/products/mach-mke-m21-sim7680c-4g-sms-call-module", "20/09/2026", "VERIFIED", "Module chuẩn 4G, dùng lệnh AT command chuẩn UART"),
         
        ("SRC-10", "Website B2C", "Nshopvn.com", "Cell pin Li-ion 18650 2000mAh", "18650 3.7V", 50000, 
         "https://nshopvn.com", "20/09/2026", "VERIFIED", "Dòng xả 5C ổn định, nuôi nguồn dự phòng")
    ]
    
    start_log_r = 6
    for idx, r in enumerate(source_log_data, start=start_log_r):
        row_num = idx
        bg = zebra_fill if idx % 2 == 1 else white_fill
        
        ws6.cell(row=row_num, column=1, value=r[0]).alignment = Alignment(horizontal="center")
        ws6.cell(row=row_num, column=2, value=r[1])
        ws6.cell(row=row_num, column=3, value=r[2]).font = bold_data_font
        ws6.cell(row=row_num, column=4, value=r[3]).font = data_font
        ws6.cell(row=row_num, column=5, value=r[4]).font = data_font
        
        c_p = ws6.cell(row=row_num, column=6, value=r[5])
        c_p.number_format = currency_fmt
        c_p.alignment = Alignment(horizontal="right")
        
        clink = ws6.cell(row=row_num, column=7, value=r[6])
        clink.hyperlink = r[6]
        clink.font = link_font
        
        ws6.cell(row=row_num, column=8, value=r[7]).alignment = Alignment(horizontal="center")
        
        c_st = ws6.cell(row=row_num, column=9, value=r[8])
        c_st.font = Font(name=font_family, size=10, bold=True, color="166534")
        c_st.fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
        c_st.alignment = Alignment(horizontal="center")
        
        ws6.cell(row=row_num, column=10, value=r[9])
        
        for c in range(1, 11):
            if c != 9:
                ws6.cell(row=row_num, column=c).fill = bg
            ws6.cell(row=row_num, column=c).border = border_all
            
    col_widths_log = {'A': 10, 'B': 16, 'C': 20, 'D': 30, 'E': 20, 'F': 15, 'G': 35, 'H': 14, 'I': 14, 'J': 35}
    for col_l, w in col_widths_log.items():
        ws6.column_dimensions[col_l].width = w
        
    ws6.freeze_panes = "C6"

    # Save to disk
    out_name = "BAO_GIA_LINH_KIEN_AIOT_SMART_BLACK_BOX.xlsx"
    wb.save(out_name)
    print(f"File Excel created successfully: {out_name}")

if __name__ == "__main__":
    build_excel_report()
