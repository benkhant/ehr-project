from app.services.validation_service import validate_data_quality

def test_invalid_blood_pressure():
    data = {
        "vital_signs": {
            "blood_pressure": "340/180"
        },
        "last_updated": "2024-11-09"
    }

    result = validate_data_quality(data)
    assert any("blood pressure" in issue["issue"].lower() for issue in result["issues_detected"])

def test_missing_last_updated_detected():
    data = {
        "demographics": {
            "name": "John Doe",
            "dob": "1955-03-16",
            "gender": "M"
        },
        "medications": ["Metformin 500mg"],
        "allergies": ["Penicillin"],
        "conditions": ["Type 2 Diabetes"],
        "vital_signs": {
            "blood_pressure": "120/80",
            "heart_rate": 72
        }
    }

    result = validate_data_quality(data)
    assert any(issue["field"] == "last_updated" for issue in result["issues_detected"])