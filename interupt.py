

import time
import signal
import sys
import RPi.GPIO as GPIO

NULL_GPIO = 20
delay = 100
rust = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(NULL_GPIO, GPIO.IN) #, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.OUT) #Blue led


def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def null_callback(channel):
    GPIO.output (19, 0)
    time.sleep(rust)
    GPIO.output (19, 1)

GPIO.add_event_detect(NULL_GPIO, GPIO.RISING, callback=null_callback, bouncetime = 4)




#signal.signal(signal.SIGINT, signal_handler) #To cleanup after a CTRL-C


try:
  while True:
    if delay < 1000:
      delay = delay + 100
    else:
      delay = 100
    #print ("delay=", delay)

    print("Waiting...")
    #rust = delay/100000
    rust =0.0045

    #print ("rust", rust)
    time.sleep(0.5)
except KeyboardInterrupt:
   GPIO.cleanup()
