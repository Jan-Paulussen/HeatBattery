

# This program calculates from the percentage of  controls the resistor Bank1,2 and 3 and write it to the database.
# It does this when the system is in "manual_percentage"-modus or when in 'auto' modus
# It does not set the physical outputs themselves.

import time # The time library is useful for delays

import mysql.connector

# Main program

def percentage_to_control():

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="raspberry",
        database="HeatBatt"
        )

    percentage = 0

#-----  #Read the modus first, to see if in auto or manual_percentage to do calculations.
    mycursor = mydb.cursor()

    mycursor.execute("SELECT setting_value FROM settings WHERE setting_name='modus'")
    myresult = mycursor.fetchone()
    txt=str(myresult)
    #print (txt)
    x=txt.find("manual_percentage")
    y=txt.find("auto")
    #print (x, y)

#-----  #Read the currentpercentage to do calculations.

    if ((x> 0) or (y>0)):
        mycursor.execute("SELECT setting_value FROM settings WHERE setting_name='percentage'")
        myresult = mycursor.fetchone()
        txt=str(myresult)
        #print (txt)
        #print (len(txt))
        if len(txt) == 7:
         percentage=int(txt[2:4]) #two figures
        if len(txt) == 6:
         percentage=int(txt[2:3]) #1 figure e.g. below 10%
        if len(txt) == 8:
         percentage=int(txt[2:5]) #3 fugures, like 100%
        #print (percentage)


# Here start reading database of maximum possible power per resistorbank

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

#Here start the calculations from total power percentage, to individual values per bank
        ttl_pwr = bank1_max_power + bank2_max_power + bank3_max_power
        req_pwr = ttl_pwr * (percentage / 100)

        if (req_pwr > bank3_max_power):
          bank3_live_pwr = bank3_max_power
          req_pwr = req_pwr - bank3_max_power
        else:
           bank3_live_pwr = str(int(req_pwr))
           bank2_live_pwr = '0'
           bank1_live_pwr = '0'
           req_pwr = 0

        #print ((ttl_pwr * (percentage / 100)),"--- ", bank3_live_pwr, bank2_live_pwr, bank1_live_pwr)
        #print (bank2_max_power)

        if (req_pwr > bank2_max_power):
           bank2_live_pwr = bank2_max_power
           req_pwr = req_pwr - bank2_max_power
        else:
           bank2_live_pwr = str(int(req_pwr))
           req_pwr = 0

        #print ((ttl_pwr * (percentage / 100)),"--- ", bank3_live_pwr, bank2_live_pwr, bank1_live_pwr)


        if (req_pwr >= bank1_max_power):
           bank1_live_pwr = bank1_max_power
          #req_pwr = req_pwr - bank1_max_power
        else:
           bank1_live_pwr = str(int(req_pwr))


        #print (int(ttl_pwr * (percentage / 100)),"--- ", bank3_live_pwr, bank2_live_pwr, bank1_live_pwr)

#Hier moet values nog weggeschreven worden naar de database!!!

#Write results in SQL

        sqlstring = "UPDATE settings SET setting_value = '" + str(bank1_live_pwr) + "' WHERE setting_name = 'Bank1_LIVE_power'"
        #print (sqlstring)
        mycursor.execute(sqlstring)

        sqlstring = "UPDATE settings SET setting_value = '" + str(bank2_live_pwr) + "' WHERE setting_name = 'Bank2_LIVE_power'"
        #print (sqlstring)
        mycursor.execute(sqlstring)

        sqlstring = "UPDATE settings SET setting_value = '" + str(bank3_live_pwr) + "' WHERE setting_name = 'Bank3_LIVE_power'"
        #print (sqlstring)
        mycursor.execute(sqlstring)


        mydb.commit()
        mydb.close()
