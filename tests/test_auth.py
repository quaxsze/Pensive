from app.cli import create_user


def test_login(runner, auth):
    result = runner.invoke(
        create_user, ['test', 'test'])
    assert 'Creating user test' in result.output

    response = auth.login()
    assert response.status_code == 200
    assert 'token' in response.json['data']


def test_retrieve_user(client, runner, auth):
    result = runner.invoke(
        create_user, ['test', 'test'])
    assert 'Creating user test' in result.output

    response = auth.login()
    assert response.status_code == 200
    token = response.json['data']['token']

    response = client.get('auth/user', headers={'Authorization': f'Token {token}'})
    print(response.json['data'])
    assert response.status_code == 200
    user = response.json['data']['user']
    assert user['username'] == 'test'
