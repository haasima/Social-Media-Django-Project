from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from PIL import Image

def profile_image_upload_path(instance, filename):
    return f"profiles_pics/{instance.user.username[0].lower()}/{filename}"

class Profile(models.Model):
    """ Profile model """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    image = models.ImageField(default='default.jpg', upload_to=profile_image_upload_path)
    bio = models.CharField(default="", blank=True, null=True, max_length=500)
    date_of_birth = models.DateField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        super(Profile, self).save(*args, **kwargs) 

        img = Image.open(self.image.path)
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self) -> str:
        return f'{self.user.username}'

 
# Система подписок
class Contact(models.Model):
    """ Contact model """
    user_from = models.ForeignKey(User, related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created'])
        ]

        ordering = ['-created']

    def __str__(self) -> str:
        return f"{self.user_from} follows to {self.user_to}"


# Добавление модели в User динамически
user_model = get_user_model()
user_model.add_to_class('following',
                        models.ManyToManyField(
                            'self', through=Contact,
                            related_name='followers',
                            symmetrical=False
                        ))