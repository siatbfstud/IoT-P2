from flask import Flask,render_template,url_for,request,redirect, make_response
import json

from time import time

from flask import Flask, render_template, make_response
app = Flask(__name__)

import sqlite3
conn=sqlite3.connect('sensor.db', check_same_thread=False)
curs=conn.cursor()

# Retrieve LAST data from database
def getLastData():
    for row in curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1"):
        dataTime = str(row[0])
        dataTemp = row[1]
        dataHum = row[2]
    #conn.close()
    return dataTime, dataTemp, dataHum

@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')


@app.route('/data', methods=["GET", "POST"])
def data():
    # Data Format
    # [TIME, Temperature, Humidity]
    dataTime, dataTemp, dataHum = getLastData()


    Temperature = dataTemp
    Humidity = dataHum
    print(dataTime)

    data = [time() * 1000, Temperature, Humidity]

    response = make_response(json.dumps(data))

    response.content_type = 'application/json'

    return response

# =====================================TEST====================================== #
@app.route("/data2.json")
def data2():
    connection = sqlite3.connect("sensor.db")
    cursor = connection.cursor()
    cursor.execute("SELECT 1000*timestamp, temp from DHT_data")
    results = cursor.fetchall()
    print (results)
    return json.dumps(results)

@app.route("/graph")
def graph():
    return render_template('graph.html')

if __name__ == "__main__":
    app.run(debug=True,
    threaded=True,
    host='0.0.0.0'
    )