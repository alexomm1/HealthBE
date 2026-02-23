from django.urls import path
from tests.views import SubmitTestView, MyTestAttemptView, TestDetailView, AllAttemptsView, AttemptHistoryView

urlpatterns = [
    path('sub_test/', SubmitTestView.as_view(), name='submit_test'),
    path('my_results/', MyTestAttemptView.as_view(), name='my_results'),
    path('attempts/<int:pk>/', TestDetailView.as_view(), name='test_detail'),
    path('statistic/', AllAttemptsView.as_view(), name='all_tests'),
    path('history/', AttemptHistoryView.as_view(), name='history'),

]