#WARNING!!! Run this file in Python3, NOT in Python2!!!


import paho.mqtt.client as mqtt # Import the MQTT library
import time # The time library is useful for delays
import datetime


import mysql.connector

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="raspberry",
	database="HeatBatt"
	)

SLOWER=0.6 #Damper to slow down the reaction?

HEATRES1_POWER = 1200 #This is the wattage for the first resistorbank (ON/OFF controlled)
HEATRES2_POWER = 1060 #This is the wattage for the 2nd   resistorbank (ON/OFF controlled), it was measured with the banktest program
HEATRESC_POWER = 1200 #This is the wattage for the controlled resistorbank (triac phase controlled)
BatteryPower=HEATRES1_POWER + HEATRES2_POWER + HEATRESC_POWER  #Power in Watts of the battery can take to charge: depending on the heating resistors


HeatRes1_Status = 0   #Can be 0 or 1200W (Depends on HEATRES1_POWER actually)
HeatRes2_Status = 0   #Can be 0 or 1200W (Depends on HEATRES2_POWER actually)
HeatResC_Status = 0   #Can be anything between 0 and 1200W (Depends on HEATRESC_POWER actually)
PushPower = 0

# Our "on message" event executes all this on every new message of the MQQT
# - First read and decode the power to and from the grid, from the MQTT message
# - Write these values (as string) into the database
# - Then check if the chargesystem is in auto or manual mode
#  - If mode in 'auto', then increase or decrease the power going to the HeatBattery depending on power availibility
#  - If in manual, do not change the percentage (it can be done through the webpage index.php)


#MessageFunction below is execute every time a message comes in.-----------------------------------------------------------------------------
def messageFunction (client, userdata, message):
        #Decode MQTT message and write it to the database
        global HeatRes1_Status
        global HeatRes2_Status
        global HeatResC_Status
        global PushPower

        topic = str(message.topic)
        mssge = str(message.payload.decode("utf-8"))
        PowerString = str(message.payload)

        positionstartCONSUME =  ( PowerString.find("svalue5"))
        positionstartFEED =  ( PowerString.find("svalue6"))

        positionendCONSUME = (PowerString.find("svalue6"))
        positionendFEED = (PowerString.find("unit"))

        #print ("Consumption is: ", PowerString[positionstartCONSUME+12:positionendCONSUME-7])
        ConsumptionString= (PowerString[positionstartCONSUME+12:positionendCONSUME-7])
        #print ("Feed is: ", PowerString[positionstartFEED+12:positionendFEED-7])
        FeedString=PowerString[positionstartFEED+12:positionendFEED-7]



        #---------------------------------------------------------------------------------#
        #          FOR SIMULATION ONLY!!!                                                 #
        #ConsumptionString = "0"                                                          #
        #FeedString = "2500"                                                              #
        #FeedSim = int(FeedString) - HeatRes1_Status - HeatRes2_Status - HeatResC_Status  #
        #print ("---", FeedSim)                                                           #
        #FeedString = str(int(FeedSim))                                                   #
        #---------------------------------------------------------------------------------#




        #Write the values to the database------------------------
        mycursor = mydb.cursor()
        #Write Grid Consumption in SQL
        sql = "UPDATE Settings SET Value = %s WHERE Setting = %s"
        val = (ConsumptionString, "Grid_Consumption")
        mycursor.execute(sql,val)


        sql = "UPDATE Settings SET Value = %s WHERE Setting = %s"
        val = (FeedString, "Grid_Supply")
        mycursor.execute(sql,val)

#-----  #Read the modus for charging from the database to check for auto/man ------------------------------------------------------------*
        mycursor.execute("SELECT Value FROM Settings WHERE Setting='modus'")

        myresult = mycursor.fetchone()
        txt=str(myresult)
        #print (txt)
        x=txt.find("auto")
        #print (x)
        if x >= 0:
          print ("Now in automatic, so percentage following Power")


