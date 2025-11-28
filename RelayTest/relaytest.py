import RPi.GPIO as GPIO
import time
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
import spidev
 
# -----------------------
# 1) GPIO TANIMLARI
# -----------------------
IN1 = 17
IN2 = 27
ENA = 18
RELAY = 16         # Röle IN pini
BUZZ = TonalBuzzer(21)   # Pasif buzzer
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
 
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(RELAY, GPIO.OUT)
 
# Başlangıçta her şey kapalı
GPIO.output(ENA, GPIO.LOW)
GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)
GPIO.output(RELAY, GPIO.LOW)
 
 
# -----------------------
# 2) MCP3008 SPI AYARLARI
# -----------------------
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000
 
def read_adc(ch):
    adc = spi.xfer2([1, (8 + ch) << 4, 0])
    value = ((adc[1] & 3) << 8) + adc[2]
    return value
 
# -----------------------
# 3) ACS712 Akım hesaplama
# -----------------------
def acs_current(raw):
    voltage = (raw / 1023.0) * 5.0   # MCP3008 → 0-5V
    zero = 2.5                       # ACS712 merkez voltaj
    sensitivity = 0.185              # 5A model → 185 mV/A
    current = (voltage - zero) / sensitivity
    return current
 
 
# -----------------------
# 4) Motor kontrol fonksiyonları
# -----------------------
def motor_start():
    GPIO.output(RELAY, GPIO.HIGH)  # Röle yolu açar → Motor beslemesi gelir
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    print("Motor ÇALIŞTI")
 
def motor_stop():
    GPIO.output(RELAY, GPIO.LOW)   # Röle motor gücünü keser
    GPIO.output(ENA, GPIO.LOW)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    print("⚠ MOTOR DURDURULDU - AŞIRI AKIM!")
 
 
# -----------------------
# 5) Buzzer ALARM
# -----------------------
def alarm():
    for f in range(400, 900, 50):
        BUZZ.play(Tone(f))
        time.sleep(0.05)
    BUZZ.stop()
 
 
# -----------------------
# 6) ANA PROGRAM
# -----------------------
LIMIT = 2.5   # Aşırı akım sınırı (deneme için 2.5A)
 
try:
    motor_start()
    time.sleep(1)
 
    while True:
        raw = read_adc(0)
        current = acs_current(raw)
 
        print(f"RAW: {raw}  Akım: {current:.2f} A")
 
        # AŞIRI AKIM KONTROLÜ
        if current > LIMIT:
            motor_stop()
            alarm()
            break
 
        time.sleep(0.2)
 
except KeyboardInterrupt:
    pass
 
finally:
    BUZZ.stop()
    GPIO.cleanup()
    print("Program sonlandırıldı.")
 