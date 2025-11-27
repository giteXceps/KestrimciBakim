import os
import time
 
BASE_DIR = "/sys/bus/w1/devices/"
 
# 28- ile başlayan klasörü otomatik bul
device_folder = None
for name in os.listdir(BASE_DIR):
    if name.startswith("28-"):
        device_folder = os.path.join(BASE_DIR, name)
        break
 
if device_folder is None:
    raise RuntimeError("DS18B20 sensörü bulunamadı (28- klasörü yok)!")
 
device_file = os.path.join(device_folder, "w1_slave")
 
def read_temp_raw():
    with open(device_file, "r") as f:
        return f.readlines()
 
def read_temp_c():
    lines = read_temp_raw()
    # İlk satırda 'YES' gelene kadar bekle
    while lines[0].strip()[-3:] != "YES":
        time.sleep(0.2)
        lines = read_temp_raw()
 
    # t= değerini bul
    equals_pos = lines[1].find("t=")
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
    else:
        return None
 
if __name__ == "__main__":
    try:
        while True:
            temp = read_temp_c()
            if temp is not None:
                print(f"Sıcaklık: {temp:.2f} °C")
            else:
                print("Sıcaklık okunamadı!")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nÇıkış yapıldı.")