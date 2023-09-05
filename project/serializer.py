from rest_framework import serializers
from .models import Project
from user.serializer import UserSerializer
from django.contrib.auth.models import User
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):

    project_owner = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        project = Project(
            project_name=validated_data['project_name'],
            project_description=validated_data['project_description'],
            project_owner=validated_data['project_owner'],
        )
        project.save()
        return project

    def update(self, instance, validated_data):
        instance.project_name = validated_data.get(
            'project_name', instance.project_name)
        instance.project_description = validated_data.get(
            'project_description', instance.project_description)
        instance.save()
        return instance
