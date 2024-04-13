from users.models import Profile
from django.urls import reverse
from rest_framework import status
from django.db import connection
from django.test.utils import CaptureQueriesContext
from .test_base import BaseTest

class TestProfile(BaseTest):
        
    def test_get_profile_page(self):
        self.client.login(username=self.user.username, password='testing123321')

        url = reverse('profile') 
        
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            self.assertEqual(len(queries), 3)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_profile_created_after_creating_user(self):
        self.assertEqual(self.user.profile, Profile.objects.get(user=self.user))
        self.client.login(username=self.user.username, password='testing123321')

        url = reverse('profile')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password(self):
        url = reverse('change_password')
        
        is_login = self.client.login(username=self.user.username, password='testing123321')
        self.assertEqual(is_login, True)


        data = {
            'old_password': 'testing123321',
            'new_password1': 'test123321',
            'new_password2': 'test123321'
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.client.logout()

        # Проверка поменялся ли пароль на test123321

        is_login = self.client.login(username=self.user.username, password='test123321')
        is_auth = self.user.is_authenticated
        self.assertEqual(is_login, True)
        self.assertEqual(is_auth, True)

    def test_change_profile_username_and_email(self):
        self.client.login(username=self.user.username, password='testing123321')

        url = reverse('profile')    

        data = {
            'username': 'testing_user_1',
            'email': 'testing_user@gmail.com',
            'image': 'default.jpg',
            'description': 'I am test user.'
        }

        response = self.client.post(url, data)
        self.user.refresh_from_db()

        self.assertRedirects(response, url)
        
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(self.user.username, 'testing_user_1')
        self.assertEqual(self.user.email, 'testing_user@gmail.com')
        self.assertEqual(self.user.profile.image, 'default.jpg')
        self.assertEqual(self.user.profile.description, 'I am test user.')


