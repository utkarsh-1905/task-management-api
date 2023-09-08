from rest_framework.viewsets import ModelViewSet
from .serializers import TasksSerializer
from .models import Tasks
from rest_framework import response, status, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from .permissions import CanModify
from django_filters.rest_framework import DjangoFilterBackend


class TasksViewSet(ModelViewSet):
    serializer_class = TasksSerializer
    queryset = Tasks.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, CanModify]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['task_assignee__username', 'task_reviewer__username']
    search_fields = ['task_name', 'task_project__project_name']

    def create(self, request, *args, **kwargs):
        data = request.data
        task = TasksSerializer(data=data)
        valid_data = task.validate(data)
        valid_data['task_creator'] = request.user
        t = task.create(valid_data, *args, **kwargs)
        return response.Response(self.get_serializer(t).data)

    def partial_update(self, request, pk=None):
        try:
            data = request.data
            if data.get('task_creator') is not None:
                return response.Response(
                    {'error': 'You cannot change the task creator'}, 
                    status=status.HTTP_400_BAD_REQUEST)
            if data.get('task_project') is not None:
                return response.Response(
                    {'error': 'You cannot change the task project'}, 
                    status=status.HTTP_400_BAD_REQUEST)
            if data.get('task_created_at') is not None:
                return response.Response(
                    {'error': 'You cannot change the default parameters'}, 
                    status=status.HTTP_400_BAD_REQUEST)
            instance = self.get_object()

            # to update the assignee
            if data.get('task_assignee') is not None:
                assignee = User.objects.filter(id=data.get("task_assignee"))
                if len(assignee) == 0:
                    return response.Response(
                        {'error': 'User does not exist'}, 
                        status=status.HTTP_400_BAD_REQUEST)
                instance.task_assignee = assignee[0]

            # to remove a reviewer
            if data.get('task_reviewer_remove') is not None:
                reviewers = instance.task_reviewer.all()
                for u in data.get('task_reviewer_remove'):
                    user = User.objects.filter(id=u)
                    if len(user) > 0:
                        instance.task_reviewer.remove(u)
                    else:
                        return response.Response(
                            {'error': '[Reviewers] User does not exist'}, 
                            status=status.HTTP_400_BAD_REQUEST)
                instance.task_reviewer.set(reviewers)

            # to add a reviewer
            if data.get('task_reviewer_add') is not None:
                reviewers = instance.task_reviewer.all()
                for u in data.get('task_reviewer_add'):
                    user = User.objects.filter(id=u)
                    if len(user) > 0:
                        instance.task_reviewer.add(u)
                    else:
                        return response.Response(
                            {'error': '[Reviewers Add] User does not exist'}, 
                            status=status.HTTP_400_BAD_REQUEST)
                instance.task_reviewer.set(reviewers)

            # to update the task
            instance.task_name = data.get('task_name', instance.task_name)
            instance.task_description = data.get(
                'task_description', instance.task_description)
            if data['task_due_date'] is not None:
                try:
                    due_date = datetime.strptime(
                        data['task_due_date'], '%Y-%m-%d').date()
                except ValueError:
                    return response.Response(
                        {'error': 'Invalid date format'}, 
                        status=status.HTTP_400_BAD_REQUEST)
                if due_date < timezone.now().date():
                    return response.Response(
                        {'error': 'Due date cannot be in the past'}, 
                        status=status.HTTP_400_BAD_REQUEST)
                instance.task_due_date = due_date
            instance.task_updated_at = timezone.now()
            instance.save()
            return response.Response(self.get_serializer(instance).data)
        except Exception as e:
            return response.Response({'detail': str(e)}, 
                                     status=status.HTTP_401_UNAUTHORIZED)
