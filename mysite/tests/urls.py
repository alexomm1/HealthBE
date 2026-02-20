from django.urls import path
from rest_framework.routers import DefaultRouter
from tests.views import SubmitTestView, MyTestAttemptView

urlpatterns = [
    path('sub_test/', SubmitTestView.as_view(), name='submit_test'),
    path('my_results/', MyTestAttemptView.as_view(), name='my_results'),
]