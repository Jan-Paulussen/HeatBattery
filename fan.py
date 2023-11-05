

# This program controls the fan

import time # The time library is useful for delays
import RPi.GPIO as GPIO

import mysql.connector

#Suppress warnings (True for debugging)
GPIO.setwarnings(False)

# Pin definitions
GPIO.setmode(GPIO.BCM)        # Use "GPIO" pin numbering
fan_pin = 26                  #Pin definition of the fan
GPIO.setup(fan_pin, GPIO.OUT) # Set fan  pin as output
afterheating_pin = 19         #Pin definition of the afterheating
GPIO.setup(fan_pin, GPIO.OUT) # Set afterheating  pin as output


# Main program

def fan():
        mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password="raspberry",
          database="HeatBatt"
          )

#-----  #Read the FanStatus from the database to set output on/off
        mycursor = mydb.cursor()
        mycursor.execute("SELECT setting_value FROM settings WHERE setting_name='FanStatus'")

        myresult = mycursor.fetchone()
        txt=str(myresult)
        # for debug: print (txt)
        x=txt.find("on")
        # for debug: print (x)
        if x >= 0:
          # for debug: print ("Fan on")
          #Here fan should be switched on
          GPIO.output(fan_pin, GPIO.HIGH)
        elif x<0:
          # for debug: print ("Fan off")
          #Here fan should be turned off
          GPIO.output(afterheating_pin, GPIO.LOW) #If fan is switched of, the afterheating should also alwys be off to avoid burning the element!
          GPIO.output(fan_pin, GPIO.LOW)
        mydb.commit()
        mydb.close()
