import pytest
from rest_framework.test import APIClient
import json

client = APIClient()

pytestmark = pytest.mark.django_db


class TestUserViews:

    def test_get_user(self, users):
        response = client.get('/api/users/')
        assert response.status_code == 200
        assert len(response.data) > 0

    def test_get_user_by_id(self, users):
        response = client.get('/api/users/2/')
        assert response.status_code == 200
        assert response.data['id'] == 2

    def test_get_user_by_id_not_found(self):
        response = client.get('/api/users/100/')
        assert response.status_code == 404

    def test_create_user(self):
        payload = {
            "username": "test_name",
            "password": "testtest",
            "email": "test@test.com",
            "first_name": "test_first",
            "last_name": "test_last"
        }
        response = client.post('/api/users/', payload, format='json')
        assert response.status_code == 201
        assert response.data['username'] == 'test_name'

    def test_create_user_with_invalid_email(self):
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

    def test_create_user_with_empty_username(self):
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

    def test_create_user_with_empty_password(self):
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

    def test_create_user_with_invalid_password(self):
        payload = {
            "username": "test_name",
            "password": "test",
            "email": "test@test.com",
            "first_name": "test_first",
            "last_name": "test_last"
        }
        response = client.post('/api/users/', payload, format='json')
        assert response.status_code == 400
        assert response.data['password'][0] == 'Ensure this field has at least 8 characters.'

    def test_user_login(self, users):
        u = users[4]
        login = {
            "username": u.username,
            "password": "password"
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        assert response.data['access'] != None

    def test_login_user_with_invalid_password(self, users):
        u = users[2]
        login = {
            "username": u.username,
            "password": "wrongpassword"
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 401
        assert response.data['detail'] == 'No active account found with the given credentials'

    def test_login_user_with_invalid_username(self):
        login = {
            "username": "test_name1",
            "password": "password"
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 401
        assert response.data['detail'] == 'No active account found with the given credentials'

    def test_refresh_token_with_invalid_token(self):
        payload = {
            "refresh": 'invalid_token'
        }
        response = client.post('/api/token/refresh/', payload, format='json')
        assert response.status_code == 401
        assert response.data['detail'] == 'Token is invalid or expired'

    def test_update_user_authenticated(self, users):
        payload = {
            "email": "updated_email@gmail.com"
        }
        login_payload = {
            "username": users[4].username,
            "password": 'password'
        }
        response = client.post('/api/login/', login_payload, format='json')
        assert response.data['access'] != None
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        url = '/api/users/' + str(users[4].id) + '/'
        get = client.get(url)
        response = client.patch(url, payload, format='json')
        assert response.status_code == 200
        assert response.data['email'] == 'updated_email@gmail.com'

    def test_update_user_unauthenticated(self):
        payload = {
            "email": "updated_email@gmail.com"
        }
        client.credentials(HTTP_AUTHORIZATION='')
        response = client.patch('/api/users/5/', payload, format='json')
        assert response.status_code == 401
        assert response.data['detail'] == 'Authentication credentials were not provided.'

    def test_update_user_not_found(self, users):
        payload = {
            "email": "updated_email@gmail.com"
        }
        login_payload = {
            "username": users[4].username,
            "password": 'password'
        }
        response = client.post('/api/login/', login_payload, format='json')
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = client.patch('/api/users/100/', payload, format='json')
        assert response.status_code == 404
        assert response.data['detail'] == 'Not found.'

    def test_update_user_with_invalid_email(self, users):
        payload = {
            "email": "updated_email"
        }
        login_payload = {
            "username": users[4].username,
            "password": 'password'
        }
        response = client.post('/api/login/', login_payload, format='json')
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        url = '/api/users/' + str(users[4].id) + '/'
        response = client.patch(
            url, payload, format='json')
        assert response.status_code == 400
        assert response.data['email'][0] == 'Enter a valid email address.'

    def test_update_with_different_credentials(self, users):
        login_payload = {
            "username": users[3].username,
            "password": 'password'
        }
        response = client.post('/api/login/', login_payload, format='json')
        assert response.data['access'] != None
        access = response.data['access']
        payload = {
            "email": "updated_email@gmail.com",
        }
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = client.patch('/api/users/5/', payload, format='json')
        assert response.status_code == 403
        assert response.data['detail'] == 'You are not authorized to perform this action.'

    def test_delete_user_unauthenticated(self):
        response = client.delete('/api/users/5/')
        client.credentials(HTTP_AUTHORIZATION='')
        assert response.status_code == 403
        assert response.data['detail'] == 'You are not authorized to perform this action.'

    def test_delete_user_authenticated(self, users):
        login_payload = {
            "username": users[4].username,
            "password": 'password'
        }
        response = client.post('/api/login/', login_payload, format='json')
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        url = '/api/users/' + str(users[4].id) + '/'
        response = client.delete(url)
        assert response.status_code == 204

    def test_delete_user_not_found(self, users):
        login_payload = {
            "username": users[4].username,
            "password": 'password'
        }
        response = client.post('/api/login/', login_payload, format='json')
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = client.delete('/api/users/100/')
        assert response.status_code == 404
        assert response.data['detail'] == 'Not found.'

    def test_delete_with_different_credentials(self, users):
        login_payload = {
            "username": users[1].username,
            "password": 'password'
        }
        response = client.post('/api/login/', login_payload, format='json')
        assert response.data['access'] != None
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = client.delete('/api/users/3/')
        assert response.status_code == 403
        assert response.data['detail'] == 'You are not authorized to perform this action.'
