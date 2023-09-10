from tasks.serializers import TasksSerializer
import pytest

pytestmark = pytest.mark.django_db

class TestTaskSerializer:

    def test_task_serializer(self, tasks_factory,user_factory):
        r1 = user_factory()
        task = tasks_factory.create(task_reviewer=[r1])
        data = TasksSerializer(task).data
        assert 'task_name' in data
        assert 'task_description' in data
        assert 'task_project' in data
        assert 'task_assignee' in data
        assert 'task_reviewer' in data
        assert 'task_creator' in data
        assert 'task_created_at' in data
        assert 'task_updated_at' in data
        assert 'task_due_date' in data
        
    def test_task_serializer_create(self,user_factory,project_factory):
        user = user_factory()
        project = project_factory()
        task = {
            'task_name':'test_task',
            'task_description':'test_task_description',
            'task_project':project,
            'task_creator':user
        }
        data = TasksSerializer.create(TasksSerializer(),task)
        assert data.task_name == 'test_task'
        assert data.task_description == 'test_task_description'
        assert data.task_project == project
        assert data.task_creator == user

    def test_task_serializer_update(self, tasks_factory):
        task = tasks_factory()
        data = {
            'task_name':'test_task_updated',
            'task_description':'test_task_description_updated',
        }
        data = TasksSerializer.update(TasksSerializer(),task,data)
        assert data.task_name == 'test_task_updated'
        assert data.task_description == 'test_task_description_updated'
    
    def test_task_serializer_validate_task_project(self,project_factory):
        project = project_factory()
        data = TasksSerializer.validate_task_project(TasksSerializer(),project.id)
        assert data == project
    
    def test_task_serializer_validate_task_project_none(self):
        with pytest.raises(Exception):
            TasksSerializer.validate_task_project(TasksSerializer(),None)
    
    def test_task_serializer_validate_task_project_does_not_exist(self):
        with pytest.raises(Exception):
            TasksSerializer.validate_task_project(TasksSerializer(),999)
    
    def test_task_serializer_validate(self,project_factory,user_factory):
        user = user_factory()
        project = project_factory()
        data = {
            'task_project':project.id,
            'task_name':'test_task_updated',
            'task_description':'test_task_description_updated',
            'task_creator':user
        }
        data = TasksSerializer.validate(TasksSerializer(),data)
        assert data['task_project'] == project
        assert data['task_name'] == 'test_task_updated'
        assert data['task_description'] == 'test_task_description_updated'
        assert data['task_creator'] == user
        
    def test_task_serializer_validate_task_creator_none(self,project_factory):
        project = project_factory()
        data = {
            'task_project':project.id,
            'task_name':'test_task_updated',
            'task_description':'test_task_description_updated',
        }
        with pytest.raises(Exception):
            TasksSerializer.validate(TasksSerializer(),data)
        
    def test_task_create_without_task_project(self,user_factory):
        user = user_factory()
        data = {
            'task_name':'test_task_updated',
            'task_description':'test_task_description_updated',
            'task_creator':user
        }
        with pytest.raises(Exception):
            TasksSerializer.validate(TasksSerializer(),data)
        
    def test_task_create_without_task_name(self,user_factory,project_factory):
        user = user_factory()
        project = project_factory()
        data = {
            'task_project':project.id,
            'task_description':'test_task_description_updated',
            'task_creator':user
        }
        with pytest.raises(Exception):
            TasksSerializer.validate(TasksSerializer(),data)
    
    def test_task_update_time(self,tasks_factory):
        task = tasks_factory()
        data = {
            'task_name':'test_task_updated',
            'task_description':'test_task_description_updated',
        }
        data = TasksSerializer.update(TasksSerializer(),task,data)
        assert data.task_updated_at is not None
    

    
