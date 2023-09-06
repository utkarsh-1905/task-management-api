from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Tasks(models.Model):

    task_name = models.CharField(max_length=100)
    task_description = models.CharField(max_length=200)
    task_project = models.ForeignKey(
        'project.Project', on_delete=models.CASCADE, null=False, blank=False, related_name='project_tasks')
    task_assignee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assignee')
    task_reviewer = models.ManyToManyField(
        User, related_name='reviewer', blank=True)
    task_creator = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, null=False, blank=False, related_name='creator')
    task_created_at = models.DateTimeField(auto_now_add=True, editable=False)
    task_updated_at = models.DateTimeField(null=True, editable=True)
    task_due_date = models.DateField(null=True, blank=True)

    REQUIRED_FIELDS = ['task_name', 'task_description',
                       'task_project']

    # only the creator can add an assignee and reviewers
    # the creator can change the assignee and reviewers
    # the creator can change the due date

    def __str__(self):
        return self.task_name

    class Meta:
        db_table = 'tasks'
