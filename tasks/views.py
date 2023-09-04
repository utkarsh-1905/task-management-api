from rest_framework.viewsets import ModelViewSet
from .serializers import TasksSerializer
from .models import Tasks
from rest_framework import response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.utils import timezone


class TasksViewSet(ModelViewSet):
    serializer_class = TasksSerializer
    queryset = Tasks.objects.all()
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = []
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        data = request.data
        task = TasksSerializer(data=data)
        task.is_valid(raise_exception=True)
        project = task.validate_task_project(data['task_project'])
        valid_data = task.validated_data
        valid_data['task_project'] = project
        # user must be authenticated to create a task
        valid_data['task_creator'] = request.user
        t = task.create(valid_data, *args, **kwargs)
        return response.Response(self.get_serializer(t).data)

    def partial_update(self, request, pk=None):
        data = request.data
        if data.get('task_creator') is not None:
            return response.Response(
                {'error': 'You cannot change the task creator'})
        instance = self.get_object()
        # to update the assignee
        if data.get('task_assignee') is not None:
            assignee = User.objects.get(id=data.get("task_assignee"))
            instance.task_assignee = assignee
        # to remove a reviewer
        if data.get('task_reviewer_remove') is not None:
            reviewers = instance.task_reviewer.all()
            for u in data.get('task_reviewer_remove'):
                instance.task_reviewer.remove(u)
            instance.task_reviewer.set(reviewers)
        # to add a reviewer
        if data.get('task_reviewer_add') is not None:
            reviewers = instance.task_reviewer.all()
            for u in data.get('task_reviewer_add'):
                instance.task_reviewer.add(u)
            instance.task_reviewer.set(reviewers)
        # to update the task
        instance.task_name = data.get('task_name', instance.task_name)
        instance.task_description = data.get(
            'task_description', instance.task_description)
        instance.task_due_date = data.get(
            'task_due_date', instance.task_due_date)
        instance.task_updated_at = timezone.now()
        instance.save()
        return response.Response(self.get_serializer(instance).data)
