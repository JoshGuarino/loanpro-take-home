class TestListUsers:
    def test_list_returns_200(self, client):
        response = client.list_users()
        assert response.status_code == 200

    def test_list_returns_array(self, client):
        response = client.list_users()
        assert isinstance(response.json(), list)

    def test_list_includes_created_user(self, client, user_factory):
        user, _ = user_factory()
        response = client.list_users()
        emails = [u["email"] for u in response.json()]
        assert user["email"] in emails

    def test_list_user_has_required_fields(self, client, user_factory):
        user_factory()
        response = client.list_users()
        for user in response.json():
            assert "name" in user
            assert "email" in user
            assert "age" in user
