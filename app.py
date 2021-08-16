# Dependencies
import datetime as dt
import numpy as np
import pandas as pd

# Get the dependencies we need for SQLAlchemy, which will help us access our data in the SQLite database.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import the dependencies that we need for Flask.
from flask import Flask, jsonify

# Access the SQLite database.
engine = create_engine("sqlite:///hawaii.sqlite")

# Function to access and query SQLite database file.
Base = automap_base()

# Python Flask function that reflects the tables into SQLAlchemy.
Base.prepare(engine, reflect=True)

# Save references to each table.
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session link from Python to database.
session = Session(engine)

# Set up Flask. All of your routes should go after the app = Flask(__name__) line of code. 
# Otherwise, your code may not run properly.
app = Flask(__name__)

# Notice the __name__ variable in this code. This is a special type of variable in Python. 
# Its value depends on where and how the code is run. 
# For example, if we wanted to import our app.py file into another Python file 
#   named example.py, the variable __name__ would be set to example.

# When we run the script with python app.py, the __name__ variable will be set to __main__. 
# This indicates that we are not using any other file to run this code.

# import app

# print("example __name__ = %s", __name__)

# if __name__ == "__main__":
#     print("example is being run directly.")
# else:
#     print("example is being imported")

# Define welcome route.
@app.route('/')

# Add the precipitation, stations, tobs, and temp routes that we'll need for this module into our return statement.
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API! </br>
    Available Routes: <br/>
    /api/v1.0/precipitation <br/>
    /api/v1.0/stations <br/>
    /api/v1.0/tobs <br/>
    /api/v1.0/temp/start/end <br/>
    ''')
# Define precipitation route.
# http://127.0.0.1:5000/api/v1.0/precipitation
@app.route('/api/v1.0/precipitation')

def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Define stations route.
# http://127.0.0.1:5000/api/v1.0/stations
@app.route('/api/v1.0/stations')

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)

# Define monthly temperature route.
# http://127.0.0.1:5000/api/v1.0/tobs
@app.route('/api/v1.0/tobs')

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    
    temps = list(np.ravel(results))
    
    return jsonify(temps)

# Define statistics route.
# Route: http://127.0.0.1:5000/api/v1.0/start/end would return [null,null,null]
# This code tells us that we have not specified a start and end date for our range. 
# Fix this by entering any date in the dataset as a start and end date. 
# The code will output the minimum, maximum, and average temperatures.

# Specify start and end on the link
# http://127.0.0.1:5000//api/v1.0/temp/2017-06-01/2017-06-30
@app.route('/api/v1.0/temp/<start>')
@app.route('/api/v1.0/temp/<start>/<end>')

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).\
        filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
    
if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)