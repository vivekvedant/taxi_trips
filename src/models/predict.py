# import findspark
# findspark.init("C:\Apps\spark-3.0.3-bin-hadoop2.7")
import pyspark
from pyspark.sql import SparkSession
from pyspark.ml.regression import RandomForestRegressionModel
from pyspark.ml.feature import VectorAssembler
import json
from geopy.geocoders import Nominatim
from geopy import distance
from src.flask_app.exceptions import SameLocation,SameTime,PassengerCount
from subprocess import check_output
import socket
from pyspark.conf import SparkConf
import os
# from pathlib import Path
# def split_time(time):
#     hour, minutes = time.split(":")
#     return (hour,minutes)

# def split_date(date):
#     year,month,day = date.split("-")
#     return (year,month,day)


def get_location_by_id(location_id):
    with open("conf/location_id.json", "r") as outfile:
        zone_info =  json.load(outfile)
    for location_name, json_location_id in zone_info.items():
        if location_id == json_location_id:
            return location_name.split("/")[0]


def get_distance(pickup_location,dropoff_location):
    geolocator = Nominatim(user_agent="distance calculator")
    pickup_location_details = geolocator.geocode(pickup_location)
    dropoff_location_details = geolocator.geocode(dropoff_location)
    return distance.distance((pickup_location_details.latitude, pickup_location_details.longitude),(dropoff_location_details.latitude, dropoff_location_details.longitude))

def predict_api(trip_distance,pickup_location,dropoff_location,pasenger_count,pickup_time,
    pickup_date,dropoff_time,dropoff_date):

    pickup_hour,pickup_minute = pickup_time.split(":")
    drop_off_hour,dropoff_minute = dropoff_time.split(":")

    pickup_year,pickup_month,pickup_day = pickup_date.split("-")
    dropoff_year,dropoff_month,dropoff_day = dropoff_date.split("-")

    if pickup_location == dropoff_location:
         raise SameLocation

    if pickup_time == dropoff_time:
         raise SameTime

    if int(pasenger_count) <=0:
        raise PassengerCount

    data_dict = [{
        'trip_distance':float(trip_distance),
        'pulocationid': int(pickup_location),
        'dolocationid': int(dropoff_location),
        'passenger_count_imputed': int(pasenger_count),
        'tpep_pickup_hour': int(pickup_hour),
        'tpep_pickup_minute': int(pickup_minute),
        'tpep_pickup_year':int(pickup_year),
        'tpep_pickup_month':int(pickup_month),
        'tpep_pickup_date':int(pickup_day),
        'tpep_dropoff_hour':int(drop_off_hour),
        'tpep_drop_off_minute': int(dropoff_minute),
        'tpep_drop_off_year': int(dropoff_year),
        'tpep_drop_off_month': int(dropoff_month),
        'tpep_drop_off__date':int(dropoff_day),

    }]


    hostname=socket.gethostname()
    spark_conf = SparkConf()
    spark_conf.setAll([('spark.master', 'spark://spark:7077'),
    ('spark.app.name', 'taxi_fare_amount_prediction'),
    ('spark.submit.deployMode', 'client'),
    ('spark.ui.showConsoleProgress', 'true'),
    ("spark.local.ip",hostname),('spark.driver.host', hostname)]
    )
    spark= SparkSession.builder.config(conf=spark_conf).getOrCreate()

    # config = pyspark.SparkConf().setAll([('spark.ui.port', '4050')])
    # spark = SparkSession.builder\
    #         .master("local[*]")\
    #         .appName("Colab")\
    #         .config(conf = config)\
    #         .getOrCreate()

    spark_dataframe = spark.createDataFrame(data=data_dict)
    vectorAssembler = VectorAssembler(inputCols = spark_dataframe.columns, outputCol = "features")
    vpp_sdf = vectorAssembler.transform(spark_dataframe)
    selected_feauture = vpp_sdf.select("features")
    # model_path = "hdfs:///taxi_trips/src/flask_app/models/randomForest/"
    # model_path = os.path.abspath('/work/trained_models/randomForest/')
    # print("=====================================")
    # print(model_path)
    # print("=====================================")
    model = RandomForestRegressionModel.load("/taxi_trips/src/flask_app/trained_models/randomForest/")
    prediction = model.transform(selected_feauture)
    return prediction.select("prediction").toJSON().map(lambda j: json.loads(j)).collect()




def api_reponse(dict_request):
    try:
        response = predict_api(dict_request['trip_distance'],dict_request['pickup_location'],dict_request['dropoff_location'],dict_request['passenger_count']
        ,dict_request['pickup_time'],dict_request['pickup_date'],dict_request['dropoff_time'],dict_request['dropoff_date'])
        response = {"response": response}
        # print(response)
        return response
    except Exception as e:
        response = {"response": str(e)}
        return response
