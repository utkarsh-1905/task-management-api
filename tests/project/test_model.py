import pytest

pytestmark = pytest.mark.django_db

class TestProjectModel:

    def test_project_str_method(self,project_factory):
        project = project_factory(project_name='test_project')
        assert project.__str__() == 'test_project'
    
    def test_project_meta_db_table(self,project_factory):
        project = project_factory(project_name='test_project')
        assert project._meta.db_table == 'project'
    
