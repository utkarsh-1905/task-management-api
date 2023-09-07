from user.serializer import UserSerializer
import pytest

pytestmark = pytest.mark.django_db


class TestUserSerializer:

    def test_user_str(self, user_factory):
        user = user_factory()
        assert user.__str__() == user.username

    def test_user_excluded_fields(self, user_factory):
        user = user_factory()
        data = UserSerializer(user).data
        assert 'last_login' not in data
        assert 'is_staff' not in data
        assert 'is_superuser' not in data
        assert 'groups' not in data
        assert 'user_permissions' not in data
        assert 'is_active' not in data
        assert 'date_joined' not in data

    def test_user_required_fields(self, user_factory):
        user = user_factory()
        data = UserSerializer(user).data
        assert 'username' in data
        assert 'email' in data
        assert 'first_name' in data
        assert 'last_name' in data

    def test_user_required_fields_error(self, user_factory):
        user = {
            'username': 'test',
            'email': 'test@gmail.com',
        }
        try:
            UserSerializer.create(UserSerializer(), user)
        except Exception as e:
            assert type(e).__name__ == 'ValidationError'
