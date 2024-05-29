from django.db import connection
from django.test.utils import CaptureQueriesContext
from rest_framework import status
from django.urls import reverse
from .base_users_case import BaseTest
from django.contrib.auth.models import User
from users.models import Contact

class TestUserDetail(BaseTest):
    def setUp(self):
        super().setUp()
        self.user2 = User.objects.create_user(username='test_user2',
                                    email='test2@gmail.com',
                                    first_name='User', last_name='Test_2',
                                    password='testing123321')

    def test_get_user_page(self):
        url = reverse('users:user_detail', kwargs={'username': self.user.username})

        # Проверка количества запросов к бд 
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            self.assertEqual(len(queries), 3)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subscribe(self):
        url = reverse('users:user_follow', kwargs={'username': self.user2.username})

        # Незалогиненный пользователь
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, '/login/?next=/follow/test_user2')

        # Залогиненный пользователь
        self.client.login(username=self.user.username, password='testing123321')
        response = self.client.post(url)
        
        is_sub = Contact.objects.filter(user_from=self.user, user_to=self.user2).exists()
        self.assertTrue(is_sub)
