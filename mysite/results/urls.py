from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tests.views import ResultsViewSet
from . import views

router = DefaultRouter()
router.register(r'results', ResultsViewSet, basename='results')

urlpatterns = [
    path('', include(router.urls)),
    path('res_view/', views.test_result, name ='test_result'),
]