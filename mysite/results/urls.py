from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tests.views import SubmitTestView
from . import views


urlpatterns = [
    path('res_view/', views.test_result, name ='test_result'),
]