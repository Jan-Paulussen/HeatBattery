



# The intention is to log every minute the values from the database. DOES NOT WORK YET!!!


import mysql.connector
import time

# Verbinding maken met de bron- en doeldatabases
source_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="raspberry",
        database="HeatBatt"
        )

target_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="raspberry",
        database="Logging"
        )


def log_data():
    # Een SQL-query uitvoeren om gegevens uit de bron-tabel op te halen
    source_cursor = source_conn.cursor()
    source_cursor.execute("SELECT * FROM settings")
    data = source_cursor.fetchall()

    test=""

    for x in data:
     print ( x)
     test = test + x

    # Een SQL-query uitvoeren om de gegevens naar de doel-tabel te loggen
    target_cursor = target_conn.cursor()
    for x in data:
     target_cursor.execute("INSERT INTO Log VALUES (%s, %s, %s)", x)

    # Transactie bevestigen en de cursors sluiten
    target_conn.commit()
    source_cursor.close()
    target_cursor.close()

# Oneindige lus om het loggen van gegevens elke minuut uit te voeren
while True:
    log_data()
    print ("Line written")
    time.sleep(60)  # Wacht 60 seconden





