class TestGetUser:
    def test_get_existing_returns_200(self, client, user_factory):
        user, _ = user_factory()
        response = client.get_user(user["email"])
        assert response.status_code == 200

    def test_get_returns_correct_data(self, client, user_factory):
        user, _ = user_factory()
        response = client.get_user(user["email"])
        data = response.json()
        assert data["name"] == user["name"]
        assert data["email"] == user["email"]
        assert data["age"] == user["age"]
        assert data["notes"] == user["notes"]

    def test_get_nonexistent_returns_404(self, client):
        response = client.get_user("nonexistent@example.com")
        assert response.status_code == 404

    def test_get_error_response_has_error_field(self, client):
        response = client.get_user("nonexistent@example.com")
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert isinstance(data["error"], str)
