from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import TestResultViewSet

router = DefaultRouter()
router.register(r'results', TestResultViewSet, basename='results')

urlpatterns = [
    path('', include(router.urls)),
    path('res_view/', views.test_result, name ='test_result'),
]