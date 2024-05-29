from django.contrib.auth.models import User
from celery import shared_task
from django.core.mail import send_mail
from social import settings


@shared_task(bind=True)
def send_mail_func(self):
    # operations
    users = User.objects.all()
    for user in users:
        mail_subject = "Hey, from Social Media Project!"
        message = "I completed this task with Celery? Yes!"
        to_email = user.email
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=False
        )
        
    return "Done"