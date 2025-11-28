import RPi.GPIO as GPIO
import time
import spidev
import glob
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
import smbus2
 
# ===========================
# ADXL345 AYARLARI
# ===========================
BUS = smbus2.SMBus(1)
ADDRESS = 0x53
 
POWER_CTL = 0x2D
DATA_FORMAT = 0x31
DATAX0 = 0x32
 
BUS.write_byte_data(ADDRESS, POWER_CTL, 0x08)
BUS.write_byte_data(ADDRESS, DATA_FORMAT, 0x08)
 
def read_axes():
    data = BUS.read_i2c_block_data(ADDRESS, DATAX0, 6)
    x = int.from_bytes(data[0:2], 'little', signed=True)
    y = int.from_bytes(data[2:4], 'little', signed=True)
    z = int.from_bytes(data[4:6], 'little', signed=True)
    return x, y, z
 
def read_vibration():
    x, y, z = read_axes()
    vib = abs(x) + abs(y) + abs(z)
    return vib
 
 
# ===========================
# RASPBERRY PI PIN AYARLARI
# ===========================
IN1 = 17
IN2 = 27
ENA = 18
RELAY = 16
BUZZ_PIN = 21
LED = 22
SOUND_PIN = 5
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
 
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(RELAY, GPIO.OUT)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(SOUND_PIN, GPIO.IN)
 
buzzer = TonalBuzzer(BUZZ_PIN)
 
 
# ===========================
# MCP3008 AYARLARI (ACS712)
# ===========================
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1350000
 
def read_adc(ch):
    adc = spi.xfer2([1, (8+ch)<<4, 0])
    return ((adc[1] & 3) << 8) + adc[2]
 
def acs_current(raw):
    voltage = (raw / 1023.0) * 5.0
    zero = 2.5
    sensitivity = 0.185
    return (voltage - zero) / sensitivity
 
 
# ===========================
# SICAKLIK OKUMA
# ===========================
def read_temp():
    try:
        device = glob.glob("/sys/bus/w1/devices/28*")[0]
        with open(device + "/w1_slave") as f:
            lines = f.readlines()
        if "YES" in lines[0]:
            temp_str = lines[1].split("t=")[-1]
            return float(temp_str) / 1000.0
    except:
        return 0.0
 
 
# ===========================
# MOTOR KONTROL
# ===========================
def motor_start():
    GPIO.output(RELAY, GPIO.HIGH)
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    print("Motor çalıştı.")
 
def motor_stop():
    GPIO.output(RELAY, GPIO.LOW)
    GPIO.output(ENA, GPIO.LOW)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    print("⚠ MOTOR DURDURULDU!")
 
 
# ===========================
# ALARM MODU
# ===========================
def alarm_mode(reason):
    print(f"\n🚨 ALARM! Sebep: {reason}")
 
    motor_stop()
    GPIO.output(LED, GPIO.HIGH)
 
    for i in range(40):
        buzzer.play(Tone(400 + (i % 10) * 50))
        time.sleep(0.05)
 
    buzzer.stop()
    GPIO.output(LED, GPIO.LOW)
    time.sleep(2)
 
 
# ===========================
# EŞİKLER
# ===========================
TEMP_LIMIT = 50
CURRENT_LIMIT = 2.5
VIB_LIMIT = 1000        # ADXL345 için MANTIKLI eşik değer
SOUND_LIMIT = 0         # Dijital sensör: 0 = gürültü algılandı
 
 
# ===========================
# ANA PROGRAM
# ===========================
try:
    motor_start()
    time.sleep(1)
 
    while True:
        temp = read_temp()
        raw = read_adc(0)
        current = acs_current(raw)
        vib = read_vibration()
        sound = GPIO.input(SOUND_PIN)
 
        print(f"TEMP={temp:.1f}C  AKIM={current:.2f}A  VIB={vib}  SES={sound}")
 
        if temp > TEMP_LIMIT:
            alarm_mode("AŞIRI SICAKLIK")
            break
 
        if current > CURRENT_LIMIT:
            alarm_mode("AŞIRI AKIM")
            break
 
        if vib > VIB_LIMIT:
            alarm_mode("AŞIRI TİTREŞİM")
            break
 
        if sound == SOUND_LIMIT:
            alarm_mode("YÜKSEK SES")
            break
 
        time.sleep(0.2)
 
except KeyboardInterrupt:
    pass
 
finally:
    buzzer.stop()
    GPIO.cleanup()
    print("Program sonlandırıldı.")
 