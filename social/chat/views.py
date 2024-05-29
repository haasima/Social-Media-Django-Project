from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Message


def chat_room(request, username):
    user = get_object_or_404(User.objects.only('username'), username=username)
    requestUser = request.user.username
    
    if user.username == requestUser:
        messages.info(request, "You can't communicate with yourself")
        return redirect(reverse('base:home'))
    
    room_name = f'chat_{"_".join(sorted([requestUser, user.username]))}'
    
    chat_messages = Message.objects.filter(room_name=room_name).order_by('room_name', 'timestamp')
    return render(request, 'chat/chat.html', {'username': user.username,
                                              'requestUser': requestUser,
                                              'chat_messages': chat_messages})