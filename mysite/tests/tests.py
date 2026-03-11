from django.shortcuts import redirect
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from tests.models import Test, TestAttempts, Factor, TestResults
from users.models import User


class TestViewsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', email='', password='')
        self.other_user = User.objects.create_user(username='other', email='', password='')

        self.test_obj = Test.objects.create(title='Базовый тест', description='Описание теста')
        self.f1 = Factor.objects.create(test=self.test_obj, name='Фактор 1')
        self.f2 = Factor.objects.create(test=self.test_obj, name='Фактор 2')

        self.submit_url = reverse('submit_test')
        self.history_url = reverse('history')
        self.stats_url = reverse('complex_stats', kwargs={'test_id': self.test_obj.id})

    def tearDown(self):
        User.objects.filter(username__startswith='test_views_').delete()

    #SubmitTestView
    def test_submit_test_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'test_id': self.test_obj.id,
            'results':[
                {'factor_id': 1, 'score': 10},
                {'factor_id': 2, 'score': 20}
            ]
        }
        response = self.client.post(self.submit_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TestAttempts.objects.filter(user=self.user).count(), 1)


    def test_submit_test_unauthenticated(self):
        data = {"test_id": self.test_obj.id, "results": []}
        response = self.client.post(self.submit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_submit_test_bad_request(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'test_id': self.test_obj.id,
            'results': [
                {'factor_id': 1, 'score': -12}
            ]
        }

        response = self.client.post(self.submit_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TestAttempts.objects.filter(user=self.user).count(), 0)


    #Complex test stats
    def test_get_complex_stats_success(self):
        self.client.force_authenticate(user=self.user)

        att1 = TestAttempts.objects.create(user=self.user, test=self.test_obj)
        TestResults.objects.create(user=self.user, attempt=att1, factor=self.f1, score=10)
        TestResults.objects.create(user=self.user, attempt=att1, factor=self.f2, score=20)

        att2 = TestAttempts.objects.create(user=self.user, test=self.test_obj)
        TestResults.objects.create(user=self.user, attempt=att2, factor=self.f1, score=30)
        TestResults.objects.create(user=self.user, attempt=att2, factor=self.f2, score=40)

        response = self.client.get(self.stats_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['attempts_count'], 2)

        self.assertEqual(float(response.data['avg_score']), 25.0)

        f1_stat = next(item for item in response.data['factor_stats'] if item['factor_id'] == self.f1.id)
        self.assertEqual(float(f1_stat['avg_score']), 20.0)

    def test_get_null_complex_stats(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.stats_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['attempts_count'], 0)
        self.assertEqual(response.data['avg_score'], 0 or None)

    def test_isolation_complex_stats(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.get(self.stats_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['attempts_count'], 0)
        self.assertEqual(response.data['avg_score'], 0 or None)
        self.assertEqual(len(response.data['factor_stats']), 2)

    def test_forbidden_complex_stats(self):
        response = self.client.get(self.stats_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #All test stats
    def test_all_tests_stats_success(self):
        self.client.force_authenticate(user=self.user)

        test_2 = Test.objects.create(title='Второй тест')
        f_2_1 = Factor.objects.create(test=test_2, name='Фактор второго теста')

        att_1_1 = TestAttempts.objects.create(user=self.user, test=self.test_obj)
        TestResults.objects.create(user=self.user, attempt=att_1_1, factor=self.f1, score=10)
        att_1_2 = TestAttempts.objects.create(user=self.user, test=self.test_obj)
        TestResults.objects.create(user=self.user, attempt=att_1_2, factor=self.f2, score=20)

        att_2_1 = TestAttempts.objects.create(user=self.user, test=test_2)
        TestResults.objects.create(user=self.user, attempt=att_2_1, factor=f_2_1, score=20)

        url = reverse('all_tests_stats')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        test_1_stats = next(t for t in response.data if t['test_id'] == self.test_obj.id)
        self.assertEqual(test_1_stats['attempts_count'], 2)
        self.assertEqual(test_1_stats['avg_score'], 15.0)

        test_2_stats = next(t for t in response.data if t['test_id'] == test_2.id)
        self.assertEqual(test_2_stats['attempts_count'], 1)
        self.assertEqual(test_2_stats['avg_score'], 20.0)

    def test_all_tests_stats_only_completed(self):
        self.client.force_authenticate(user=self.user)

        Test.objects.create(title="Непройденный тест")

        att = TestAttempts.objects.create(user=self.user, test=self.test_obj)
        TestResults.objects.create(user=self.user, attempt=att, factor=self.f1, score=10)

        url = reverse('all_tests_stats')
        response = self.client.get(url)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['test_id'], self.test_obj.id)

    def test_all_test_stats_user_isolation(self):
        for i in range(5):
            att_U2 = TestAttempts.objects.create(user=self.other_user, test=self.test_obj)
            TestResults.objects.create(user=self.other_user, attempt=att_U2, factor=self.f1, score=10)

        att_U1 = TestAttempts.objects.create(user=self.user, test=self.test_obj)
        TestResults.objects.create(user=self.user, attempt=att_U1, factor=self.f1, score=20)

        self.client.force_authenticate(user=self.user)
        url = reverse('all_tests_stats')
        response = self.client.get(url)

        self.assertEqual(response.data[0]['attempts_count'], 1)
        self.assertEqual(float(response.data[0]['avg_score']), 20.0)

    def test_all_test_stats_correct_null(self):
        self.client.force_authenticate(user=self.user)

        TestAttempts.objects.create(user=self.user, test=self.test_obj)

        url = reverse('all_tests_stats')
        response = self.client.get(url)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['attempts_count'], 1)
        self.assertEqual(float(response.data[0]['avg_score']), 0)

    #история прохождения тестов
    def test_recent_history_no_stats(self):
        self.client.force_authenticate(user=self.user)

        url = reverse('history')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_history_total_score(self):
        self.client.force_authenticate(user=self.user)

        att = TestAttempts.objects.create(user=self.user, test=self.test_obj)
        TestResults.objects.create(user=self.user, attempt=att, factor=self.f1, score=10)
        TestResults.objects.create(user=self.user, attempt=att, factor=self.f2, score=20)
        TestResults.objects.create(user=self.user, attempt=att, factor=self.f1, score=15)

        url = reverse('history')
        response = self.client.get(url)

        self.assertEqual(response.data[0]['result'], 45)

    def test_recent_history_isolation(self):
        att = TestAttempts.objects.create(user=self.user, test=self.test_obj)
        TestResults.objects.create(user=self.user, attempt=att, factor=self.f1, score=10)

        att_u2 = TestAttempts.objects.create(user=self.other_user, test=self.test_obj)
        TestResults.objects.create(user=self.other_user, attempt=att_u2, factor=self.f1, score=20)
        TestResults.objects.create(user=self.other_user, attempt=att_u2, factor=self.f2, score=15)

        self.client.force_authenticate(user=self.user)
        url = reverse('history')
        response = self.client.get(url)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['result'], 10)

    def test_check_history_limit(self):
        for i in range(12):
            TestAttempts.objects.create(user=self.user, test=self.test_obj)

        self.client.force_authenticate(user=self.user)
        url = reverse('history')
        response = self.client.get(url)

        self.assertEqual(len(response.data), 10)