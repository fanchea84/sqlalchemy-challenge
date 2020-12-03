# ------------------- C L I M A T E   A P P ------------------- #
# --------------------------------------------------------------#
# Import libraries and resources 
# --------------------------------------------------------------#
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_
from flask import Flask, jsonify
# --------------------------------------------------------------#
# Setup Database 
# --------------------------------------------------------------#
engine = create_engine("sqlite:///hawaii.sqlite")
# Declare a Base using  AUTOMAP_BASE()
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)
# Create references to the two tables: MEASUREMENT and STATION
Measurement = Base.classes.measurement
Station = Base.classes.station
# --------------------------------------------------------------#
# Setup Flask 
# --------------------------------------------------------------#
app = Flask(__name__)
# --------------------------------------------------------------#
# Setup Flask Routes
# --------------------------------------------------------------#
# ------- L I S T    A L L    R O U T E S ------- #
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to Hawaii Climate Analysis API :-)<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
    )
# ------- P R E C I P I T A T I O N    R O U T E ------- #
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query dates and precipitation values
    results =   session.query(Measurement.date, Measurement.prcp).\
                order_by(Measurement.date).all()
    # Convert to list of dictionaries, then jsonify
    precip_date_list = []
    for date, prcp in results:
        new_dicty = {}
        new_dicty[date] = prcp
        precip_date_list.append(new_dicty)
    session.close()
    return jsonify(precip_date_list)
# ------- S T A T I O N    R O U T E ------- #
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    stations = {}
    # Query all stations
    results = session.query(Station.station, Station.name).all()
    for s,name in results:
        stations[s] = name
    session.close()
    return jsonify(stations)
# ------- T O B S    R O U T E ------- #
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Find last date in MEASUREMENT table, and calculate date one year prior to that (by subtracting 365 days)
    end_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_year_date = (dt.datetime.strptime(end_date[0],'%Y-%m-%d') \
                    - dt.timedelta(days=365)).strftime('%Y-%m-%d')
    # Query dates & temperatures within that date range, from MEASUREMENT table
    results =   session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= last_year_date).\
                order_by(Measurement.date).all()
    # Convert results to list of dictionaries, then jsonify
    tobs_date_list = []
    for date, tobs in results:
        new_dicty = {}
        new_dicty[date] = tobs
        tobs_date_list.append(new_dicty)
    session.close()
    return jsonify(tobs_date_list)
# ------- S T A R T    R O U T E ------- #
@app.route("/api/v1.0/start")
def temp_range_start(start):
    """Min_Temp, Avg_Temp, and Max_Temp per date starting from a starting date.
    Args:
        start (string): A date string in the format %Y-%m-%d
    Returns:
        Min_Temp, Avg_Temp, and Max_Temp
    """
    # Create our session (link) from Python to the DB
    session = Session(engine)
    start_list = []
    results =   session.query(  Measurement.date,\
                                func.min(Measurement.tobs), \
                                func.avg(Measurement.tobs), \
                                func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start).\
                        group_by(Measurement.date).all()
    for date, min, avg, max in results:
        new_dict = {}
        new_dict["Date"] = date
        new_dict["Min_Temp"] = min
        new_dict["Avg_Temp"] = avg
        new_dict["Max_Temp"] = max
        start_list.append(new_dict)
    session.close()    
    return jsonify(start_list)
# --------------------------------------------------------------#
# Debug
# --------------------------------------------------------------#
if __name__ == '__main__':
    app.run(debug=True)