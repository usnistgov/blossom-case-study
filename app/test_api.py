from fastapi.testclient import TestClient

from .api import enroller

client = TestClient(enroller)

def test_read_landing():
    response = client.get("/")
    assert response.status_code == 200
