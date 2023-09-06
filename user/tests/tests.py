import pytest
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_get_user(Users):
    response = client.get('/api/users/')
    assert response.status_code == 200
    assert len(response.data) == 10


@pytest.mark.django_db
def test_get_user_by_id(Users):
    response = client.get('/api/users/5/')
    assert response.status_code == 200
    assert response.data['id'] == 5


@pytest.mark.django_db
def test_get_user_by_id_not_found(Users):
    response = client.get('/api/users/100/')
    assert response.status_code == 404


@pytest.mark.django_db
def test_create_user():
    payload = {
        "username": "test_name",
        "password": "test",
        "email": "test@test.com",
        "first_name": "test_first",
        "last_name": "test_last"
    }

    response = client.post('/api/users/', payload, format='json')
    assert response.status_code == 201
    assert response.data['username'] == 'test_name'


@pytest.mark.django_db
def test_create_user_with_invalid_email():
    payload = {
        "username": "test_name",
        "password": "test",
        "email": "test",
        "first_name": "test_first",
        "last_name": "test_last"
    }

    response = client.post('/api/users/', payload, format='json')
    assert response.status_code == 400
    assert response.data['email'][0] == 'Enter a valid email address.'


@pytest.mark.django_db
def test_create_user_with_empty_username():
    payload = {
        "username": "",
        "password": "test",
        "email": "test@gmail.com",
        "first_name": "test_first",
        "last_name": "test_last"
    }
    response = client.post('/api/users/', payload, format='json')
    assert response.status_code == 400
    assert response.data['username'][0] == 'This field may not be blank.'


@pytest.mark.django_db
def test_create_user_with_empty_password():
    payload = {
        "username": "test",
        "password": "",
        "email": "test@gmail.com",
        "first_name": "test_first",
        "last_name": "test_last"
    }
    response = client.post('/api/users/', payload, format='json')
    assert response.status_code == 400
    assert response.data['password'][0] == 'This field may not be blank.'


@pytest.mark.django_db
def test_login_user(Users):
    u = Users[4]
    payload = {
        "username": u.username,
        "password": 'password'
    }
    response = client.post('/api/login/', payload, format='json')
    pytest.refresh = response.data['refresh']
    pytest.access = response.data['access']
    assert response.status_code == 200
    assert response.data['access'] != None


@pytest.mark.django_db
def test_login_user_with_invalid_password(Users):
    u = Users[4]
    payload = {
        "username": u.username,
        "password": 'pass'
    }
    response = client.post('/api/login/', payload, format='json')
    assert response.status_code == 401
    assert response.data['detail'] == 'No active account found with the given credentials'


@pytest.mark.django_db
def test_login_user_with_invalid_username(Users):
    u = Users[4]
    payload = {
        "username": 'user_100',
        "password": 'password'
    }
    response = client.post('/api/login/', payload, format='json')
    assert response.status_code == 401
    assert response.data['detail'] == 'No active account found with the given credentials'


@pytest.mark.django_db
def test_refresh_token():
    payload = {
        "refresh": pytest.refresh
    }
    response = client.post('/api/token/refresh/', payload, format='json')
    pytest.access = response.data['access']
    assert response.status_code == 200
    assert response.data['access'] != None


@pytest.mark.django_db
def test_refresh_token_with_invalid_token():
    payload = {
        "refresh": 'invalid_token'
    }
    response = client.post('/api/token/refresh/', payload, format='json')
    assert response.status_code == 401
    assert response.data['detail'] == 'Token is invalid or expired'
