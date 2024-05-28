from django.test import TestCase
from django.contrib.auth.models import User
from base.models import Post


class BaseTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                    email='test@gmail.com',
                                    first_name='User', last_name='Test',
                                    password='testing123321') 
        
        self.post = Post.objects.create(author=self.user, title='Test Post',
                                        content='Test Content')