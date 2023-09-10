from rest_framework import serializers
from .models import Tasks
from project.serializer import ProjectSerializer
from user.serializer import UserSerializer
from project.models import Project
from django.utils import timezone


class TasksSerializer(serializers.ModelSerializer):
    task_creator = UserSerializer()
    task_reviewer = UserSerializer(many=True)
    task_assignee = UserSerializer()
    task_project = ProjectSerializer()

    def validate_task_project(self, project):
        if project is None:
            raise serializers.ValidationError(
                "Project cannot be empty")
        else:
            try:
                project = Project.objects.get(pk=project)
            except Project.DoesNotExist:
                raise serializers.ValidationError(
                    "Project does not exist")
            return project

    def validate(self, data):
        if data['task_project'] is not None:
            project = self.validate_task_project(
                data['task_project'])
            if project is not None:
                data['task_project'] = project
        if 'task_creator' not in data:
            raise serializers.ValidationError(
                "Task creator cannot be empty")
        if 'task_name' not in data:
            raise serializers.ValidationError(
                "Task name cannot be empty")
        if 'task_description' not in data:
            raise serializers.ValidationError(
                "Task description cannot be empty")
        return data

    def create(self, data):
        task = Tasks(
            task_name=data['task_name'],
            task_description=data['task_description'],
            task_project=data['task_project'],
            task_creator=data['task_creator'],
        )
        task.save()
        return task

    def update(self, instance, data):
        if 'task_creator' in data:
            raise serializers.ValidationError(
                "Task creator cannot be updated")
        data['task_updated_at'] = timezone.now()
        return super().update(instance, data)

    class Meta:
        model = Tasks
        fields = '__all__'
        read_only_fields = ['task_name', 'task_created_at',
                            'task_creator', 'task_project']
        extra_kwargs = {
            'task_description': {'required': True},
            'task_project': {'required': True},
            'task_creator': {'required': True},
            'task_name': {'required': True},
        }
