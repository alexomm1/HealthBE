from django.db.models import Count, Sum
from django.db.models.aggregates import Avg, Max
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from tests.models import TestAttempts, Test, TestResults
from tests.serializers import TestSubmissionSerializer, AttemptDetailWithFactorSerializer

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
        test = Test.objects.prefetch_related('attempts__results').get(id=test_id)
        attempts = TestAttempts.objects.filter(test=test, user=request.user).prefetch_related('results')

        total_stats = attempts.aggregate(
            attempts_count=Count('id', distinct=True),
            avg_score=Avg('results__score'),
            best_score=Max('results__score')
        )

        factor_stats = []
        for factor in test.factor.all():
            factor_results = TestResults.objects.filter(
                factor=factor,
                attempt__user=request.user
            ).aggregate(
                avg_score=Avg('score'),
                max_score=Max('score'),
                count=Count('id')
            )
            factor_stats.append({
                'factor_id': factor.id,
                'factor_name': factor.name,
                'avg_score': factor_results['avg_score'] or 0,
                'max_score': factor_results['max_score'] or 0,
                'attempts_count_fac': factor_results['count'] or 0
            })

        recent_attempts = attempts.order_by('-completed_at')[:5]

        return Response({
            'test_id': test.id,
            'title': test.title,
            'description': test.description,
            'attempts_count': total_stats['attempts_count'],
            'avg_score': total_stats['avg_score'],
            'best_score': total_stats['best_score'],
            'factor_stats': factor_stats,
            'recent_attempts': AttemptDetailWithFactorSerializer(recent_attempts, many=True).data
        })


#all test stats
class AllTestStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tests = Test.objects.all()
        data = []

        for test in tests:
            attempts = TestAttempts.objects.filter(
                test=test, user=request.user
            )

            if attempts.exists():
                stats = attempts.aggregate(
                    avg_score=Avg('results__score'),
                    attempts_count=Count('id'),
                    best_score=Max('results__score')
                )
                data.append({
                    'test_id': test.id,
                    'title': test.title,
                    'attempts_count': stats['attempts_count'],
                    'avg_score': stats['avg_score'] or 0,
                    'best_score': stats['best_score'] or 0
                })

        return Response(data)



#история прохождения тестов
class RecentHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        attempts = TestAttempts.objects.filter(user=self.request.user).select_related('test').prefetch_related('results').order_by('-completed_at')[:10]

        data = []
        for attempt in attempts:
            total_score = attempt.results.aggregate(Sum('score'))['score__sum'] or 0

            data.append({
                'data': attempt.completed_at,
                'test_name': attempt.test.title,
                'result': total_score
            })

        return Response(data)