from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app


client = TestClient(app)

def test_search_item_endpoint():
    response = client.get("/search-item", params={"name": "Case", "currency": 3})
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)

def test_item_data_endpoint():
    response = client.get("/item-data", params={"name": "Fever Case", "currency": 3})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "name" in data

def test_cors_headers():
    headers = {
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "GET"
    }
    response = client.options("/search-item", headers=headers)
    
    assert response.status_code in [200, 204]
    assert "access-control-allow-origin" in response.headers
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"