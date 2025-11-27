import RPi.GPIO as GPIO
import time
 
HALL = 23
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(HALL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
 
try:
    while True:
        print(GPIO.input(HALL))
        time.sleep(0.1)
 
except KeyboardInterrupt:
    GPIO.cleanup()