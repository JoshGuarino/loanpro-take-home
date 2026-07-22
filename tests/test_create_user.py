class TestCreateUser:
    def test_create_returns_201(self, client, sample_user):
        response = client.create_user(sample_user)
        assert response.status_code == 201

    def test_create_returns_user_data(self, client, sample_user):
        response = client.create_user(sample_user)
        data = response.json()
        assert data["name"] == sample_user["name"]
        assert data["email"] == sample_user["email"]
        assert data["age"] == sample_user["age"]

    def test_create_duplicate_email_returns_409(self, client, created_user):
        response = client.create_user(created_user)
        assert response.status_code == 409

    def test_create_missing_name_returns_400(self, client, unique_email):
        response = client.create_user({"email": unique_email, "age": 30})
        assert response.status_code == 400

    def test_create_missing_email_returns_400(self, client):
        response = client.create_user({"name": "Test", "age": 30})
        assert response.status_code == 400

    def test_create_missing_age_returns_400(self, client, unique_email):
        response = client.create_user({"name": "Test", "email": unique_email})
        assert response.status_code == 400

    def test_create_invalid_age_zero_returns_400(self, client, unique_email):
        response = client.create_user({"name": "Test", "email": unique_email, "age": 0})
        assert response.status_code == 400

    def test_create_invalid_age_negative_returns_400(self, client, unique_email):
        response = client.create_user({"name": "Test", "email": unique_email, "age": -1})
        assert response.status_code == 400

    def test_create_invalid_age_over_max_returns_400(self, client, unique_email):
        response = client.create_user({"name": "Test", "email": unique_email, "age": 151})
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