#-----  #Calculate the resistorbanks to be puton or off or precentage
          #From here calculate how the heating battery should charge: This calculations should only be done if modus is in 'auto'
          Feedpower = int(FeedString) - int(ConsumptionString) #This is the Power that is actually coming/going really from/to the grid, in Watt
          # A positive value for Feedpower means it is feeding to the grid. A negative value is consuming from the grid.

          #Push Power is the Gross-power that would be left over if there was no charging at all of the battery. 
          #From that value it is decided how much charging will take place.
          if (Feedpower > 50): #increment if more Power available
           PushPower = PushPower +30
          if (Feedpower > 500):
           PushPower = PushPower +150
          if (Feedpower <=0): #decrement if not enough power available
           PushPower = PushPower -100
          if (Feedpower < -500):
           PushPower = PushPower - 500

          if (PushPower >3600): #Limit the maximum
           PushPower = 3600
          if (PushPower < 0): #Limit the minimum
           PushPower = 0

          print ( " PushPower= ", PushPower, "Feedpower = ", Feedpower) 


          if PushPower >= (HEATRES1_POWER + HEATRES2_POWER + HEATRESC_POWER) : #Bigger than the maximum 3600W
             HeatRes1_Status = HEATRES1_POWER
             HeatRes2_Status = HEATRES2_POWER
             HeatResC_Status = HEATRESC_POWER
             #NOG WEGSCHRIJVEN NAAR DB!!!!!!!!!!!!!!!
             sql = "UPDATE Settings SET Value = %s WHERE Setting = %s"
             val = (str(int(100)), "HeatResistorC") #Set to 100%
             mycursor.execute(sql,val)
             sql = "UPDATE Settings SET Value = %s WHERE Setting = %s"
             val = ("on", "HeatResistor1")
             mycursor.execute(sql,val)
             sql = "UPDATE Settings SET Value = %s WHERE Setting = %s"
             val = ("on", "HeatResistor2")
             mycursor.execute(sql,val)


          if (PushPower < (HEATRES1_POWER + HEATRES2_POWER + HEATRESC_POWER)) and (PushPower > (HEATRES1_POWER + HEATRES2_POWER)): #Between 2400 and 3600W left over of own consumption
             HeatRes1_Status = HEATRES1_POWER
             HeatRes2_Status = HEATRES2_POWER
             HeatResC_Status =int( (PushPower - HEATRES1_POWER - HEATRES2_POWER) * SLOWER)
             #NOG WEGSCHRIJVEN NAAR DB
             sql = "UPDATE Settings SET Value = %s WHERE Setting = %s"
             val = (str(int((HeatResC_Status)/(HEATRES1_POWER/100))), "HeatResistorC") # to go from 1200W to 100%
             mycursor.execute(sql,val)
             sql = "UPDATE Settings SET Value = %s WHERE Setting = %s"
             val = ("on", "HeatResistor1")
             mycursor.execute(sql,val)
             sql = "UPDATE Settings SET Value = %s WHERE Setting = %s"
             val = ("on", "HeatResistor2")
             mycursor.execute(sql,val)

          if (PushPower <= (HEATRES1_POWER + HEATRES2_POWER)) and (PushPower > (HEATRES1_POWER)): #Between 1200 and 2400W left over of own consumption
             HeatRes1_Status = HEATRES1_POWER
             HeatRes2_Status = 0
             HeatResC_Status = int((PushPower - HEATRES1_POWER)* SLOWER)
             #NOG WEGSCHRIJVEN NAAR DB
             sql = "UPDATE Settings SET Value = %s WHERE Setting = %s"
             val = (str(int((HeatResC_Status)/(HEATRESC_POWER/100))), "HeatResistorC") # to go from 1200W to 100%
             mycursor.execute(sql,val)
             sql = "UPDATE Settings SET Value = %s WHERE Setting = %s"
             val = ("on", "HeatResistor1")
             mycursor.execute(sql,val)
             sql = "UPDATE Settings SET Value = %s WHERE Setting = %s"
             val = ("off", "HeatResistor2")
             mycursor.execute(sql,val)

          if (PushPower < HEATRES1_POWER) or (Feedpower == 0): #Lower than 1200W left over of own consumption
             HeatRes1_Status = 0
             HeatRes2_Status = 0
             if (PushPower >=0):
              HeatResC_Status = int(PushPower * SLOWER)
             else:
              HeatResC_Status = 0
             #NOG WEGSCHRIJVEN NAAR DB
             sql = "UPDATE Settings SET Value = %s WHERE Setting = %s"
             val = (str(int((HeatResC_Status)/(HEATRESC_POWER/100))), "HeatResistorC") #to go from 1200W to 100%
             mycursor.execute(sql,val)
             sql = "UPDATE Settings SET Value = %s WHERE Setting = %s"
             val = ("off", "HeatResistor1")
             mycursor.execute(sql,val)
             sql = "UPDATE Settings SET Value = %s WHERE Setting = %s"
             val = ("off", "HeatResistor2")
             mycursor.execute(sql,val)


          print ("R1", HeatRes1_Status, " R2:", HeatRes2_Status, " R3:", HeatResC_Status)
          print (" ")




          #From here existing to be cleaned up??????????
          ChargePercentage = PushPower / BatteryPower * 100
          if ChargePercentage>100:
            ChargePercentage = 100
