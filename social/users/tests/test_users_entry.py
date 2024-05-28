from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from .base_users_case import BaseTest

class TestEntry(BaseTest):
    def setUp(self):
        self.username = 'register_user'
        self.email = 'registeruser@gmail.com'
        self.password1 = 'testing123321'
        self.password2 = 'testing123321'
        
        super().setUp()

        
    def test_login_page_url(self):
        """ Получение страницы login """
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login(self):
        """ Успешная аутентификация пользователя через username и email"""
        url = reverse('login')

        # Проверка аутентификации пользователя через username
        data = {
            'username': self.user.username,
            'password': 'testing123321'
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        # Проверка аутентификации пользователя через email

        data = {
            'username': self.user.email,
            'password': 'testing123321'
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


    def test_register_page_url(self):
        """ Получение страницы register """
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register(self):
        """ Успешная регистрация пользователя """
        url = reverse('register')

        data = {
            'username': self.username,
            'email': self.email,
            'password1': self.password1,
            'password2': self.password2
        }

        response = self.client.post(url, data=data)

        is_in_users = User.objects.filter(username=self.username, email=self.email).exists()

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(is_in_users, True)

        
    def test_failed_register(self):
        """ Неудачная регистрация пользователя """
        url = reverse('register')

        data = {
            'username': self.username,
            'email': self.email,
            'password1': 'testing123321',
            'password2': 'testing123'
        }

        response = self.client.post(url, data)
        self.assertNotEqual(response.status_code, status.HTTP_302_FOUND)


    def test_logout(self):
        self.client.login(username=self.user.username, password='testing123321')

        url_profile = reverse('profile')
        url = reverse('logout')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_profile = self.client.get(url_profile)
        self.assertRedirects(response_profile, '/login/?next=/profile/')


        