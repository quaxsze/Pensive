import bson


def test_get_posts(app, client):
    response = client.get('/posts')
    assert response.status_code == 200
    posts = response.json['data']['posts']
    assert posts == []


def test_create_post(app, client):
    response = client.post('/posts', json={
        'title':'test title',
        'content':'test content',
        'remote_url':'http://test.local'
    })
    assert response.status_code == 201
    assert 'post' in response.json['data']
    post_id = response.json['data']['post']
    assert bson.objectid.ObjectId.is_valid(post_id)


def test_get_specific_post(app, client):
    response = client.post('/posts', json={
        'title': 'test title',
        'content': 'test content',
        'remote_url': 'http://test.local'
    })
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
