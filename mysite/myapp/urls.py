from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ='home'),
    path('tests/', views.tests_view, name ='tests_page'),
]