from urllib import response


import pytest
from src.flask_app.app import server
from src.models.predict import predict_api,api_reponse
from src.flask_app import exceptions




input_data = {
    'incorrect_location_value':{
        "trip_distance":'18.90097223225815',
        "pickup_location":'1',
        "dropoff_location":'1',
        "passenger_count":'1',
        "pickup_time":'14:01',
        "pickup_date":'2022-04-19',
        "dropoff_time":'15:01',
        "dropoff_date":'2022-04-19',
    },

    'incorrect_time_value':{
        "trip_distance":'18.90097223225815',
        "pickup_location":'1',
        "dropoff_location":'2',
        "passenger_count":'1',
        "pickup_time":'14:01',
        "pickup_date":'2022-04-19',
        "dropoff_time":'14:01',
        "dropoff_date":'2022-04-19',
    },
    'incorrect_passenger_count_value':{
        "trip_distance":'18.90097223225815',
        "pickup_location":'1',
        "dropoff_location":'2',
        "passenger_count":'0',
        "pickup_time":'14:01',
        "pickup_date":'2022-04-19',
        "dropoff_time":'15:01',
        "dropoff_date":'2022-04-19',
    }

}

@pytest.fixture
def client():
    return server.test_client()


def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200



def test_Location(data = input_data['incorrect_location_value']):
    res = api_reponse(data)
    assert res['response'] == exceptions.SameLocation().message



def test_time(data = input_data['incorrect_time_value']):
    res = api_reponse(data)
    assert res['response'] == exceptions.SameTime().message


def test_passenger(data = input_data['incorrect_passenger_count_value']):
    print(data)
    res = api_reponse(data)
    assert res['response'] == exceptions.PassengerCount().message
