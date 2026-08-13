import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.api.main import app
from src.api.auth import get_current_user

client = TestClient(app)

def override_get_current_user():
    return {"username": "testuser"}

app.dependency_overrides[get_current_user] = override_get_current_user

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@patch("src.api.routes.run_optimization_task")
def test_optimize(mock_task):
    class MockTask:
        id = "12345"
    mock_task.delay.return_value = MockTask()
    
    response = client.post("/optimize", json={"parameters": {"dummy": "data"}})
    assert response.status_code == 200
    assert response.json() == {"message": "Optimization started", "task_id": "12345"}
    mock_task.delay.assert_called_once_with({"dummy": "data"})
