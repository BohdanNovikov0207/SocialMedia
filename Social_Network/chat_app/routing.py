"""
    Файл для налаштування маршрутизації WebSocket-з`єднань.
    Цей файл є аналогом urls.py і працює в асинхронному режимі. 
    В цьому файлі ми створюємо url-адреси для WebSocket-з`єднань.
"""
from django.urls import re_path
from .consumers import ChatConsumer, PresenceConsumer

websocket_urlpatterns = [
    re_path(r'^chat/online/$', PresenceConsumer.as_asgi()),
    re_path(r'^chat_with/(?P<chat_id>\d+)/$', ChatConsumer.as_asgi()),
]