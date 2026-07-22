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
def sample_user(unique_email):
    return {
        "name": "Test User",
        "email": unique_email,
        "age": 30
    }


@pytest.fixture
def created_user(client, sample_user):
    client.create_user(sample_user)
    return sample_user


@pytest.fixture
def second_user(unique_email):
    return {
        "name": "Second User",
        "email": unique_email,
        "age": 25
    }
