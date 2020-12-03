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
# Flask Routes
# --------------------------------------------------------------#
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to Hawaii Climate Analysis API :-)<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end<br/>"
        # f"/api/v1.0/<start><br/>"
        # f"/api/v1.0/<start>/<end>"
    )

# ------- P R E C I P I T A T I O N    R O U T E ------- #
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query for the dates and precipitation values
    results =   session.query(Measurement.date, Measurement.prcp).\
                order_by(Measurement.date).all()
    # Convert to list of dictionaries to jsonify
    precip_date_list = []
    for date, prcp in results:
        new_dict = {}
        new_dict[date] = prcp
        precip_date_list.append(new_dict)
    session.close()
    return jsonify(precip_date_list)

# # ------- S T A T I O N    R O U T E ------- #
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



if __name__ == '__main__':
    app.run(debug=True)
