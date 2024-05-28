from django.shortcuts import render
from django.contrib.auth.models import User
from notification.models import Notification
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from base.models import Post
from users.models import Profile


@login_required
def showNotifications(request):
    """ All notifications """
    user = request.user
    notifications = Notification.objects.filter(user=user)\
        .select_related('post')\
        .prefetch_related(Prefetch('sender',
                        queryset=User.objects.select_related('profile').only('username', 'profile__image')))\
        .only('post__title', 'post__date_posted', 'post__slug', 'id', 'sender_id', 'notification_type', 'text_preview', 'date')\
        .order_by('-date')
                                
    return render(request, 'base/notifications.html', {'notifications': notifications})