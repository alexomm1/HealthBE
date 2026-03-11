from os import name

from django.test import TestCase
from tests.models import Test, Factor, TestAttempts, TestResults
from tests.serializers import TestSubmissionSerializer, AttemptDetailWithFactorSerializer
from users.models import User
from rest_framework.test import APITestCase, APIRequestFactory


class TestSerializerTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='')
        self.client.force_authenticate(user=self.user)

        self.test_obj = Test.objects.create(title='Базовый тест')
        self.f1 = Factor.objects.create(test=self.test_obj, name='Factor1')
        self.f2 = Factor.objects.create(test=self.test_obj, name='Factor2')

        self.factory = APIRequestFactory()

    def test_submission_create_object(self):
        data = {
            'test_id': self.test_obj.id,
            'results': [
                {'factor_id': 1, 'score': 5},
                {'factor_id': 2, 'score': 10}
            ]
        }

        request = self.factory.post('/fake_url/')
        request.user = self.user

        serializer = TestSubmissionSerializer(data=data, context={'request': request})

        self.assertTrue(serializer.is_valid(), serializer.errors)
        attempt = serializer.save()

        self.assertEqual(TestAttempts.objects.count(), 1)
        self.assertEqual(TestResults.objects.filter(attempt=attempt).count(), 2)
        self.assertEqual(attempt.user, self.user)

    def test_submission_invalid_score(self):
        data = {
            'test_id': 1,
            'results': [{'factor_id': 1, 'score': -5}]
        }

        request = self.factory.post('/fake_url/')
        request.user = self.user

        serializer = TestSubmissionSerializer(data=data, context={'request': request})

        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn('results', serializer.errors)
        self.assertIn('score', serializer.errors['results'][0])

    def test_detail_serializer_total_score(self):
        att = TestAttempts.objects.create(user=self.user, test_id=1)
        TestResults.objects.create(attempt=att, user=self.user, factor_id=1, score=5)
        TestResults.objects.create(attempt=att, user=self.user, factor_id=2, score=10)

        serializer = AttemptDetailWithFactorSerializer(instance=att)

        self.assertEqual(serializer.data['total_score'], 15)
        self.assertEqual(len(serializer.data['results']), 2)
