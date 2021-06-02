import pytest
from app import create_app


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create the app with common test config
    app = create_app({
        "MONGODB_HOST": 'mongodb://localhost:27017/pensive_test',
        "MONGODB_CONNECT": False,
        "TESTING": True
        })
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
            "/auth/login", data={"username": username, "password": password}
        )


@pytest.fixture
def auth(client):
    return AuthActions(client)
