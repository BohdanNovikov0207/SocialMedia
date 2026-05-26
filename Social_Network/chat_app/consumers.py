# """
#     Відповідає за обробку подій WebSocket-з`єднань.
#     Цей файл є аналогом views.py і працює в асинхронному режимі обробки подій.
# """
from channels.generic.websocket import AsyncWebsocketConsumer
from .forms import MessageForm
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 
        self.room_group_name = 'test_group'
        await self.channel_layer.group_add(
            self.room_group_name, 
            # ця властивість відповідає за ім'я каналу (зв'язок поточного клієнту з сервером)
            self.channel_name
        )
        await self.accept()
        # await self.send(json.dumps({
        #     'message': 'hello, world!'
        # }))
        # await self.send(json.dumps({
        #     'message': 'msg from server'
        # }))
        
        
    async def receive(self, text_data):
        # data = json.loads(text_data)
        # await self.send(json.dumps({
        #     "type": 'chat',
        #     'message': data.get('message')
        # }))
        
        # надіслати повідомлення до групи 
        await self.channel_layer.group_send(
            group= self.room_group_name,
            message= {
                # 
                'type': 'chat_message',
                # 
                'message': text_data
            }
        ) 
    # 
    async def chat_message(self, event):
        '''
            метод, що містить логіку відправки повідомлення
        '''
        text_data_dict = json.loads(event['message'])
        form = MessageForm(text_data_dict)
        
        if form.is_valid():
            message = form.cleaned_data['message']
            
            await self.send(text_data= json.dumps(
                {
                    "type": 'chat',
                    'message': message
                }
            ))
        else:
            print('Error')
        
        
