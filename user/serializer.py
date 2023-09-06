from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["last_login", "is_staff",
                   "is_superuser", "groups", "user_permissions", "is_active", "date_joined"]
        extra_kwargs = {'password': {'write_only': True}}
        required_fields = ['username', 'email',
                           'first_name', 'last_name', 'password']
        # this lets password appear only when a post request is send to the server
        # the password is not send in a read request/GET request

    def __str__(self):
        return self.username

    def create(self, data):
        user = User(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
        )
        user.set_password(data['password'])
        user.save()
        return user
