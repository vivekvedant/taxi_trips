
import time
# import findspark
# findspark.init("C:\Apps\spark-3.0.3-bin-hadoop2.7")
import pyspark
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.regression import DecisionTreeRegressor

import mlflow
from urllib.parse import urlparse

from pyspark.ml.tuning import TrainValidationSplit, ParamGridBuilder

# https://muttdata.ai/blog/2021/02/12/ml-flow.html
def train_model(processed_csv_path = None):
        spark = SparkSession.builder \
               .appName('taxi_fare_amount_prediction') \
                .master('spark://vps00:7077') \
                .config('spark.ui.port', '4050') \
                .config('spark.sql.execution.arrow.pyspark.enabled', True) \
                .config('spark.sql.session.timeZone', 'UTC') \
                .config('spark.driver.memory','6G') \
                .config('spark.ui.showConsoleProgress', True) \
                .config('spark.sql.repl.eagerEval.enabled', True) \
                .getOrCreate()


        #read csv_file in pyspark
        print("===")
        print("read data")
        print("====")
        trip_fare_amount_data = spark.read.options(header=True).csv(processed_csv_path,inferSchema = True)

        print("===")
        print("get input and output column names")
        print("====")
        # print(trip_fare_amount_data.printSchema())
        input_column_name_lambda_fun = lambda col_name: col_name if(col_name !="fare_amount") else None
        input_column_names = input_column_name_lambda_fun(trip_fare_amount_data.columns)

        print("===")
        print("vectorized the data")
        print("====")
        vectorAssembler = VectorAssembler(inputCols = input_column_names, outputCol = "unscaled_features")
        # ['trip_distance','pulocationid','dolocationid','tpep_pickup_hour', \
                # 'tpep_pickup_minute','tpep_pickup_year','tpep_pickup_month','tpep_pickup_date','tpep_dropoff_hour','tpep_dropoff_minute','tpep_dropoff_year',\
                # 'tpep_dropoff_month','tpep_dropoff_date']
        vpp_sdf = vectorAssembler.transform(trip_fare_amount_data)
        # vpp_sdf.show(2, False)
        vpp_sdf_final = vpp_sdf.select(["unscaled_features","fare_amount"])
        # http://host.docker.internal:4040/jobs/
        print("===")
        print("split the data")
        print("====")
        splits = vpp_sdf_final.randomSplit([0.7,0.3])
        train_df = splits[0]
        test_df = splits[1]
        print("===")
        print("train the data")
        print("====")
        mlflow.pyspark.ml.autolog()
        # mlflow.set_tracking_uri("http://localhost:5000")
        mlflow.set_tracking_uri("http://localhost:5000")
        mlflow.set_experiment("Decision_Tree Regression test parameter with TrainValidationSplit")
        with mlflow.start_run(run_name="Decision_Tree Regression  test parameter with TrainValidationSplit") :

                Decision_tree_reg = DecisionTreeRegressor(featuresCol = "unscaled_features",labelCol = "fare_amount")

                grid = ParamGridBuilder()\
                    .addGrid(Decision_tree_reg.maxBins, [27, 32,37])\
                    .addGrid(Decision_tree_reg.maxDepth, [4, 5,10])\
                    .addGrid(Decision_tree_reg.minInstancesPerNode, [1,10,20])\
                    .build()
                evaluator = RegressionEvaluator(
                labelCol="fare_amount", predictionCol="prediction", metricName="rmse")
                cv = TrainValidationSplit(estimator=Decision_tree_reg, estimatorParamMaps=grid, evaluator=evaluator,trainRatio=0.8)

                start_time = time.process_time()
                Decision_tree_reg_model = cv.fit(train_df)
                end_time = time.process_time()
                ### Predictions
                pred_results=Decision_tree_reg_model.transform(test_df)

                r2_evaluator = RegressionEvaluator(
                labelCol="fare_amount", predictionCol="prediction", metricName="r2")
                r2_eval = r2_evaluator.evaluate(pred_results)



                rmse = evaluator.evaluate(pred_results)

                mse_evaluator = RegressionEvaluator(
                labelCol="fare_amount", predictionCol="prediction", metricName="mse")
                mse_eval = mse_evaluator.evaluate(pred_results)


                mae_evaluator = RegressionEvaluator(
                labelCol="fare_amount", predictionCol="prediction", metricName="mae")
                mae_eval = mae_evaluator.evaluate(pred_results)

                decision_Tree_reg = {}
                decision_Tree_reg['rmse'] = rmse
                decision_Tree_reg['mae'] = mae_eval
                decision_Tree_reg['r2'] = r2_eval
                decision_Tree_reg['mse'] = mse_eval

                mlflow.log_param("rmse", rmse)
                mlflow.log_param("mae", mae_eval)
                mlflow.log_param("r2", r2_eval)
                mlflow.log_param("mse", mse_eval)

                print(decision_Tree_reg)
                print("Time taken by model for fitting: {}".format(end_time - start_time))

                mlflow.spark.save_model(Decision_tree_reg_model, "models")
        spark.stop()

                # tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

                #  # Model registry does not work with file store
                # if tracking_url_type_store != "file":

                #         # Register the model
                #         # There are other ways to use the Model Registry, which depends on the use case,
                #         # please refer to the doc for more information:
                #         # https://mlflow.org/docs/latest/model-registry.html#api-workflow
                #         mlflow.spark.log_model(Decision_tree_reg_model, "model", registered_model_name="Decision_tree_regression tunned_model using hyperopt")
                # else:
                #         mlflow.spark.log_model(Decision_tree_reg_model, "model")

if __name__ == '__main__':
        train_model('data/processed/data.csv')