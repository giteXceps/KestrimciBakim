import RPi.GPIO as GPIO
import time
 
# Yeni pin eşlemesi
IN1 = 17     # Pin 11
IN2 = 27     # Pin 13
IN3 = 5      # Pin 29
IN4 = 6      # Pin 31
 
SEQUENCE = [
    [1,0,0,1],
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1]
]
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
 
def step():
    for step in SEQUENCE:
        GPIO.output(IN1, step[0])
        GPIO.output(IN2, step[1])
        GPIO.output(IN3, step[2])
        GPIO.output(IN4, step[3])
        time.sleep(0.002)
 
try:
    print("Motor dönüyor (ileri)...")
    for i in range(512):
        step()
 
    print("Bitti.")
 
except KeyboardInterrupt:
    pass
 
finally:
    GPIO.cleanup()