#include <Arduino.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <RTClib.h>
#include <TinyGPSPlus.h>
#include "SdFat.h"

// ====================================================================
// SƠ ĐỒ CHÂN NGOẠI VI TRÊN ESP32-S3
// ====================================================================
#define I2C_SDA_PIN   8
#define I2C_SCL_PIN   9

#define SD_CS_PIN     10
#define SPI_MOSI_PIN  11
#define SPI_SCK_PIN   12
#define SPI_MISO_PIN  13

#define SIM_RX_PIN    15   // Nối vào TXD của SIM A7682S
#define SIM_TX_PIN    16   // Nối vào RXD của SIM A7682S
#define SIM_BAUD      115200

#define GPS_RX_PIN    18   // Nối vào TX của GPS NEO-M8N
#define GPS_TX_PIN    17   // Nối vào RX của GPS NEO-M8N
#define GPS_BAUD      9600

// Số điện thoại nhận tin nhắn của bạn
const char* DEFAULT_PHONE = "09xxxxxxxx"; // Placeholder: Thay bang so dien thoai nhan tin nhan SOS/GPS thuc te

// Khởi tạo các đối tượng ngoại vi
Adafruit_SSD1306 display(128, 64, &Wire, -1);
Adafruit_MPU6050 mpu;
RTC_DS3231 rtc;
TinyGPSPlus gps;
HardwareSerial gpsSerial(1);
HardwareSerial simSerial(2);

SdFs sd;
FsFile logFile;
const char* LOG_FILENAME = "edr_blackbox.csv";

bool oledOK = false, rtcOK = false, mpuOK = false, sdOK = false, simOK = false;
int csqVal = 0;

// Các thông số cảm biến thời gian thực
float liveSpeed = 0.0, liveRoll = 0.0, livePitch = 0.0, liveG = 1.0;
double liveLat = 0.0, liveLon = 0.0;
int liveSats = 0;
String liveTime = "00:00:00";
String liveDate = "2026-00-00";

// Hàm gửi lệnh AT sang module SIM
String sendSIM(String cmd, unsigned long timeout = 1000) {
  while (simSerial.available()) simSerial.read();
  simSerial.println(cmd);
  String res = "";
  unsigned long start = millis();
  while (millis() - start < timeout) {
    while (simSerial.available()) res += (char)simSerial.read();
  }
  return res;
}

bool rtcSynced = false;
unsigned long lastSyncAttempt = 0;

// ====================================================================
// ĐỒNG BỘ GIỜ THỰC TẾ VÀO RTC DS3231 TỰ ĐỘNG (4G HOẶC VỆ TINH GPS)
// ====================================================================

// 1. Đồng bộ giờ từ trạm phát sóng nhà mạng 4G (Viettel, Vina, Mobi)
bool syncRTCfrom4G() {
  if (!simOK || !rtcOK) return false;
  String res = sendSIM("AT+CCLK?", 500);
  res.trim();
  int idx = res.indexOf("+CCLK:");
  if (idx == -1) {
    Serial.printf("[4G CLOCK] SIM chua tra ve gio: %s\n", res.c_str());
    return false;
  }

  int q1 = res.indexOf("\"", idx);
  if (q1 == -1) q1 = idx + 6;
  else q1 += 1;

  int yy = res.substring(q1, q1 + 2).toInt();
  int MM = res.substring(q1 + 3, q1 + 5).toInt();
  int dd = res.substring(q1 + 6, q1 + 8).toInt();
  int hh = res.substring(q1 + 9, q1 + 11).toInt();
  int mm = res.substring(q1 + 12, q1 + 14).toInt();
  int ss = res.substring(q1 + 15, q1 + 17).toInt();

  int year = 2000 + yy;
  if (year >= 2024 && year <= 2035 && MM >= 1 && MM <= 12 && dd >= 1 && dd <= 31) {
    rtc.adjust(DateTime(year, MM, dd, hh, mm, ss));
    Serial.printf("\n>>> [RTC AUTO-SYNC] DA DONG BO GIO CHUAN TU MANG 4G: %04d-%02d-%02d %02d:%02d:%02d <<<\n\n",
                  year, MM, dd, hh, mm, ss);
    return true;
  } else {
    Serial.printf("[4G CLOCK] Nha mang chua phat gio NITZ (Doc duoc: %s)\n", res.c_str());
  }
  return false;
}

