from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from main import app, get_session, Task
import pytest

# Use test database
TEST_DB_URL = "sqlite:///test.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})


# Override DB dependency
def get_test_session():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = get_test_session


# Create tables before tests
@pytest.fixture(scope="module", autouse=True)
def create_test_db():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


client = TestClient(app)


# -------------------------------
# TESTS
# -------------------------------

def test_create_task():
    response = client.post(
        "/tasks",
        json={"title": "Test Task", "description": "Test Description"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert "id" in data


def test_get_all_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_get_task_by_id():
    response = client.get("/tasks/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1


def test_update_task_put():
    response = client.put(
        "/tasks/1",
        json={"title": "Updated Task", "description": "Updated Description"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["description"] == "Updated Description"


def test_delete_task():
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted"


def test_get_deleted_task():
    response = client.get("/tasks/1")
    assert response.status_code == 404
