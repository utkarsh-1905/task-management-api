from pytest_factoryboy import register
from .factories import UserFactory, ProjectFactory
import pytest

register(UserFactory)
register(ProjectFactory)


@pytest.fixture(autouse=True)
def users():
    return UserFactory.create_batch(5)
