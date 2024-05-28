from .base_case import BaseTest
from django.urls import reverse
from rest_framework import status
from django.test.utils import CaptureQueriesContext
from django.db import connection


class TestEntry(BaseTest):
        
    def test_entry_home_page(self):
        """ Получение страницы home
        и проверка количества запросов к бд """
        url = reverse('base:home')
        
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            self.assertEqual(len(queries), 2)
            
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_entry_post_detail(self):
        """ Получение страницы post-detail
            и проверка количества запросов """
        url = reverse('base:post-detail', kwargs={'slug': self.post.slug,
                                                   'year': self.post.date_posted.year,
                                                   'month': self.post.date_posted.month,
                                                   'day': self.post.date_posted.day,
                                                   'pk': self.post.pk})
        
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            self.assertEqual(len(queries), 5)
            
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_entry_post_create(self):
        """ Получение страницы post-create
            login permission """
        url = reverse('base:post-create')
        self.client.login(username=self.user.username, password='testing123321')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        