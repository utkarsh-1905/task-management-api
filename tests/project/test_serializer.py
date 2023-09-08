import pytest
from project.serializer import ProjectSerializer
pytestmark = pytest.mark.django_db

class TestProjectSerializer:
    
    def test_project_serializer(self,project_factory):
        project = project_factory()
        data = ProjectSerializer(project).data
        assert 'project_name' in data
        assert 'project_description' in data
        assert 'project_owner' in data
    
    def test_project_serializer_create(self,project_factory,user_factory):
        user = user_factory()
        project = {
            'project_name':'test_project',
            'project_description':'test_project_description',
            'project_owner':user
        }
        data = ProjectSerializer.create(ProjectSerializer(),project)
        assert data.project_name == 'test_project'
        assert data.project_description == 'test_project_description'
        assert data.project_owner == user
    
    def test_project_serializer_update(self,project_factory):
        project = project_factory()
        data = {
            'project_name':'test_project',
            'project_description':'test_project_description'
        }
        data = ProjectSerializer.update(ProjectSerializer(),project,data)
        assert data.project_name == 'test_project'
        assert data.project_description == 'test_project_description'

        
    