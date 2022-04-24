import sys, os
from pyspark.conf import SparkConf
from pyspark.sql import SparkSession, Catalog
from pyspark.sql import DataFrame, DataFrameStatFunctions, DataFrameNaFunctions
from pyspark.sql import functions as F
from pyspark.sql import types as T
from pyspark.sql.types import Row

spark_conf = SparkConf()
import socket
hostname=socket.gethostname()
spark_conf.setAll([('spark.master', 'spark://spark:7077'),
('spark.app.name', 'testApp_3'),
('spark.submit.deployMode', 'client'),
('spark.ui.showConsoleProgress', 'true'),
("spark.local.ip",hostname),('spark.driver.host', hostname)])
spark_sess= SparkSession.builder.config(conf=spark_conf).getOrCreate()
#

myDF  = spark_sess.createDataFrame([Row(col0=0, col1=1, col2=2)])

myGDF = myDF.select('*').groupBy('col1')
myDF.createOrReplaceTempView('mydf_as_sqltable')
print(myDF.collect())
myGDF.sum().show()
#
spark_sess.stop(); quit()


# spark_ctxt          = spark_sess.sparkContext
# spark_reader        = spark_sess.read
# spark_streamReader  = spark_sess.readStream
# spark_ctxt.setLogLevel("WARN")