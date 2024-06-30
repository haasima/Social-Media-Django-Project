import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def create_chat(self, user, room_name, message):
        return Message.objects.create(user=user, room_name=room_name, text=message)
    
    async def connect(self):
        self.user = self.scope['user']
        self.username1 = self.scope['url_route']['kwargs']['username1']
        self.username2 = self.scope['url_route']['kwargs']['username2']
        
        self.room_group_name = f'chat_{"_".join(sorted([self.username1, self.username2]))}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # accept connection
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message_text = text_data_json['message']
        user_image = text_data_json['user_image']
        now = timezone.now()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_text,
                'user': self.user.username,
                'user_image': user_image,
                'datetime': now.isoformat(),
            }
        )
        
    @database_sync_to_async
    def get_user_by_username(self, username):
        return User.objects.get(username=username)

    async def chat_message(self, event):
        message = event['message']
        username = event['user']
        user_image = event['user_image']
        user = await self.get_user_by_username(username)
        new_message = await self.create_chat(user=user, message=message, room_name=self.room_group_name)
        await self.send(text_data=json.dumps({
            "message": new_message.text,
            "user": new_message.user.username,
            "user_image": user_image,
            "datetime": new_message.timestamp.isoformat()
        }))