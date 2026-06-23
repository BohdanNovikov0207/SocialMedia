from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
import datetime
from django.db.models import Q

from .forms import MessageForm
from chat_app.models import Chat, Message

class PresenceConsumer(AsyncWebsocketConsumer):
    online_users = set()

    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
            return

        self.user_id = str(self.user.id)
        self.group_name = "online_users"
        self.personal_group_name = f"user_notes_{self.user_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.channel_layer.group_add(self.personal_group_name, self.channel_name)
        
        await self.accept()
        
        self.online_users.add(self.user_id)
        
        unread_count = await self.get_user_unread_total(self.user)
        await self.send(text_data=json.dumps({
            'unread_count': unread_count
        }))

        for user_id in self.online_users:
            await self.send_status(user_id, 'online')
            
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "presence_status",
                "user_id": self.user_id,
                "status": "online"
            }
        )

    async def unread_update(self, event):
        unread_count = event['unread_count']
        await self.send(text_data=json.dumps({
            'unread_count': unread_count
        }))

    async def presence_status(self, event):
        await self.send_status(event['user_id'], event['status'])

    async def send_status(self, user_id, status):
        await self.send(text_data=json.dumps({
            'user_id': user_id,
            'status': status,
            'online_users_count': list(self.online_users)
        }))

    async def disconnect(self, close_code):
        self.online_users.discard(self.user_id)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "presence_status",
                "user_id": self.user_id,
                "status": "offline"
            }
        )
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.channel_layer.group_discard(self.personal_group_name, self.channel_name)

    @database_sync_to_async
    def get_user_unread_total(self, user):
        if user and user.is_authenticated:
            return Message.objects.filter(chat__users=user).exclude(sender=user).exclude(readers=user).distinct().count()
        return 0


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
       
        self.chat_id = self.scope['url_route']['kwargs'].get('chat_id')
    
        if not self.chat_id:
            await self.close()
            return
            
        self.room_group_name = f'chat_{self.chat_id}'
        username = await self.get_other_username()
        if username is None:
            await self.close()
            return
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        
        user = self.scope.get('user')
        if user and user.is_authenticated:
            await self.mark_message_as_read(user)
            unread_total = await self.get_user_unread_total(user)
            
            await self.channel_layer.group_send(
                f"user_notes_{user.id}",
                {
                    'type': 'unread_update',
                    'unread_count': unread_total
                }
            )

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
            
    async def receive(self, text_data):
        data = json.loads(text_data)
        text = data.get('text', '').strip()
        if not text:
            return
        message = await self.save_message(text)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': "send_message",
                "id": message["id"],
                "text": message["text"],
                "sender": message["sender"],
                "created_at": datetime.datetime.now().strftime('%H:%M'),
                "images": message["images"]
            }
        )
        
    async def send_message(self, text):
        await self.send(text_data=json.dumps({
            'id': text["id"],
            'chat_id': self.chat_id,
            'text': text["text"],
            "sender": text["sender"],
            'current_user': self.scope["user"].username,
            "created_at": text["created_at"],
            "images": text.get("images", [])
        }))
 
    @database_sync_to_async
    def save_message(self, text):
        user = self.scope.get("user")
        message = Message.objects.create(chat_id=self.chat_id, sender=user, text=text)
        message.readers.add(user)
        return {
            'id': message.id,
            'text': message.text,
            'sender': user.username,
            "images": []
        }

    @database_sync_to_async
    def get_other_username(self):
        user = self.scope.get("user")
        if user is None or user.is_anonymous:
            return None
        chat = Chat.objects.get(id=self.chat_id)
        other_user = chat.users.exclude(id=user.id).first()
        if other_user is None:
            return None
        return other_user.username
    
    @database_sync_to_async
    def mark_message_as_read(self, user):
        if user and user.is_authenticated:
            unread_messages = Message.objects.filter(chat_id=self.chat_id).exclude(sender=user).exclude(readers=user)
            for unread_message in unread_messages:
                unread_message.readers.add(user)

    @database_sync_to_async
    def get_user_unread_total(self, user):
        if user and user.is_authenticated:
            return Message.objects.filter(chat__users=user).exclude(sender=user).exclude(readers=user).distinct().count()
        return 0
    # async def connect(self):
    #     # 
    #     self.room_group_name = 'test_group'
    #     await self.channel_layer.group_add(
    #         self.room_group_name, 
    #         # ця властивість відповідає за ім'я каналу (зв'язок поточного клієнту з сервером)
    #         self.channel_name
    #     )
    #     await self.accept()
    #     # await self.send(json.dumps({
    #     #     'message': 'hello, world!'
    #     # }))
    #     # await self.send(json.dumps({
    #     #     'message': 'msg from server'
    #     # }))
        
        
    # async def receive(self, text_data):
    #     # data = json.loads(text_data)
    #     # await self.send(json.dumps({
    #     #     "type": 'chat',
    #     #     'message': data.get('message')
    #     # }))
        
    #     # надіслати повідомлення до групи 
    #     await self.channel_layer.group_send(
    #         group= self.room_group_name,
    #         message= {
    #             # 
    #             'type': 'chat_message',
    #             # 
    #             'message': text_data
    #         }
    #     ) 
    # # 
    # async def chat_message(self, event):
    #     '''
    #         метод, що містить логіку відправки повідомлення
    #     '''
    #     text_data_dict = json.loads(event['message'])
    #     form = MessageForm(text_data_dict)
        
    #     if form.is_valid():
    #         message = form.cleaned_data['message']
            
    #         await self.send(text_data= json.dumps(
    #             {
    #                 "type": 'chat',
    #                 'message': message
    #             }
    #         ))
    #     else:
    #         print('Error')
        
        
