import time
import board
import adafruit_dht
import sqlite3

dbname="sensorsData.db"
sampleFreq = 5
dhtDevice = adafruit_dht.DHT11(board.D16)

def getDHTdata():
    temperature = dhtDevice.temperature
    humidity = dhtDevice.humidity
    return temperature, humidity

def logData(temperature, humidity):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("INSERT INTO DHT_data values(datetime('now'), (?), (?))", (temperature, humidity))
    conn.commit()
    conn.close()

while True:
    try:
        temperature, humidity = getDHTdata()
        logData(temperature, humidity)
    
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
    
    time.sleep(sampleFreq)