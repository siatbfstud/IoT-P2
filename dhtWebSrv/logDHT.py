import time
import board
import adafruit_dht
import sqlite3

# init db and frequency
dbname="sensorsData.db"
sampleFreq = 5 # time in seconds ==> Sample each 1 min
dhtDevice = adafruit_dht.DHT11(board.D16)

# get dht data or update it
def getDHTdata():	
    temperature = dhtDevice.temperature
    humidity = dhtDevice.humidity
    return temperature, humidity

# log sensor data on database
def logData(temperature, humidity):
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("INSERT INTO DHT_data values(datetime('now'), (?), (?))", (temperature, humidity))
	conn.commit()
	conn.close()

while True:
    temperature, humidity = getDHTdata()
    logData(temperature, humidity)
    print("did it")
    time.sleep(sampleFreq)


