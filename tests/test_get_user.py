class TestGetUser:
    def test_get_existing_returns_200(self, client, created_user):
        response = client.get_user(created_user["email"])
        assert response.status_code == 200

    def test_get_returns_correct_data(self, client, created_user):
        response = client.get_user(created_user["email"])
        data = response.json()
        assert data["name"] == created_user["name"]
        assert data["email"] == created_user["email"]
        assert data["age"] == created_user["age"]

    def test_get_nonexistent_returns_404(self, client):
        response = client.get_user("nonexistent@example.com")
        assert response.status_code == 404

    def test_get_error_response_has_error_field(self, client):
        response = client.get_user("nonexistent@example.com")
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert isinstance(data["error"], str)
