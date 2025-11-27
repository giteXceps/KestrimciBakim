import os
import time
import RPi.GPIO as GPIO
 
# --- GPIO Ayarları ---
LED_PIN = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
 
# --- DS18B20 Ayarları ---
BASE_DIR = "/sys/bus/w1/devices/"
device_folder = None
for name in os.listdir(BASE_DIR):
    if name.startswith("28-"):
        device_folder = os.path.join(BASE_DIR, name)
        break
 
if device_folder is None:
    raise RuntimeError("DS18B20 sensörü bulunamadı!")
 
device_file = os.path.join(device_folder, "w1_slave")
 
def read_temp_raw():
    with open(device_file, "r") as f:
        return f.readlines()
 
def read_temp_c():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != "YES":
        time.sleep(0.2)
        lines = read_temp_raw()
 
    equals_pos = lines[1].find("t=")
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        return float(temp_string) / 1000.0
 
# --- Ana Döngü ---
try:
    while True:
        temp = read_temp_c()
        print(f"Sıcaklık: {temp:.2f} °C")
 
        # ----- ŞART: 50°C üstüyse LED YAK -----
        if temp > 50:
            GPIO.output(LED_PIN, GPIO.HIGH)   # LED Aç
        else:
            GPIO.output(LED_PIN, GPIO.LOW)    # LED Kapa
 
        time.sleep(1)
 
except KeyboardInterrupt:
    print("\nÇıkış yapıldı.")
 
finally:
    GPIO.cleanup()