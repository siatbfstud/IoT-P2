from flask import Flask,render_template,url_for,request,redirect, make_response
import json

from time import time

from flask import Flask, render_template, make_response
app = Flask(__name__)

import sqlite3
conn=sqlite3.connect('tempDB.db', check_same_thread=False)
curs=conn.cursor()

# Retrieve LAST data from database
def getLastData():
    for row in curs.execute("SELECT * FROM tempData ORDER BY timestamp DESC LIMIT 1"):
        dataTime = str(row[0])
        dataTemp = row[1]
    #conn.close()
    return dataTime, dataTemp

@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')

@app.route('/option1') # 0-2 grader (fisk)
def option1():
    print ("Setting prefered temperature to 0-2 degrees")
    return ("nothing")

@app.route('/option2') # 3-5 grader (mælk)
def option2():
    print ("Setting prefered temperature to 3-5 degrees")   
    return ("nothing")

@app.route('/option3') # 6-8 grader (grønt)
def optionp3():
    print ("Setting prefered temperature to 6-8 degrees")
    return ("nothing")



@app.route('/data', methods=["GET", "POST"])
def data():
    # Data Format
    # [TIME, Temperature]
    dataTime, dataTemp = getLastData()


    Temperature = dataTemp
    Time = dataTime

    data = [time() * 1000, Temperature]

    response = make_response(json.dumps(data))

    response.content_type = "application/json"

    return response


if __name__ == "__main__":
    app.run(debug=True,
    threaded=True
    )