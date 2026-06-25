import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login():
    response = client.post("/login")
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_chat_unauthorized():
    response = client.post("/chat", json={"question": "test"})
    assert response.status_code == 401