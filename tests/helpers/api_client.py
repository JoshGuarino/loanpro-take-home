import os
import requests


class APIClient:
    BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:3000")
    AUTH_TOKEN = os.environ.get("API_AUTH_TOKEN", "mysecrettoken")

    def __init__(self, environment: str):
        if environment not in ("dev", "prod"):
            raise ValueError(f"Invalid environment: {environment}. Must be 'dev' or 'prod'.")
        self.base = f"{self.BASE_URL}/{environment}"
        self.headers = {"Content-Type": "application/json"}

    def list_users(self) -> requests.Response:
        return requests.get(f"{self.base}/users")

    def create_user(self, data: dict) -> requests.Response:
        return requests.post(f"{self.base}/users", json=data, headers=self.headers)

    def get_user(self, email: str) -> requests.Response:
        return requests.get(f"{self.base}/users/{email}")

    def update_user(self, email: str, data: dict) -> requests.Response:
        return requests.put(f"{self.base}/users/{email}", json=data, headers=self.headers)

    def delete_user(self, email: str) -> requests.Response:
        headers = {**self.headers, "Authentication": self.AUTH_TOKEN}
        return requests.delete(f"{self.base}/users/{email}", headers=headers)

    def delete_user_no_auth(self, email: str) -> requests.Response:
        return requests.delete(f"{self.base}/users/{email}", headers=self.headers)

    def delete_user_bad_auth(self, email: str) -> requests.Response:
        headers = {**self.headers, "Authentication": "badtoken123"}
        return requests.delete(f"{self.base}/users/{email}", headers=headers)

    def add_note(self, email: str, data: dict) -> requests.Response:
        return requests.post(f"{self.base}/users/{email}/notes", json=data, headers=self.headers)

    def add_note(self, email: str, data: dict) -> requests.Response:
        return requests.post(f"{self.base}/users/{email}/notes", json=data, headers=self.headers)
