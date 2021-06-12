import bson


def test_get_posts(client):
    response = client.get('/posts')
    assert response.status_code == 200
    posts = response.json['data']['posts']
    assert len(posts) == 1
    post_id = response.json['data']['posts'][0]['id']
    assert bson.objectid.ObjectId.is_valid(post_id)


def test_get_specific_post(client):
    response = client.get('/posts')
    assert response.status_code == 200
    post_id = response.json['data']['posts'][0]['id']
    assert bson.objectid.ObjectId.is_valid(post_id)

    response = client.get(f'/posts/{post_id}')
    assert response.status_code == 200
    assert 'post' in response.json['data']
    assert response.json['data']['post']['title'] == 'test title'
    assert response.json['data']['post']['content'] == 'test content'
    assert response.json['data']['post']['remote_url'] == 'http://test.local'


def test_create_post(client, auth):
    response = auth.login()
    assert response.status_code == 200
    token = response.json['data']['token']

    response = client.post('/posts', json={
        'title': 'test post creation',
        'content': 'test post creation',
        'remote_url': 'http://test.local'
    }, headers={'Authorization': f'Token {token}'})
    assert response.status_code == 201
    assert 'post' in response.json['data']
    post_id = response.json['data']['post']
    assert bson.objectid.ObjectId.is_valid(post_id)


def test_update_post(client, auth):
    response = auth.login()
    assert response.status_code == 200
    token = response.json['data']['token']

    response = client.get('/posts')
    assert response.status_code == 200
    post_id = response.json['data']['posts'][0]['id']
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
