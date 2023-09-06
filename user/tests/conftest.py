from pytest_factoryboy import register
from .factories import UserFactory
import pytest

register(UserFactory)


@pytest.fixture
def Users():
    return UserFactory.create_batch(10)


pytest.refresh = None
pytest.access = None
# this is to set refresh token as a global variable so that it can be used in other tests
