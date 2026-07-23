import pytest


class TestUpdateUser:
    def test_update_returns_200(self, client, user_factory):
        user, _ = user_factory()
        updated = {**user, "name": "Updated Name"}
        response = client.update_user(user["email"], updated)
        assert response.status_code == 200

    def test_update_returns_updated_data(self, client, user_factory):
        user, _ = user_factory()
        updated = {**user, "name": "Updated Name"}
        response = client.update_user(user["email"], updated)
        assert response.json()["name"] == "Updated Name"

    def test_update_persists_changes(self, client, user_factory):
        user, _ = user_factory()
        updated = {**user, "name": "Persisted Name"}
        client.update_user(user["email"], updated)
        response = client.get_user(user["email"])
        assert response.json()["name"] == "Persisted Name"

    def test_update_nonexistent_returns_404(self, client):
        response = client.update_user("nonexistent@example.com", {
            "name": "Test", "email": "nonexistent@example.com", "age": 30
        })
        assert response.status_code == 404

    def test_update_duplicate_email_returns_409(self, client, user_factory):
        user1, _ = user_factory()
        user2, _ = user_factory()
        updated = {**user1, "email": user2["email"]}
        response = client.update_user(user1["email"], updated)
        assert response.status_code == 409

    @pytest.mark.parametrize("age", [0, -1, 151])
    def test_update_invalid_age_returns_400(self, client, user_factory, age):
        user, _ = user_factory()
        updated = {**user, "age": age}
        response = client.update_user(user["email"], updated)
        assert response.status_code == 400

    def test_update_invalid_email_format_returns_400(self, client, user_factory):
        user, _ = user_factory()
        updated = {**user, "email": "not-an-email"}
        response = client.update_user(user["email"], updated)
        assert response.status_code == 400

    def test_update_error_response_has_error_field(self, client):
        response = client.update_user("nonexistent@example.com", {})
        assert "error" in response.json()
