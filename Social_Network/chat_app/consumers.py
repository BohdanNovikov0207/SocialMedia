# """
#     Відповідає за обробку подій WebSocket-з`єднань.
#     Цей файл є аналогом views.py і працює в асинхронному режимі обробки подій.
# """
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .forms import MessageForm
import json
from chat_app.models import Chat, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'
        username = await self.get_other_username()
        if username is None:
            await self.close()
            return
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.send(text_data= json.dumps(
            {
                "type": "connection_established",
                "message": f"Зв`язок з {username} встановлено",
                "username": username
            }
        ))

    async def disconnect(self, close_code):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
            
        #
    async def receive(self, text_data):
        data = json.loads(text_data)
        text = data.get('text', '').strip()
        if not text:
            return
        message = await self.save_message(text)
        await self.channel_layer.group_send(
            group= self.room_group_name,
            message= {
                'type': "send_message",
                "id": message["id"],
                "text": message["text"],
                "sender": message["sender"]
            }
        )
    #   
    async def send_message(self, text):
        await self.send(text_data= json.dumps(
            {
                'id': text["id"],
                'text': text["text"],
                "sender": text["sender"]
            }
        ))
    # 
    @database_sync_to_async
    def save_message(self, text):
        user = self.scope.get("user")
        message = Message.objects.create(chat_id = self.chat_id, sender= user, text= text)
        return {
            'id': message.id,
            'text': message.text,
            'sender': user.username
        }
    @database_sync_to_async
    def get_other_username(self):
        user = self.scope.get("user")
        if user is None or user.is_anonymous:
            return None
        chat = Chat.objects.get(id= self.chat_id)
        other_user = chat.users.exclude(id= user.id).first()
        if other_user is None:
            return None
        return other_user.username
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
        
        
