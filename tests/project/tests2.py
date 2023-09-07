import pytest
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_get_all_projects(Projects):
    response = client.get('/api/projects/')
    assert response.status_code == 200
    assert len(response.data) == len(Projects)


@pytest.mark.django_db
def test_get_project(Projects):
    response = client.get('/api/projects/1/')
    assert response.status_code == 200
    assert response.data['project_name'] == Projects[0].project_name


@pytest.mark.django_db
def test_get_project_not_found():
    response = client.get('/api/projects/100/')
    assert response.status_code == 404


@pytest.mark.django_db
def test_create_project_user():
    user = {
        'username': 'test_user_project',
        'password': 'pass',
        'email': 'project@test.com',
        'first_name': 'test_first_name_project',
        'last_name': 'test_last_name_project',
    }
    response = client.post('/api/users/', user, format='json')
    pytest.user = response.data
    print('response from create', response.data)
    assert response.status_code == 201
    assert response.data['username'] == user['username']


@pytest.mark.django_db
def test_get_all_users():
    response = client.get('/api/users/1')
    print(response)
    assert response.status_code == 200
    assert response.data['username'] == pytest.user['username']


# @pytest.mark.django_db
# def test_login_project_user():
#     payload = {
#         'username': 'test_user_project',
#         'password': 'pass',
#     }
#     response = client.post('/api/login/', payload, format='json')
#     print(response.data)
#     pytest.access = response.data['access']
#     pytest.refresh = response.data['refresh']
#     assert response.status_code == 200
#     assert response.data['access'] is not None


# @pytest.mark.django_db
# def test_create_project():
#     response = client.post('/api/projects/', {
#         'project_name': 'project_name_11',
#         'project_description': 'project_description_11',
#     }, HTTP_AUTHORIZATION='Bearer ' + pytest.access, format='json')
#     assert response.status_code == 201
#     assert response.data['project_name'] == 'project_name_11'


# @pytest.mark.django_db
# def test_update_project():
#     response = client.patch('/api/projects/1/', {
#         'project_name': 'project_name_1_ipdated',
#         'project_description': 'project_description_1_updated',
#     })
#     assert response.status_code == 200
#     assert response.data['project_name'] == 'project_name_1_ipdated'
#     assert response.data['project_description'] == 'project_description_1_updated'


# @pytest.mark.django_db
# def test_update_project_owner():
#     response = client.patch('/api/projects/1/', {
#         'project_owner': 2
#     })
#     assert response.status_code == 200
#     assert response.data['project_owner'] == 2
