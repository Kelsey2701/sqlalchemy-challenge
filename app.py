# Import the dependencies.
from flask import Flask, jsonify
import datetime as dt
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import numpy as np

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# reflect the tables
measurement = Base.classes.measurement
station = Base.classes.station

# Save references to each table

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date (replace start_date with an actual date)<br/>"
        f"/api/v1.0/start_date/end_date (replace start_date and end_date with actual dates)"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    one_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation_data = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= one_year_date).all()
    precip_dict = {date: prcp for date, prcp in precipitation_data}
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(station.station).all()
    stations_list = list(np.ravel(results))
    return jsonify(stations=stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    most_active_station_id = 'USC00519281'  
    one_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_data = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == most_active_station_id).\
        filter(measurement.date >= one_year_date).all()
    tobs_dict = {date: tobs for date, tobs in tobs_data}
    return jsonify(tobs=tobs_dict)

@app.route("/api/v1.0/<start>")
def start_date(start):
    start_date_results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()
    temperatures = list(np.ravel(start_date_results))
    return jsonify(temperatures=temperatures)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    start_end_date_results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    temperatures = list(np.ravel(start_end_date_results))
    return jsonify(temperatures=temperatures)

if __name__ == "__main__":
    app.run(debug=True)

