import RPi.GPIO as GPIO
import spidev
import time
import statistics
 
### -----------------------------
### 1) MCP3008 SPI başlat
### -----------------------------
spi = spidev.SpiDev()
spi.open(0, 0)                  # CE0
spi.max_speed_hz = 1350000
 
def read_adc(channel=0):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data
 
def adc_to_voltage(raw):
    return (raw * 3.3) / 1023.0
 
 
### -----------------------------
### 2) ACS712 Kalibrasyonu
### -----------------------------
def calibrate_zero(samples=100):
    print("\n>>> 0A kalibrasyonu yapılıyor (motor kapalı)...")
    vals = []
    for _ in range(samples):
        raw = read_adc(0)
        vals.append(adc_to_voltage(raw))
        time.sleep(0.01)
 
    zero = statistics.mean(vals)
    print(f">>> Kalibrasyon tamamlandı: Zero = {zero:.3f} V\n")
    return zero
 
 
### -----------------------------
### 3) Motor ayarları
### -----------------------------
IN1 = 17
IN2 = 27
ENA = 12   # PWM pin
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
 
pwm = GPIO.PWM(ENA, 1000)
pwm.start(0)
 
 
def motor_forward(speed=50):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(speed)
 
 
def motor_stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)
 
 
### -----------------------------
### 4) Akım okuma
### -----------------------------
SENSITIVITY = 0.185   # ACS712-05B
def get_current(zero_volt):
    raw = read_adc(0)
    volt = adc_to_voltage(raw)
    current = (volt - zero_volt) / SENSITIVITY
    return current, volt, raw
 
 
### -----------------------------
### 5) Ana Program
### -----------------------------
try:
    zero = calibrate_zero()
 
    print("Motor 20 saniye çalışacak...\n")
    motor_forward(70)   # %70 hızla çalıştır
 
    start = time.time()
    while time.time() - start < 20:
        current, volt, raw = get_current(zero)
        print(f"RAW:{raw:4d}  Volt:{volt:5.3f}V  Akım:{current:5.3f} A")
        time.sleep(0.2)
 
    motor_stop()
    print("\nMotor durduruldu.")
 
except KeyboardInterrupt:
    motor_stop()
 
finally:
    pwm.stop()
    GPIO.cleanup()
    spi.close()
 