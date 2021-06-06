import bson
from app.cli import create_user


def test_get_posts(app, client):
    response = client.get('/posts')
    assert response.status_code == 200
    posts = response.json['data']['posts']
    assert posts == []


def test_get_specific_post(client, runner, auth):
    result = runner.invoke(create_user, ['test', 'test'])
    assert 'Creating user test' in result.output

    response = auth.login()
    assert response.status_code == 200
    token = response.json['data']['token']

    response = client.post('/posts', json={
        'title': 'test title',
        'content': 'test content',
        'remote_url': 'http://test.local'
    }, headers={'Authorization': f'Token {token}'})
    assert response.status_code == 201
    assert 'post' in response.json['data']
    post_id = response.json['data']['post']
    assert bson.objectid.ObjectId.is_valid(post_id)
    response = client.get(f'/posts/{post_id}')
    assert response.status_code == 200
    assert 'post' in response.json['data']
    assert response.json['data']['post']['title'] == 'test title'
    assert response.json['data']['post']['content'] == 'test content'
    assert response.json['data']['post']['remote_url'] == 'http://test.local'


def test_create_post(client, runner, auth):
    result = runner.invoke(create_user, ['test', 'test'])
    assert 'Creating user test' in result.output

    response = auth.login()
    assert response.status_code == 200
    token = response.json['data']['token']

    response = client.post('/posts', json={
        'title':'test title',
        'content':'test content',
        'remote_url':'http://test.local'
    }, headers={'Authorization': f'Token {token}'})
    assert response.status_code == 201
    assert 'post' in response.json['data']
    post_id = response.json['data']['post']
    assert bson.objectid.ObjectId.is_valid(post_id)


def test_update_post(client, runner, auth):
    result = runner.invoke(create_user, ['test', 'test'])
    assert 'Creating user test' in result.output

    response = auth.login()
    assert response.status_code == 200
    token = response.json['data']['token']

    response = client.post('/posts', json={
        'title': 'test title',
        'content': 'test content',
        'remote_url': 'http://test.local'
    }, headers={'Authorization': f'Token {token}'})
    assert response.status_code == 201
    assert 'post' in response.json['data']
    post_id = response.json['data']['post']
    assert bson.objectid.ObjectId.is_valid(post_id)

    response = client.put(f'/posts/{post_id}', json={
        'title': 'test title updated',
        'content': 'test content updated',
        'remote_url': 'http://test.com'
    }, headers={'Authorization': f'Token {token}'})
    assert response.status_code == 200
    assert 'post' in response.json['data']
    assert response.json['data']['post']['title'] == 'test title updated'
    assert response.json['data']['post']['content'] == 'test content updated'
    assert response.json['data']['post']['remote_url'] == 'http://test.com'
