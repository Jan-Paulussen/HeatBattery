

# This program sets everything to zero when modus is disabled.
# It does this when the system is in "disabled"-modus
# It does not set the physical outputs themselves.

import time # The time library is useful for delays

import mysql.connector

# Main program
def disabled():

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="raspberry",
        database="HeatBatt"
        )


#-----  #Read the modus first, to see if in auto or manual_percentage to do calculations.
    mycursor = mydb.cursor()

    mycursor.execute("SELECT setting_value FROM settings WHERE setting_name='modus'")
    myresult = mycursor.fetchone()
    txt=str(myresult)
    #print (txt)
    x=txt.find("disabled")

    if (x > 0 ):

#Write results in SQL

        sqlstring = "UPDATE settings SET setting_value = '" + '0' + "' WHERE setting_name = 'percentage'"
        mycursor.execute(sqlstring)

        sqlstring = "UPDATE settings SET setting_value = '" + '0' + "' WHERE setting_name = 'Bank1_LIVE_power'"
        mycursor.execute(sqlstring)

        sqlstring = "UPDATE settings SET setting_value = '" + '0' + "' WHERE setting_name = 'Bank2_LIVE_power'"
        mycursor.execute(sqlstring)

        sqlstring = "UPDATE settings SET setting_value = '" + '0' + "' WHERE setting_name = 'Bank3_LIVE_power'"
        mycursor.execute(sqlstring)


        mydb.commit()
        mydb.close()
