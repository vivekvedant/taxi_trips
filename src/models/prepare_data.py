import json
import glob

# import findspark
# findspark.init("C:\Apps\spark-3.0.3-bin-hadoop2.7")
import pyspark
from pyspark.sql import SparkSession
from pyspark.ml.feature import Imputer
from pyspark.sql.functions import isnan, when, count, col,hour,minute,year,month,dayofmonth


def read_data_conf():
    with open("conf/data_conf.json","r") as data:
        data_conf = json.load(data)
    return data_conf



def prepare_data(csv_file_list = None,processed_data_path = None):
    """
    This method preprocess the data for the model

    :param csv_file_list: a list of csv file_names defaults to None
    :type  csv_file_list: list, optional

    :param processed_data_path: path to store procssed data defaults to None
    :type  processed_data_path: string, optional

    :return: Processed Data
    :rtype: pyspark.
    """

    spark = SparkSession.builder \
               .appName('taxi_fare_amount_prediction') \
                .master('spark://vps00:7077')  \
                .config('spark.sql.execution.arrow.pyspark.enabled', True) \
                .config('spark.sql.session.timeZone', 'UTC') \
                .config('spark.driver.memory','6G') \
                .config('spark.ui.showConsoleProgress', True) \
                .config('spark.sql.repl.eagerEval.enabled', True) \
                .getOrCreate()

    #read csv_file in pyspark
    trip_fare_amount_data = spark.read.options(header=True).csv(csv_file_list,inferSchema= True)

    #drop columns
    drop_cols = ['payment_type','extra','mta_tax','tip_amount','tolls_amount',
         'improvement_surcharge','total_amount','congestion_surcharge','ratecodeid','store_and_fwd_flag','vendorid']
    trip_fare_amount_data_v2 = trip_fare_amount_data.drop(*drop_cols)

    #deal with missing_values
    # print())
    if trip_fare_amount_data_v2.select([count(when(col('passenger_count').isNull(),True))]).collect()[0][0] > 0:
        print("Got in")
        imputer = Imputer(inputCols = ['passenger_count'],outputCols = ['passenger_count_imputed']).setStrategy("mean")
        trip_fare_amount_data_v2 = imputer.fit(trip_fare_amount_data_v2).transform(trip_fare_amount_data_v2)

    data_conf = read_data_conf()

    trip_fare_amount_data_v3 = trip_fare_amount_data_v2.filter((trip_fare_amount_data_v2['trip_distance'] > data_conf['Min']['trip_distance']) & (trip_fare_amount_data_v2['fare_amount'] > data_conf["Min"]['fare_amount']))

    trip_fare_amount_data_v4 = trip_fare_amount_data_v3.withColumn("{}_hour".format("tpep_pickup"),hour(col("tpep_pickup_datetime"))) \
        .withColumn("{}_minute".format("tpep_pickup"),minute(col("tpep_pickup_datetime"))) \
        .withColumn("{}_year".format("tpep_pickup"),year(col("tpep_pickup_datetime"))) \
        .withColumn("{}_month".format("tpep_pickup"),month(col("tpep_pickup_datetime"))) \
        .withColumn("{}_date".format("tpep_pickup"),dayofmonth(col("tpep_pickup_datetime")))\
        .withColumn("{}_hour".format("tpep_dropoff"),hour(col("tpep_dropoff_datetime"))) \
        .withColumn("{}_minute".format("tpep_dropoff"),minute(col("tpep_dropoff_datetime"))) \
        .withColumn("{}_year".format("tpep_dropoff"),year(col("tpep_dropoff_datetime"))) \
        .withColumn("{}_month".format("tpep_dropoff"),month(col("tpep_dropoff_datetime"))) \
        .withColumn("{}_date".format("tpep_dropoff"),dayofmonth(col("tpep_dropoff_datetime")))

    drop_cols = ['tpep_pickup_datetime','tpep_dropoff_datetime','passenger_count']
    trip_fare_amount_data_v5 = trip_fare_amount_data_v4.drop(*drop_cols)

    trip_fare_amount_data_v6 = trip_fare_amount_data_v5.filter((trip_fare_amount_data_v5['tpep_pickup_year'] <=data_conf["Max"]['tpep_pickup_year'] ))
    trip_fare_amount_data_v7 = trip_fare_amount_data_v6.filter((trip_fare_amount_data_v6['fare_amount'] >= data_conf["Max"]['fare_amount']))

    print("Exporting dataframe to parquet")
    trip_fare_amount_data_v7.write.parquet(processed_data_path)

