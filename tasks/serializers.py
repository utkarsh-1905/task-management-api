from rest_framework import serializers
from .models import Tasks
from project.serializer import ProjectSerializer
from user.serializer import UserSerializer
from project.models import Project


class TasksSerializer(serializers.ModelSerializer):
    task_creator = UserSerializer()
    task_reviewer = UserSerializer(many=True)
    task_assignee = UserSerializer()
    # ? can owner change the assignee?
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

    def create(self, data):
        task = Tasks(
            task_name=data['task_name'],
            task_description=data['task_description'],
            task_project=data['task_project'],
            task_creator=data['task_creator'],
        )
        task.save()
        return task

    class Meta:
        model = Tasks
        fields = '__all__'
