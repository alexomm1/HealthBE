from rest_framework.routers import DefaultRouter
from tests.views import TestViewSet

router = DefaultRouter()
router.register(r'api/tests', TestViewSet, basename='test')

urlpatterns = router.urls