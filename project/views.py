from rest_framework import viewsets, response
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

    def create(self, request, *args, **kwargs):
        data = request.data
        project = ProjectSerializer(data=data)
        project.is_valid(raise_exception=True)
        validated_data = project.validated_data
        validated_data['project_owner'] = request.user
        p = project.create(validated_data, *args, **kwargs)
        return response.Response(self.get_serializer(p).data)
