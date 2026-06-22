"""
    Файл для налаштування маршрутизації WebSocket-з`єднань.
    Цей файл є аналогом urls.py і працює в асинхронному режимі. 
    В цьому файлі ми створюємо url-адреси для WebSocket-з`єднань.
"""
from django.urls import path
from .consumers import ChatConsumer, PresenceConsumer

websocket_urlpatterns = [
    path(route='chat_with/<int:chat_id>/', view= ChatConsumer.as_asgi()),
    path(route= "chat/online/", view= PresenceConsumer.as_asgi())
]