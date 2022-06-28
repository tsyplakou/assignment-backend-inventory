from fastapi import FastAPI
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_table_setup():
    pass


def test_items_retrieving_in_storage():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}