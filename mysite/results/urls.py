from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tests.views import SubmitTestView
from . import views
<<<<<<< feature/86c83t13e-save-test-result

=======
from .views import ResultsViewSet

router = DefaultRouter()
router.register(r'results', ResultsViewSet, basename='results')
>>>>>>> develop

urlpatterns = [
    path('res_view/', views.test_result, name ='test_result'),
]