import time
import sqlite3
from w1thermsensor import W1ThermSensor
from datetime import datetime
import pytz

dbname="tempDB.db"
sampleFreq = 10
sensor = W1ThermSensor()

def getTempData():
    temperature = sensor.get_temperature()
    temperature = int(temperature)
    current_time_get = datetime.now(pytz.timezone('Europe/Berlin'))
    current_time = current_time_get.strftime("%Y-%m-%d %H:%M:%S")
    return temperature, current_time

def logData(temperature, current_time):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("INSERT INTO tempData values((?), (?))", (current_time, temperature))
    conn.commit()
    conn.close()

while True:
    try:
        temperature, current_time = getTempData()
        logData(temperature, current_time)
    
    except RuntimeError as error:
        # If error occurs, keep going
        print(error.args[0])
        time.sleep(0.5)
        continue
    
    time.sleep(sampleFreq)