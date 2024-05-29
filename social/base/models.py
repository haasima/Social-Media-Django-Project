from django.template.defaultfilters import slugify
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField


class Post(models.Model):
    """ Post model """
    title = models.CharField(max_length=100)
    content = RichTextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, null=True,
                            unique_for_date='date_posted')
    likes = models.ManyToManyField(User, related_name='post_like', blank=True)
    
    def total_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("base:post-detail", kwargs={'slug': self.slug,
                                                   'year': self.date_posted.year,
                                                   'month': self.date_posted.month,
                                                   'day': self.date_posted.day,
                                                   'pk': self.pk})
        
    def __str__(self) -> str:
        return f'{self.author}: {self.title}'
    
    class Meta:
        default_related_name = 'posts'
        ordering = ['-date_posted']
        indexes = [
            models.Index(fields=['-date_posted', 'slug'])
        ]
    

class Comment(models.Model):
    """ Comment model """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        default_related_name = 'comments'
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self) -> str:
        return f'Comment by {self.username} on {self.post}' 