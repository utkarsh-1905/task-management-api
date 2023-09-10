from rest_framework.test import APIClient
import pytest

pytestmark = pytest.mark.django_db

client = APIClient()

class TestTasksViews:

    def test_get_all_tasks(self, tasks):
        response = client.get('/api/tasks/')
        assert response.status_code == 200
        assert len(response.data) == len(tasks)

    def test_get_task(self, tasks):
        response = client.get('/api/tasks/1/')
        assert response.status_code == 200
        assert response.data['task_name'] == tasks[0].task_name
    
    def test_get_task_not_found(self, tasks):
        response = client.get('/api/tasks/100/')
        assert response.status_code == 404
    
    def test_create_task_authenticated(self, user_factory, project_factory):
        projects = project_factory()
        user = user_factory()
        task = {
            'task_name': 'test_task',
            'task_description': 'test_task_description',
            'task_project': projects.id,
        }
        login = {
            'username': user.username,
            'password': 'password'
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        assert response.data['access'] is not None
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = client.post('/api/tasks/', task, format='json')
        assert response.status_code == 201
        assert response.data['task_name'] == 'test_task'
        assert response.data['task_project'].get(
            'project_name') == projects.project_name
        assert response.data['task_creator'].get(
            'username') == user.username
        
    def test_create_task_unauthenticated(self, project_factory):
        projects = project_factory()
        task = {
            'task_name': 'test_task',
            'task_description': 'test_task_description',
            'task_project': projects.id,
        }
        client.credentials(HTTP_AUTHORIZATION='')
        response = client.post('/api/tasks/', task, format='json')
        assert response.status_code == 401
        assert response.data['detail'] == 'Authentication credentials were not provided.'

    def test_create_task_without_task_name(self, user_factory, project_factory):
        projects = project_factory()
        user = user_factory()
        task = {
            'task_description': 'test_task_description',
            'task_project': projects.id,
        }
        login = {
            'username': user.username,
            'password': 'password'
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        assert response.data['access'] is not None
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = client.post('/api/tasks/', task, format='json')
        print(response.data)
        assert response.status_code == 400
        assert response.data[0].__str__() == 'Task name cannot be empty'

    def test_update_task(self, tasks):
        user = tasks[0].task_creator
        login = {
            'username': user.username,
            'password': 'password'
        }
        task = {
            'task_name': 'updated_task_name',
            'task_description': 'updated_task_description'
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        assert response.data['access'] is not None
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        url = '/api/tasks/'+str(tasks[0].id)+'/'
        response = client.patch(url, task, format='json')
        assert response.status_code == 200
        assert response.data['task_name'] == 'updated_task_name'
        assert response.data['task_description'] == 'updated_task_description'

    def test_update_task_unauthenticated(self, tasks):
        task = {
            'task_name': 'updated_task_name',
            'task_description': 'updated_task_description'
        }
        client.credentials(HTTP_AUTHORIZATION='')
        response = client.patch('/api/tasks/1/', task, format='json')
        assert response.status_code == 401
        assert response.data['detail'] == 'Authentication credentials were not provided.'

    def test_update_task_not_creator(self, tasks):
        user = tasks[1].task_creator
        login = {
            'username': user.username,
            'password': 'password'
        }
        task = {
            'task_name': 'updated_task_name',
            'task_description': 'updated_task_description'
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        assert response.data['access'] is not None
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = client.patch('/api/tasks/1/', task, format='json')
        assert response.status_code == 401
        assert response.data['detail'] == 'You are not authorized to perform this action.'
    
    def test_update_task_not_found(self, tasks):
        user = tasks[0].task_creator
        login = {
            'username': user.username,
            'password': 'password'
        }
        task = {
            'task_name': 'updated_task_name',
            'task_description': 'updated_task_description'
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        assert response.data['access'] is not None
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = client.patch('/api/tasks/100/', task, format='json')
        assert response.status_code == 401
    
    def test_delete_task(self, tasks):
        user = tasks[0].task_creator
        login = {
            'username': user.username,
            'password': 'password'
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        url = '/api/tasks/'+str(tasks[0].id)+'/'
        response = client.delete(url)
        assert response.status_code == 204
    
    def test_delete_task_not_creator(self, tasks):
        user = tasks[1].task_creator
        login = {
            'username': user.username,
            'password': 'password'
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        url = '/api/tasks/'+str(tasks[0].id)+'/'
        response = client.delete(url)
        assert response.status_code == 403
        assert response.data['detail'] == 'You are not authorized to perform this action.'

    def test_delete_task_unauthenticated(self, tasks):
        client.credentials(HTTP_AUTHORIZATION='')
        response = client.delete('/api/tasks/1/')
        assert response.status_code == 401
        assert response.data['detail'] == 'Authentication credentials were not provided.'
    
    def test_delete_task_not_found(self, tasks):
        user = tasks[0].task_creator
        login = {
            'username': user.username,
            'password': 'password'
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = client.delete('/api/tasks/100/')
        assert response.status_code == 404
        assert response.data['detail'] == 'Not found.'
    
    def test_update_task_assignee(self, tasks, user_factory):
        user = tasks[0].task_creator
        login = {
            'username': user.username,
            'password': 'password'
        }
        assignee = user_factory()
        task = {
            'task_assignee': assignee.id
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        url = '/api/tasks/'+str(tasks[0].id)+'/'
        response = client.patch(url, task, format='json')
        assert response.status_code == 200
        assert response.data['task_assignee'].get('username') == assignee.username  

    def test_update_task_assignee_not_found(self, tasks):
        user = tasks[0].task_creator
        login = {
            'username': user.username,
            'password': 'password'
        }
        task = {
            'task_assignee': 100
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = client.patch('/api/tasks/1/', task, format='json')
        assert response.status_code == 400
        assert response.data['error'] == 'User does not exist'
    
    def test_update_task_assignee_not_creator(self, tasks):
        user = tasks[1].task_creator
        login = {
            'username': user.username,
            'password': 'password'
        }
        task = {
            'task_assignee': 2
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = client.patch('/api/tasks/1/', task, format='json')
        assert response.status_code == 401
        assert response.data['detail'] == 'You are not authorized to perform this action.'
    
    def test_update_task_assignee_unauthenticated(self, tasks):
        task = {
            'task_assignee': 2
        }
        client.credentials(HTTP_AUTHORIZATION='')
        response = client.patch('/api/tasks/1/', task, format='json')
        assert response.status_code == 401
        assert response.data['detail'] == 'Authentication credentials were not provided.'

    def test_update_task_reviewer_remove(self, tasks, user_factory):
        user = tasks[0].task_creator
        login = {
            'username': user.username,
            'password': 'password'
        }
        reviewer = user_factory()
        tasks[0].task_reviewer.add(reviewer)
        task = {
            'task_reviewer_remove': [reviewer.id]
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        url = '/api/tasks/'+str(tasks[0].id)+'/'
        response = client.patch(url, task, format='json')
        assert response.status_code == 200
        assert len(response.data['task_reviewer']) == 0
    
    def test_update_task_reviewer_remove_not_found(self, tasks):
        user = tasks[0].task_creator
        login = {
            'username': user.username,
            'password': 'password'
        }
        task = {
            'task_reviewer_remove': [100]
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = client.patch('/api/tasks/1/', task, format='json')
        assert response.status_code == 400
        assert response.data['error'] == '[Reviewers] User does not exist'

    def test_update_task_reviewer_add(self, tasks, user_factory):
        user = tasks[0].task_creator
        login = {
            'username': user.username,
            'password': 'password'
        }
        reviewer = user_factory()
        task = {
            'task_reviewer_add': [reviewer.id]
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        url = '/api/tasks/'+str(tasks[0].id)+'/'
        response = client.patch(url, task, format='json')
        assert response.status_code == 200
        assert len(response.data['task_reviewer']) == 1

    def test_update_task_reviewer_add_not_found(self, tasks):
        user = tasks[0].task_creator
        login = {
            'username': user.username,
            'password': 'password'
        }
        task = {
            'task_reviewer_add': [100]
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = client.patch('/api/tasks/1/', task, format='json')
        assert response.status_code == 400
        assert response.data['error'] == '[Reviewers Add] User does not exist'
    
    def test_update_task_due_date(self, tasks):
        user = tasks[0].task_creator
        login = {
            'username': user.username,
            'password': 'password'
        }
        task = {
            'task_due_date': '2023-10-10'
        }
        url = '/api/tasks/'+str(tasks[0].id)+'/'
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        access = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)        
        response = client.patch(url, task, format='json')
        assert response.status_code == 200
        assert response.data['task_due_date'] == '2023-10-10'
    
    def test_update_task_due_date_invalid_format(self, tasks):
        user = tasks[0].task_creator
        login = {
            'username': user.username,
            'password': 'password'
        }
        task = {
            'task_due_date': '2023-10-10 10:10:10'
        }
        url = '/api/tasks/'+str(tasks[0].id)+'/'
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        access = response.data['access']        
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = client.patch(url, task, format='json')
        assert response.status_code == 400
        assert response.data['error'] == 'Invalid date format'
    
    def test_update_task_due_date_invalid_date(self, tasks):
        user = tasks[0].task_creator
        login = {
            'username': user.username,
            'password': 'password'
        }
        task = {
            'task_due_date': '2020-10-10'
        }
        url = '/api/tasks/'+str(tasks[0].id)+'/'
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        access = response.data['access']        
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = client.patch(url, task, format='json')
        assert response.status_code == 400
        assert response.data['error'] == 'Due date cannot be in the past'