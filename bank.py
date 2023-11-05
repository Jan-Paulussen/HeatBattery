

# This program sets controls the resistor Bank1,2 and 3 from the database.
# The settings of the database is done in different modules depending on the modus
# IMPORTANT!!!: The prgramming of the IO's with phaze-cutting still needs to happen here...


import time # The time library is useful for delays
import RPi.GPIO as GPIO
import mysql.connector

#mydb = mysql.connector.connect(
#        host="localhost",
#        user="root",
#        password="raspberry",
#        database="HeatBatt"
#        )


# Pin definitions
GPIO.setmode(GPIO.BCM)        # Use "GPIO" pin numbering
bank1_pin = 21                  #Pin definition of Bank1
bank2_pin = 12                  #Pin definition of Bank2
bank3_pin = 16                  #Pin definition of Bank3

GPIO.setup(bank1_pin, GPIO.OUT) # Set pin as output
GPIO.setup(bank2_pin, GPIO.OUT) # Set pin as output
GPIO.setup(bank3_pin, GPIO.OUT) # Set pin as output


# Main program

def bank():

        mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password="raspberry",
          database="HeatBatt"
          )

#-----  #Read the Bank1_LIVE_power from the database to set output on/off
        mycursor = mydb.cursor()

#    mycursor.execute("SELECT setting_value FROM settings WHERE setting_name='modus'")
#    myresult = mycursor.fetchone()
#    txt=str(myresult)
#    x=txt.find("manual_GPIO")
#    if x>= 0:

        mycursor.execute("SELECT setting_value FROM settings WHERE setting_name='Bank1_LIVE_power'")
        myresult = mycursor.fetchone()
        txt=str(myresult)
        x=txt.find("1201") #currently the maximum power: program update needed to take the max value from the database instead.
        if x >= 0:
          GPIO.output(bank1_pin, GPIO.HIGH)
        elif x<0:
          GPIO.output(bank1_pin, GPIO.LOW)

        mycursor.execute("SELECT setting_value FROM settings WHERE setting_name='Bank2_LIVE_power'")
        myresult = mycursor.fetchone()
        txt=str(myresult)
        x=txt.find("1202")
        if x >= 0:
          GPIO.output(bank2_pin, GPIO.HIGH)
        elif x<0:
          GPIO.output(bank2_pin, GPIO.LOW)

        mycursor.execute("SELECT setting_value FROM settings WHERE setting_name='Bank3_LIVE_power'")
        myresult = mycursor.fetchone()
        txt=str(myresult)
        x=txt.find("1203")
        if x >= 0:
          GPIO.output(bank3_pin, GPIO.HIGH)
        elif x<0:
          GPIO.output(bank3_pin, GPIO.LOW)


        mydb.commit()
        mydb.close()
