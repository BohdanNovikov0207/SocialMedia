from django.shortcuts import render
from django.views.generic import TemplateView , FormView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from .forms import MessageForm
from user_app.utils.friend_queries import get_users_by_section

class ChatView(
        LoginRequiredMixin,
        TemplateView
        # FormView, 
    ):
    template_name = "chat_app/chat.html"
    # form_class = MessageForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friends'] = get_users_by_section(user= self.request.user, section= 'friends')
        # 
        # context['personal_chats'] = 
        return context
    

