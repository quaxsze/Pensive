import pytest
from app import create_app


class TestConfig():
    TESTING = True
    SECRET_KEY = 'you-will-never-guess'
    MONGODB_DB = 'pensive_test'
    MONGODB_HOST = 'mongomock://localhost'


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app(TestConfig)
    return app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login", json={"username": username, "password": password}
        )


@pytest.fixture
def auth(client):
    return AuthActions(client)
