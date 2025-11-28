import RPi.GPIO as GPIO
import time
import spidev
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
 
# ===========================
#   PIN AYARLARI
# ===========================
IN1 = 17
IN2 = 27
ENA = 18
RELAY = 16
BUZZ_PIN = 21
LED = 22             # Fiziksel pin 15 → GPIO22
SOUND_PIN = 5        # Örnek dijital giriş
TEMP_SENSOR_PATH = "/sys/bus/w1/devices/28*/w1_slave"
 
# ===========================
#   GPIO AYARLARI
# ===========================
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
 
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(RELAY, GPIO.OUT)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(SOUND_PIN, GPIO.IN)
 
GPIO.output(ENA, GPIO.LOW)
GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)
GPIO.output(RELAY, GPIO.LOW)
GPIO.output(LED, GPIO.LOW)
 
buzzer = TonalBuzzer(BUZZ_PIN)
 
# ===========================
#   MCP3008 (ACS712)
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
#   SICAKLIK (DS18B20)
# ===========================
import glob
def read_temp():
    try:
        device = glob.glob("/sys/bus/w1/devices/28*")[0]
        with open(device + "/w1_slave") as f:
            lines = f.readlines()
        if "YES" in lines[0]:
            temp_str = lines[1].split("t=")[-1]
            return float(temp_str)/1000.0
    except:
        return 0.0
 
# ===========================
# ADXL345 TİTREŞİM
# ===========================
# Senin kullandığın adxl fonksiyonunu buraya koyacağız
def read_vibration():
    # Örnek: ivmelerin toplamını kullan
    import adxl345
    accel = adxl345.ADXL345()
    axes = accel.getAxes(True)
    vib = abs(axes['x']) + abs(axes['y']) + abs(axes['z'])
    return vib
 
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
# ALARM
# ===========================
def alarm_mode():
    print("\n🚨 ALARM MODU AKTİF!")
    motor_stop()
    GPIO.output(LED, GPIO.HIGH)
 
    # Buzzer sireni
    for i in range(40):
        buzzer.play(Tone(400 + (i % 10) * 50))
        time.sleep(0.05)
 
    buzzer.stop()
    time.sleep(2)
    GPIO.output(LED, GPIO.LOW)
    print("Alarm tamamlandı.\n")
 
# ===========================
# EŞİK DEĞERLERİ
# ===========================
TEMP_LIMIT = 50
CURRENT_LIMIT = 2.5
VIB_LIMIT = 2.0
 
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
        sound = GPIO.input(SOUND_PIN)
        vib = read_vibration()
 
        print(f"TEMP={temp:.1f}C  AKIM={current:.2f}A  SES={sound}  TITREŞIM={vib:.2f}")
 
        if temp > TEMP_LIMIT:
            print("⚠ SICAKLIK ALARMI")
            alarm_mode()
            break
 
        if current > CURRENT_LIMIT:
            print("⚠ AŞIRI AKIM ALARMI")
            alarm_mode()
            break
 
        if sound == SOUND_LIMIT:  # Dijital ses sensörü
            print("⚠ SES ALARMI")
            alarm_mode()
            break
 
        if vib > VIB_LIMIT:
            print("⚠ TİTREŞİM ALARMI")
            alarm_mode()
            break
 
        time.sleep(0.2)
 
except KeyboardInterrupt:
    pass
 
finally:
    buzzer.stop()
    GPIO.cleanup()