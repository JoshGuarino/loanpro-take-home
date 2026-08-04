import pytest


class TestAddNote:
    def test_add_note_returns_201(self, client, user_factory):
        user, _ = user_factory()
        response = client.add_note(user["email"], {"note": "Hello world"})
        assert response.status_code == 201

    def test_add_note_nonexistent_user_returns_404(self, client):
        response = client.add_note("nonexistent@example.com", {"note": "Hi"})
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert isinstance(data["error"], str)

    @pytest.mark.parametrize("payload", [
        {},
        {"note": ""},
        {"foo": "bar"},
    ])
    def test_add_note_missing_field_returns_400(self, client, user_factory, payload):
        user, _ = user_factory()
        response = client.add_note(user["email"], payload)
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert isinstance(data["error"], str)

    def test_add_note_appears_in_get_user(self, client, user_factory):
        user, _ = user_factory()
        client.add_note(user["email"], {"note": "Persisted note"})
        response = client.get_user(user["email"])
        assert "Persisted note" in response.json()["notes"]

    def test_add_note_appears_in_list_users(self, client, user_factory):
        user, _ = user_factory()
        client.add_note(user["email"], {"note": "Visible note"})
        response = client.list_users()
        target = next(u for u in response.json() if u["email"] == user["email"])
        assert "Visible note" in target["notes"]

    def test_notes_only_included_when_present(self, client, user_factory):
        user, _ = user_factory()
        assert "notes" not in client.get_user(user["email"]).json()
        client.add_note(user["email"], {"note": "Now there is a note"})
        assert "notes" in client.get_user(user["email"]).json()
