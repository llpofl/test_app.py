import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_index_default(client):
    response = client.get("/")
    assert response.status_code == 200  # Изменено с 404 на 200
    assert b"Hello World" in response.data  # Изменено с "Bye" на "Hello World"

def test_index_injection(client):
    response = client.get("/?name=2*21")
    assert b"Hello 2*21" in response.data  # Добавлено "Hello "

def test_fetch_mocked(monkeypatch, client):
    class MockResponse:
        text = "mocked response"  # Изменено значение

    def mock_get(url, verify):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    response = client.get("/fetch?url=http://example.com")
    assert response.status_code == 200  # Изменено с 500 на 200
    assert b"mocked response" in response.data