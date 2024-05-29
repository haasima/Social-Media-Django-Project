from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Message


def chat_room(request, username):
    user = get_object_or_404(User.objects.only('username'), username=username)
    requestUser = request.user.username
    room_name = f'chat_{"_".join(sorted([requestUser, user.username]))}'
    
    chat_messages = Message.objects.filter(room_name=room_name).order_by('timestamp')
    return render(request, 'chat/chat.html', {'username': user.username,
                                              'requestUser': requestUser,
                                              'chat_messages': chat_messages})