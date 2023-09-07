from rest_framework import viewsets, filters
from django.contrib.auth.models import User
from .serializer import UserSerializer
from .permissions import CanModify


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [CanModify]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
