from tests.models import TestAttempts, TestResults


def create_test_submission(user, test_id: int, results_data: list):
    attempt = TestAttempts.objects.create(user=user, test_id=test_id)

    results_obj = [
        TestResults.objects.create(
            user=user,
            attempt=attempt,
            factor_id=res['factor_id'],
            score=res['score']
        )for res in results_data
    ]

    TestResults.objects.bulk_create(results_obj)

    return attempt