from django.urls import path
from .views import ChatView, ChatWithView, MessageHistoryView

urlpatterns = [
    path(route= '', view= ChatView.as_view(), name= 'ChatsPage'),
    path(route= 'chat_with/<int:user_id>/', view= ChatWithView.as_view(), name= 'chat_with'),
    path(route= '<int:chat_id>/messages/', view= MessageHistoryView.as_view(), name= 'message_history')
]