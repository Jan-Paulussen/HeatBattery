

# This program controls the afterheating

#import paho.mqtt.client as mqtt # Import the MQTT library
import time # The time library is useful for delays
import RPi.GPIO as GPIO

import mysql.connector

#mydb = mysql.connector.connect(
#        host="localhost",
#        user="root",
#        password="raspberry",
#        database="HeatBatt"
#        )

#Suppress warnings (True for debugging)
GPIO.setwarnings(False)

# Pin definitions

GPIO.setmode(GPIO.BCM)        # Use "GPIO" pin numbering
afterheating_pin = 19         #Pin definition of the afterheating
GPIO.setup(afterheating_pin, GPIO.OUT) # Set afterheating  pin as output
fan_pin = 26                  #Pin definition of the fan (needs to be on when afterheating is on to avoid burning the element!!!
GPIO.setup(fan_pin, GPIO.OUT) # Set fan  pin as output


# Main program

def afterheating():
        mydb = mysql.connector.connect(
         host="localhost",
         user="root",
         password="raspberry",
         database="HeatBatt"
         )



#-----  #Read the AfterHeating from the database to set output on/off
        mycursor = mydb.cursor()
        mycursor.execute("SELECT setting_value FROM settings WHERE setting_name='AfterHeating'")

        myresult = mycursor.fetchone()
        txt=str(myresult)
        #debug print (txt)
        x=txt.find("on")
        # for debug: print (x)
        if x >= 0:
          #debug print ("afterheating on")
          #Here afterheating should be switched on
          GPIO.output(fan_pin, GPIO.HIGH)   #The fan should always be on when activatiing the afterheating
          GPIO.output(afterheating_pin, GPIO.HIGH)

        elif x<0:
          #debugprint ("afterheating off")
          #Here afterheating should be turned off
          GPIO.output(afterheating_pin, GPIO.LOW)
        mydb.commit()
        mydb.close()
