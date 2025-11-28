import RPi.GPIO as GPIO
import time
 
MIC = 24  # OUT bağlı olduğu pin
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(MIC, GPIO.IN)
 
try:
    while True:
        val = GPIO.input(MIC)
        print(val)
        time.sleep(0.1)
 
except KeyboardInterrupt:
    GPIO.cleanup()