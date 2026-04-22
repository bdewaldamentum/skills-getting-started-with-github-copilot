import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity():
    # Use a unique email to avoid duplicate error
    response = client.post("/activities/Chess Club/signup?email=tester1@mergington.edu")
    assert response.status_code == 200 or response.status_code == 400
    if response.status_code == 200:
        assert "Signed up" in response.json()["message"]
    else:
        assert response.json()["detail"] == "Student already signed up for this activity"

def test_signup_duplicate():
    # Try to sign up the same email again
    client.post("/activities/Chess Club/signup?email=tester2@mergington.edu")
    response = client.post("/activities/Chess Club/signup?email=tester2@mergington.edu")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_remove_participant():
    # Add, then remove
    client.post("/activities/Programming Class/signup?email=tester3@mergington.edu")
    response = client.delete("/activities/Programming Class/participants/tester3@mergington.edu")
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]

def test_remove_nonexistent_participant():
    response = client.delete("/activities/Programming Class/participants/notfound@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
