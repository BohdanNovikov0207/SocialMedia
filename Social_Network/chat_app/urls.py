from django.urls import path
from .views import ChatView

urlpatterns = [
    path(route= '', view= ChatView.as_view(), name= 'ChatsPage'),
    # path(route= 'chat_with/<int:user_id>/', view= ChatView.as_view(), name= 'chat_with'),
]