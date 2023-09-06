import factory
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user_%d' % n)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(
        lambda a: '%s@gmail.com' % a.username)
    password = factory.django.Password('password')
