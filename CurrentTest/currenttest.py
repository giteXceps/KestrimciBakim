import RPi.GPIO as GPIO
import spidev
import time
import statistics
 
# -----------------------------
# MOTOR PINLERİ (Senin çalışan koduna göre)
# -----------------------------
IN1 = 17
IN2 = 27
ENA = 18
 
# -----------------------------
# MCP3008 SPI başlat
# -----------------------------
spi = spidev.SpiDev()
spi.open(0, 0)                # CE0
spi.max_speed_hz = 1350000
 
VREF = 3.3
SENSITIVITY = 0.185           # ACS712-05B
ZERO_VOLT_THEORIC = 2.5
 
 
def read_adc(channel=0):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data
 
 
def adc_to_voltage(raw):
    return (raw * VREF) / 1023.0
 
 
def calibrate_zero(samples=80):
    print("\n>>> Motor KAPALIYKEN 0A kalibrasyonu yapılıyor...\n")
    vals = []
    for _ in range(samples):
        raw = read_adc(0)
        vals.append(adc_to_voltage(raw))
        time.sleep(0.01)
    zero = statistics.mean(vals)
    print(f">>> Kalibrasyon tamamlandı: Zero = {zero:.3f} V\n")
    return zero
 
 
def get_current(zero_volt):
    raw = read_adc(0)
    volt = adc_to_voltage(raw)
    current = (volt - zero_volt) / SENSITIVITY
    return current, volt, raw
 
 
# -----------------------------
# MOTOR FONKSİYONLARI
# -----------------------------
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
 
 
def motor_forward():
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
 
 
def motor_backward():
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
 
 
def motor_stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(ENA, GPIO.LOW)
 
 
# -----------------------------
# ANA PROGRAM
# -----------------------------
try:
    motor_stop()  # güvenlik
 
    zero = calibrate_zero()
 
    print(">>> Motor 5 saniye ileri dönüyor...\n")
    motor_forward()
 
    start = time.time()
    while time.time() - start < 5:
        current, volt, raw = get_current(zero)
        print(f"RAW:{raw:4d} | Volt:{volt:5.3f}V | Akım:{current:5.3f} A")
        time.sleep(0.25)
 
    print("\n>>> Motor 5 saniye geri dönüyor...\n")
    motor_backward()
 
    start = time.time()
    while time.time() - start < 5:
        current, volt, raw = get_current(zero)
        print(f"RAW:{raw:4d} | Volt:{volt:5.3f}V | Akım:{current:5.3f} A")
        time.sleep(0.25)
 
    print("\n>>> Motor durduruluyor...")
    motor_stop()
 
except KeyboardInterrupt:
    motor_stop()
 
finally:
    GPIO.cleanup()
    spi.close()
 