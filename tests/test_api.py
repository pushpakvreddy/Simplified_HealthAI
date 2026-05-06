import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Unified Health AI Platform Backend is running!"}

def test_analyze_endpoint_structure():
    # Test with sample data
    payload = {
        "age": 45,
        "bmi": 28.5,
        "glucose": 110,
        "blood_pressure": 130,
        "cholesterol": 210,
        "heart_rate": 75,
        "insulin": 15,
        "smoking": 0,
        "physical_activity": 1,
        "sleep_hours": 7
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    assert "ml_prediction" in response.json()
    assert "comparison" in response.json()
