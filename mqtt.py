
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

#  "on message" event executes all this on every new message of the MQQT
# - First read and decode the power to and from the grid, from the MQTT message
# - Write these values (as string) into the database


#MessageFunction below is execute every time a message comes in.-----------------------------------------------------------------------------
def messageFunction (client, userdata, message):
        #Decode MQTT message and write it to the database
        global PushPower

        topic = str(message.topic)
        mssge = str(message.payload.decode("utf-8"))
        PowerString = str(message.payload)

        positionstartCONSUME =  ( PowerString.find("svalue5"))
        positionstartFEED =  ( PowerString.find("svalue6"))

        positionendCONSUME = (PowerString.find("svalue6"))
        positionendFEED = (PowerString.find("unit"))

        #debug: print ("Consumption is: ", PowerString[positionstartCONSUME+12:positionendCONSUME-7])
        ConsumptionString= (PowerString[positionstartCONSUME+12:positionendCONSUME-7])
        #debug: print ("Feed is: ", PowerString[positionstartFEED+12:positionendFEED-7])
        FeedString=PowerString[positionstartFEED+12:positionendFEED-7]



        #Write the values to the database------------------------
        mycursor = mydb.cursor()
        #Write Grid Consumption in SQL
        sql = "UPDATE settings SET setting_value = %s WHERE setting_name = %s"
        val = (ConsumptionString, "Grid_Consumption")
        mycursor.execute(sql,val)


        sql = "UPDATE settings SET setting_value = %s WHERE setting_name = %s"
        val = (FeedString, "Grid_Supply")
        mycursor.execute(sql,val)

        mydb.commit()

#Realtime power is currently:
        realpwr = int(FeedString) - int(ConsumptionString)
        #print (realpwr)
# Here start the calculation of the overall percentage (when in auto) that can be used to calculate the individual outputs.
# start reading database of maximum possible power per resistorbank

#-----  #Read the modus first, to see if in auto or not_percentage to do calculations.
        mycursor = mydb.cursor()

        mycursor.execute("SELECT setting_value FROM settings WHERE setting_name='modus'")
        myresult = mycursor.fetchone()
        txt=str(myresult)
        y=txt.find("auto")

        if (y>=0):
          mycursor.execute("SELECT setting_value FROM settings WHERE setting_name='Bank1_MAX_power'")
          myresult = mycursor.fetchone()
          txt=str(myresult)
          bank1_max_power=int(txt[2:6])

          mycursor.execute("SELECT setting_value FROM settings WHERE setting_name='Bank2_MAX_power'")
          myresult = mycursor.fetchone()
          txt=str(myresult)
          bank2_max_power=int(txt[2:6])

          mycursor.execute("SELECT setting_value FROM settings WHERE setting_name='Bank3_MAX_power'")
          myresult = mycursor.fetchone()
          txt=str(myresult)
          bank3_max_power=int(txt[2:6])

          #print (bank1_max_power,bank2_max_power, bank3_max_power)

          #Extract previous percentage from DB to calculate new percentage:
          mycursor.execute("SELECT setting_value FROM settings WHERE setting_name='percentage'")
          myresult = mycursor.fetchone()
          #convert from string to integer
          num = ""
          for c in myresult:
             if c.isdigit():
               num = num + c
          #print (myresult)
          lstprct = num
          #print (lstprct)

          ttlpwr = bank1_max_power + bank2_max_power +  bank3_max_power

          #Calculation of the new percentage to be used!
          ttlprct = (realpwr / ttlpwr)*100 + int(lstprct) #Previous power needs to be added (what was already on before last update): It could also be negative in case of consumption
          #set limits:
          if ttlprct > 100:
               #print ("test", ttlprct)
               ttlprct = 100
          if ttlprct < 0:
               #print ("test", ttlprct)
               ttlprct = 0


          sql = "UPDATE settings SET setting_value = %s WHERE setting_name = %s"
          val = (str(int(ttlprct)), "percentage")
          mycursor.execute(sql,val)

          mydb.commit()




#client MQTT connectie maken met MQTT-brooker/server--------------------
ourClient = mqtt.Client("HeatBattV2_client_mqtt") # Create a MQTT client object
ourClient.connect("192.168.123.8", 1883) # Connect to the test MQTT broker
ourClient.subscribe('domoticz/out/Power') # Subscribe to the topic AC_unit

ourClient.on_message = messageFunction # Attach the messageFunction to subscription
ourClient.loop_start() # Start the MQTT client
