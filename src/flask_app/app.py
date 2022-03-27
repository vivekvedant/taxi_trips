from flask import Flask, render_template,request
import os
import pickle
# import pandas as pd
import json

template_dir =  os.path.join(os.path.dirname(os.path.abspath(__file__)),"templates")

static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"static")


server = Flask(__name__,static_folder = static_dir,template_folder = template_dir)


@server.route("/",methods = ['GET'])
def index():
    # get the location zone name
    # json_file_loc = os.path.join("conf","location_id.json")

    with open("conf/location_id.json", "r") as outfile:
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



