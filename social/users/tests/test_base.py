from django.test import TestCase
from django.contrib.auth.models import User


class BaseTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                    email='test@gmail.com',
                                    first_name='User', last_name='Test',
                                    password='testing123321')