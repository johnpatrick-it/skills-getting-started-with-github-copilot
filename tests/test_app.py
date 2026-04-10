"""Backend tests for the Mergington High School FastAPI application."""

from urllib.parse import quote


class TestGetActivities:
    """Tests for GET /activities."""

    def test_get_activities_returns_activity_list(self, client):
        # Arrange
        expected_activity = "Chess Club"

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert expected_activity in activities
        assert "participants" in activities[expected_activity]
        assert isinstance(activities[expected_activity]["participants"], list)


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup."""

    def test_signup_success_adds_new_participant(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{quote(activity_name)}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"

        verification = client.get("/activities").json()
        assert email in verification[activity_name]["participants"]

    def test_signup_duplicate_returns_400(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{quote(activity_name)}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up"

    def test_signup_unknown_activity_returns_404(self, client):
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{quote(activity_name)}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"


class TestUnregisterParticipant:
    """Tests for DELETE /activities/{activity_name}/participants/{email}."""

    def test_unregister_participant_success(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{quote(activity_name)}/participants/{quote(email)}"
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

        verification = client.get("/activities").json()
        assert email not in verification[activity_name]["participants"]

    def test_unregister_missing_participant_returns_404(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "missing@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{quote(activity_name)}/participants/{quote(email)}"
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Participant not found"

    def test_unregister_unknown_activity_returns_404(self, client):
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{quote(activity_name)}/participants/{quote(email)}"
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
