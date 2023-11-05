

# This program reads the temperature inside the Heat Battery (optional Pt100)

import board
import digitalio
import adafruit_max31865


spi = board.SPI()
cs = digitalio.DigitalInOut(board.D5)  # Chip select of the MAX31865 board.
sensor = adafruit_max31865.MAX31865(spi, cs)

##import time # The time library is useful for delays
##import RPi.GPIO as GPIO

import mysql.connector


# Main program

def  batterytemperature():

 mydb = mysql.connector.connect(
         host="localhost",
         user="root",
         password="raspberry",
         database="HeatBatt"
         )
 mycursor = mydb.cursor()


 #Read the temperature from the Pt100
# spi = board.SPI()
# cs = digitalio.DigitalInOut(board.D5)  # Chip select of the MAX31865 board.
# sensor = adafruit_max31865.MAX31865(spi, cs)
 # Read temperature.
 temp = sensor.temperature
 # Print the value.
 #print("Temperature: {0:0.3f}C".format(temp))
 temperaturestring=str("{0:0.3f}".format(temp))


 #Write results in SQL

 sqlstring = "UPDATE settings SET setting_value = '" + temperaturestring + "' WHERE setting_name = 'Battery_temperature'"
 #print (sqlstring)
 mycursor.execute(sqlstring)

 mydb.commit()
 mydb.close()
