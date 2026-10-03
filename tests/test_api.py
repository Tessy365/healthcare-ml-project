from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Verify that the API root health check returns status 200 and operational message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "online",
        "message": "Healthcare ML API is operational"
    }

def test_predict_endpoint_success():
    """Verify that valid patient data returns a prediction and confidence score."""
    payload = {
        "Age": 56,
        "Gender": "Male",
        "Blood_Type": "AB+",
        "Medical_Condition": "Cancer",
        "Admission_Type": "Urgent",
        "Medication": "Aspirin",
        "Insurance_Provider": "Medicare",
        "Billing_Amount": 70000.0
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "predicted_test_result" in data
    assert "confidence_score" in data
    assert isinstance(data["confidence_score"], float)

def test_predict_endpoint_invalid_data():
    """Verify that malformed or missing payload fields return a 422 validation error."""
    invalid_payload = {
        "Age": "invalid_string_age"
    }
    response = client.post("/predict", json=invalid_payload)
    assert response.status_code == 422