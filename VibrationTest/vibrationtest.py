import smbus2
import time
 
BUS = smbus2.SMBus(1)
ADDRESS = 0x53  # i2cdetect ile gördüğün adres
 
# ADXL345 register
POWER_CTL = 0x2D
DATA_FORMAT = 0x31
DATAX0 = 0x32
 
# Sensörü aç
BUS.write_byte_data(ADDRESS, POWER_CTL, 0x08)     # Ölçüm modu
BUS.write_byte_data(ADDRESS, DATA_FORMAT, 0x08)   # Full resolution
 
def read_axes():
    bytes = BUS.read_i2c_block_data(ADDRESS, DATAX0, 6)
    x = int.from_bytes(bytes[0:2], byteorder='little', signed=True)
    y = int.from_bytes(bytes[2:4], byteorder='little', signed=True)
    z = int.from_bytes(bytes[4:6], byteorder='little', signed=True)
    return x, y, z
 
try:
    while True:
        x, y, z = read_axes()
        print(f"X={x}, Y={y}, Z={z}")
        time.sleep(0.1)
 
except KeyboardInterrupt:
    print("\nÇıkış yapıldı.")
 