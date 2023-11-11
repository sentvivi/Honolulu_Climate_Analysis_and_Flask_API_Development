# Honolulu_Climate_Analysis_and_Flask_API_Development

Overview

This project revolves around performing a comprehensive climate analysis and designing a Flask API based on the collected data for Honolulu, Hawaii. Using Python, SQLAlchemy, and Flask, the project involves data exploration, analysis, and the creation of a robust API.

Project Structure

1. Data Files
    * climate_starter.ipynb: Jupyter Notebook file for executing climate analysis and exploration.
    * hawaii.sqlite: Database file containing the climate data.
 
2. Data Retrieval and Analysis:
    * Use the provided climate_starter.ipynb and hawaii.sqlite to perform the climate analysis.
    * Utilize SQLAlchemy ORM queries to interact with the database.
    * Execute Precipitation and Station Analysis:
        * Identify the most recent date in the dataset.
        * Retrieve the previous 12 months of precipitation data.
        * Calculate summary statistics for precipitation data.
        * Analyze stations and their observations to find the most active station.
     
3. Flask API Development:
    * Develop various routes to retrieve climate data:
        * /api/v1.0/precipitation: Retrieve the last 12 months of precipitation data.
        * /api/v1.0/stations: Fetch a JSON list of stations.
        * /api/v1.0/tobs: Query temperature observations of the most-active station for the previous year.
        * /api/v1.0/<start> and /api/v1.0/<start>/<end>: Calculate temperature statistics based on specified date ranges.
        * Use Flask jsonify function to ensure valid JSON response objects.
    
4. Running the Flask App:
    * Launch the Flask application to access the designed routes.