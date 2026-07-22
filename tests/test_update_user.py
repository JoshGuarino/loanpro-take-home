class TestUpdateUser:
    def test_update_returns_200(self, client, created_user):
        updated = {**created_user, "name": "Updated Name"}
        response = client.update_user(created_user["email"], updated)
        assert response.status_code == 200

    def test_update_returns_updated_data(self, client, created_user):
        updated = {**created_user, "name": "Updated Name"}
        response = client.update_user(created_user["email"], updated)
        data = response.json()
        assert data["name"] == "Updated Name"

    def test_update_persists_changes(self, client, created_user):
        updated = {**created_user, "name": "Persisted Name"}
        client.update_user(created_user["email"], updated)
        response = client.get_user(created_user["email"])
        assert response.json()["name"] == "Persisted Name"

    def test_update_nonexistent_returns_404(self, client):
        response = client.update_user("nonexistent@example.com", {
            "name": "Test", "email": "nonexistent@example.com", "age": 30
        })
        assert response.status_code == 404

    def test_update_duplicate_email_returns_409(self, client, created_user, second_user):
        client.create_user(second_user)
        updated = {**created_user, "email": second_user["email"]}
        response = client.update_user(created_user["email"], updated)
        assert response.status_code == 409

    def test_update_invalid_age_zero_returns_400(self, client, created_user):
        updated = {**created_user, "age": 0}
        response = client.update_user(created_user["email"], updated)
        assert response.status_code == 400

    def test_update_invalid_age_negative_returns_400(self, client, created_user):
        updated = {**created_user, "age": -1}
        response = client.update_user(created_user["email"], updated)
        assert response.status_code == 400

    def test_update_invalid_age_over_max_returns_400(self, client, created_user):
        updated = {**created_user, "age": 151}
        response = client.update_user(created_user["email"], updated)
        assert response.status_code == 400

    def test_update_invalid_email_format_returns_400(self, client, created_user):
        updated = {**created_user, "email": "not-an-email"}
        response = client.update_user(created_user["email"], updated)
        assert response.status_code == 400

    def test_update_error_response_has_error_field(self, client):
        response = client.update_user("nonexistent@example.com", {})
        assert "error" in response.json()
