from datetime import datetime

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import io

from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)

import sqlite3
conn=sqlite3.connect('sensorsData.db', check_same_thread=False)
curs=conn.cursor()

# Retrieve LAST data from database
def getLastData():
	for row in curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1"):
		time = str(row[0])
		temp = row[1]
		hum = row[2]
	#conn.close()
	return time, temp, hum

# Get 'x' samples of historical data
def getHistData (numSamples):
	curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT "+str(numSamples))
	data = curs.fetchall()
	dates = []
	temps = []
	hums = []
	for row in reversed(data):
		dates.append(row[0])
		temps.append(row[1])
		hums.append(row[2])
		temps, hums = testeData(temps, hums)
	return dates, temps, hums

# Test data for cleanning possible "out of range" values
def testeData(temps, hums):
	n = len(temps)
	for i in range(0, n-1):
		if (temps[i] < -10 or temps[i] >50):
			temps[i] = temps[i-2]
		if (hums[i] < 0 or hums[i] >100):
			hums[i] = temps[i-2]
	return temps, hums


# Get Max number of rows (table size)
def maxRowsTable():
	for row in curs.execute("select COUNT(temp) from  DHT_data"):
		maxNumberRows=row[0]
	return maxNumberRows

# Get sample frequency in minutes
def freqSample():
	times, temps, hums = getHistData (2)
	fmt = '%Y-%m-%d %H:%M:%S'
	tstamp0 = datetime.strptime(times[0], fmt)
	tstamp1 = datetime.strptime(times[1], fmt)
	freq = tstamp1-tstamp0
	freq = int(round(freq.total_seconds()/60))
	return (freq)

# define and initialize global variables
global numSamples
numSamples = maxRowsTable()
if (numSamples > 101):
        numSamples = 100

global freqSamples
freqSamples = freqSample()

global rangeTime
rangeTime = 0

global userTemp
userTemp = 0
				
		
# main route 
@app.route("/")
def index():
	time, temp, hum = getLastData()
	templateData = {
	  'time'		: time,
      'temp'		: temp,
      'hum'			: hum
	}
	return render_template('index.html', **templateData)


@app.route('/', methods=['POST'])
def my_form_post():
    global userTemp

    userTemp = int (request.form['userTemp']) #???

    time, temp, hum = getLastData()
    
    templateData = {
    'time'		: time,
    'temp'		: temp,
    'hum'		: hum
    }
    return render_template('index.html', **templateData)
	
	
@app.route('/plot/temp')
# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    # Create figure for plotting
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []

    # Read temperature (Celsius) from DHT11
    time, temp, hum = getLastData()

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(temp)

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('DHT11 Temperature over Time')
    plt.ylabel('Temperature Celsius')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
plt.show()

# def plot_temp():
# 	times, temps, hums = getHistData(numSamples)
# 	ys = temps
# 	fig = Figure()
# 	axis = fig.add_subplot(1, 1, 1)
# 	axis.set_title("Temperature [°C]")
# 	axis.set_xlabel("Samples")
# 	axis.grid(True)
# 	xs = range(numSamples)
# 	axis.plot(xs, ys)
# 	canvas = FigureCanvas(fig)
# 	output = io.BytesIO()
# 	canvas.print_png(output)
# 	response = make_response(output.getvalue())
# 	response.mimetype = 'image/png'
# 	return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False)
