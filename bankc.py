

# This program sets controls the resistor Bank1,2 and 3 from the database.
# The settings of the database is done in different modules depending on the modus
# IMPORTANT!!!: The setting of the I/O is done by the compiled C-program dutycycle(.c) with 3 in line argument: the percentage for the three banks
# e.g. like this: /home/pi/dutycycle 98 30 1


import time # The time library is useful for delays
import RPi.GPIO as GPIO
import mysql.connector
import os #to call external c-program
import re #to extract a number from a string

"""
# Pin definitions
GPIO.setmode(GPIO.BCM)        # Use "GPIO" pin numbering
bank1_pin = 21                  #Pin definition of Bank1
bank2_pin = 12                  #Pin definition of Bank2
bank3_pin = 16                  #Pin definition of Bank3

GPIO.setup(bank1_pin, GPIO.OUT) # Set pin as output
GPIO.setup(bank2_pin, GPIO.OUT) # Set pin as output
GPIO.setup(bank3_pin, GPIO.OUT) # Set pin as output
"""

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


        mycursor.execute("SELECT setting_value FROM settings WHERE setting_name='Bank1_LIVE_power'")
        myresult = mycursor.fetchone()
        txt=str(myresult)
        live = (re.findall(r'\b\d+\b', txt)) #extract only the number

        mycursor.execute("SELECT setting_value FROM settings WHERE setting_name='Bank1_MAX_power'")
        myresult = mycursor.fetchone()
        txt=str(myresult)
        max = (re.findall(r'\b\d+\b', txt)) #extract only the number

        duty1 = int(int(live[0]) / int(max[0]) * 100 )   #Calculate percentage in time (would be better to use the sinus calculated time?)
        cmd_string = "/home/pi/dutycycle " +  str(duty1)



        mycursor.execute("SELECT setting_value FROM settings WHERE setting_name='Bank2_LIVE_power'")
        myresult = mycursor.fetchone()
        txt=str(myresult)
        live = (re.findall(r'\b\d+\b', txt)) #extract only the number

        mycursor.execute("SELECT setting_value FROM settings WHERE setting_name='Bank2_MAX_power'")
        myresult = mycursor.fetchone()
        txt=str(myresult)
        max = (re.findall(r'\b\d+\b', txt)) #extract only the number

        duty2 = int(int(live[0]) / int(max[0]) * 100 )   #Calculate percentage in time (would be better to use the sinus calculated time?)
        cmd_string = cmd_string + " " + str(duty2)



        mycursor.execute("SELECT setting_value FROM settings WHERE setting_name='Bank3_LIVE_power'")
        myresult = mycursor.fetchone()
        txt=str(myresult)
        live = (re.findall(r'\b\d+\b', txt)) #extract only the number

        mycursor.execute("SELECT setting_value FROM settings WHERE setting_name='Bank3_MAX_power'")
        myresult = mycursor.fetchone()
        txt=str(myresult)
        max = (re.findall(r'\b\d+\b', txt)) #extract only the number

        duty3 = int(int(live[0]) / int(max[0]) * 100 )   #Calculate percentage in time (would be better to use the sinus calculated time?)
        cmd_string = cmd_string + " " + str(duty3)




        print (cmd_string)


        mydb.commit()
        mydb.close()

        #os.system ("/home/pi/dutycycle 98 30 1")   #start the C-program with the proper dutycycle (it will run for 1 second)
        os.system (cmd_string)   #start the C-program with the proper dutycycle (it will run for 1 second)

