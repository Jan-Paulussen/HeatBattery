
#import config #Commun configuration variables (passwords, database names etc...)

import fan
import afterheating
import batterytemperature
import mqtt #once this module is imported, the mqtt message will triger the routine to update the database (no cyclic call needed!) for the percentage
import percentage_to_control #in manual% or in auto, this will take the total percentage and set the live values for the banks, in the DB
import disabled #in 'disabled' modus outputs are set to zero
import bankc #This will take the live power for each bank, and control the GPIO for them (should be replaced with the C0program?)

#Following lines are for the temperature measurement with the Adafruit max31865 amplifier
import board
import digitalio
import adafruit_max31865


#Main loop starts here (mqtt is on event only as defined in the mqtt.py library)
while(1):

 fan.fan()                   #Control the fan

 afterheating.afterheating() #Control the afterheating

 batterytemperature.batterytemperature() #Reads the temperature INSIDE the heat battery.

 percentage_to_control.percentage_to_control() #calculates the output of the banks from the total percentage to the individual powers

 disabled.disabled()                                    #Checks if modus is disabled, and sets outputs al to zero

 bankc.bank()                          #control the status of the GPIO for the banks, depending on the database and callout to the c-program
                                       #Remember the mqtt.py subroutine will run on every received message, this will calculate the new percentage to use when in auto


#still to do: 
#          Program the timed modus (time settings?)
#          Backup!!!!!!
