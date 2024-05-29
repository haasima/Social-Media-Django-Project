from django.conf import settings
from django.contrib.auth.models import User
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.pagination import PageNumberPagination
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from rest_framework import routers, serializers, viewsets
from base.base_api import views as base_views
from sending_email_app import views as mail_views


# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 2
#     page_size_query_param = 'page_size'

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class UserViewSet(viewsets.ModelViewSet):
    # pagination_class = StandardResultsSetPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', base_views.PostViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls', namespace='base')),
    path('', include('users.urls', namespace='users')),
    path('', include('notification.urls', namespace='notification')),
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('sendmail/', mail_views.sending_mail_to_all, name="sendmail"),

    # Profile/Registration/Login/Logout
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

    # Change password
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='registration/change_password_form.html',
                                                                    success_url=reverse_lazy('change_password_done')),
                                                                    name='change_password'),
    path('change-password/done', auth_views.PasswordChangeDoneView.as_view(template_name='registration/change_password_done.html'),
                                                                            name='change_password_done'),
]


if settings.DEBUG:
    # Media
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # Debug Toolbar
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
        ]