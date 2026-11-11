# DANH SÁCH VẤN ĐỀ MỞ (`PCB_OPEN_ISSUES.md`)

> **Đã lỗi thời (snapshot cuối Gate 1.5).** Danh sách hiện hành: `..\GATE_2_PLACEMENT\PCB_OPEN_ISSUES.md` (Gate 2 = CONDITIONAL).

**Trạng thái lúc đó:** **`0 BLOCKING ISSUES — SẴN SÀNG VÀO GATE 2 (PLACEMENT PCB 1 LỚP)`**

| Mã | Hạng mục trước đây | Giải pháp đã chốt (`LOCKED`) | Trạng thái |
| :---: | :--- | :--- | :---: |
| `ISS-01` | Khoảng cách 2 hàng chân `ESP32-S3 N16R8` (`22.86mm` vs `25.40mm`) | Đã chốt chính thức **`Row Pitch = 25.40 mm` (`1000 mil`)**, xóa bỏ hoàn toàn footprint `22.86 mm`. | **RESOLVED / LOCKED** |
| `ISS-02` | Điện áp `VCC` của `MicroSD Breakout` (`J1`) | Đã chốt nối **`5V_SYS → MicroSD VCC (Pin 5)`** (sử dụng LDO 3.3V + Level Shifter có sẵn trên breakout). | **RESOLVED / LOCKED** |
| `ISS-03` | Tên module SIM 4G & Điện áp `SIM_PWR` (`U5`) | Đã đồng bộ tên **`A7680C`**, nối **`5V_SYS → SIM_PWR → VCC breakout A7680C`** kèm tụ `C3 (470µF)` + `C4 (100nF)` và `TP_SIM_PWR`. | **RESOLVED / LOCKED** |
| `ISS-04` | Chân dự phòng `BUZZER`, `CANCEL`, `LED_STATUS` | Đã khóa trên schematic/PCB: **`GPIO5 = BUZZER_CTRL`** (+ `R_BE 10kΩ`), **`GPIO6 = CANCEL`**, **`GPIO7 = LED_STATUS`**. | **RESOLVED / LOCKED** |
