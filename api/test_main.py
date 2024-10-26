from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == '"Hello World!"'

def test_register_auth():
    response = client.post("/auth/register", data={"email": "test@techmed.stasiak", "password": "password"})
    assert response.status_code == 200
    assert response.headers["set-cookie"]