// 2. Đồng bộ giờ từ Vệ tinh GPS (Giờ nguyên tử UTC + 7)
bool syncRTCfromGPS() {
  if (!rtcOK) return false;
  if (gps.location.isValid() && gps.date.isValid() && gps.time.isValid()) {
    int year = gps.date.year();
    if (year >= 2024) {
      DateTime utc(year, gps.date.month(), gps.date.day(),
                   gps.time.hour(), gps.time.minute(), gps.time.second());
      DateTime vnTime = utc + TimeSpan(0, 7, 0, 0); // UTC+7 (Múi giờ Việt Nam)
      rtc.adjust(vnTime);
      Serial.printf("\n>>> [RTC AUTO-SYNC] DA DONG BO GIO CHUAN TU VE TINH GPS: %04d-%02d-%02d %02d:%02d:%02d <<<\n\n",
                    vnTime.year(), vnTime.month(), vnTime.day(), vnTime.hour(), vnTime.minute(), vnTime.second());
      return true;
    }
  }
  return false;
}

// ====================================================================
// HÀM GỬI VỊ TRÍ GPS QUA TIN NHẮN SMS (ĐÃ TỐI ƯU GÓI GỌN < 120 KÝ TỰ)
// ====================================================================
bool sendGPSLocationSMS(String destPhone) {
  if (!simOK) {
    Serial.println("[SMS THAT BAI] Module SIM chua san sang!");
    return false;
  }

  Serial.println("\n-------------------------------------------------------------");
  Serial.printf("📍 [DANG GUI VI TRI GPS] Den so: %s ...\n", destPhone.c_str());

  sendSIM("AT+CMGF=1", 1000);
  sendSIM("AT+CSCS=\"GSM\"", 500);
  delay(100);

  while (simSerial.available()) simSerial.read();
  simSerial.print("AT+CMGS=\"");
  simSerial.print(destPhone);
  simSerial.println("\"");

  unsigned long t = millis();
  bool prompt = false;
  while (millis() - t < 5000) {
    if (simSerial.available() && simSerial.read() == '>') {
      prompt = true;
      break;
    }
  }

  if (!prompt) {
    Serial.println("[LOI] Module SIM khong mo dau nhac '>'!");
    return false;
  }

  delay(200);

  // SOẠN NỘI DUNG GỌN GÀNG (~110 KÝ TỰ, KHÔNG BAO GIỜ BỊ QUÁ TẢI)
  if (liveLat != 0.0 && liveLon != 0.0) {
    simSerial.printf("[EDR VI TRI XE]\nhttps://maps.google.com/?q=%.6f,%.6f\n", liveLat, liveLon);
    simSerial.printf("V: %.1fkm/h | Sat: %d\n", liveSpeed, liveSats);
    simSerial.printf("Nghieng: %.1f do | %s", liveRoll, liveTime.c_str());
  } else {
    simSerial.printf("[EDR VI TRI XE]\nGPS dang tim ve tinh (Sat: %d)\n", liveSats);
    simSerial.printf("https://maps.google.com/?q=10.8416,106.7660\n");
    simSerial.printf("Nghieng: %.1f do | %s", liveRoll, liveTime.c_str());
  }

  delay(200);
  simSerial.write(26); // Ký tự kết thúc Ctrl+Z

  // Đợi phản hồi và in trực tiếp ra Terminal
  Serial.print("[SIM PHAN HOI] ");
  t = millis();
  String res = "";
  while (millis() - t < 20000) {
    while (simSerial.available()) {
      char c = (char)simSerial.read();
      res += c;
      Serial.write(c);
    }
    if (res.indexOf("+CMGS:") != -1 && res.indexOf("OK") != -1) {
      Serial.println("\n>>> [THANH CONG RUC RO] TOA DO GPS DA GUI DEN DIEN THOAI! <<<");
      return true;
    }
    if (res.indexOf("ERROR") != -1) {
      Serial.println("\n>>> [THAT BAI] Nha mang tu choi (Kiem tra tai khoan SIM)!");
      return false;
    }
  }

  Serial.println("\n>>> [TIMEOUT] Het thoi gian cho!");
  return false;
}

