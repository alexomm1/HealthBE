from unittest.mock import patch
from rest_framework import status
from users.models import User
from django.urls import reverse
from rest_framework.test import APITestCase


class TestAuthViewsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email='test@gmail.com', password='testpassword')

        self.jwt_url = reverse('get_jwt')
        self.callback_url = reverse('google_callback')

    def test_get_jwt_tokens_success(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.jwt_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['email'], self.user.email)

    def test_get_jwt_tokens_unauthenticated(self):
        response = self.client.get(self.jwt_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch('requests.post')
    @patch('requests.get')
    def test_google_callback_success(self, mock_get, mock_post):
        mock_post.return_value.status_code = status.HTTP_200_OK
        mock_post.return_value.json.return_value = {'access_token': 'fake_google_token'}

        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.json.return_value = {
            'email': 'newuser@gmail.com',
            'id': '0001'
        }

        response = self.client.get(self.callback_url, {'code': 'fake_code'})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(User.objects.filter(email='newuser@gmail.com').exists())

        session = self.client.session
        self.assertIn('jwt_access', session)

    @patch('requests.post')
    def test_google_callback_token_error(self, mock_post):
        mock_post.return_value.status_code = status.HTTP_400_BAD_REQUEST
        mock_post.return_value.text = 'Invalid code'

        response = self.client.get(self.callback_url, {'code': 'fake_code'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('ошибка токена', response.content.decode('utf-8'))

    @patch('requests.post')
    @patch('requests.get')
    def test_google_callback_no_email(self, mock_get, mock_post):
        mock_post.return_value.status_code = status.HTTP_200_OK
        mock_post.return_value.json.return_value = {'access_token': 'fake_token'}

        mock_get.return_value.json.return_value = {'id': '123'}

        response = self.client.get(self.callback_url, {'code': 'fake_code'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('нету email', response.content.decode('utf-8'))

