# -*- coding: utf-8 -*-
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

def build_updated_excel_report():
    wb = openpyxl.Workbook()
    # Remove default sheet
    default_sheet = wb.active
    wb.remove(default_sheet)

    # Typography and Color Palette
    font_family = "Segoe UI"
    
    title_font = Font(name=font_family, size=15, bold=True, color="1B365D")
    subtitle_font = Font(name=font_family, size=11, italic=True, color="475569")
    h2_font = Font(name=font_family, size=12, bold=True, color="1B365D")
    
    header_font = Font(name=font_family, size=10.5, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    
    section_header_fill = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
    
    category_font = Font(name=font_family, size=11, bold=True, color="0F2C59")
    category_fill = PatternFill(start_color="E2E8F0", end_color="E2E8F0", fill_type="solid")
    
    total_font = Font(name=font_family, size=11, bold=True, color="0F172A")
    total_fill = PatternFill(start_color="CBD5E1", end_color="CBD5E1", fill_type="solid")
    
    highlight_total_font = Font(name=font_family, size=11, bold=True, color="991B1B")
    highlight_total_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
    
    contingency_font = Font(name=font_family, size=11, bold=True, color="92400E")
    contingency_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
    
    data_font = Font(name=font_family, size=10, color="1E293B")
    link_font = Font(name=font_family, size=10, color="0284C7", underline="single")
    bold_data_font = Font(name=font_family, size=10, bold=True, color="1E293B")
    
    # Priority & Status Styles
    stock_in_font = Font(name=font_family, size=9.5, bold=True, color="166534")
    stock_in_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
    
    stock_likely_font = Font(name=font_family, size=9.5, bold=True, color="854D0E")
    stock_likely_fill = PatternFill(start_color="FEF9C3", end_color="FEF9C3", fill_type="solid")
    
    stock_out_font = Font(name=font_family, size=9.5, bold=True, color="991B1B")
    stock_out_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
    
    prio_first_font = Font(name=font_family, size=9.5, bold=True, color="166534")
    prio_first_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
    
    prio_later_font = Font(name=font_family, size=9.5, bold=True, color="1E40AF")
    prio_later_fill = PatternFill(start_color="DBEAFE", end_color="DBEAFE", fill_type="solid")
    
    prio_opt_font = Font(name=font_family, size=9.5, bold=True, color="475569")
    prio_opt_fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    
    prio_thesis_font = Font(name=font_family, size=9.5, bold=True, color="6B21A8")
    prio_thesis_fill = PatternFill(start_color="F3E8FF", end_color="F3E8FF", fill_type="solid")

    mand_font = Font(name=font_family, size=9.5, bold=True, color="166534")
    mand_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
    
    opt_font = Font(name=font_family, size=9.5, bold=True, color="854D0E")
    opt_fill = PatternFill(start_color="FEF9C3", end_color="FEF9C3", fill_type="solid")
    
    zebra_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    
    thin_gray = Side(style='thin', color="D0D5DD")
    border_all = Border(left=thin_gray, right=thin_gray, top=thin_gray, bottom=thin_gray)
    double_bottom = Border(left=thin_gray, right=thin_gray, top=thin_gray, bottom=Side(style='double', color="1B365D"))
    
    currency_fmt = '#,##0 "₫"'
    date_fmt = 'DD/MM/YYYY'

    # =============================================================
    # SHEET 1: TONG_QUAN
    # =============================================================
    ws1 = wb.create_sheet(title="TONG_QUAN")
    ws1.views.sheetView[0].showGridLines = True
    
    ws1.cell(row=2, column=2, value="DỰ TOÁN CHI PHÍ & BẢNG BÓC TÁCH LINH KIỆN (BOM)").font = title_font
    ws1.cell(row=3, column=2, value="Đề tài: Hộp đen AIoT thông minh phân tích và tái hiện hiện trường tai nạn xe máy").font = subtitle_font
    ws1.cell(row=4, column=2, value="Ưu tiên nguồn cung cấp thực tế tại TP. HỒ CHÍ MINH (ThegioiIC, Hshop, Nshop, Shopee TP.HCM) | Khảo sát: 20/09/2026").font = subtitle_font
    
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
        
        c_pct = ws1.cell(row=idx, column=6, value=f"=E{idx}/$E$22")
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
        
    # Block 3: Linh kien nen mua truoc (Phase 1)
    ws1.cell(row=24, column=2, value="3. LINH KIỆN NÊN MUA TRƯỚC (BẮT BUỘC ĐỂ KHỞI ĐỘNG DỰ ÁN TẠI TP.HCM)").font = h2_font
    
    first_buy_headers = ["STT", "Linh kiện ưu tiên mua trước", "Model khuyến nghị", "Shop đề xuất (TP.HCM)", "Đơn giá", "Lý do bắt buộc phải mua trước"]
    for col_idx, h in enumerate(first_buy_headers, start=2):
        cell = ws1.cell(row=25, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_all
        
    first_buy_data = [
        (1, "Bo mạch vi điều khiển ESP32-S3", "ESP32-S3-DevKitC-1 N16R8", "ThegioiIC (Thủ Đức)", 185000, 
         "Bộ não trung tâm; cần mua đầu tiên để cài toolchain PlatformIO, kiểm tra 8MB PSRAM và dựng khung đa luồng FreeRTOS."),
        (2, "Cảm biến quán tính IMU 6 trục", "MPU6050 (GY-521)", "ThegioiIC / Hshop", 75000, 
         "Thu thập dữ liệu rung chấn, va chạm, lật góc để tạo tập dữ liệu huấn luyện mô hình TinyML trên Edge Impulse."),
        (3, "Mạch đọc thẻ MicroSD", "MicroSD SPI Module", "Nshop / ThegioiIC", 20000, 
         "Xây dựng hệ thống tệp FATFS trên giao tiếp SPI và kiểm thử chức năng lưu trữ file log nhị phân/CSV."),
        (4, "Thẻ nhớ MicroSD 32GB Class 10", "SanDisk Ultra 32GB A1", "Shopee Mall SanDisk TP.HCM", 85000, 
         "Cần có cùng mạch đọc để kiểm tra độ trễ ghi thực tế (write latency); thẻ kém chất lượng sẽ làm tràn circular buffer."),
        (5, "Module định vị GPS", "GY-NEO6MV2 kèm anten gốm", "ThegioiIC (Thủ Đức)", 135000, 
         "Lập trình ngắt UART nhận bản tin NMEA, bóc tách tọa độ kinh vĩ độ và tốc độ xe phục vụ định vị hiện trường."),
        (6, "Phụ kiện thử nghiệm cơ bản", "Breadboard, Dây cắm, Cáp Type-C", "Hshop (Q.11 / Thủ Đức)", 101000, 
         "Dụng cụ cắm mạch và nạp code/debug Serial Monitor; không thể bắt đầu lập trình nếu thiếu các phụ kiện này.")
    ]
    
    for idx, r in enumerate(first_buy_data, start=26):
        ws1.cell(row=idx, column=2, value=r[0]).alignment = Alignment(horizontal="center")
        ws1.cell(row=idx, column=3, value=r[1]).font = bold_data_font
        ws1.cell(row=idx, column=4, value=r[2]).font = data_font
        ws1.cell(row=idx, column=5, value=r[3]).font = bold_data_font
        
        c_pr = ws1.cell(row=idx, column=6, value=r[4])
        c_pr.font = bold_data_font
        c_pr.number_format = currency_fmt
        c_pr.alignment = Alignment(horizontal="right")
        
        c_rs = ws1.cell(row=idx, column=7, value=r[5])
        c_rs.font = data_font
        c_rs.alignment = Alignment(wrap_text=True)
        
        for c in range(2, 8):
            ws1.cell(row=idx, column=c).border = border_all
            
    tot_fb_row = 26 + len(first_buy_data)
    ws1.cell(row=tot_fb_row, column=2, value="").border = double_bottom
    ws1.cell(row=tot_fb_row, column=3, value="TỔNG CHI PHÍ ĐỢT 1 (KHỞI ĐỘNG LAB)").font = total_font
    ws1.cell(row=tot_fb_row, column=4, value="6 Hạng mục thiết yếu").font = total_font
    ws1.cell(row=tot_fb_row, column=5, value="").font = total_font
    c_tot_fb = ws1.cell(row=tot_fb_row, column=6, value=f"=SUM(F26:F{tot_fb_row-1})")
    c_tot_fb.font = total_font
    c_tot_fb.fill = total_fill
    c_tot_fb.number_format = currency_fmt
    c_tot_fb.alignment = Alignment(horizontal="right")
    ws1.cell(row=tot_fb_row, column=7, value="Chỉ cần ~601.000 ₫ là hoàn thành được 80% phần mềm & thuật toán AI của ĐA2").font = bold_data_font
    for c in range(2, 8):
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
    ws1.column_dimensions['C'].width = 34
    ws1.column_dimensions['D'].width = 28
    ws1.column_dimensions['E'].width = 24
    ws1.column_dimensions['F'].width = 18
    ws1.column_dimensions['G'].width = 46

    # =============================================================
    # SHEET 2: BOM_DA2 (Main purchasing list with TP.HCM locations)
    # =============================================================
    ws2 = wb.create_sheet(title="BOM_DA2")
    ws2.views.sheetView[0].showGridLines = True
    
    ws2.cell(row=2, column=2, value="BẢNG BÓC TÁCH LINH KIỆN MUA SẮM ĐỒ ÁN 2 (BOM - BILL OF MATERIALS)").font = title_font
    ws2.cell(row=3, column=2, value="Cấu hình khuyến nghị chính thức — Xác minh thực tế tại các cửa hàng TP. HỒ CHÍ MINH").font = subtitle_font
    
    bom_cols = [
        "STT", "Nhóm linh kiện", "Tên linh kiện", "Model đề xuất", "Thông số chính", 
        "Mục đích sử dụng", "Phân loại", "Số lượng", "Giá thấp nhất", "Giá cao nhất", 
        "Giá lựa chọn", "Thành tiền", "Cửa hàng đề xuất", "Địa chỉ tại TP.HCM", "Tình trạng", "Link sản phẩm", "Ngày kiểm tra", "Ghi chú kỹ thuật"
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
         "ThegioiIC", "939/1A Kha Vạn Cân, P. Linh Tây, TP. Thủ Đức", "IN STOCK", "https://thegioiic.com/esp32-s3-devkitc-1-n8", "20/09/2026", "Bắt buộc bản có 8MB PSRAM để chứa buffer 30s"),
          
        # Cảm biến
        (2, "Cảm biến", "Cảm biến quán tính IMU", "MPU6050 (GY-521)", "Gia tốc 3 trục ±16g, Con quay hồi chuyển ±2000°/s", 
         "Đo lực va đập, rung chấn và góc lật nghiêng xe", "Bắt buộc", 1, 62000, 85000, 75000, 
         "ThegioiIC / Hshop", "Kha Vạn Cân, Thủ Đức / Lý Thường Kiệt, Q.11", "IN STOCK", "https://thegioiic.com/gy-521-mpu-6050-cam-bien-con-quay-gia-toc", "20/09/2026", "Linh kiện nguyên vỉ, IC chuẩn không bị lỗi thanh ghi I2C"),
          
        # GPS
        (3, "GPS", "Module định vị GPS", "GY-NEO6MV2 / NEO-6M", "Bắt sóng GPS vệ tinh, ngõ ra UART 9600 bps kèm anten gốm", 
         "Ghi nhận tọa độ tai nạn và tốc độ di chuyển", "Bắt buộc", 1, 98040, 155000, 135000, 
         "ThegioiIC / Dientu360", "939/1A Kha Vạn Cân, P. Linh Tây, TP. Thủ Đức", "IN STOCK", "https://thegioiic.com", "20/09/2026", "Kèm sẵn anten gốm thụ động 25x25mm"),
          
        # Lưu trữ
        (4, "Lưu trữ", "Mạch đọc thẻ MicroSD", "MicroSD SPI Module", "Giao tiếp SPI 5V/3.3V, hỗ trợ thẻ nhớ dung lượng đến 32GB", 
         "Giao tiếp phần cứng giữa ESP32 và thẻ nhớ", "Bắt buộc", 1, 12000, 37620, 20000, 
         "Nshop / ThegioiIC", "1 Vườn Chuối, Q.3 / Kha Vạn Cân, Thủ Đức", "IN STOCK", "https://thegioiic.com", "20/09/2026", "Hỗ trợ điện áp 3.3V/5V có trở đệm chuyển mức"),
          
        (5, "Lưu trữ", "Thẻ nhớ MicroSD", "SanDisk Ultra 32GB Class 10", "Chuẩn A1/U1, tốc độ đọc 100MB/s, chống sốc/nhiệt", 
         "Lưu trữ vĩnh viễn file log CSV 30 giây tai nạn", "Bắt buộc", 1, 75000, 95000, 85000, 
         "Shopee Mall SanDisk", "Gian hàng chính hãng SanDisk VN (Kho TP.HCM)", "IN STOCK", "https://shopee.vn", "20/09/2026", "Bắt buộc Class 10 chính hãng tránh nghẽn ghi"),
          
        # Đồng hồ thời gian thực
        (6, "Thời gian thực", "Module RTC DS3231", "DS3231 I2C AT24C32", "Đồng hồ thạch anh bù nhiệt sai số <2ppm, kèm pin CR2032", 
         "Giữ mốc giờ chính xác khi xe mất GPS hoặc tắt máy", "Khuyến nghị", 1, 55000, 70670, 60000, 
         "Hshop / ThegioiIC", "269/20 Lý Thường Kiệt, Q.11 / Thủ Đức", "IN STOCK", "https://thegioiic.com", "20/09/2026", "Kèm pin nuôi độc lập duy trì giờ khi mất nguồn"),
          
        # Nguồn
        (7, "Nguồn điện", "Mạch hạ áp DC-DC", "LM2596S Buck 3A", "Điện áp vào 4-35V, ra 5V/3A ổn định hiệu suất cao", 
         "Hạ áp từ ắc-quy 12V xe máy nuôi toàn bộ mạch", "Bắt buộc", 1, 18000, 35000, 25000, 
         "Hshop / ThegioiIC", "269/20 Lý Thường Kiệt, Q.11 / Thủ Đức", "IN STOCK", "https://hshop.vn", "20/09/2026", "Tụ lọc Low-ESR chống sụt áp khi đề xe"),
          
        (8, "Nguồn điện", "Pin Li-ion dự phòng", "Cell pin 18650 2000mAh", "Pin sạc Li-ion 3.7V dung lượng 2000mAh", 
         "Nguồn nuôi khẩn cấp 30 giây khi ắc-quy xe bị đứt", "Khuyến nghị", 1, 45000, 65000, 50000, 
         "Nshop TP.HCM", "Số 7 Trần Hưng Đạo, P. Hiệp Phú, TP. Thủ Đức", "IN STOCK", "https://nshopvn.com", "20/09/2026", "Duy trì ghi file khi mất nguồn chính ắc-quy"),
          
        (9, "Nguồn điện", "Mạch sạc pin Li-ion", "TP4056 Type-C Protection", "Sạc pin Li-ion 1A tích hợp ngắt khi quá xả <2.5V", 
         "Tự động sạc pin dự phòng khi xe nổ máy", "Khuyến nghị", 1, 10000, 15000, 12000, 
         "Hshop / Nshop", "269/20 Lý Thường Kiệt, Q.11, TP.HCM", "IN STOCK", "https://hshop.vn", "20/09/2026", "Bản có 2 IC bảo vệ quá tải/quá xả pin"),
          
        # Giao tiếp IoT
        (10, "Giao tiếp IoT", "Module 4G LTE Cat-1", "MKE-M21 SIM7680C", "Giao tiếp UART AT command, hỗ trợ SMS, VoLTE, TCP/MQTT", 
         "Gửi tin nhắn SMS khẩn cấp chứa link Google Maps", "Khuyến nghị", 1, 220000, 260000, 245000, 
         "Hshop.vn TP.HCM", "269/20 Lý Thường Kiệt, Q.11 / Thủ Đức", "IN STOCK", "https://hshop.vn/products/mach-mke-m21-sim7680c-4g-sms-call-module", "20/09/2026", "Module 4G chuẩn, sóng 2G đã bị cắt hoàn toàn ở VN"),
          
        (11, "Giao tiếp IoT", "SIM 4G IoT Viettel/Vina", "Gói cước IoT Data/SMS", "Sim 4G duy trì 6 tháng gửi tin nhắn cảnh báo", 
         "Duy trì kết nối viễn thông di động ngoài đường", "Khuyến nghị", 1, 40000, 60000, 50000, 
         "Đại lý Viettel TP.HCM", "Viettel Store TP.HCM / Shopee TP.HCM", "IN STOCK", "https://vietteltelecom.vn", "20/09/2026", "Cần kích hoạt dịch vụ VoLTE/SMS gửi tin khẩn"),
          
        # Phụ kiện
        (12, "Phụ kiện", "Bo cắm thử nghiệm", "Breadboard MB-102", "Bo mạch cắm lỗ thử nghiệm 830 điểm cắm", 
         "Cắm nối linh kiện thử nghiệm trên bàn Lab", "Bắt buộc", 1, 30000, 45000, 35000, 
         "Hshop / Nshop", "269/20 Lý Thường Kiệt, Q.11, TP.HCM", "IN STOCK", "https://hshop.vn", "20/09/2026", "Dùng cho giai đoạn nghiên cứu Lab"),
          
        (13, "Phụ kiện", "Dây cắm Jumper", "Tép dây 20cm Đực-Cái, Đực-Đực", "Dây đồng bọc nhựa 40 sợi dài 20cm", 
         "Kết nối các chân tín hiệu giữa các module", "Bắt buộc", 2, 15000, 25000, 18000, 
         "Hshop / ThegioiIC", "Q.11 / TP. Thủ Đức, TP.HCM", "IN STOCK", "https://hshop.vn", "20/09/2026", "2 tép gồm 1 tép Đ-C và 1 tép Đ-Đ"),
          
        (14, "Phụ kiện", "Cáp nạp Type-C", "Cáp USB Type-C 1m", "Lõi đồng truyền dữ liệu tốc độ cao và cấp nguồn", 
         "Nạp code chương trình và debug với máy tính", "Bắt buộc", 1, 25000, 40000, 30000, 
         "Hshop / Phụ kiện số", "269/20 Lý Thường Kiệt, Q.11, TP.HCM", "IN STOCK", "https://hshop.vn", "20/09/2026", "Bắt buộc cáp có truyền data (4 sợi)"),
          
        (15, "Phụ kiện", "Khối cảnh báo tại chỗ", "Buzzer 5V + Nút nhấn 12mm", "Còi chíp báo động âm lượng 85dB + Nút nhấn hủy", 
         "Phát còi đếm ngược 15s và cho người lái bấm hủy", "Bắt buộc", 1, 15000, 25000, 20000, 
         "ThegioiIC / Hshop", "939/1A Kha Vạn Cân, P. Linh Tây, TP. Thủ Đức", "IN STOCK", "https://thegioiic.com", "20/09/2026", "Còi active 5V kêu to rõ, nút nhấn có đèn"),
          
        (16, "Phụ kiện", "Hộp bảo vệ chống sốc", "Hộp nhựa ABS IP65 100x68x50", "Nhựa ABS đúc có gioăng cao su chống nước bụi", 
         "Đóng gói hệ thống chắc chắn gắn lên sườn xe máy", "Khuyến nghị", 1, 35000, 55000, 45000, 
         "ThegioiIC TP.HCM", "939/1A Kha Vạn Cân, P. Linh Tây, TP. Thủ Đức", "IN STOCK", "https://thegioiic.com", "20/09/2026", "Bảo vệ mạch khi xe rung lắc dằn xóc"),
          
        (17, "Phụ kiện", "Bo hàn đa năng (Proto)", "Phíp đồng đục lỗ 7x9 cm", "Phíp thủy tinh FR4 hai mặt mạ thiếc", 
         "Hàn cố định các module trước ngày bảo vệ đồ án", "Khuyến nghị", 2, 10000, 15000, 12000, 
         "ThegioiIC / Nshop", "Kha Vạn Cân, Thủ Đức / Vườn Chuối, Q.3", "IN STOCK", "https://nshopvn.com", "20/09/2026", "Gắn chắc chắn hơn breadboard cắm dây")
    ]
    
    start_r = 6
    for idx, r_data in enumerate(bom_raw_data, start=start_r):
        row_num = idx
        bg = zebra_fill if idx % 2 == 1 else white_fill
        
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
        
        ws2.cell(row=row_num, column=13, value=r_data[11]).font = bold_data_font
        ws2.cell(row=row_num, column=14, value=r_data[12]).font = data_font
        
        # Status
        c_st = ws2.cell(row=row_num, column=15, value=r_data[13])
        c_st.font = stock_in_font
        c_st.fill = stock_in_fill
        c_st.alignment = Alignment(horizontal="center")
        
        # Hyperlink
        c_link = ws2.cell(row=row_num, column=16, value="Xem sản phẩm")
        c_link.hyperlink = r_data[14]
        c_link.font = link_font
        c_link.alignment = Alignment(horizontal="center")
        
        ws2.cell(row=row_num, column=17, value=r_data[15]).alignment = Alignment(horizontal="center")
        ws2.cell(row=row_num, column=18, value=r_data[16])
        
        for c in range(1, 19):
            if c not in (7, 15):
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
    
    for c in range(1, 19):
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
    
    for c in range(1, 19):
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
    
    for c in range(1, 19):
        ws2.cell(row=fin_row, column=c).fill = highlight_total_fill
        ws2.cell(row=fin_row, column=c).border = double_bottom
        
    # Column widths for BOM_DA2
    col_widths_bom = {
        'A': 6, 'B': 16, 'C': 25, 'D': 25, 'E': 35, 'F': 32, 'G': 14, 
        'H': 10, 'I': 14, 'J': 14, 'K': 15, 'L': 16, 'M': 18, 'N': 32, 'O': 14, 'P': 16, 'Q': 14, 'R': 35
    }
    for col_l, w in col_widths_bom.items():
        ws2.column_dimensions[col_l].width = w
        
    ws2.freeze_panes = "D6"
    ws2.auto_filter.ref = f"A5:R{end_r}"

    # =============================================================
    # SHEET 3: SO_SANH_GIA (Multi-seller comparison focusing on TP.HCM)
    # =============================================================
    ws3 = wb.create_sheet(title="SO_SANH_GIA")
    ws3.views.sheetView[0].showGridLines = True
    
    ws3.cell(row=2, column=2, value="ĐỐI CHIẾU GIÁ ĐA NHÀ CUNG CẤP TẠI TP. HỒ CHÍ MINH").font = title_font
    ws3.cell(row=3, column=2, value="Khảo sát độc lập giữa các cửa hàng điện tử có pháp nhân và kho hàng thực tế tại TP.HCM").font = subtitle_font
    
    ss_cols = [
        "STT", "Linh kiện cốt lõi", "Model đề xuất", "Cửa hàng khảo sát", "Địa chỉ / Quận (TP.HCM)", 
        "Nền tảng", "Tên sản phẩm niêm yết", "Đơn giá (VNĐ)", "Tình trạng", "Link sản phẩm", "Ngày kiểm tra", "Đánh giá & Lý do lựa chọn", "Đề xuất chọn"
    ]
    
    for c_idx, h in enumerate(ss_cols, start=1):
        cell = ws3.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border_all
        
    multi_seller_data = [
        # ESP32-S3
        (1, "ESP32-S3 DevKit", "ESP32-S3-DevKitC-1 N16R8", "ThegioiIC", "939/1A Kha Vạn Cân, P. Linh Tây, TP. Thủ Đức",
         "Web B2B/B2C", "ESP32-S3-DevKitC-1-N8 / N16R8", 185000, "IN STOCK", "https://thegioiic.com/esp32-s3-devkitc-1-n8", "20/09/2026",
         "Bản chuẩn N16R8 có 8MB PSRAM giá hợp lý nhất, hàng sẵn tại kho Thủ Đức, đổi trả 1-1", "CHỌN MUA"),
        (1, "ESP32-S3 DevKit", "ESP32-S3-DevKitC-1 N16R8", "Hshop.vn", "269/20 Lý Thường Kiệt, P.15, Q.11, TP.HCM",
         "Web B2C", "Mạch phát triển MKE-K01 ESP32-S3 Dev Kit", 255000, "IN STOCK", "https://hshop.vn/products/mach-phat-trien-mke-k01-esp32-s3-dev-kit", "20/09/2026",
         "Hàng chuẩn của MakerLab, có chân header cắm nhanh, tài liệu tiếng Việt chi tiết nhưng giá cao hơn 70k", "-"),
        (1, "ESP32-S3 DevKit", "ESP32-S3-DevKitC-1 N16R8", "Nshop", "1 Vườn Chuối, P.4, Q.3, TP.HCM",
         "Web B2C", "Mạch ESP32-S3 UNO Dual Type-C", 195000, "LIKELY IN STOCK", "https://nshopvn.com", "20/09/2026",
         "Form factor dạng Arduino UNO, thuận tiện cắm shield nhưng kích thước lớn khó nhét hộp đen", "-"),

        # MPU6050
        (2, "Cảm biến quán tính IMU", "MPU6050 (GY-521)", "ThegioiIC", "939/1A Kha Vạn Cân, P. Linh Tây, TP. Thủ Đức",
         "Web B2B/B2C", "GY-521 MPU-6050 Cảm Biến Con Quay Gia Tốc", 62000, "IN STOCK", "https://thegioiic.com/gy-521-mpu-6050-cam-bien-con-quay-gia-toc", "20/09/2026",
         "Linh kiện nguyên seal, IC chuẩn InvenSense, thanh ghi I2C 0x68 nhận diện mượt mà", "CHỌN MUA"),
        (2, "Cảm biến quán tính IMU", "MPU6050 (GY-521)", "Hshop.vn", "269/20 Lý Thường Kiệt, Q.11 / Đặng Văn Bi, Thủ Đức",
         "Web B2C", "Cảm biến gia tốc MPU6050 IMU 6DOF GY-521", 85000, "LIKELY IN STOCK", "https://hshop.vn", "20/09/2026",
         "Có kèm tài liệu mẫu kết nối Arduino/ESP32; nếu hết hàng có sẵn MPU6500 thay thế 55k", "DỰ PHÒNG"),
        (2, "Cảm biến quán tính IMU", "MPU6050 (GY-521)", "Nshop", "1 Vườn Chuối, Q.3 / 7 Trần Hưng Đạo, Thủ Đức",
         "Web B2C", "Cảm biến gia tốc GY-521 6DOF IMU MPU6050", 67000, "OUT OF STOCK", "https://nshopvn.com", "20/09/2026",
         "Hiện tại website Nshop đang báo Hết hàng (OUT OF STOCK), sinh viên cần lưu ý tránh đến mất công", "-"),
        (2, "Cảm biến quán tính IMU", "MPU6050 (GY-521)", "Shopee TP.HCM", "Cửa hàng Linh kiện SG (Giao hỏa tốc TP.HCM)",
         "Sàn TMĐT", "Module GY-521 MPU6050 6 trục kèm chân rào", 45000, "IN STOCK", "https://shopee.vn", "20/09/2026",
         "Giá rẻ nhất nhưng rủi ro gặp chip MPU clone giá rẻ dễ bị trôi nhiệt độ và lỗi bus I2C", "-"),

        # GPS NEO-6M
        (3, "Module định vị GPS", "GY-NEO6MV2 / NEO-6M", "ThegioiIC", "939/1A Kha Vạn Cân, P. Linh Tây, TP. Thủ Đức",
         "Web B2B/B2C", "GY-NEO6MV2 Module GPS Kèm Anten Gốm", 98040, "IN STOCK", "https://thegioiic.com", "20/09/2026",
         "Mức giá tốt nhất tại TP.HCM, có sẵn pin sạc backup RTC lưu almanac bắt vệ tinh nhanh", "CHỌN MUA"),
        (3, "Module định vị GPS", "GY-NEO6MV2 / NEO-6M", "Nshop", "Số 7 Trần Hưng Đạo, P. Hiệp Phú, TP. Thủ Đức",
         "Web B2C", "Module định vị GPS NEO-6M V2", 145000, "IN STOCK", "https://nshopvn.com", "20/09/2026",
         "Hàng sẵn tại chi nhánh Thủ Đức, được test trước khi giao", "DỰ PHÒNG"),
        (3, "Module định vị GPS", "GY-NEO6MV2 / NEO-6M", "Dientu360", "Điện Tử 360 (Giao nhanh TP.HCM 24h)",
         "Web B2C", "Module GPS NEO-6M Anten Rời", 155000, "IN STOCK", "https://dientu360.com/module-gps-neo-6m", "20/09/2026",
         "Kho Hà Nội ship TP.HCM mất 1-2 ngày, giá cao hơn", "-"),

        # MicroSD Module & Card
        (4, "Mạch đọc thẻ MicroSD", "MicroSD SPI Module", "Nshop", "1 Vườn Chuối, P.4, Q.3, TP.HCM",
         "Web B2C", "Module đọc thẻ nhớ Micro SD SPI 4AP3", 12000, "IN STOCK", "https://nshopvn.com", "20/09/2026",
         "Giá rẻ nhất, có IC đệm chuyển mức 5V sang 3.3V, cắm trực tiếp chân SPI của ESP32-S3", "CHỌN MUA"),
        (4, "Mạch đọc thẻ MicroSD", "MicroSD SPI Module", "ThegioiIC", "939/1A Kha Vạn Cân, P. Linh Tây, TP. Thủ Đức",
         "Web B2B/B2C", "Mạch Đọc Thẻ Nhớ MicroSD, SD 2 Trong 1", 37620, "IN STOCK", "https://thegioiic.com", "20/09/2026",
         "Chất lượng mạch in mạ thiếc dầy dặn, tụ lọc chống nhiễu tốt", "DỰ PHÒNG"),
        (4, "Thẻ nhớ MicroSD 32GB", "SanDisk Ultra 32GB Class 10", "Shopee Mall SanDisk", "Gian hàng chính hãng SanDisk VN (Kho Tân Phú, TP.HCM)",
         "Sàn TMĐT", "Thẻ nhớ SanDisk Ultra microSDHC 32GB A1 100MB/s", 85000, "IN STOCK", "https://shopee.vn", "20/09/2026",
         "Chính hãng Synnex FPT / Dầu Khí, tốc độ ghi thực tế >15MB/s, chống treo bộ đệm circular buffer", "CHỌN MUA"),
        (4, "Thẻ nhớ MicroSD 32GB", "SanDisk Ultra 32GB Class 10", "CellphoneS TP.HCM", "Hệ thống CellphoneS toàn TP.HCM",
         "Bán lẻ IT", "Thẻ nhớ SanDisk MicroSD Ultra 32GB", 90000, "IN STOCK", "https://cellphones.com.vn", "20/09/2026",
         "Đến lấy ngay tại shop gần trường, bảo hành 5 năm", "DỰ PHÒNG"),

        # RTC DS3231
        (5, "Đồng hồ thời gian thực", "DS3231 I2C AT24C32", "ThegioiIC", "939/1A Kha Vạn Cân, P. Linh Tây, TP. Thủ Đức",
         "Web B2B/B2C", "DS3231 Mạch Thời Gian Thực Kèm Pin Cúc Áo", 70670, "IN STOCK", "https://thegioiic.com", "20/09/2026",
         "Thạch anh tích hợp bù nhiệt sai số dưới 1 phút/năm, có sẵn pin nuôi CR2032 và EEPROM AT24C32", "CHỌN MUA"),
        (5, "Đồng hồ thời gian thực", "DS3231 I2C AT24C32", "Hshop.vn", "269/20 Lý Thường Kiệt, P.15, Q.11, TP.HCM",
         "Web B2C", "Mạch thời gian thực RTC DS3231", 65000, "IN STOCK", "https://hshop.vn", "20/09/2026",
         "Giá tốt, sẵn hàng tại chi nhánh Q.11", "DỰ PHÒNG"),
        (5, "Đồng hồ thời gian thực", "DS3231 I2C AT24C32", "Nshop", "1 Vườn Chuối, P.4, Q.3, TP.HCM",
         "Web B2C", "Module RTC DS3231 độ chính xác cao", 55000, "IN STOCK", "https://nshopvn.com", "20/09/2026",
         "Giá rẻ nhưng chưa kèm pin cúc áo, cần mua thêm pin 10k", "-"),

        # LM2596
        (6, "Mạch hạ áp DC-DC", "LM2596S Buck 3A", "ThegioiIC", "939/1A Kha Vạn Cân, P. Linh Tây, TP. Thủ Đức",
         "Web B2B/B2C", "Mạch Giảm Áp DC-DC LM2596S 3A", 18000, "IN STOCK", "https://thegioiic.com", "20/09/2026",
         "Linh kiện dán chuẩn, chịu áp vào đến 35V, hạ xuống 5V cực kỳ ổn định nuôi ESP32 và module 4G", "CHỌN MUA"),
        (6, "Mạch hạ áp DC-DC", "LM2596S Buck 3A", "Hshop.vn", "269/20 Lý Thường Kiệt, P.15, Q.11, TP.HCM",
         "Web B2C", "Mạch giảm áp DC-DC Buck LM2596S 3A", 20000, "IN STOCK", "https://hshop.vn", "20/09/2026",
         "Hàng sẵn tại Q.11 và Thủ Đức", "DỰ PHÒNG"),

        # SIM7680C 4G
        (7, "Module 4G LTE Cat-1", "SIM7680C 4G (MKE-M21)", "Hshop.vn", "269/20 Lý Thường Kiệt, Q.11 / Thủ Đức",
         "Web B2C", "Mạch MKE-M21 SIM7680C 4G SMS/CALL Module", 245000, "IN STOCK", "https://hshop.vn/products/mach-mke-m21-sim7680c-4g-sms-call-module", "20/09/2026",
         "Khuyên dùng tuyệt đối: Tương thích 100% với mẫu thực nghiệm của Thầy, hỗ trợ tập lệnh AT command, có anten FPC dán", "CHỌN MUA"),
        (7, "Module 4G LTE Cat-1", "SIM7680C 4G (Breakout)", "Shopee TP.HCM", "Shop Linh kiện Sài Gòn (Giao hỏa tốc TP.HCM)",
         "Sàn TMĐT", "Module SIM7680C Core Board 4G Cat-1", 235000, "IN STOCK", "https://shopee.vn", "20/09/2026",
         "Bản trần breakout, không có mạch đệm nguồn và trở bảo vệ như bản MKE-M21 của Hshop", "-"),
        (7, "Module 4G LTE Cat-1", "SIM7600C 4G Module", "ThegioiIC", "939/1A Kha Vạn Cân, P. Linh Tây, TP. Thủ Đức",
         "Web B2B/B2C", "SIM7600C-H 4G LTE Module Công Nghiệp", 380000, "IN STOCK", "https://thegioiic.com", "20/09/2026",
         "Dòng công nghiệp tốc độ cao hơn nhưng giá đắt hơn 135k, quá thừa so với nhu cầu gửi SMS và tọa độ của ĐA2", "-"),

        # Pin Li-ion 18650 & TP4056
        (8, "Nguồn pin dự phòng", "Cell 18650 + Sạc TP4056", "Nshop", "Số 7 Trần Hưng Đạo, P. Hiệp Phú, TP. Thủ Đức",
         "Web B2C", "Combo Pin 18650 2000mAh (50k) + Mạch TP4056 Type-C (12k)", 62000, "IN STOCK", "https://nshopvn.com", "20/09/2026",
         "Cell pin dòng xả ổn định, mạch sạc Type-C có IC bảo vệ quá dòng/quá xả pin", "CHỌN MUA"),
        (8, "Nguồn pin dự phòng", "Cell 18650 + Sạc TP4056", "Hshop.vn", "269/20 Lý Thường Kiệt, P.15, Q.11, TP.HCM",
         "Web B2C", "Mạch sạc pin Li-ion TP4056 Type-C có bảo vệ", 12000, "IN STOCK", "https://hshop.vn", "20/09/2026",
         "Mạch sạc chuẩn, tiện gom chung đơn hàng tại Hshop", "DỰ PHÒNG"),

        # Hộp ABS & Bo Proto
        (9, "Đóng gói & Hàn mạch", "Hộp ABS IP65 + Bo Proto", "ThegioiIC", "939/1A Kha Vạn Cân, P. Linh Tây, TP. Thủ Đức",
         "Web B2B/B2C", "Hộp Nhựa Kín Nước IP65 (45k) + Phíp Đồng FR4 7x9cm (12k)", 57000, "IN STOCK", "https://thegioiic.com", "20/09/2026",
         "Hộp có gioăng cao su chống nước gắn đuôi xe máy; bo hàn đồng 2 mặt FR4 chắc chắn", "CHỌN MUA")
    ]
    
    start_ss_r = 6
    for idx, r in enumerate(multi_seller_data, start=start_ss_r):
        row_num = idx
        bg = zebra_fill if idx % 2 == 1 else white_fill
        
        ws3.cell(row=row_num, column=1, value=r[0]).alignment = Alignment(horizontal="center")
        ws3.cell(row=row_num, column=2, value=r[1]).font = bold_data_font
        ws3.cell(row=row_num, column=3, value=r[2]).font = data_font
        ws3.cell(row=row_num, column=4, value=r[3]).font = bold_data_font
        ws3.cell(row=row_num, column=5, value=r[4]).font = data_font
        ws3.cell(row=row_num, column=6, value=r[5]).alignment = Alignment(horizontal="center")
        ws3.cell(row=row_num, column=7, value=r[6]).font = data_font
        
        c_pr = ws3.cell(row=row_num, column=8, value=r[7])
        c_pr.font = bold_data_font
        c_pr.number_format = currency_fmt
        c_pr.alignment = Alignment(horizontal="right")
        
        # Availability status
        c_st = ws3.cell(row=row_num, column=9, value=r[8])
        if r[8] == "IN STOCK":
            c_st.font = stock_in_font
            c_st.fill = stock_in_fill
        elif r[8] == "LIKELY IN STOCK":
            c_st.font = stock_likely_font
            c_st.fill = stock_likely_fill
        else:
            c_st.font = stock_out_font
            c_st.fill = stock_out_fill
        c_st.alignment = Alignment(horizontal="center")
        
        clink = ws3.cell(row=row_num, column=10, value="Xem tại shop")
        clink.hyperlink = r[9]
        clink.font = link_font
        clink.alignment = Alignment(horizontal="center")
        
        ws3.cell(row=row_num, column=11, value=r[10]).alignment = Alignment(horizontal="center")
        ws3.cell(row=row_num, column=12, value=r[11]).font = data_font
        
        c_rec = ws3.cell(row=row_num, column=13, value=r[12])
        if r[12] == "CHỌN MUA":
            c_rec.font = Font(name=font_family, size=9.5, bold=True, color="166534")
            c_rec.fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
        elif r[12] == "DỰ PHÒNG":
            c_rec.font = Font(name=font_family, size=9.5, bold=True, color="854D0E")
            c_rec.fill = PatternFill(start_color="FEF9C3", end_color="FEF9C3", fill_type="solid")
        else:
            c_rec.font = data_font
        c_rec.alignment = Alignment(horizontal="center")
        
        for c in range(1, 14):
            if c not in (9, 13):
                ws3.cell(row=row_num, column=c).fill = bg
            ws3.cell(row=row_num, column=c).border = border_all
            
    end_ss_r = start_ss_r + len(multi_seller_data) - 1
    
    col_widths_ss = {
        'A': 6, 'B': 22, 'C': 25, 'D': 18, 'E': 34, 'F': 14, 
        'G': 32, 'H': 15, 'I': 14, 'J': 14, 'K': 14, 'L': 42, 'M': 16
    }
    for col_l, w in col_widths_ss.items():
        ws3.column_dimensions[col_l].width = w
        
    ws3.freeze_panes = "D6"
    ws3.auto_filter.ref = f"A5:M{end_ss_r}"

    # =============================================================
    # SHEET 4: MUA_O_TPHCM (NEW SHEET - Practical TP.HCM Purchasing Checklist)
    # =============================================================
    ws_hcm = wb.create_sheet(title="MUA_O_TPHCM")
    ws_hcm.views.sheetView[0].showGridLines = True
    
    ws_hcm.cell(row=2, column=2, value="DANH MỤC MUA SẮM LINH KIỆN TẠI TP. HỒ CHÍ MINH (PURCHASING CHECKLIST)").font = title_font
    
    # Top KPI Budget Cards
    ws_hcm.cell(row=3, column=2, value="TỔNG CHI PHÍ LINH KIỆN MUA TRƯỚC (ĐỢT 1):").font = Font(name=font_family, size=11, bold=True, color="166534")
    c_kpi_first = ws_hcm.cell(row=3, column=5, value='=SUMIF(K7:K26, "MUA TRƯỚC", H7:H26)')
    c_kpi_first.font = Font(name=font_family, size=12, bold=True, color="166534")
    c_kpi_first.fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
    c_kpi_first.number_format = currency_fmt
    c_kpi_first.alignment = Alignment(horizontal="right")
    
    ws_hcm.cell(row=3, column=7, value="TỔNG CHI PHÍ TOÀN BỘ CẤU HÌNH ĐA2:").font = Font(name=font_family, size=11, bold=True, color="1B365D")
    c_kpi_full = ws_hcm.cell(row=3, column=9, value='=SUMIF(K7:K26, "MUA TRƯỚC", H7:H26) + SUMIF(K7:K26, "MUA SAU", H7:H26)')
    c_kpi_full.font = Font(name=font_family, size=12, bold=True, color="1B365D")
    c_kpi_full.fill = PatternFill(start_color="DBEAFE", end_color="DBEAFE", fill_type="solid")
    c_kpi_full.number_format = currency_fmt
    c_kpi_full.alignment = Alignment(horizontal="right")
    
    ws_hcm.cell(row=4, column=2, value="Bảng phân loại mức độ ưu tiên theo tiến độ: MUA TRƯỚC (Tuần 1-3) | MUA SAU (Tuần 4-8) | ĐATN (Khóa luận)").font = subtitle_font
    
    hcm_cols = [
        "STT", "Tên linh kiện", "Model đề xuất", "Số lượng", "Shop đề xuất tại TP.HCM", 
        "Quận / Khu vực (TP.HCM)", "Đơn giá (VNĐ)", "Thành tiền (VNĐ)", "Tình trạng", "Link mua hàng", "Mức ưu tiên", "Ghi chú mua sắm"
    ]
    
    for c_idx, h in enumerate(hcm_cols, start=1):
        cell = ws_hcm.cell(row=6, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border_all
        
    hcm_purchasing_data = [
        # GIAI ĐOẠN 1: MUA TRƯỚC (6 món thiết yếu khởi động Lab)
        (1, "Bo mạch ESP32-S3 DevKit", "ESP32-S3-DevKitC-1 N16R8", 1, "ThegioiIC", "939/1A Kha Vạn Cân, P. Linh Tây, TP. Thủ Đức", 
         "='BOM_DA2'!K6", "IN STOCK", "https://thegioiic.com/esp32-s3-devkitc-1-n8", "MUA TRƯỚC", "Bộ não chạy TinyML; ghé trực tiếp shop lấy ngay trong ngày"),
        (2, "Cảm biến gia tốc IMU 6 trục", "MPU6050 (GY-521)", 1, "ThegioiIC / Hshop", "Kha Vạn Cân, Thủ Đức / Lý Thường Kiệt, Q.11", 
         "='BOM_DA2'!K7", "IN STOCK", "https://thegioiic.com/gy-521-mpu-6050-cam-bien-con-quay-gia-toc", "MUA TRƯỚC", "Thu thập dataset va đập; ThegioiIC còn sẵn hàng, Hshop có MPU6500 thay thế"),
        (3, "Mạch đọc thẻ nhớ MicroSD", "MicroSD SPI Module", 1, "Nshop / ThegioiIC", "1 Vườn Chuối, Q.3 / Kha Vạn Cân, Thủ Đức", 
         "='BOM_DA2'!K9", "IN STOCK", "https://thegioiic.com", "MUA TRƯỚC", "Xây dựng driver lưu file CSV/nhị phân trên thẻ nhớ"),
        (4, "Thẻ nhớ MicroSD 32GB", "SanDisk Ultra 32GB Class 10", 1, "Shopee Mall SanDisk", "Gian hàng chính hãng (Kho Tân Phú, TP.HCM)", 
         "='BOM_DA2'!K10", "IN STOCK", "https://shopee.vn", "MUA TRƯỚC", "Bắt buộc Class 10 chính hãng tránh nghẽn ghi, ship hỏa tốc TP.HCM 2h"),
        (5, "Module định vị GPS", "GY-NEO6MV2 kèm anten", 1, "ThegioiIC", "939/1A Kha Vạn Cân, P. Linh Tây, TP. Thủ Đức", 
         "='BOM_DA2'!K8", "IN STOCK", "https://thegioiic.com", "MUA TRƯỚC", "Bóc tách tọa độ kinh vĩ độ và tốc độ xe phục vụ định vị hiện trường"),
        (6, "Phụ kiện thực hành Lab", "Breadboard + Dây cắm + Cáp Type-C", 1, "Hshop.vn", "269/20 Lý Thường Kiệt, P.15, Q.11, TP.HCM", 
         "='BOM_DA2'!K17+'BOM_DA2'!L18+'BOM_DA2'!K19", "IN STOCK", "https://hshop.vn", "MUA TRƯỚC", "Cắm nối mạch thử nghiệm và nạp code debug Serial Monitor"),
         
        # GIAI ĐOẠN 2: MUA SAU (Hoàn thiện đồ án nộp hội đồng)
        (7, "Đồng hồ thời gian thực RTC", "DS3231 I2C AT24C32", 1, "ThegioiIC / Hshop", "Kha Vạn Cân, Thủ Đức / Lý Thường Kiệt, Q.11", 
         "='BOM_DA2'!K11", "IN STOCK", "https://thegioiic.com", "MUA SAU", "Đã kèm pin CR2032; giữ mốc giờ chuẩn khi xe tắt máy hoặc mất GPS"),
        (8, "Mạch hạ áp nguồn xe máy", "LM2596S Buck 3A", 1, "ThegioiIC / Hshop", "Kha Vạn Cân, Thủ Đức / Lý Thường Kiệt, Q.11", 
         "='BOM_DA2'!K12", "IN STOCK", "https://thegioiic.com", "MUA SAU", "Hạ áp 12V ắc-quy xe máy xuống 5V ổn định khi lắp thử nghiệm thật"),
        (9, "Pin Li-ion dự phòng", "Cell pin 18650 2000mAh", 1, "Nshop TP.HCM", "Số 7 Trần Hưng Đạo, P. Hiệp Phú, TP. Thủ Đức", 
         "='BOM_DA2'!K13", "IN STOCK", "https://nshopvn.com", "MUA SAU", "Nuôi nguồn cứu hộ 30s khi dây ắc-quy bị đứt do va đập mạnh"),
        (10, "Mạch sạc pin Li-ion Type-C", "TP4056 Type-C Protection", 1, "Hshop / Nshop", "269/20 Lý Thường Kiệt, Q.11, TP.HCM", 
         "='BOM_DA2'!K14", "IN STOCK", "https://hshop.vn", "MUA SAU", "Tự động sạc pin dự phòng khi xe máy nổ máy"),
        (11, "Module viễn thông 4G LTE", "SIM7680C 4G (MKE-M21)", 1, "Hshop.vn", "269/20 Lý Thường Kiệt, Q.11 / Thủ Đức", 
         "='BOM_DA2'!K15", "IN STOCK", "https://hshop.vn/products/mach-mke-m21-sim7680c-4g-sms-call-module", "MUA SAU", "Gửi SMS khẩn cấp tọa độ tai nạn; tương thích chuẩn mẫu của Thầy"),
        (12, "SIM 4G IoT Viettel/Vina", "Gói cước IoT Data/SMS", 1, "Đại lý Viettel TP.HCM", "Viettel Store TP.HCM / Shopee TP.HCM", 
         "='BOM_DA2'!K16", "IN STOCK", "https://vietteltelecom.vn", "MUA SAU", "Mua cùng module 4G ở Tuần 6 để tránh trôi hạn cước thuê bao di động"),
        (13, "Còi Buzzer + Nút bấm hủy", "Buzzer 5V + Nút nhấn 12mm", 1, "ThegioiIC", "939/1A Kha Vạn Cân, P. Linh Tây, TP. Thủ Đức", 
         "='BOM_DA2'!K20", "IN STOCK", "https://thegioiic.com", "MUA SAU", "Cảnh báo còi 85dB đếm ngược 15s cho tài xế bấm hủy khi ngã nhẹ"),
        (14, "Hộp bảo vệ chống sốc IP65", "Hộp nhựa ABS 100x68x50", 1, "ThegioiIC", "939/1A Kha Vạn Cân, P. Linh Tây, TP. Thủ Đức", 
         "='BOM_DA2'!K21", "IN STOCK", "https://thegioiic.com", "MUA SAU", "Mua khi chốt kích thước mạch để khoét lỗ gắn cố định lên xe máy"),
        (15, "Bo mạch hàn đa năng Proto", "Phíp đồng đục lỗ 7x9cm", 2, "ThegioiIC / Nshop", "Kha Vạn Cân, Thủ Đức / Vườn Chuối, Q.3", 
         "='BOM_DA2'!K22", "IN STOCK", "https://nshopvn.com", "MUA SAU", "Hàn cố định các module chống rung tuột dây trước ngày chấm đồ án"),
         
        # GIAI ĐOẠN 3: NÂNG CẤP KHÓA LUẬN TỐT NGHIỆP (ĐATN / TÙY CHỌN)
        (16, "Micro MEMS I2S", "INMP441 Digital Mic", 1, "Hshop.vn", "269/20 Lý Thường Kiệt, Q.11 / Thủ Đức", 
         45000, "IN STOCK", "https://hshop.vn", "ĐATN", "Thu âm thanh va chạm kim loại đanh sắc đối chiếu AI với IMU"),
        (17, "Cảm biến IMU công nghiệp", "ICM-42688-P 6-axis", 1, "ThegioiIC", "939/1A Kha Vạn Cân, P. Linh Tây, TP. Thủ Đức", 
         135000, "IN STOCK", "https://thegioiic.com", "ĐATN", "Độ trôi nhiệt siêu thấp, chống rung động cơ xe máy chuyên dụng"),
        (18, "Module Camera hiện trường", "ESP32-CAM / OV2640", 1, "Nshop TP.HCM", "Số 7 Trần Hưng Đạo, P. Hiệp Phú, TP. Thủ Đức", 
         110000, "IN STOCK", "https://nshopvn.com", "ĐATN", "Chụp 1-3 bức ảnh hiện trường va chạm gửi về máy chủ máy học"),
        (19, "Màn hình OLED tại chỗ", "OLED SSD1306 I2C 128x64", 1, "Hshop.vn", "269/20 Lý Thường Kiệt, P.15, Q.11, TP.HCM", 
         65000, "IN STOCK", "https://hshop.vn", "TÙY CHỌN", "Hiển thị tốc độ xe, số vệ tinh GPS và trạng thái thẻ nhớ tại chỗ"),
        (20, "Gia công mạch in PCB công nghiệp", "PCB 2 lớp mạ thiếc JLCPCB", 1, "JLCPCB (Ship TP.HCM)", "Đặt online giao tận nhà TP.HCM", 
         150000, "IN STOCK", "https://jlcpcb.com", "ĐATN", "Thiết kế bo mạch nguyên khối SMD sau khi bảo vệ xong Đồ án 2")
    ]
    
    start_hcm_r = 7
    for idx, r in enumerate(hcm_purchasing_data, start=start_hcm_r):
        row_num = idx
        bg = zebra_fill if idx % 2 == 1 else white_fill
        
        ws_hcm.cell(row=row_num, column=1, value=r[0]).alignment = Alignment(horizontal="center")
        ws_hcm.cell(row=row_num, column=2, value=r[1]).font = bold_data_font
        ws_hcm.cell(row=row_num, column=3, value=r[2]).font = data_font
        ws_hcm.cell(row=row_num, column=4, value=r[3]).alignment = Alignment(horizontal="center")
        ws_hcm.cell(row=row_num, column=5, value=r[4]).font = bold_data_font
        ws_hcm.cell(row=row_num, column=6, value=r[5]).font = data_font
        
        c_pr = ws_hcm.cell(row=row_num, column=7, value=r[6])
        c_pr.font = data_font
        c_pr.number_format = currency_fmt
        c_pr.alignment = Alignment(horizontal="right")
        
        # Subtotal: Quantity * Price = D * G
        c_sub = ws_hcm.cell(row=row_num, column=8, value=f"=D{row_num}*G{row_num}")
        c_sub.font = bold_data_font
        c_sub.number_format = currency_fmt
        c_sub.alignment = Alignment(horizontal="right")
        
        # Stock status
        c_st = ws_hcm.cell(row=row_num, column=9, value=r[7])
        c_st.font = stock_in_font
        c_st.fill = stock_in_fill
        c_st.alignment = Alignment(horizontal="center")
        
        clink = ws_hcm.cell(row=row_num, column=10, value="Mua ngay")
        clink.hyperlink = r[8]
        clink.font = link_font
        clink.alignment = Alignment(horizontal="center")
        
        # Priority
        c_prio = ws_hcm.cell(row=row_num, column=11, value=r[9])
        if r[9] == "MUA TRƯỚC":
            c_prio.font = prio_first_font
            c_prio.fill = prio_first_fill
        elif r[9] == "MUA SAU":
            c_prio.font = prio_later_font
            c_prio.fill = prio_later_fill
        elif r[9] == "ĐATN":
            c_prio.font = prio_thesis_font
            c_prio.fill = prio_thesis_fill
        else:
            c_prio.font = prio_opt_font
            c_prio.fill = prio_opt_fill
        c_prio.alignment = Alignment(horizontal="center")
        
        ws_hcm.cell(row=row_num, column=12, value=r[10]).font = data_font
        
        for c in range(1, 13):
            if c not in (9, 11):
                ws_hcm.cell(row=row_num, column=c).fill = bg
            ws_hcm.cell(row=row_num, column=c).border = border_all
            
    end_hcm_r = start_hcm_r + len(hcm_purchasing_data) - 1
    
    col_widths_hcm = {
        'A': 6, 'B': 24, 'C': 26, 'D': 10, 'E': 20, 'F': 34, 
        'G': 15, 'H': 16, 'I': 14, 'J': 14, 'K': 16, 'L': 42
    }
    for col_l, w in col_widths_hcm.items():
        ws_hcm.column_dimensions[col_l].width = w
        
    ws_hcm.freeze_panes = "D7"
    ws_hcm.auto_filter.ref = f"A6:L{end_hcm_r}"

    # =============================================================
    # SHEET 5: CAU_HINH_CHI_PHI
    # =============================================================
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

    # =============================================================
    # SHEET 6: LINH_KIEN_TUY_CHON (Optional & Thesis Upgrades)
    # =============================================================
    ws5 = wb.create_sheet(title="LINH_KIEN_TUY_CHON")
    ws5.views.sheetView[0].showGridLines = True
    
    ws5.cell(row=2, column=2, value="DANH MỤC LINH KIỆN MỞ RỘNG & TÙY CHỌN (OPTIONAL UPGRADES)").font = title_font
    ws5.cell(row=3, column=2, value="Các module nâng cấp cho Khóa luận Tốt nghiệp hoặc khi có thêm kinh phí").font = subtitle_font
    
    opt_cols = [
        "STT", "Tên linh kiện", "Model đề xuất", "Mục đích sử dụng", 
        "Đơn giá ước tính", "Mức độ ưu tiên", "Thời điểm nên mua", "Shop đề xuất tại TP.HCM", "Link tham khảo"
    ]
    
    for c_idx, h in enumerate(opt_cols, start=1):
        cell = ws5.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_all
        
    opt_raw_data = [
        (1, "Micro MEMS I2S", "INMP441 Digital Microphone", "Thu âm tiếng đâm va kim loại, tiếng kính vỡ để đối chiếu kép với IMU", 
         45000, "MEDIUM", "Khóa luận Tốt nghiệp", "Hshop.vn (Q.11 / Thủ Đức)", "https://hshop.vn"),
          
        (2, "Cảm biến IMU công nghiệp", "ICM-42688-P 6-axis", "Độ trôi nhiệt siêu thấp, chống rung cơ học xe máy chuyên dụng", 
         135000, "MEDIUM", "Khóa luận Tốt nghiệp", "ThegioiIC (Thủ Đức)", "https://thegioiic.com"),
          
        (3, "Module Camera hiện trường", "ESP32-CAM / OV2640", "Chụp 1-3 bức ảnh hiện trường va chạm trước và sau cú đâm", 
         110000, "HIGH", "Khóa luận Tốt nghiệp", "Nshop (Q.3 / Thủ Đức)", "https://nshopvn.com"),
          
        (4, "Màn hình OLED 0.96 inch", "OLED SSD1306 I2C 128x64", "Hiển thị tốc độ xe, số vệ tinh GPS và trạng thái hộp đen tại chỗ", 
         65000, "LOW", "Mua sau nếu thích", "Hshop.vn (Q.11 / Thủ Đức)", "https://hshop.vn"),
          
        (5, "Gia công mạch in PCB", "PCB 2 lớp mạ thiếc JLCPCB", "Thiết kế bo mạch nguyên khối gắn linh kiện dán, đóng hộp chuyên nghiệp", 
         150000, "HIGH", "Khóa luận Tốt nghiệp", "JLCPCB (Ship TP.HCM)", "https://jlcpcb.com"),
          
        (6, "Cổng giao tiếp chẩn đoán ECU", "Module MCP2515 CAN-bus", "Giao tiếp cổng OBD-II xe máy đọc tay ga, vòng tua máy RPM, phanh ABS", 
         45000, "LOW", "Khóa luận Tốt nghiệp", "ThegioiIC (Thủ Đức)", "https://thegioiic.com"),
          
        (7, "Máy tính biên thị giác sâu", "Raspberry Pi Zero 2W", "Nếu muốn chạy mô hình YOLOv8 nhận diện biển số xe gây tai nạn", 
         480000, "LOW", "Khóa luận Tốt nghiệp", "Hshop / Cybershop TP.HCM", "https://hshop.vn")
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
        ws5.cell(row=row_num, column=8, value=r[7]).font = bold_data_font
        
        clink = ws5.cell(row=row_num, column=9, value="Xem linh kiện")
        clink.hyperlink = r[8]
        clink.font = link_font
        clink.alignment = Alignment(horizontal="center")
        
        for c in range(1, 10):
            if c != 6:
                ws5.cell(row=row_num, column=c).fill = bg
            ws5.cell(row=row_num, column=c).border = border_all
            
    col_widths_opt = {'A': 6, 'B': 22, 'C': 25, 'D': 38, 'E': 16, 'F': 16, 'G': 20, 'H': 24, 'I': 16}
    for col_l, w in col_widths_opt.items():
        ws5.column_dimensions[col_l].width = w
        
    ws5.freeze_panes = "C6"

    # =============================================================
    # SHEET 7: NGUON_GIA (Price Log with TP.HCM Stores)
    # =============================================================
    ws6 = wb.create_sheet(title="NGUON_GIA")
    ws6.views.sheetView[0].showGridLines = True
    
    ws6.cell(row=2, column=2, value="NHẬT KÝ KIỂM CHỨNG NGUỒN GIÁ & CỬA HÀNG THẬT TẠI TP.HCM").font = title_font
    ws6.cell(row=3, column=2, value="Toàn bộ báo giá được khảo sát trực tiếp từ các cửa hàng linh kiện điện tử hoạt động thực tế tại TP.HCM").font = subtitle_font
    
    log_cols = [
        "Mã nguồn (ID)", "Nền tảng / Đơn vị", "Tên cửa hàng", "Địa chỉ thực tế tại TP.HCM", "Tên sản phẩm niêm yết", 
        "Model / Biến thể", "Giá niêm yết", "Đường dẫn URL xác thực", "Ngày kiểm tra", "Trạng thái", "Ghi chú kỹ thuật"
    ]
    
    for c_idx, h in enumerate(log_cols, start=1):
        cell = ws6.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_all
        
    source_log_data = [
        ("SRC-01", "Website B2C", "Hshop.vn", "269/20 Lý Thường Kiệt, P.15, Q.11, TP.HCM", "Mạch MKE-K01 ESP32-S3 Dev Kit", "ESP32-S3 N16R8", 255000, 
         "https://hshop.vn/products/mach-phat-trien-mke-k01-esp32-s3-dev-kit", "20/09/2026", "VERIFIED", "Bản thiết kế tương thích chân ESP32-S3 DevKitC-1"),
          
        ("SRC-02", "Website B2B/B2C", "Thegioiic.com", "939/1A Kha Vạn Cân, P. Linh Tây, TP. Thủ Đức", "ESP32-S3-DevKitC-1-N8", "ESP32-S3-WROOM-1", 185000, 
         "https://thegioiic.com/esp32-s3-devkitc-1-n8", "20/09/2026", "VERIFIED", "Có sẵn hàng tại kho TP. Thủ Đức, lấy ngay"),
          
        ("SRC-03", "Website B2B/B2C", "Thegioiic.com", "939/1A Kha Vạn Cân, P. Linh Tây, TP. Thủ Đức", "GY-521 MPU-6050 Cảm Biến Con Quay Gia Tốc", "GY-521 MPU6050", 62000, 
         "https://thegioiic.com/gy-521-mpu-6050-cam-bien-con-quay-gia-toc", "20/09/2026", "VERIFIED", "Module nguyên vỉ, IC chuẩn đo được cả 6 trục gia tốc và góc"),
          
        ("SRC-04", "Website B2C", "Hshop.vn", "64/2 Đặng Văn Bi, P. Bình Thọ, TP. Thủ Đức", "Cảm biến gia tốc MPU6050 IMU 6DOF GY-521", "GY-521 MPU6050", 85000, 
         "https://hshop.vn", "20/09/2026", "VERIFIED", "Có sẵn tài liệu mẫu, nếu hết hàng có MPU6500 thay thế 55k"),
          
        ("SRC-05", "Website B2B/B2C", "Thegioiic.com", "939/1A Kha Vạn Cân, P. Linh Tây, TP. Thủ Đức", "GY-NEO6MV2 Module GPS", "NEO-6M V2", 98040, 
         "https://thegioiic.com", "20/09/2026", "VERIFIED", "Kèm anten gốm thụ động 25x25mm và pin backup RTC"),
          
        ("SRC-06", "Website B2C", "Nshopvn.com", "1 Vườn Chuối, P.4, Q.3, TP.HCM", "Module đọc thẻ nhớ Micro SD SPI 4AP3", "SPI MicroSD", 12000, 
         "https://nshopvn.com", "20/09/2026", "VERIFIED", "Giao tiếp SPI chuẩn có IC đệm chuyển mức 5V sang 3.3V"),
          
        ("SRC-07", "Sàn TMĐT", "Shopee Mall SanDisk", "Gian hàng chính hãng SanDisk VN (Kho TP.HCM)", "Thẻ nhớ SanDisk Ultra microSDHC 32GB", "SanDisk 32GB A1", 85000, 
         "https://shopee.vn", "20/09/2026", "VERIFIED", "Chính hãng Synnex FPT / Dầu Khí, Class 10 U1 tốc độ đọc 100MB/s"),
          
        ("SRC-08", "Website B2B/B2C", "Thegioiic.com", "939/1A Kha Vạn Cân, P. Linh Tây, TP. Thủ Đức", "DS3231 Mạch Thời Gian Thực Có IC Nhớ", "DS3231 + AT24C32", 70670, 
         "https://thegioiic.com", "20/09/2026", "VERIFIED", "Có thạch anh bù nhiệt độ sai số <2ppm, kèm pin CR2032"),
          
        ("SRC-09", "Website B2C", "Hshop.vn", "269/20 Lý Thường Kiệt, P.15, Q.11, TP.HCM", "Mạch giảm áp DC-DC Buck LM2596S 3A", "LM2596S", 20000, 
         "https://hshop.vn", "20/09/2026", "VERIFIED", "Chịu dòng đỉnh 3A, hạ áp 12V ắc-quy xe máy xuống 5V ổn định"),
          
        ("SRC-10", "Website B2C", "Hshop.vn", "269/20 Lý Thường Kiệt, P.15, Q.11, TP.HCM", "Mạch MKE-M21 SIM7680C 4G SMS/CALL Module", "SIM7680C 4G Cat-1", 245000, 
         "https://hshop.vn/products/mach-mke-m21-sim7680c-4g-sms-call-module", "20/09/2026", "VERIFIED", "Module chuẩn 4G Cat-1 do MakerLab sản xuất, sóng 2G đã bị cắt ở VN"),
          
        ("SRC-11", "Website B2C", "Nshopvn.com", "Số 7 Trần Hưng Đạo, P. Hiệp Phú, TP. Thủ Đức", "Cell pin Li-ion 18650 2000mAh", "18650 3.7V", 50000, 
         "https://nshopvn.com", "20/09/2026", "VERIFIED", "Dòng xả 5C ổn định, nuôi nguồn dự phòng khi đứt dây ắc-quy"),
          
        ("SRC-12", "Website B2B/B2C", "Thegioiic.com", "939/1A Kha Vạn Cân, P. Linh Tây, TP. Thủ Đức", "Hộp Nhựa Chống Thấm Nước IP65 100x68x50", "ABS IP65", 45000, 
         "https://thegioiic.com", "20/09/2026", "VERIFIED", "Có gioăng cao su chống nước và ốc vít inox siết nắp")
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
        ws6.cell(row=row_num, column=6, value=r[5]).font = data_font
        
        c_p = ws6.cell(row=row_num, column=7, value=r[6])
        c_p.number_format = currency_fmt
        c_p.alignment = Alignment(horizontal="right")
        
        clink = ws6.cell(row=row_num, column=8, value=r[7])
        clink.hyperlink = r[7]
        clink.font = link_font
        
        ws6.cell(row=row_num, column=9, value=r[8]).alignment = Alignment(horizontal="center")
        
        c_st = ws6.cell(row=row_num, column=10, value=r[9])
        c_st.font = Font(name=font_family, size=10, bold=True, color="166534")
        c_st.fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
        c_st.alignment = Alignment(horizontal="center")
        
        ws6.cell(row=row_num, column=11, value=r[10]).font = data_font
        
        for c in range(1, 12):
            if c != 10:
                ws6.cell(row=row_num, column=c).fill = bg
            ws6.cell(row=row_num, column=c).border = border_all
            
    col_widths_log = {'A': 10, 'B': 16, 'C': 18, 'D': 34, 'E': 30, 'F': 18, 'G': 15, 'H': 35, 'I': 14, 'J': 14, 'K': 38}
    for col_l, w in col_widths_log.items():
        ws6.column_dimensions[col_l].width = w
        
    ws6.freeze_panes = "D6"

    # Save to disk
    out_name = "BAO_GIA_LINH_KIEN_AIOT_SMART_BLACK_BOX.xlsx"
    wb.save(out_name)
    print(f"File Excel successfully updated and saved: {out_name}")

if __name__ == "__main__":
    build_updated_excel_report()
