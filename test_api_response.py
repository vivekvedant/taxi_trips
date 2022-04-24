from src.models.predict import api_reponse
data ={
        "trip_distance":'18.90097223225815',
        "pickup_location":'1',
        "dropoff_location":'1',
        "passenger_count":'1',
        "pickup_time":'14:01',
        "pickup_date":'2022-04-19',
        "dropoff_time":'15:01',
        "dropoff_date":'2022-04-19',
    }

res = api_reponse(data)

print(res['response'])