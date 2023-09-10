import pytest
pytestmark = pytest.mark.django_db

class TestTaskModel:

    def test_task_name(self, user_factory, tasks_factory):
        r1 = user_factory()
        task = tasks_factory.create(task_reviewer=[r1],task_name='task_name_test')
        assert task.task_name == 'task_name_test'
        assert task.__str__() == 'task_name_test'

    def test_task_db_table_name(self,tasks_factory):
        task = tasks_factory.create(task_name='task_name_test')
        assert task._meta.db_table == 'tasks'
    
    def test_task_created_at_is_UTC(self,tasks_factory):
        task = tasks_factory.create(task_name='task_name_test')
        assert task.task_created_at is not None
        assert str(task.task_created_at.tzinfo) == 'UTC'
        assert task.task_updated_at is None
    
    def test_task_assignee_is_null(self,tasks_factory):
        task = tasks_factory.create(task_name='task_name_test', task_assignee=None)
        assert task.task_assignee is None
    
    def test_task_creator_is_not_null(self,tasks_factory):
        task = tasks_factory.create(task_name='task_name_test')
        assert task.task_creator is not None
    
    def test_task_creator_is_null(self,tasks_factory):
        try:
            tasks_factory.create(task_name='task_name_test', task_creator=None)
        except Exception as e:
            assert str(e) == 'NOT NULL constraint failed: tasks.task_creator_id'
    
    def test_task_project_is_not_null(self,tasks_factory):
        task = tasks_factory.create(task_name='task_name_test')
        assert task.task_project is not None
    
    def test_task_project_is_null(self,tasks_factory):
        try:
            tasks_factory.create(task_name='task_name_test', task_project=None)
        except Exception as e:
            assert str(e) == 'NOT NULL constraint failed: tasks.task_project_id'
