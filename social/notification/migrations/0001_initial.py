# Generated by Django 4.2.7 on 2024-05-29 23:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.IntegerField(choices=[(1, 'Like'), (2, 'Follow'), (3, 'Comment')])),
                ('text_preview', models.CharField(blank=True, max_length=120)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_seen', models.BooleanField(default=False)),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notify_post', to='base.post')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notify_from_user', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notify_to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
