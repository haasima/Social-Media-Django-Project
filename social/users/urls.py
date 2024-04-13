from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('users/', views.user_search, name='users_list'),
    # Профиль других пользователей
    path('users/<username>', views.user_detail, name='user_detail'),
    path('follow/<username>', views.user_follow, name="user_follow"),
]
