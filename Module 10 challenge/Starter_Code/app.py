# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///C:\\Users\\ben_j\\Downloads\\Module 10 challenge\\Starter_Code\\Resources\\hawaii.sqlite")

# reflect the tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Index route
@app.route("/")
def home():
     return (
         f"Welcome to Hawaii's climate<br/>"
         f"Routes:<br/>"
         f"/api/v1.0/precipitation<br/>"
         f"/api/v1.0/stations<br/>"
         f"/api/v1.0/tobs<br/>"
         f"Minimum, average, and max temperaturs by date by adding /api/v1.0/ to your browser and inputing the date in a 'yyyy-mm-dd' format<br/>"
         f"Minimum, average, and max temperaturs by date range by adding /api/v1.0/'yyyy-mm-dd'/'yyyy-mm-dd' to your browser"
     )
 

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():

     session = Session(engine)

     """List of all percipitation data from stations"""

     results = session.query(measurement.date, measurement.prcp).all()


     all_percipitation = []
     for date, prcp in results:
         percipitation_dict = {}
         percipitation_dict["date"] = date
         percipitation_dict["prcp"] = prcp    
         all_percipitation.append(percipitation_dict)
         
     return jsonify(all_percipitation)

# Stations route
@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)
    
    """List of stations"""
    
    stations = session.query(measurement.station, Station.name).distinct()
    

    all_stations = []
    for station in stations:
         station_dict = {}
         station_dict["station"] = station
         all_stations.append(station_dict)
    
    return jsonify(all_stations)


# Temperature route
@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)

    """Tempatures listed for station USC00519281"""

    temp_active = session.query(measurement.station, measurement.date, measurement.tobs).\
    filter(measurement.date > '2016-08-23').\
    filter(measurement.date < '2017-08-23').\
    filter(measurement.station == "USC00519281").all()
        
    temp_list = []
    for tobs in temp_active:
         temperatures_dict = {}
         temperatures_dict["tobs"] = tobs
         temp_list.append(temperatures_dict)
    
    return jsonify(temp_list)



@app.route("/api/v1.0/<start>")
def temperature_s(start):

     """List of min_temp, avg_temp, and max_temp by date"""
     
     session = Session(engine)
     

     temp_results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
     filter(measurement.date >= start).all()

     start_temp = []
     for tobs in temp_results:
         start_dict = {}
         start_dict["tobs"] = tobs
         start_temp.append(start_dict)

     return jsonify(start_temp)


def start_end(start_date,end_date):

     """List of min_temp, avg_temp, and max_temp by date"""

     session = Session(engine)


     temp_results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
          filter(measurement.date >= start_date).\
          filter(measurement.date <= end_date).all()
     
     session.close() 
     
     return jsonify(temp_results)

if __name__ == "__main__":
     app.run(debug=True)