#          print ("Chargepercentage", ChargePercentage)

          sql = "UPDATE Settings SET Value = %s WHERE Setting = %s"
          val = (str(int(ChargePercentage)), "Percentage")
          mycursor.execute(sql,val)

#        else x<0:
#          print ("now in manual, so percentage not changing")
        mydb.commit()


#client MQTT connectie maken met MQTT-brooker/server--------------------
ourClient = mqtt.Client("Zero_client_mqtt") # Create a MQTT client object
ourClient.connect("192.168.123.8", 1883) # Connect to the test MQTT broker
ourClient.subscribe('domoticz/out/Power') # Subscribe to the topic AC_unit

ourClient.on_message = messageFunction # Attach the messageFunction to subscription
ourClient.loop_start() # Start the MQTT client



# Main program loop
while(1):
        time.sleep(2) # Sleep for a second or 2

	#The 'timed' mode can be programmed here if the battery is not MQTT controlled.

        mydb.commit()
        mycursor2 = mydb.cursor()
        mycursor2.execute("SELECT Value FROM Settings WHERE Setting='modus'")

        myresult2 = mycursor2.fetchone()
        txt=str(myresult2)
        #print (txt)
        if txt.find("timed")>0:
          #print ("Now in 'timed', Power on certain times")
          uur = (datetime.datetime.now())
          print (uur.strftime("%H"))
          if (int(uur.strftime("%H")) == 3 or int(uur.strftime("%H")) == 4):
             print ("het is nu 3h of 4h")

             #NOG WEGSCHRIJVEN NAAR DB
             sql = "UPDATE Settings SET Value = %s WHERE Setting = %s"
             val = ("100", "HeatResistorC") #to go from 1200W to 100%
             mycursor2.execute(sql,val)
             sql = "UPDATE Settings SET Value = %s WHERE Setting = %s"
             val = ("on", "HeatResistor1")
             mycursor2.execute(sql,val)
             sql = "UPDATE Settings SET Value = %s WHERE Setting = %s"
             val = ("on", "HeatResistor2")
             mycursor2.execute(sql,val)


          else:
             print ("Nu geen 3h of 4h")
             #NOG WEGSCHRIJVEN NAAR DB
             sql = "UPDATE Settings SET Value = %s WHERE Setting = %s"
             val = ("0", "HeatResistorC") #to go from 1200W to 100%
             mycursor2.execute(sql,val)
             sql = "UPDATE Settings SET Value = %s WHERE Setting = %s"
             val = ("off", "HeatResistor1")
             mycursor2.execute(sql,val)
             sql = "UPDATE Settings SET Value = %s WHERE Setting = %s"
             val = ("off", "HeatResistor2")
             mycursor2.execute(sql,val)
        mydb.commit()
             

