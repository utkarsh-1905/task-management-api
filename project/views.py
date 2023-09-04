from rest_framework import viewsets
from .serializer import ProjectSerializer
from .models import Project
from rest_framework.permissions import IsAuthenticated


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return super().get_permissions()
    # altering the default permission getting function to allow GET requests without authentication
    # https://stackoverflow.com/questions/52690247/how-to-set-authentication-and-permission-only-on-put-requests-in-django-rest-in
