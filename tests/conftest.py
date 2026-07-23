import pytest
import uuid
from helpers.api_client import APIClient


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        choices=["dev", "prod"],
        help="Target environment: dev or prod"
    )


@pytest.fixture(scope="session")
def environment(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def client(environment):
    return APIClient(environment)


@pytest.fixture
def unique_email():
    return f"test_{uuid.uuid4().hex[:8]}@example.com"


@pytest.fixture
def user_factory(client, unique_email):
    users = []

    def _create(name="Test User", email=None, age=30):
        if email is None:
            email = unique_email
        user = {"name": name, "email": email, "age": age}
        response = client.create_user(user)
        users.append(user)
        return user, response

    yield _create

    for user in users:
        client.delete_user(user["email"])
