from django.test import TestCase, Client
from users.models import User

class MyResultTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='google_user', email='google@gmail.com')
        self.client = Client()

    def test_access_my_results(self):
        self.client.force_login(self.user)
        response = self.client.get('/my_results/')
        self.assertEqual(response.status_code, 200)

