import pytest


class TestCreateUser:
    def test_create_returns_201(self, client, user_factory):
        user, response = user_factory()
        assert response.status_code == 201

    def test_create_returns_user_data(self, client, user_factory):
        user, response = user_factory()
        data = response.json()
        assert data["name"] == user["name"]
        assert data["email"] == user["email"]
        assert data["age"] == user["age"]

    def test_create_duplicate_email_returns_409(self, client, user_factory):
        user, _ = user_factory()
        response = client.create_user(user)
        assert response.status_code == 409

    @pytest.mark.parametrize("payload", [
        {"email": "a@b.com", "age": 30},
        {"name": "Test", "age": 30},
        {"name": "Test", "email": "a@b.com"},
    ])
    def test_create_missing_required_field_returns_400(self, client, payload):
        response = client.create_user(payload)
        assert response.status_code == 400

    @pytest.mark.parametrize("age", [0, -1, 151])
    def test_create_invalid_age_returns_400(self, client, user_factory, age):
        user, response = user_factory(age=age)
        assert response.status_code == 400

    def test_create_invalid_email_format_returns_400(self, client):
        response = client.create_user({"name": "Test", "email": "not-an-email", "age": 30})
        assert response.status_code == 400

    def test_create_error_response_has_error_field(self, client):
        response = client.create_user({})
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert isinstance(data["error"], str)
