from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    user = models.ForeignKey(User, related_name='sent_messages', on_delete=models.SET_NULL, null=True)
    room_name = models.CharField(max_length=255)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['room_name', 'timestamp']
    
    def __str__(self):
        return f'Message from {self.user if self.user else "(deleted user)"}'
    
        