import pytest
from rest_framework.test import APIClient

client = APIClient()

pytestmark = pytest.mark.django_db


class TestProjectViews:
    def test_get_all_projects(self, projects):
        response = client.get('/api/projects/')
        assert response.status_code == 200
        assert len(response.data) == len(projects)

    def test_get_project(self, projects):
        response = client.get('/api/projects/1/')
        assert response.status_code == 200
        assert response.data['project_name'] == projects[0].project_name

    def test_get_project_not_found(self, users):
        response = client.get('/api/projects/100/')
        assert response.status_code == 404

    def test_create_project_authenticated(self, users):
        project = {
            'project_name': 'test_project',
            'project_description': 'test_project_description',
        }
        login = {
            'username': users[0].username,
            'password': 'password'
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        assert response.data['access'] is not None
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = client.post('/api/projects/', project, format='json')
        assert response.status_code == 201
        assert response.data['project_name'] == 'test_project'
        assert response.data['project_owner'].get(
            'username') == users[0].username

    def test_create_project_unauthenticated(self):
        project = {
            'project_name': 'test_project',
            'project_description': 'test_project_description',
        }
        client.credentials(HTTP_AUTHORIZATION='')
        response = client.post('/api/projects/', project, format='json')
        assert response.status_code == 401
        assert response.data['detail'] == 'Authentication credentials were not provided.'

    def test_create_project_without_project_name(self, users):
        project = {
            'project_description': 'test_project_description',
        }
        login = {
            'username': users[0].username,
            'password': 'password'
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        assert response.data['access'] is not None
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = client.post('/api/projects/', project, format='json')
        assert response.status_code == 400
        assert response.data['project_name'][0] == 'This field is required.'

    def test_update_project(self, projects):
        user = projects[1].project_owner
        login = {
            'username': user.username,
            'password': 'password'
        }
        project = {
            'project_name': 'updated_project_name',
            'project_description': 'updated_project_description'
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        assert response.data['access'] is not None
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = client.patch('/api/projects/2/', project, format='json')
        assert response.status_code == 200
        assert response.data['project_name'] == 'updated_project_name'
        assert response.data['project_description'] == 'updated_project_description'

    def test_update_project_not_owner(self, projects):
        user = projects[0].project_owner
        login = {
            'username': user.username,
            'password': 'password'
        }
        project = {
            'project_name': 'updated_project_name',
            'project_description': 'updated_project_description'
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        assert response.data['access'] is not None
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = client.patch('/api/projects/2/', project, format='json')
        assert response.status_code == 403
        assert response.data['detail'] == 'You are not authorized to perform this action.'

    def test_update_project_unauthenticated(self, projects):
        project = {
            'project_name': 'updated_project_name',
            'project_description': 'updated_project_description'
        }
        client.credentials(HTTP_AUTHORIZATION='')
        response = client.patch('/api/projects/2/', project, format='json')
        assert response.status_code == 401
        assert response.data['detail'] == 'Authentication credentials were not provided.'

    def test_update_project_not_found(self, projects):
        user = projects[1].project_owner
        login = {
            'username': user.username,
            'password': 'password'
        }
        project = {
            'project_name': 'updated_project_name',
            'project_description': 'updated_project_description'
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        assert response.data['access'] is not None
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = client.patch('/api/projects/100/', project, format='json')
        assert response.status_code == 404
        assert response.data['detail'] == 'Not found.'

    def test_delete_unauthenticated(self, projects):
        client.credentials(HTTP_AUTHORIZATION='')
        response = client.delete('/api/projects/2/')
        assert response.status_code == 401
        assert response.data['detail'] == 'Authentication credentials were not provided.'

    def test_delete_project(self, projects):
        user = projects[1].project_owner
        login = {
            'username': user.username,
            'password': 'password'
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = client.delete('/api/projects/2/')
        assert response.status_code == 204

    def test_delete_project_not_owner(self, projects):
        user = projects[0].project_owner
        login = {
            'username': user.username,
            'password': 'password'
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = client.delete('/api/projects/2/')
        assert response.status_code == 403
        assert response.data['detail'] == 'You are not authorized to perform this action.'

    def test_delete_project_not_found(self, projects):
        user = projects[1].project_owner
        login = {
            'username': user.username,
            'password': 'password'
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = client.delete('/api/projects/100/')
        assert response.status_code == 404
        assert response.data['detail'] == 'Not found.'

    def test_search_project(self, projects):
        response = client.get('/api/projects/?search=project_name')
        assert response.status_code == 200
        assert len(response.data) > 0

    def test_search_project_not_found(self, projects):
        response = client.get('/api/projects/?search=project_name_100')
        assert response.status_code == 200
        assert len(response.data) == 0
