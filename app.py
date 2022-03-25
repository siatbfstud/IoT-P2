from flask import Flask,render_template,url_for,request,redirect, make_response
import json
import RPi.GPIO as GPIO

from flask import Flask, render_template, make_response
app = Flask(__name__)

import sqlite3
conn=sqlite3.connect('tempDB.db', check_same_thread=False)
curs=conn.cursor()

class var:
    mode = 0
    Temperature = None

PWMcool = 18
PWMpel = 12
PWMvarme = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(PWMcool,GPIO.OUT)
GPIO.setup(PWMpel,GPIO.OUT)
GPIO.setup(PWMvarme,GPIO.OUT)
GPIO.setwarnings(False)
cooler = GPIO.PWM(PWMcool,1000)		#create PWM instance with frequency
peltier = GPIO.PWM(PWMpel, 1000)    #create PWM instance with frequency
varme = GPIO.PWM(PWMvarme, 1000)    #create PWM instance with frequency


# Retrieve LAST data from database
def getLastData():
    for row in curs.execute("SELECT * FROM tempData ORDER BY timestamp DESC LIMIT 1"):
        dataTime = str(row[0])
        dataTemp = row[1]
    return dataTime, dataTemp

@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')

@app.route('/option1') # 0-2 grader (fisk)/Test
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



@app.route('/data', methods=["GET", "POST"])
def data():
    dataTime, dataTemp = getLastData()

    var.Temperature = dataTemp
    
    data = [dataTime, dataTemp]

    response = make_response(json.dumps(data))

    response.content_type = "application/json"

    return response


if __name__ == "__main__":
    app.run(debug=True,
    threaded=True
    )