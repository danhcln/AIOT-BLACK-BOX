# BÁO CÁO KIẾN TRÚC NGUỒN ĐÃ CHỐT (`POWER_ARCHITECTURE_REVIEW.md`)

**Trạng thái:** **`LOCKED & VERIFIED (ERC = 0 Errors, 0 Warnings)`**

---

## 1. SƠ ĐỒ KIẾN TRÚC PHÂN PHỐI NGUỒN CHÍNH THỨC

```text
[Bộ nguồn ngoài 2x18650 LX-2BUPS 5V/3A]
                 │
                 ▼ (Qua Domino J2: TermBlock_1x02_P5.08mm)
      ════════ 5V_SYS (Đặt điểm đo TP1: TP_5V & TP4: TP_GND) ════════
       ├──► 1. ESP32-S3-DevKitC-1 N16R8 (U1 Pin 21: 5Vin)
       ├──► 2. MicroSD Card Adapter (J1 Pin 5: VCC = 5V -> qua LDO 3.3V AMS1117 nội trên breakout)
       ├──► 3. Mạch Còi Báo Động Chủ Động 5V (BZ1 Pin 1: +5V, đóng cắt qua Q1 2SC1815 ở GPIO5 + R6 10k R_BE)
       ├──► 4. Nhánh nguồn riêng SIM 4G (Qua J3: SIM_PWR_BRANCH tách hình sao ngay tại đầu vào 5V_SYS)
       │         │
       │         ▼
       │      SIM_PWR (5V) ──► Tụ bù dòng đỉnh C3 (470µF Low-ESR) + C4 (100nF) + Điểm đo TP3 (TP_SIM_PWR)
       │         │
       │         └──► Module 4G LTE A7680C Breakout (U5 Pin 1: VCC = 5V trên J6)
       │
       └──► 5. Module Hạ Áp 3.3V Độc Lập (U6 Pin 1: IN+ 5V_SYS -> Pin 3: 3V3_SYS)
                 │
                 ▼
      ════════ 3V3_SYS (Tụ lọc C1: 100nF & Điểm đo TP2: TP_3V3) ════════
                 ├──► OLED 0.96" SSD1306 GM009605v4.3 (U7 Pin 2: VDD)
                 ├──► Cảm biến GY-521 MPU6050 (U2 Pin 1: VCC & Pin 7: AD0 = 0x69)
                 ├──► RTC DS3231 ZS-042 (U3 Pin 5: VCC — Đã gỡ R5 sạc)
                 ├──► GPS NEO-M8N V2149 (U4 Pin 1: VCC)
                 └──► Điện trở kéo lên I2C (R_PU1, R_PU2 = 4.7kΩ) & Nút nhấn CANCEL (R3 = 10kΩ)
```

---

## 2. BẢNG PHÂN BỔ ĐIỆN ÁP VÀ DÒNG ĐIỆN TỪNG KHỐI

| Linh kiện / Module | Ký hiệu | Đường nguồn cấp | Điện áp danh định | Dòng tiêu thụ TB | Dòng đỉnh (Peak) | Ghi chú kỹ thuật đã xác minh |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Nguồn tổng UPS 2 cell 18650** | `J2` | Đầu vào `5V_SYS` | `5.0 V` | — | `3000 mA` (Max) | Cấp qua domino vít `5.08mm` chịu dòng cao |
| **ESP32-S3-DevKitC-1 N16R8** | `U1` | `5V_SYS` | `5.0 V` (Pin 21 `5V`) | `90 mA` | `350 mA` | Chân `3V3` (Pin 1, 2) để `NC`, không dùng cấp nguồn ngoại vi |
| **MicroSD Card Adapter** | `J1` | **`5V_SYS`** | **`5.0 V`** (Pin 5 `VCC`) | `30 mA` | `100 mA` | Có sẵn LDO `3.3V` (`U2`) + đệm mức logic `U3` trên breakout |
| **Module 4G LTE `A7680C`** | `U5` | **`SIM_PWR` (từ `5V_SYS`)** | **`5.0 V`** (Pin 1 `VCC`) | `60 mA` | `1500 - 2000 mA` | Đi nhánh sao riêng từ `5V_SYS` qua `J3` + tụ `C3 (470µF)` + `C4 (100nF)` |
| **Còi báo động 5V (`BZ1`)** | `BZ1` | `5V_SYS` | `5.0 V` (Pin 1 `+`) | `25 mA` | `35 mA` | Đóng cắt qua NPN `Q1 (2SC1815)` tại `GPIO5`, có `R6 (10kΩ R_BE)` xuống `GND` |
| **Module hạ áp `3.3V`** | `U6` | `5V_SYS -> 3V3_SYS` | `5.0 V -> 3.3 V` | — | `>= 800 mA` | Tạo đường nguồn `3V3_SYS` độc lập cho toàn bộ cảm biến & GPS |
| **OLED 0.96" `GM009605v4.3`** | `U7` | `3V3_SYS` | `3.3 V` (Pin 2 `VDD`) | `15 mA` | `25 mA` | Thứ tự chân thực tế: `1:GND, 2:VDD, 3:SCK, 4:SDA` |
| **GY-521 `MPU6050`** | `U2` | `3V3_SYS` | `3.3 V` (Pin 1 `VCC`) | `4 mA` | `5 mA` | Chân `AD0` (Pin 7) nối `3V3_SYS` khóa địa chỉ I2C `0x69` |
| **RTC `DS3231` ZS-042** | `U3` | `3V3_SYS` | `3.3 V` (Pin 5 `VCC`) | `2 mA` | `3 mA` | Đã gỡ điện trở sạc `R5` để bảo vệ pin `CR2032` |
| **GPS `NEO-M8N` V2149** | `U4` | `3V3_SYS` | `3.3 V` (Pin 1 `VCC`) | `35 mA` | `65 mA` | Kết nối qua header `1x05` (`CONNECTOR_ONLY`) |

---

## 3. YÊU CẦU BẮT BUỘC KHI PLACEMENT & ROUTING PCB 1 LỚP (`B.Cu`)
1. **Tách nhánh hình sao (`Star Point`) cho `SIM_PWR`:** Đường đồng từ domino `J2` (`5V_SYS`) tới `J3` → `C3 (470µF)` → `C4 (100nF)` → `U5 (A7680C Pin 1 VCC)` và đường `GND` trả về từ `U5 (Pin 5 GND)` về `J2 (Pin 2)` phải có bề rộng **`>= 1.5 mm - 2.0 mm`**, không đi vòng qua chân `ESP32-S3` hay `MicroSD`.
2. **Đặt tụ lọc sát tải:** `C3 (470µF)` và `C4 (100nF)` phải đặt ngay cạnh đầu nối `U5` (`A7680C`). Tụ `C1 (100nF)` đặt ngay cạnh ngõ ra `3V3_SYS` của `U6`.
