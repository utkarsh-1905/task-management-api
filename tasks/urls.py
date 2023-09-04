from rest_framework.routers import DefaultRouter
from .views import TasksViewSet

router = DefaultRouter()
router.register(r'', TasksViewSet)
urlpatterns = router.urls
