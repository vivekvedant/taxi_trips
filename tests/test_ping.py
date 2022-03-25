from urllib import response


import pytest
from src.flask_app.app import server


@pytest.fixture
def client():
    return server.test_client()


def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200