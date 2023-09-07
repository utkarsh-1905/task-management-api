from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["last_login", "is_staff",
                   "is_superuser", "groups", "user_permissions", "is_active", "date_joined"]
        extra_kwargs = {'password': {'write_only': True, 'required': True, 'min_length': 8, 'style': {'input_type': 'password'}},
                        'username': {'required': True},
                        'email': {'required': True},
                        'first_name': {'required': True},
                        'last_name': {'required': True}
                        }

    def __str__(self):
        return self.username

    def validate_during_create(self, data):
        if not data.get('first_name'):
            raise serializers.ValidationError(
                {'first_name': 'This field is required.'})
        if not data.get('last_name'):
            raise serializers.ValidationError(
                {'last_name': 'This field is required.'})
        if not data.get('email'):
            raise serializers.ValidationError(
                {'email': 'This field is required.'})
        if not data.get('username'):
            raise serializers.ValidationError(
                {'username': 'This field is required.'})
        if not data.get('password'):
            raise serializers.ValidationError(
                {'password': 'This field is required.'})
        if len(data.get('password')) < 8:
            raise serializers.ValidationError(
                {'password': 'Password must be at least 8 characters long.'})
        return data

    def create(self, data):
        self.validate_during_create(data)
        user = User(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
        )
        user.set_password(data['password'])
        user.save()
        return user
