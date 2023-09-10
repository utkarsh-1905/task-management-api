import factory
from project.models import Project
from django.contrib.auth.models import User
from tasks.models import Tasks

class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Faker('name')
    email = factory.Faker('email')
    password = factory.django.Password(password="password")
    first_name = factory.LazyAttribute(
        lambda n: 'first_name_%s' % n.username.split(' ')[0])
    last_name = factory.LazyAttribute(
        lambda n: 'last_name_%s' % n.username.split(' ')[1])

class ProjectFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Project

    project_name = factory.Sequence(lambda n: 'project_name_%d' % n)
    project_description = factory.Sequence(
        lambda n: 'project_description_%d' % n)

    project_owner = factory.SubFactory(UserFactory)

class TasksFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Tasks
    
    task_name = factory.Sequence(lambda n: 'task_name_%d' % n)
    task_description = factory.Sequence(lambda n: 'task_description_%d' % n)
    task_project = factory.SubFactory(ProjectFactory)
    task_assignee = factory.SubFactory(UserFactory)
    task_creator = factory.SubFactory(UserFactory)
    task_due_date = factory.Faker('date_between', start_date='-30d', end_date='+30d')
    
    @factory.post_generation
    def task_reviewer(self,create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.task_reviewer.add(*extracted)