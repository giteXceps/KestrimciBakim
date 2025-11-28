import RPi.GPIO as GPIO
import time
 
BUZZ = 21
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZ, GPIO.OUT)
 
pwm = GPIO.PWM(BUZZ, 1)  # başlangıç frekansı (önemsiz)
pwm.start(0)             # duty %0 = sessiz
 
def beep(freq=1000, duration=0.3):
    pwm.ChangeFrequency(freq)
    pwm.ChangeDutyCycle(50)   # %50 duty → ses
    time.sleep(duration)
    pwm.ChangeDutyCycle(0)    # kapanır
 
try:
    print("3 defa bip sesi veriyor...")
    beep(1000, 0.2)
    time.sleep(0.1)
    beep(1500, 0.2)
    time.sleep(0.1)
    beep(2000, 0.2)
 
finally:
    pwm.stop()
    GPIO.cleanup()