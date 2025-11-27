import RPi.GPIO as GPIO
import time
 
IN1 = 17
IN2 = 27
ENA = 18
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
 
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
 
print("Motor tam hız ileri (ENA HIGH)")
GPIO.output(ENA, GPIO.HIGH)
GPIO.output(IN1, GPIO.HIGH)
GPIO.output(IN2, GPIO.LOW)
time.sleep(3)
 
print("Motor tam hız geri (ENA HIGH)")
GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.HIGH)
time.sleep(3)
 
print("Duruyor")
GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)
GPIO.output(ENA, GPIO.LOW)
 
GPIO.cleanup()