from typing import Dict, Any
from django.db.models import Avg, Max, Count, Sum
from tests.models import TestAttempts, TestResults, Test


def create_test_submission(user, test_id: int, results_data: list):
    attempt = TestAttempts.objects.create(user=user, test_id=test_id)

    results_obj = [
        TestResults(
            user=user,
            attempt=attempt,
            factor_id=res['factor_id'],
            score=res['score']
        ) for res in results_data
    ]

    TestResults.objects.bulk_create(results_obj)

    return attempt


class TestStatsService:

    def get_full_test_stats(self, test_id: int, user_id: int) -> Dict[str, Any]:
        test = self._get_test_with_relations(test_id)
        attempts = self._get_test_attempts(user_id, test_id)
        total_stats = self._get_total_stats(attempts)
        factor_stats = self._get_factor_stats(test, user_id)
        recent_attempts = self._get_recent_attempts(attempts, 5)

        return {
            'test': test,
            'total_stats': total_stats,
            'factor_stats': factor_stats,
            'recent_attempts': recent_attempts
        }

    def get_all_tests_stats(self, user_id: int):
        tests = self._get_all_tests()
        data = self._get_test_data(tests, user_id)

        return data

    def get_recent_history(self, user_id: int):
        attempts = TestAttempts.objects.filter(user_id=user_id).prefetch_related(
            'results'
        ).select_related('test').order_by('-completed_at')[:10]

        data = []
        for attempt in attempts:
            total_score = attempt.results.aggregate(Sum('score'))['score__sum'] or 0

            data.append({
                'date': attempt.completed_at,
                'test_name': attempt.test.title,
                'result': total_score
            })

        return data


    def _get_test_data(self, tests, user_id):
        data = []

        for test in tests:
            attempts = self._get_test_attempts(user_id, test.id)

            if attempts.exists():
                stats = self._get_total_stats(attempts)

                data.append({
                    'test_id': test.id,
                    'title': test.title,
                    'attempts_count': stats['attempts_count'],
                    'avg_score': stats['avg_score'] or 0,
                    'best_score': stats['best_score'] or 0
                })

        return data


    def _get_test_with_relations(self, test_id: int):
        return Test.objects.prefetch_related(
            'attempts__results',
            'factor'
        ).get(id=test_id)

    def _get_all_tests(self):
        return Test.objects.all()

    def _get_test_attempts(self, user_id: int, test_id: int):
        return TestAttempts.objects.filter(user_id=user_id, test_id=test_id).prefetch_related(
            'results'
        ).select_related(
            'test'
        )

    def _get_total_stats(self, attempts):
        stats = attempts.aggregate(
            attempts_count=Count('id', distinct=True),
            avg_score=Avg('results__score'),
            best_score=Max('results__score')
        )

        return {
            'attempts_count': stats['attempts_count'],
            'avg_score': stats['avg_score'] or 0,
            'best_score': stats['best_score'] or 0
        }

    def _get_factor_stats(self, test: Test, user_id: int):
        factor_stats = []
        for factor in test.factor.all():
            factor_results = TestResults.objects.filter(
                factor=factor,
                attempt__user_id=user_id
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

        return factor_stats

    def _get_recent_attempts(self, attempts, limit: int):
        return attempts.order_by('-completed_at')[:limit]

