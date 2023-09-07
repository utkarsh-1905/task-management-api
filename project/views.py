from rest_framework import viewsets, response, filters, status
from .serializer import ProjectSerializer
from .models import Project
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import CanModify


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, CanModify]
    filter_backends = [filters.SearchFilter]
    search_fields = ['project_name', 'project_owner__username']

    def create(self, request, *args, **kwargs):
        data = request.data
        project = ProjectSerializer(data=data)
        project.is_valid(raise_exception=True)
        validated_data = project.validated_data
        validated_data['project_owner'] = request.user
        p = project.create(validated_data, *args, **kwargs)
        return response.Response(self.get_serializer(p).data,
                                 status=status.HTTP_201_CREATED)
