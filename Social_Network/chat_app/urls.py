from django.urls import path
from .views import ChatView, ChatWithView, MessageHistoryView, CreateGroupView

urlpatterns = [
    path(route= '', view= ChatView.as_view(), name= 'ChatsPage'),
    path(route= 'chat_with/<int:user_id>/', view= ChatWithView.as_view(), name= 'chat_with'),
    path(route= 'chat_with/<int:chat_id>/messages/', view= MessageHistoryView.as_view(), name= 'message_history'),
    path(route= "create_group/", view= CreateGroupView.as_view(), name="create_group"),
]