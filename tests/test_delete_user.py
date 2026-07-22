class TestDeleteUser:
    def test_delete_returns_204(self, client, created_user):
        response = client.delete_user(created_user["email"])
        assert response.status_code == 204

    def test_delete_removes_user(self, client, created_user):
        client.delete_user(created_user["email"])
        response = client.get_user(created_user["email"])
        assert response.status_code == 404

    def test_delete_nonexistent_returns_404(self, client):
        response = client.delete_user("nonexistent@example.com")
        assert response.status_code == 404

    def test_delete_no_auth_returns_401(self, client, created_user):
        response = client.delete_user_no_auth(created_user["email"])
        assert response.status_code == 401

    def test_delete_bad_auth_returns_401(self, client, created_user):
        response = client.delete_user_bad_auth(created_user["email"])
        assert response.status_code == 401

    def test_delete_error_response_has_error_field(self, client):
        response = client.delete_user("nonexistent@example.com")
        if response.status_code == 404:
            data = response.json()
            assert "error" in data
            assert isinstance(data["error"], str)
