from django.test import TestCase
from tests.models import Test, Factor, TestAttempts, TestResults
from tests.serializers import TestSubmissionSerializer
from users.models import User


class TestSerializersTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_serializer_user', email='', password='')
        self.test_obj = Test.objects.create(title='Base test')
        self.factors = Factor.objects.bulk_create([
            Factor(id=1, test_id=self.test_obj.id, name='Factor1'),
            Factor(id=2, test_id=self.test_obj.id, name='Factor2'),
        ])

    def test_submission_serializer_valid(self):
        data = {
            'test_id': self.test_obj.id,
            'results': [
                {'factor_id':1, 'score': 11 },
                {'factor_id':2, 'score': 12 }
            ]
        }

        serializer = TestSubmissionSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        attempt = serializer.save_results(self.user)
        self.assertEqual(TestAttempts.objects.count(), 1)
        self.assertEqual(TestResults.objects.count(), 2)
        self.assertEqual(attempt.user, self.user)

    def test_submission_invalid_score(self):
        data = {
            'test_id': self.test_obj.id,
            'results': [{'factor_id':1, 'score': -5}]
        }

        serializer = TestSubmissionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('results', serializer.errors)
        self.assertEqual(
            serializer.errors['results'][0]['score'][0],
            'Результат не должен быть меньше 0!'
        )


    def tearDown(self):
        User.objects.filter(username='test_serializer_user').delete()


