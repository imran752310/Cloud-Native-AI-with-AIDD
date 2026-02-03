from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello world"
    }

def test_create_user():
    payload = {
        "name": "Alice",
        "email": "alice@test.com",
        "age": 22
    }

    response = client.post("/users", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Alice"
    assert data["email"] == "alice@test.com"