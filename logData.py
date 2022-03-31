import time
import sqlite3
from w1thermsensor import W1ThermSensor
from datetime import datetime
import pytz

# Global variables used in functions
dbname="tempDB.db"
sleepAmount = 10
sensor = W1ThermSensor()

def getTempData():
    temperature = sensor.get_temperature()                          # Captures sensor temperature
    temperature = int(temperature)                                  # Converts the temperature from float to int
    current_time_get = datetime.now(pytz.timezone('Europe/Berlin')) # Takes current time from CEST timezone
    current_time = current_time_get.strftime("%Y-%m-%d %H:%M:%S")   # Cuts off miliseconds from time
    return temperature, current_time

def logData(temperature, current_time):
    conn=sqlite3.connect(dbname)                                                        # Connects to our database
    curs=conn.cursor()                                                                  # We can edit tables values etc via cursor method
    curs.execute("INSERT INTO tempData values((?), (?))", (current_time, temperature))  # Executes command which inserts two variables into our table
    conn.commit()                                                                       # Commits the changes made
    conn.close()                                                                        # Closes the connection to out database

while True:
    try:
        # Runs the two functions and 
        temperature, current_time = getTempData()
        logData(temperature, current_time)
    
    except RuntimeError as error:
        # If error occurs, keep going after 0.5 seconds
        print(error.args[0])
        time.sleep(0.5)
        continue
    
    time.sleep(sleepAmount)