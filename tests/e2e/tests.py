from rest_framework.test import APIClient
from django.utils.timezone import is_aware
from datetime import datetime
import pytest
client = APIClient()

pytestmark = pytest.mark.django_db

# End to end testing for the api with custom data as in real world use case
# without using fixtures and factories

class TestE2E:
    
    u1 = {
        "username": "testuser1",
        "password": "testpassword1",
        "email": "testuser1@gmail.com",
        "first_name":"user1",
        "last_name":"test1"
    }

    u2 = {
        "username": "testuser2",
        "password": "testpassword2",
        "email": "testuser2@gmail.com",
        "first_name":"user2",
        "last_name":"test2"
    }

    a1 = None # token for user1
    a2 = None # token for user2

    def test_signup_login_create_project_create_task(self):
        user = client.post('/api/users/', self.u1, format='json')
        assert user.status_code == 201

        login = {
            "username": self.u1['username'],
            "password": self.u1['password']
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        self.a1 = response.data['access']

        # create a project now
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.a1)
        project = {
            'project_name':'test project',
            'project_description':'test description',
            'project_owner':user.data['id']
        }
        project = client.post('/api/projects/', project, format='json')
        assert project.status_code == 201

        # check project is created with this user
        response = client.get('/api/projects/'+str(project.data['id'])+'/')
        assert response.status_code == 200
        assert response.data['project_owner']['username'] == user.data['username']

        # create a task now
        task = {
            'task_name':'test task',
            'task_description':'test description',
            'task_project':project.data['id'],
        }
        task = client.post('/api/tasks/', task, format='json')
        assert task.status_code == 201

        # check task is created with this user and project
        response = client.get('/api/tasks/'+str(task.data['id'])+'/')
        client.credentials(HTTP_AUTHORIZATION='')
        assert response.status_code == 200
        assert response.data['task_project']['project_owner']['username'] == user.data['username']
        assert response.data['task_project']['project_name'] == project.data['project_name']

    def test_signup_login_create_project_create_task_with_different_user_and_try_to_update(self):
        user2 = client.post('/api/users/', self.u2, format='json')
        assert user2.status_code == 201

        login = {
            "username": self.u2['username'],
            "password": self.u2['password']
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        self.a2 = response.data['access']
        # creating second user for testing
        user1 = client.post('/api/users/', self.u1, format='json')
        assert user1.status_code == 201

        login = {
            "username": self.u1['username'],
            "password": self.u1['password']
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        self.a1 = response.data['access']

        # create a project now
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.a2)
        project = {
            'project_name':'test project',
            'project_description':'test description',
            'project_owner':user2.data['id']
        }
        project = client.post('/api/projects/', project, format='json')
        assert project.status_code == 201

        # check project is created with this user
        response = client.get('/api/projects/'+str(project.data['id'])+'/')
        assert response.status_code == 200
        assert response.data['project_owner']['username'] == user2.data['username']
        
        # create a task now
        task = {
            'task_name':'test task',
            'task_description':'test description',
            'task_project':project.data['id'],
        }
        task = client.post('/api/tasks/', task, format='json')
        assert task.status_code == 201

        # check task is created with this user and project
        response = client.get('/api/tasks/'+str(task.data['id'])+'/')
        assert response.status_code == 200
        assert response.data['task_project']['project_owner']['username'] == user2.data['username']
        assert response.data['task_project']['project_name'] == project.data['project_name']

        # try to update task with different user
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.a1)
        utask = {
            'task_name':'test task',
            'task_description':'test description',
        }
        ntask = client.patch('/api/tasks/'+str(task.data['id'])+'/', utask, format='json')
        client.credentials(HTTP_AUTHORIZATION='')
        assert ntask.status_code == 401

    
    def test_signup_login_create_project_create_task_with_different_user_and_try_to_delete(self):
        user2 = client.post('/api/users/', self.u2, format='json')
        assert user2.status_code == 201

        login = {
            "username": self.u2['username'],
            "password": self.u2['password']
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        self.a2 = response.data['access']
        # creating second user for testing
        user1 = client.post('/api/users/', self.u1, format='json')
        assert user1.status_code == 201

        login = {
            "username": self.u1['username'],
            "password": self.u1['password']
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        self.a1 = response.data['access']

        # create a project now
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.a2)
        project = {
            'project_name':'test project',
            'project_description':'test description',
        }
        project = client.post('/api/projects/', project, format='json')
        assert project.status_code == 201

        # check project is created with this user
        response = client.get('/api/projects/'+str(project.data['id'])+'/')
        assert response.status_code == 200
        assert response.data['project_owner']['username'] == user2.data['username']

        # create a task now
        task = {
            'task_name':'test task',
            'task_description':'test description',
            'task_project':project.data['id'],
        }
        task = client.post('/api/tasks/', task, format='json')
        assert task.status_code == 201

        # check task is created with this user and project
        response = client.get('/api/tasks/'+str(task.data['id'])+'/')
        assert response.status_code == 200
        assert response.data['task_project']['project_owner']['username'] == user2.data['username']
        assert response.data['task_project']['project_name'] == project.data['project_name']

        # try to delete task with different user
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.a1)
        ntask = client.delete('/api/tasks/'+str(task.data['id'])+'/', format='json')
        client.credentials(HTTP_AUTHORIZATION='')
        assert ntask.status_code == 403


    def test_signup_login_create_project_create_task_delete_task(self):
        user = client.post('/api/users/', self.u1, format='json')
        assert user.status_code == 201

        login = {
            "username": self.u1['username'],
            "password": self.u1['password']
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        self.a1 = response.data['access']

        # create a project now
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.a1)
        project = {
            'project_name':'test project',
            'project_description':'test description',
            'project_owner':user.data['id']
        }
        project = client.post('/api/projects/', project, format='json')
        assert project.status_code == 201

        # check project is created with this user
        response = client.get('/api/projects/'+str(project.data['id'])+'/')
        assert response.status_code == 200
        assert response.data['project_owner']['username'] == user.data['username']

        # create a task now
        task = {
            'task_name':'test task',
            'task_description':'test description',
            'task_project':project.data['id'],
        }
        task = client.post('/api/tasks/', task, format='json')
        assert task.status_code == 201

        # check task is created with this user and project
        response = client.get('/api/tasks/'+str(task.data['id'])+'/')
        assert response.status_code == 200
        assert response.data['task_project']['project_owner']['username'] == user.data['username']
        assert response.data['task_project']['project_name'] == project.data['project_name']

        # delete task
        ntask = client.delete('/api/tasks/'+str(task.data['id'])+'/', format='json')
        client.credentials(HTTP_AUTHORIZATION='')
        assert ntask.status_code == 204
    
    def test_signup_login_create_project_delete_project(self):
        user = client.post('/api/users/', self.u1, format='json')
        assert user.status_code == 201

        login = {
            "username": self.u1['username'],
            "password": self.u1['password']
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        self.a1 = response.data['access']

        # create a project now
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.a1)
        project = {
            'project_name':'test project',
            'project_description':'test description',
            'project_owner':user.data['id']
        }
        project = client.post('/api/projects/', project, format='json')
        assert project.status_code == 201

        # check project is created with this user
        response = client.get('/api/projects/'+str(project.data['id'])+'/')
        assert response.status_code == 200
        assert response.data['project_owner']['username'] == user.data['username']

        # try to delete it with different user first
        user = client.post('/api/users/', self.u2, format='json')
        assert user.status_code == 201

        login = {
            "username": self.u2['username'],
            "password": self.u2['password']
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        self.a2 = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.a2)
        nproject = client.delete('/api/projects/'+str(project.data['id'])+'/', 
                                 format='json')
        assert nproject.status_code == 403

        # delete project
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.a1)
        nproject = client.delete('/api/projects/'+str(project.data['id'])+'/', 
                                 format='json')
        client.credentials(HTTP_AUTHORIZATION='')
        assert nproject.status_code == 204


    def test_signup_login_create_project_update_project(self):
        user = client.post('/api/users/', self.u1, format='json')
        assert user.status_code == 201

        login = {
            "username": self.u1['username'],
            "password": self.u1['password']
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        self.a1 = response.data['access']

        # create a project now
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.a1)
        project = {
            'project_name':'test project',
            'project_description':'test description',
        }
        project = client.post('/api/projects/', project, format='json')
        assert project.status_code == 201

        # check project is created with this user
        response = client.get('/api/projects/'+str(project.data['id'])+'/')
        assert response.status_code == 200
        assert response.data['project_owner']['username'] == user.data['username']
        uproject = {
            'project_name':'test project',
            'project_description':'test description',
        }

        user = client.post('/api/users/', self.u2, format='json')
        assert user.status_code == 201

        login = {
            "username": self.u2['username'],
            "password": self.u2['password']
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        self.a2 = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.a2)
        nproject = client.patch('/api/projects/'+str(project.data['id'])+'/', uproject, 
                                format='json')
        assert nproject.status_code == 403
        # update project
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.a1)
        nproject = client.patch('/api/projects/'+str(project.data['id'])+'/', uproject, 
                                format='json')
        client.credentials(HTTP_AUTHORIZATION='')
        assert nproject.status_code == 200

    def test_signup_login_create_project_update_task(self):
        user = client.post('/api/users/', self.u1, format='json')
        assert user.status_code == 201

        login = {
            "username": self.u1['username'],
            "password": self.u1['password']
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        self.a1 = response.data['access']

        user2 = client.post('/api/users/', self.u2, format='json')
        assert user2.status_code == 201

        login = {
            "username": self.u2['username'],
            "password": self.u2['password']
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        self.a2 = response.data['access']

        # create a project now
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.a1)
        project = {
            'project_name':'test project',
            'project_description':'test description',
        }
        project = client.post('/api/projects/', project, format='json')
        assert project.status_code == 201

        # check project is created with this user
        response = client.get('/api/projects/'+str(project.data['id'])+'/')
        assert response.status_code == 200
        assert response.data['project_owner']['username'] == user.data['username']

        # create a task now
        task = {
            'task_name':'test task',
            'task_description':'test description',
            'task_project':project.data['id'],
        }
        task = client.post('/api/tasks/', task, format='json')
        assert task.status_code == 201

        # check task is created with this user and project
        response = client.get('/api/tasks/'+str(task.data['id'])+'/')
        assert response.status_code == 200
        assert response.data['task_project']['project_owner']['username'] == user.data['username']
        assert response.data['task_project']['project_name'] == project.data['project_name']
        assert response.data['task_created_at'] is not None
        assert is_aware(datetime.fromisoformat(response.data['task_created_at'])) is True

        # try to update task with different user
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.a1)
        utask = {
            'task_name':'test task',
            'task_description':'test description',
            'task_assignee':user2.data['id'],
            'task_reviewer_add':[user2.data['id']],
            'task_reviewer_remove':[],
        }
        ntask = client.patch('/api/tasks/'+str(task.data['id'])+'/?time_zone=Asia/Kolkata', 
                             utask, format='json')
        client.credentials(HTTP_AUTHORIZATION='')
        assert ntask.status_code == 200
        assert ntask.data['task_assignee']['username'] == user2.data['username']
        assert ntask.data['task_reviewer'][0]['username'] == user2.data['username']
        assert ntask.data['task_project']['project_owner']['username'] == user.data['username']
        assert ntask.data['task_project']['project_name'] == project.data['project_name']
        assert ntask.data['task_updated_at'] is not None

    def test_signup_login_delete_project_delete_task_cascade(self):
        user = client.post('/api/users/', self.u1, format='json')
        assert user.status_code == 201

        login = {
            "username": self.u1['username'],
            "password": self.u1['password']
        }
        response = client.post('/api/login/', login, format='json')
        assert response.status_code == 200
        self.a1 = response.data['access']

        # create a project now
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.a1)
        project = {
            'project_name':'test project',
            'project_description':'test description',
        }
        project = client.post('/api/projects/', project, format='json')
        assert project.status_code == 201

        # create a task now
        task = {
            'task_name':'test task',
            'task_description':'test description',
            'task_project':project.data['id'],
        }
        task = client.post('/api/tasks/', task, format='json')
        assert task.status_code == 201

        # delete project
        nproject = client.delete('/api/projects/'+str(project.data['id'])+'/', 
                                 format='json')
        assert nproject.status_code == 204

        # check task is deleted with project
        response = client.get('/api/tasks/'+str(task.data['id'])+'/')
        assert response.status_code == 404        