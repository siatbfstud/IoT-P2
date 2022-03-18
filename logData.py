import time
import board
import adafruit_dht
import sqlite3

from datetime import datetime
import pytz

dbname="sensor.db"
sampleFreq = 10
dhtDevice = adafruit_dht.DHT11(board.D16)

def getDHTdata():
    temperature = dhtDevice.temperature
    humidity = dhtDevice.humidity
    current_time_get = datetime.now(pytz.timezone('Europe/Berlin'))
    current_time = current_time_get.strftime("%Y-%m-%d %H:%M:%S")
    return temperature, humidity, current_time

def logData(temperature, humidity, current_time):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("INSERT INTO DHT_data values((?), (?), (?))", (current_time, temperature, humidity))
    conn.commit()
    conn.close()

while True:
    try:
        temperature, humidity, current_time = getDHTdata()
        logData(temperature, humidity, current_time)
    
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
    
    time.sleep(sampleFreq)