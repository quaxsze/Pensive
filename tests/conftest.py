import pytest
from app import create_app, db
from app.cli import create_user, create_post
from app.models.post import Post


class TestConfig():
    TESTING = True
    SECRET_KEY = 'you-will-never-guess'
    MONGODB_DB = 'test'
    MONGODB_HOST = 'mongomock://localhost'
    ELASTICSEARCH_URL = None
    POSTS_PER_PAGE = 20


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


@pytest.fixture(autouse=True)
def append_first(app, auth, runner, client):
    user_result = runner.invoke(create_user, ['test', 'test'])
    assert 'Creating user test' in user_result.output
    post_result = runner.invoke(create_post, ['test title', 'test content', 'http://test.local'])
    assert 'Creating post test title' in post_result.output
    yield
    with app.app_context():
        db.connection.drop_database('test')
