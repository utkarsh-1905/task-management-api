from .views import UserViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'', UserViewSet, basename='')

urlpatterns = router.urls
