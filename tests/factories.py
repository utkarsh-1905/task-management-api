import factory
from project.models import Project
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Faker('name')
    email = factory.LazyAttribute(
        lambda n: 'email_%s@gmail.com' % n.username.split(' ')[0])
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
