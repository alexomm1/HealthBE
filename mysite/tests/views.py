from django.db.models import Count, Sum
from django.db.models.aggregates import Avg, Max
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from tests.models import TestAttempts, Test, TestResults
from tests.serializers import TestSubmissionSerializer, AttemptDetailWithFactorSerializer
from tests.service import TestStatsService


#отправка результатов
class SubmitTestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TestSubmissionSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#норм получение результатов
class ComplexStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, test_id):
        stats_service = TestStatsService()

        stats = stats_service.get_full_test_stats(test_id, request.user.id)

        return Response({
            'test_id': stats['test'].id,
            'title': stats['test'].title,
            'description': stats['test'].description,
            'attempts_count': stats['total_stats']['attempts_count'],
            'avg_score': stats['total_stats']['avg_score'],
            'best_score': stats['total_stats']['best_score'],
            'factor_stats': stats['factor_stats'],
            'recent_attempts': AttemptDetailWithFactorSerializer(stats['recent_attempts'], many=True).data
        })


#all test stats
class AllTestStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data_service = TestStatsService()
        data = data_service.get_all_tests_stats(request.user.id)
        return Response(data)


#история прохождения тестов
class RecentHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data_service = TestStatsService()
        data = data_service.get_recent_history(request.user.id)

        return Response(data)
