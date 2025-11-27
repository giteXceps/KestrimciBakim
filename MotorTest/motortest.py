import RPi.GPIO as GPIO
import time
 
IN1 = 17      # Pin 11
IN2 = 27      # Pin 13
ENA = 18      # Pin 12 (Yeni ENA pinimiz)
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
 
pwm = GPIO.PWM(ENA, 1000)  # PWM 1kHz
pwm.start(0)
 
def ileri(hiz):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(hiz)
 
def geri(hiz):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pwm.ChangeDutyCycle(hiz)
 
def dur():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)
 
try:
    print("İleri 60% hız...")
    ileri(60)
    time.sleep(3)
 
    print("Duruyor...")
    dur()
    time.sleep(1)
 
    print("Geri 80% hız...")
    geri(80)
    time.sleep(3)
 
    print("Duruyor...")
    dur()
 
except KeyboardInterrupt:
    pass
 
finally:
    pwm.stop()
    GPIO.cleanup()
 