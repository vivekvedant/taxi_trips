from flask import Flask, render_template,request
import os
import pickle
# import pandas as pd
import json
from prometheus_flask_exporter import PrometheusMetrics
import logging
from src.models.predict import predict_api, get_distance,get_location_by_id

template_dir =  os.path.join(os.path.dirname(os.path.abspath(__file__)),"templates")

static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"static")


server = Flask(__name__,static_folder = static_dir,template_folder = template_dir)

metrics  = PrometheusMetrics(server)


logging.basicConfig(level=logging.INFO)
logging.info("Setting LOGLEVEL to INFO")


metrics.info("app_info", "App Info, this can be anything you want", version="1.0.0")

@server.route("/",methods = ['GET'])
def index():
    with open("/taxi_trips/src/flask_app/conf/location_id.json", "r") as outfile:
        zone_info =  json.load(outfile)
    return render_template("index.html",zone_list=zone_info)


@server.route('/predict',methods = ['POST'])
def predict():
     pickup_location = request.form['pickup_location']
     dropoff_location  = request.form['dropoff_location']
     passenger_count = request.form['passenger_count']
     pickup_time = request.form['pickup_time']
     pickup_date = request.form['pickup_date']
     dropoff_time = request.form['dropoff_time']
     dropoff_date = request.form['dropoff_date']
     error = {}

     if pickup_location == dropoff_location:
        error['Location'] = "Pickup and dropoff location is same"

     if pickup_time == dropoff_time:
        error['Time'] = "Pickup and dropoff time is same"

     if int(passenger_count) <=0:
        error['PassengerCount'] = "Passenger Count should be greater than 0"

     if any(error):
          with open("/taxi_trips/src/flask_app/conf/location_id.json", "r") as outfile:
            zone_info =  json.load(outfile)
          return render_template("index.html",zone_list=zone_info,errors = error)
     else:
         pickup_location_name = get_location_by_id(pickup_location)
         drop_off_location_name  = get_location_by_id(dropoff_location)

         trip_distance  = get_distance(pickup_location_name,drop_off_location_name)
         predict_value = predict_api(trip_distance.miles,pickup_location,dropoff_location,passenger_count,pickup_time,
         pickup_date,dropoff_time,dropoff_date)
         return render_template('predict.html',predict_value=predict_value)