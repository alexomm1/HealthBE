from django.urls import path
from tests.views import SubmitTestView, ComplexStatsView, RecentHistoryView, AllTestStatsView

urlpatterns = [
    #save results
    path('sub_test/', SubmitTestView.as_view(), name='submit_test'),
    #get results
    # path('my_results/', MyTestAttemptView.as_view(), name='my_results'),
    # path('attempts/<int:pk>/', TestDetailView.as_view(), name='test_detail'),
    # path('statistic/', AllAttemptsView.as_view(), name='all_tests'),
    # path('history/', AttemptHistoryView.as_view(), name='history'),
    # path('test/<int:test_id>/stats/', TestStatsView.as_view(), name='test_stats'),
    # path('test/stats/', AllTestsStatsView.as_view(), name='all_tests_stats'),
    # path('attempt/history/', AttemptHistoryView.as_view(), name='attempt_history'),
    path('stats/<int:test_id>/', ComplexStatsView.as_view(), name='complex_stats'),
    path('all_stats/', AllTestStatsView.as_view(), name='all_tests_stats'),
    path('history/', RecentHistoryView.as_view(), name='history'),
]