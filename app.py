from flask import Flask,render_template,url_for,request,redirect, make_response
import json
import RPi.GPIO as GPIO
import sqlite3
from flask import Flask, render_template, make_response

app = Flask(__name__)

# Makes it so we can connect to out database without it checking for threads
conn=sqlite3.connect('tempDB.db', check_same_thread=False)
curs=conn.cursor()

# Class that handles global variables
class var:
    mode = 0
    Temperature = None

# Variables used for handling PWM
PWMcool = 18
PWMpel = 12
PWMvarme = 13
freq = 1000

GPIO.setwarnings(False)     # Makes it so we dont get random warnings constantly
GPIO.setmode(GPIO.BCM)      # Refers to a certain layout of the raspberry pi GPIO layout

# Setup for all three PWM modules as OUTPUT
GPIO.setup(PWMcool,GPIO.OUT)
GPIO.setup(PWMpel,GPIO.OUT)
GPIO.setup(PWMvarme,GPIO.OUT)

# Create PWM instances with frequency
cooler = GPIO.PWM(PWMcool, freq)
peltier = GPIO.PWM(PWMpel, freq)
varme = GPIO.PWM(PWMvarme, freq)


# Retrieve LAST data from database via timestamp
def getLastData():
    for row in curs.execute("SELECT * FROM tempData ORDER BY timestamp DESC LIMIT 1"):
        dataTime = str(row[0])
        dataTemp = row[1]
    return dataTime, dataTemp

# Standard routing that shows the html file
@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')

# Route that when called, starts function that keeps temp about 2 degrees
@app.route('/option1') # 0-2 grader (fisk)
def option1():
    var.mode = 1
    while var.mode == 1:
        if var.Temperature > 2:
            cooler.start(0)
            peltier.start(0)
            cooler.ChangeDutyCycle(100)
            peltier.ChangeDutyCycle(70)
        elif var.Temperature < 0:
            varme.start(0)
            varme.ChangeDutyCycle(70)
        else:
            cooler.stop()
            peltier.stop()

# Same as above, just for 3 - 5 degrees
@app.route('/option2') # 3-5 grader (mælk)
def option2():
    var.mode = 2
    while var.mode == 2:
        if var.Temperature > 5:
            cooler.start(0)
            peltier.start(0)
            cooler.ChangeDutyCycle(100)
            peltier.ChangeDutyCycle(70)
        elif var.Temperature < 3:
            varme.start(0)
            varme.ChangeDutyCycle(70)
        else:
            cooler.stop()
            peltier.stop()
            varme.stop()

# Once again, same as above with varying degrees
@app.route('/option3') # 6-8 grader (grønt)
def option3():
    var.mode = 3
    while var.mode == 3:
        if var.Temperature > 8:
            cooler.start(0)
            peltier.start(0)
            cooler.ChangeDutyCycle(100)
            peltier.ChangeDutyCycle(70)
        elif var.Temperature < 6:
            varme.start(0)
            varme.ChangeDutyCycle(70)
        else:
            cooler.stop()
            peltier.stop()
            varme.stop()

#Route to POST data to website via JSON
@app.route('/data', methods=["GET", "POST"])
def data():
    dataTime, dataTemp = getLastData()

    var.Temperature = dataTemp
    
    data = [dataTime, dataTemp]

    response = make_response(json.dumps(data))

    response.content_type = "application/json"

    return response


if __name__ == "__main__":
    app.run(debug=False, threaded=True)