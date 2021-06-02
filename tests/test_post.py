import pytest


def test_get_posts(app, client):
    response = client.get("/posts")
    posts = response.json['data']['posts']
    assert response.status_code == 200
    assert posts == []
