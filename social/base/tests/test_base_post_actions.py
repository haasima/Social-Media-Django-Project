from .base_case import BaseTest
from django.urls import reverse
from rest_framework import status
from base.models import Post
from django.template.defaultfilters import slugify


class TestPostActions(BaseTest):
    def test_create_post(self):
        url = reverse('base:post-create')
        self.client.login(username=self.user.username, password='testing123321')
        
        data = {
            "title": "Test Create Post",
            "content": "Test Create Post",
        }
        
        response = self.client.post(url, data=data)
        
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        
        
        post = Post.objects.filter(title=data["title"]).first()
        
        redirect_url = reverse('base:post-detail', kwargs={
            'slug': post.slug,
            'year': post.date_posted.year,
            'month': post.date_posted.month,
            'day': post.date_posted.day,
            'pk': post.pk
        })
        
        self.assertRedirects(response, redirect_url)
        
    def test_update_post(self):
        url = reverse('base:post-update', kwargs={
            "pk": self.post.pk
        })
        
        self.client.login(username=self.user.username, password='testing123321')
        
        data = {
            "title": "Test Update Post",
            "content": "Test Update Post"
        }
        
        response = self.client.post(url, data=data)
        
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        
        redirect_url = reverse('base:post-detail', kwargs = {
                                                   'slug': slugify(data["title"]),
                                                   'year': self.post.date_posted.year,
                                                   'month': self.post.date_posted.month,
                                                   'day': self.post.date_posted.day,
                                                   'pk': self.post.pk
                                                   })
        
        self.assertRedirects(response, redirect_url)
        
    def test_delete_post(self):
        url = reverse('base:post-delete', kwargs={
            "pk": self.post.pk
        })
        self.client.login(username=self.user.username, password='testing123321')
        
        post_before_delete_exists = Post.objects.filter(pk=self.post.pk).exists()
        self.assertTrue(post_before_delete_exists)
        
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, reverse('base:home'))
        
        post_afrer_delete_exists = Post.objects.filter(pk=self.post.pk).exists()
        self.assertFalse(post_afrer_delete_exists)