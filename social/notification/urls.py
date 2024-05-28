from django.urls import path
from notification.views import showNotifications

app_name = 'notification'

urlpatterns = [
    path('notifications/', showNotifications, name='notifications')
]
