from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_activities_returns_all_activities():
    # Arrange
    # (fixture already reset state)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_adds_participant_and_prevents_duplicates():
    # Arrange
    email = "newstudent@mergington.edu"

    # Act (signup success)
    signup_response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
    )

    # Assert success
    assert signup_response.status_code == 200
    assert email in client.get("/activities").json()["Chess Club"]["participants"]

    # Act (duplicate signup)
    duplicate_response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
    )

    # Assert failure for duplicate
    assert duplicate_response.status_code == 400


def test_unregister_removes_participant_and_errors_when_not_signed_up():
    # Arrange
    email = "michael@mergington.edu"  # already signed up in initial state

    # Act (unregister success)
    unregister_response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email},
    )

    # Assert removal worked
    assert unregister_response.status_code == 200
    assert email not in client.get("/activities").json()["Chess Club"]["participants"]

    # Act (unregister again, should fail)
    second_response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email},
    )

    # Assert error when not signed up
    assert second_response.status_code == 400
