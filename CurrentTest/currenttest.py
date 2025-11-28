import spidev
import time
import statistics
 
# SPI başlat
spi = spidev.SpiDev()
spi.open(0, 0)              # bus 0, device 0 (CE0)
spi.max_speed_hz = 1350000
 
VREF = 3.3                  # MCP3008 referans gerilimi
SENSITIVITY = 0.185         # ACS712-05B için 185 mV/A
ZERO_VOLT = 2.5             # 0A'daki teorik merkez voltaj
 
def read_adc(channel=0):
    # 10-bit değer okuyoruz (0-1023)
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data
 
def adc_to_voltage(raw):
    return (raw * VREF) / 1023.0
 
def calibrate_zero(samples=100):
    print("Kalibrasyon: Motor KAPALI, akım yok. Bekleyin...")
    vals = []
    for _ in range(samples):
        raw = read_adc(0)
        vals.append(adc_to_voltage(raw))
        time.sleep(0.01)
    zero = statistics.mean(vals)
    print(f"Kalibrasyon bitti. Zero voltaj = {zero:.3f} V")
    return zero
 
def get_current(zero_volt):
    raw = read_adc(0)
    volt = adc_to_voltage(raw)
    # Voltaj farkını Amper'e çevir
    current = (volt - zero_volt) / SENSITIVITY
    return current, volt, raw
 
try:
    zero_volt = calibrate_zero()
 
    while True:
        current, volt, raw = get_current(zero_volt)
        print(f"RAW: {raw:4d}  Volt: {volt:5.3f} V  Akım: {current:5.3f} A")
        time.sleep(0.5)
 
except KeyboardInterrupt:
    print("Çıkılıyor...")
finally:
    spi.close()
 