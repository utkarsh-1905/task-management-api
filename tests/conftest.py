from pytest_factoryboy import register
from .factories import UserFactory, ProjectFactory
import pytest

register(UserFactory)
register(ProjectFactory)


@pytest.fixture(autouse=True)
def users():
    return UserFactory.create_batch(5)


@pytest.fixture(autouse=True)
def projects():
    return ProjectFactory.create_batch(5)


def pytest_html_report_title(report):
    report.title = 'Task Management API Test Report'
