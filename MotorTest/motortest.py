import RPi.GPIO as GPIO
import time
 
# PIN eşleşmesi
IN1 = 17
IN2 = 27
IN3 = 5
IN4 = 6
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
 
# FULL-STEP ve HALF-STEP dizileri
FULL_STEP = [
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1]
]
 
HALF_STEP = [
    [1,0,0,1],
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1]
]
 
def step_motor(steps, speed=0.001, mode="full"):
    """
    steps : Toplam adım sayısı
    speed : Adımlar arası bekleme süresi (daha düşük = daha hızlı)
    mode  : "full" veya "half"
    """
    seq = FULL_STEP if mode == "full" else HALF_STEP
 
    for _ in range(steps):
        for pattern in seq:
            GPIO.output(IN1, pattern[0])
            GPIO.output(IN2, pattern[1])
            GPIO.output(IN3, pattern[2])
            GPIO.output(IN4, pattern[3])
            time.sleep(speed)
 
def stop_motor():
    GPIO.output(IN1, 0)
    GPIO.output(IN2, 0)
    GPIO.output(IN3, 0)
    GPIO.output(IN4, 0)
 
try:
    print("Hızlı dönüş başlıyor...")
    
    # 1 tam tur ~ 2048 FULL step
    step_motor(steps=2048, speed=0.0008, mode="full")
    
    print("Ters yönde daha hızlı...")
    step_motor(steps=2048, speed=0.0006, mode="full")
    
    print("Yavaş ve güçlü HALF-STEP modu...")
    step_motor(steps=4096, speed=0.0015, mode="half")
 
    stop_motor()
    print("Bitti.")
 
except KeyboardInterrupt:
    stop_motor()
 
finally:
    GPIO.cleanup()