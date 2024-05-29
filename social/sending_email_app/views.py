from django.shortcuts import render
from django.http import HttpResponse
from sending_email_app.tasks import send_mail_func
from django.core.mail import BadHeaderError
from django.http import HttpResponse

def sending_mail_to_all(request):
    try:
        send_mail_func.delay()
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    else:
        return HttpResponse("Sent Email successfully...Check your mail :)")
