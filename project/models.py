from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    project_name = models.CharField(max_length=100)
    project_description = models.CharField(max_length=200, null=True)

    project_owner = models.ForeignKey(
        User, null=False, on_delete=models.CASCADE, related_name='projects')
    # add editable = false

    REQUIRED_FIELDS = ['project_name']

    def __str__(self):
        return self.project_name

    class Meta:
        db_table = 'project'
