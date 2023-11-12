# Import the dependencies.
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
import numpy as np


#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///Resources/hawaii.sqlite').connect()

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
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
@app.route('/')
def homepage():
    return (
        "<h1 style='text-align: center; font-size: 36px;'>Welcome to the Climate App!</h1>"
        "<h2><a href='/api/v1.0/precipitation' style='color: red;'>Precipitation</a></h2>"
        "<h2><a href='/api/v1.0/stations' style='color: red;'>Stations</a></h2>"
        "<h2><a href='/api/v1.0/tobs' style='color: red;'>Tobs</a></h2>"
        "<h2><p style='color: green;'>Start date query</p></h2>"
        "<h5><p style='color: green;'>example: /api/v1.0/start?start=yyyy-mm-dd</p></h5>"
        "<h2><p style='color: green;'>Start & End date query</p></h2>"
        "<h5><p style='color: green;'>example: /api/v1.0/start_end?start=yyyy-mm-dd&end=yyyy-mm-dd</p></h5>"
    )

# Define routes for precipitation
@app.route('/api/v1.0/precipitation')
def precipitation():
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    most_recent_date = datetime.strptime(most_recent_date.date, '%Y-%m-%d')

    # Calculate one year ago from the most recent date
    one_year_ago = datetime(most_recent_date.year - 1, most_recent_date.month, most_recent_date.day -1)

    # Query to retrieve the last 12 months of precipitation data
    results = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= one_year_ago)\
        .filter(Measurement.date <= most_recent_date)\
        .order_by(Measurement.date).all()
    
    # Create a dictionary from the query results
    precipitation_data ={}
    for date, prcp in results:
        precipitation_data[date]=prcp

    return jsonify(precipitation_data)

# Define routes for stations
@app.route('/api/v1.0/stations')
def stations():
     # Query return a JSON list of stations from the dataset
    stations = session.query(Station.station).all()
    station_list = list(np.ravel(stations))
          
    return jsonify(station_list)

# Define routes for tobs
@app.route('/api/v1.0/tobs')
def tobs():
    # Find the date one year ago from the last data point in the database
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = datetime.strptime(last_date[0], '%Y-%m-%d').date()
    one_year_ago = last_date - timedelta(days=365)
    
    # Query for the most active station's temperature observations for the last year
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= one_year_ago).all()
    
    # Create a dictionary from the query results
    tobs_data = {}
    for date, tobs in results:
        tobs_data[date] = tobs

    return jsonify(tobs_data)
# Define routes for start
@app.route('/api/v1.0/start', methods=['GET'])
def start():
    # Query to retrieve the last 12 months of precipitation data
    start_date = request.args.get('start')

    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        # Query for start
        min_max_dates = session.query(func.min(Measurement.date), func.max(Measurement.date)).first()
        min_date, max_date = min_max_dates

        min_date = datetime.strptime(min_date, '%Y-%m-%d')  # Convert to datetime
        max_date = datetime.strptime(max_date, '%Y-%m-%d')  # Convert to datetime
        
        # make sure input date is within range of the dataset
        if start_date < min_date or start_date > max_date:
            return jsonify({"error": "Provided dates are outside the dataset's date range"}), 400

        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).all()
        
    if not results:
            return jsonify({"error": "No data found for the given start date"}), 404

    # Create a list of dictionaries with temperature data
    temperature_data = []
    for min, avg, max in results:
        temp_dict = {}
        temp_dict["TMIN"] = min
        temp_dict["TAVG"] = avg
        temp_dict["TMAX"] = max
        temperature_data.append(temp_dict)

    return jsonify(temperature_data)

# Define routes for start/end ranges
@app.route('/api/v1.0/start_end', methods=['GET'])
def start_end_date():
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Query for start-end range
        min_max_dates = session.query(func.min(Measurement.date), func.max(Measurement.date)).first()
        min_date, max_date = min_max_dates

        min_date = datetime.strptime(min_date, '%Y-%m-%d')  # Convert to datetime
        max_date = datetime.strptime(max_date, '%Y-%m-%d')  # Convert to datetime
        
        # make sure input date is within range of the dataset
        if start_date < min_date or end_date > max_date:
            return jsonify({"error": "Provided dates are outside the dataset's date range"}), 400

        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)) \
            .filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
        
        if not any(results):
            return jsonify({"error": "No data found for the given date range"}), 404

        temperature_data = []
        for min_temp, avg_temp, max_temp in results:
            temp_dict = {
                "TMIN": min_temp,
                "TAVG": avg_temp,
                "TMAX": max_temp
            }
            temperature_data.append(temp_dict)

        return jsonify(temperature_data)
    
    else:
        return "Please provide both start and end dates."

if __name__ == '__main__':
    app.run(debug=True)