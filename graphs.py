import matplotlib.pyplot as plt
import numpy as np
from dateutil import parser
from matplotlib import style
import sqlite3
import matplotlib.dates as mdates


conn = sqlite3.connect('IoT.db')
c = conn.cursor()
style.use('fivethirtyeight')
zoomOutFormat = mdates.DateFormatter('%d/%m-%H:%M')
zoomInFormat = mdates.DateFormatter('%H:%M:%S')
graphCounter = 1

def graph_data(metric):
    global graphCounter
    c.execute('SELECT Timestamp, Value FROM ' + metric)
    data = c.fetchall()
    dates = []
    values = []
    for row in data:
        dates.append(parser.parse(row[0]))
        values.append(row[1])
    plt.subplot(4, 1, graphCounter)
    plt.plot_date(dates,values,'-', linewidth=1.0)
    plt.xlabel('time of day', fontsize=14)
    plt.ylabel(metric, fontsize=8)
    plt.gca().xaxis.set_major_formatter(zoomOutFormat
    )
    plt.gca().xaxis.set_minor_formatter(zoomInFormat)
    datemin = np.datetime64(dates[0], 'D')
    datemax = np.datetime64(dates[-1], 'D') + np.timedelta64(1, 'D')
    plt.xlim(datemin, datemax)
    graphCounter = graphCounter + 1



graph_data('cpu')
graph_data('ram')
graph_data('netDownloadBandwidth')
graph_data('netUploadBandwidth')
plt.suptitle('Laptop Stats')


plt.show()
plt.close()