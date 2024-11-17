from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)


def test_get_users_without_token():
    response = client.get("/api/v1/auth/users/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authorised"}


def test_signup():
    USER_CREDENTIALS = {
        "username": "PyTest",
        "email": "pytest@mail.com",
        "password": "123",
    }
    response = client.post("/api/v1/auth/signup/", json=USER_CREDENTIALS)
    assert response.status_code == 200 or response.status_code == 400


def test_login():
    USER_CREDENTIALS = {
        "email": "pytest@mail.com",
        "password": "123",
    }
    response = client.post("/api/v1/auth/login/", json=USER_CREDENTIALS)
    assert response.status_code == 200


def test_get_users_with_token():
    token = client.cookies.get("authorisation")
    client.cookies.set("authorisation", token)
    response = client.get("/api/v1/auth/users/")
    assert response.status_code == 200