void setup() {
  Serial.begin(115200);
  delay(2000);

  Serial.println("\n\n==========================================================");
  Serial.println("  AIoT EDR BLACKBOX: DINH VI XE & GUI GPS QUA TIN NHAN SMS");
  Serial.println("==========================================================");

  // 1. I2C (OLED, RTC, MPU6050)
  Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN);
  Wire.setTimeOut(200);

  if (display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    oledOK = true;
    display.clearDisplay();
    display.setTextColor(WHITE);
    display.setTextSize(1);
    display.setCursor(15, 10);
    display.println("AIoT BLACKBOX EDR");
    display.setCursor(10, 30);
    display.println("GPS + SMS Ready...");
    display.display();
    Serial.println("[1] OLED SSD1306 (0x3C) ... OK");
  }

  if (rtc.begin(&Wire)) {
    rtcOK = true;
    Serial.println("[2] RTC DS3231 (0x68)   ... OK");
    if (rtc.lostPower()) {
      Serial.println("  -> [CANH BAO] RTC mat nguon pin, khoi tao tam tu may tinh.");
      rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
    }
  }

  if (mpu.begin(0x69, &Wire)) {
    mpuOK = true;
    mpu.setAccelerometerRange(MPU6050_RANGE_16_G);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
    Serial.println("[3] MPU-6050 (0x69)     ... OK");
  }

  // 2. SPI (THẺ NHỚ MICROSD)
  SPI.begin(SPI_SCK_PIN, SPI_MISO_PIN, SPI_MOSI_PIN, SD_CS_PIN);
  delay(150);
  SdSpiConfig sdConfig(SD_CS_PIN, SHARED_SPI, SD_SCK_MHZ(16), &SPI);

  for (int retry = 0; retry < 3; retry++) {
    if (sd.cardBegin(sdConfig) && sd.volumeBegin()) {
      sdOK = true;
      break;
    }
    delay(200);
  }

  if (sdOK) {
    Serial.println("[4] Thẻ nhớ MicroSD     ... OK");
    if (!sd.exists(LOG_FILENAME)) {
      if (logFile.open(LOG_FILENAME, O_RDWR | O_CREAT | O_AT_END)) {
        logFile.println("DateTime,Speed_kmh,Lat,Lon,Sats,Ax,Ay,Az,Roll,Pitch,GForce,CSQ,Event");
        logFile.close();
      }
    }
  } else {
    Serial.println("[4] Thẻ nhớ MicroSD     ... THAT BAI (Kiem tra the hoac chan SPI)!");
  }

  // 3. UART1 (GPS NEO-M8N)
  gpsSerial.begin(GPS_BAUD, SERIAL_8N1, GPS_RX_PIN, GPS_TX_PIN);
  Serial.println("[5] GPS NEO-M8N (UART1) ... OK (9600 bps)");

  // 4. UART2 (MODULE 4G A7682S)
  simSerial.begin(SIM_BAUD, SERIAL_8N1, SIM_RX_PIN, SIM_TX_PIN);
  delay(1500);
  String atRes = sendSIM("AT", 1000);
  if (atRes.indexOf("OK") != -1) {
    simOK = true;
    sendSIM("ATE0", 500);
    sendSIM("AT+CTZU=1", 500); // Tu dong lay mui gio va thoi gian tu nha mang 4G
    sendSIM("AT+CMGF=1", 500);
    // Kích hoạt tự động đẩy SMS khi điện thoại nhắn tới
    sendSIM("AT+CNMI=2,2,0,0,0", 500);
    Serial.println("[6] 4G LTE A7682S       ... OK");
  }

  Serial.println("\n----------------------------------------------------------");
  Serial.println("HUONG DAN LENH TERMINAL:");
  Serial.println("-> Go 'sms'  : Gui tin nhan chua vi tri GPS den dien thoai.");
  Serial.println("-> Go 'sync' : Dong bo ngay gio may tinh vao chip pin RTC DS3231.");
  Serial.println("----------------------------------------------------------\n");
  delay(1500);
}

