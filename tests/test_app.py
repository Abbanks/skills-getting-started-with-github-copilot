import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert pattern for each test

def test_get_activities():
    # Arrange
    # (No setup needed, uses in-memory data)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "Chess Club" in response.json()


def test_signup_for_activity_success():
    # Arrange
    activity = "Art Studio"
    email = "newstudent@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Confirm participant added
    get_resp = client.get("/activities")
    assert email in get_resp.json()[activity]["participants"]


def test_signup_for_activity_already_registered():
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_for_activity_not_found():
    # Arrange
    activity = "Nonexistent Club"
    email = "student@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_from_activity_success():
    # Arrange
    activity = "Programming Class"
    email = "emma@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity}"
    # Confirm participant removed
    get_resp = client.get("/activities")
    assert email not in get_resp.json()[activity]["participants"]


def test_unregister_from_activity_not_found():
    # Arrange
    activity = "Nonexistent Club"
    email = "student@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_from_activity_participant_not_found():
    # Arrange
    activity = "Art Studio"
    email = "notregistered@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]
