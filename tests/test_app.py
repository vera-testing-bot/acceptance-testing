import pytest
from src.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_status_1_returns_200(client):
    response = client.get("/status/1")
    assert response.status_code == 200


def test_status_1_returns_json(client):
    response = client.get("/status/1")
    assert response.content_type == "application/json"


def test_status_1_returns_correct_body(client):
    response = client.get("/status/1")
    data = response.get_json()
    assert data == {"round": 1, "status": "ok"}