unsigned long lastSample = 0;
unsigned long lastCsqCheck = 0;

void loop() {
  // Tiếp nhận dòng dữ liệu NMEA liên tục từ GPS
  while (gpsSerial.available()) {
    gps.encode(gpsSerial.read());
  }

  // LỆNH ĐIỀU KHIỂN TỪ BÀN PHÍM MÁY TÍNH
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    if (cmd.equalsIgnoreCase("sms")) {
      sendGPSLocationSMS(DEFAULT_PHONE);
    } else if (cmd.equalsIgnoreCase("gps")) {
      Serial.println("\n----------------------------------------------------------");
      Serial.println(">>> DUMP TIN HIEU RAW NMEA TU GPS (XEM GPS CO DANG PHAT KHONG):");
      unsigned long tDump = millis();
      int lines = 0;
      while (millis() - tDump < 3000 && lines < 10) {
        if (gpsSerial.available()) {
          char c = gpsSerial.read();
          gps.encode(c);
          Serial.write(c);
          if (c == '\n') lines++;
        }
      }
      Serial.println("\n----------------------------------------------------------\n");
    } else if (cmd.equalsIgnoreCase("sync")) {
      rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
      rtcSynced = true;
      Serial.println("\n>>> [THANH CONG] DA DONG BO GIO BUILD MAY TINH VAO CHIP PIN RTC DS3231! <<<");
    } else if (cmd.indexOf(":") != -1) {
      // Cho phép gõ trực tiếp giờ hiện tại trên máy tính, ví dụ: 11:25:00 hoặc set 11:25:00
      String timePart = cmd;
      if (timePart.startsWith("set ") || timePart.startsWith("time ")) {
        timePart = timePart.substring(timePart.indexOf(" ") + 1);
      }
      timePart.trim();
      int c1 = timePart.indexOf(":");
      int c2 = timePart.indexOf(":", c1 + 1);
      if (c1 != -1) {
        int h = timePart.substring(0, c1).toInt();
        int m = (c2 != -1) ? timePart.substring(c1 + 1, c2).toInt() : timePart.substring(c1 + 1).toInt();
        int s = (c2 != -1) ? timePart.substring(c2 + 1).toInt() : 0;
        if (h >= 0 && h < 24 && m >= 0 && m < 60 && s >= 0 && s < 60) {
          DateTime now = rtc.now();
          int y = (now.year() >= 2024 && now.year() <= 2035) ? now.year() : 2026;
          int mo = (now.month() >= 1 && now.month() <= 12) ? now.month() : 11;
          int d = (now.day() >= 1 && now.day() <= 31) ? now.day() : 2;
          rtc.adjust(DateTime(y, mo, d, h, m, s));
          rtcSynced = true;
          Serial.printf("\n>>> [THANH CONG] DA CAI GIO CHINH XAC TU BAN PHIM: %02d:%02d:%02d <<<\n\n", h, m, s);
        } else {
          Serial.println("\n[LOI] Gio khong hop le! Vui long nhap dinh dang HH:MM:SS (vi du: 11:25:00)");
        }
      }
    }
  }

  // CÁCH 2: ĐIỆN THOẠI BẠN NHẮN TIN TỚI SIM TRÊN XE
  if (simSerial.available()) {
    String line = simSerial.readStringUntil('\n');
    line.trim();

    // Phát hiện tin nhắn mới đến: +CMT: "+84961542477",...
    if (line.startsWith("+CMT:")) {
      int firstQuote = line.indexOf("\"");
      int secondQuote = line.indexOf("\"", firstQuote + 1);
      String sender = line.substring(firstQuote + 1, secondQuote);

      // Đọc tiếp dòng nội dung tin nhắn
      String content = simSerial.readStringUntil('\n');
      content.trim();
      content.toUpperCase();

      Serial.printf("\n📩 [CO TIN NHAN DEN TU: %s] Noi dung: '%s'\n", sender.c_str(), content.c_str());

      // Nếu tin nhắn có chữ SMS hoặc VITRI hoặc GPS -> Tự động reply lại link tọa độ!
      if (content.indexOf("SMS") != -1 || content.indexOf("VITRI") != -1 || content.indexOf("GPS") != -1) {
        Serial.println("-> Yeu cau lay vi tri hop le! Dang tu dong tra loi vi tri GPS...");
        sendGPSLocationSMS(sender);
      }
    }
  }

  // Quét sóng 4G mỗi 3 giây
  if (simOK && (millis() - lastCsqCheck > 3000)) {
    lastCsqCheck = millis();
    String res = sendSIM("AT+CSQ", 300);
    int idx = res.indexOf("+CSQ: ");
    if (idx != -1) {
      csqVal = res.substring(idx + 6, res.indexOf(",", idx)).toInt();
    }
  }

  // Tự động đồng bộ giờ RTC từ trạm sóng 4G hoặc Vệ tinh GPS
  if (!rtcSynced && (millis() - lastSyncAttempt > 4000)) {
    lastSyncAttempt = millis();
    // 1. Ưu tiên đồng bộ từ mạng 4G (rất nhanh, chạy ngay trong nhà khi có sóng 4G)
    if (simOK && csqVal > 0) {
      rtcSynced = syncRTCfrom4G();
    }
    // 2. Dự phòng: đồng bộ từ vệ tinh GPS (khi ra ngoài trời bắt được sóng GPS)
    if (!rtcSynced && gps.location.isValid()) {
      rtcSynced = syncRTCfromGPS();
    }
  }

  // Chu kỳ lấy mẫu 500ms
  if (millis() - lastSample >= 500) {
    lastSample = millis();

    if (rtcOK) {
      DateTime now = rtc.now();
      char bufT[16], bufD[16];
      snprintf(bufT, sizeof(bufT), "%02d:%02d:%02d", now.hour(), now.minute(), now.second());
      snprintf(bufD, sizeof(bufD), "%04d-%02d-%02d", now.year(), now.month(), now.day());
      liveTime = String(bufT);
      liveDate = String(bufD);
    }

    liveSats  = gps.satellites.isValid() ? gps.satellites.value() : 0;
    liveLat   = gps.location.isValid() ? gps.location.lat() : 0.0;
    liveLon   = gps.location.isValid() ? gps.location.lng() : 0.0;

    // THUẬT TOÁN TÍNH VẬN TỐC CHUẨN Ô TÔ / HỘP ĐEN EDR:
    // 1. Chỉ chấp nhận vận tốc khi có ít nhất 4 vệ tinh (Đã khóa 3D Fix hoàn chỉnh)
    // 2. Dữ liệu GPS không bị cũ/đơ (age < 1500ms)
    // 3. Ngưỡng lọc tĩnh 4.5 km/h: Triệt tiêu hoàn toàn sóng dội vách tường khi đứng yên
    if (liveSats >= 4 && gps.speed.isValid() && gps.speed.age() < 1500) {
      float spd = gps.speed.kmph();
      if (spd < 4.5) {
        liveSpeed = 0.0; // Đang đỗ / đứng yên -> Ép về 0.0 km/h tuyệt đối
      } else {
        liveSpeed = spd; // Xe di chuyển thật -> Hiển thị tốc độ thật
      }
    } else {
      liveSpeed = 0.0; // Mất vệ tinh hoặc sóng chập chờn (< 4 vệ tinh) -> Luôn là 0.0
    }

    float ax = 0, ay = 0, az = 0;
    bool isCrash = false;

    if (mpuOK) {
      sensors_event_t a, g, temp;
      mpu.getEvent(&a, &g, &temp);
      ax = a.acceleration.x;
      ay = a.acceleration.y;
      az = a.acceleration.z;
      liveRoll  = atan2(ay, az) * 180.0 / PI;
      livePitch = atan2(-ax, sqrt(ay * ay + az * az)) * 180.0 / PI;
      liveG     = sqrt(ax * ax + ay * ay + az * az) / 9.80665;

      if (abs(liveRoll) > 55.0 || abs(livePitch) > 55.0 || liveG > 2.8) {
        isCrash = true;
      }
    }

    // Ghi thẻ nhớ
    if (sdOK) {
      if (logFile.open(LOG_FILENAME, O_RDWR | O_CREAT | O_AT_END)) {
        logFile.printf("%s %s,%.1f,%.6f,%.6f,%d,%.2f,%.2f,%.2f,%.1f,%.1f,%.2f,%d,%s\n",
                       liveDate.c_str(), liveTime.c_str(),
                       liveSpeed, liveLat, liveLon, liveSats,
                       ax, ay, az, liveRoll, livePitch, liveG, csqVal,
                       isCrash ? "CRASH_EVENT" : "NORMAL");
        logFile.close();
      }
    }

    // In Serial Monitor
    Serial.printf("[%s] V:%4.1f | Roll:%5.1f* | 4G:%2d | Sat:%2d (GPS-Bytes:%lu) | Lat:%.4f Lon:%.4f | SD:%s\n",
                  liveTime.c_str(), liveSpeed, liveRoll, csqVal, liveSats, gps.charsProcessed(), liveLat, liveLon,
                  sdOK ? "REC" : "ERR");

    // Hiển thị OLED
    if (oledOK) {
      display.clearDisplay();

      display.fillRect(0, 0, 128, 12, WHITE);
      display.setTextColor(BLACK, WHITE);
      display.setTextSize(1);
      display.setCursor(2, 2);
      if (csqVal < 99 && csqVal > 0) display.printf("%s | 4G:%d", liveTime.c_str(), csqVal);
      else display.printf("%s | 4G:NOSIG", liveTime.c_str());
      display.setCursor(95, 2);
      display.printf("SD:%c", sdOK ? 'V' : 'X');

      display.setTextColor(WHITE);

      // Tốc độ xe & Vệ tinh
      display.setCursor(0, 16);
      display.setTextSize(2);
      display.printf("%4.1f", liveSpeed);
      display.setTextSize(1);
      display.print(" km/h");
      display.setCursor(85, 20);
      display.printf("Sat:%d", liveSats);

      display.drawLine(0, 34, 127, 34, WHITE);

      // Góc nghiêng Roll & Lực G
      display.setCursor(0, 38);
      display.printf("Roll : %5.1f*", liveRoll);
      display.setCursor(75, 38);
      display.printf("G:%4.2fG", liveG);

      // Dòng GPS
      display.setCursor(0, 52);
      if (gps.charsProcessed() == 0) {
        display.print("GPS: MAT KET NOI DAY!");
      } else if (liveSats >= 3) {
        display.printf("GPS: %.4f, %.4f", liveLat, liveLon);
      } else {
        display.printf("GPS: Tim ve tinh (%luB)", gps.charsProcessed());
      }

      display.display();
    }
  }
}