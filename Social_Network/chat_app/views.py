from django.shortcuts import render
from django.views.generic import TemplateView , FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

# Create your views here.
from .models import Chat, Message
from .forms import MessageForm
from user_app.utils.friend_queries import get_users_by_section

User = get_user_model()

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
        context['personal_chats'] = Chat.objects.filter(users= self.request.user, is_group= False).order_by('id')
        return context
    

class ChatWithView(
        LoginRequiredMixin,
        View
    ):
    def post(self, request, user_id, *args, **kwargs):
        other_user = User.objects.get(id= user_id)
        friends = get_users_by_section(user= request.user, section= 'friends')
        if other_user not in friends:
            return JsonResponse({"success": False}, status= 403)
        # flat = True [1, 2, 3], без True [(1,), (2,), (3,)]
        user_id_chats = Chat.objects.filter(users= request.user, is_group= False).values_list('id', flat= True)
        # отримуємо чат з другом на якого натиснули у контактах
        chat = Chat.objects.filter(id__in = user_id_chats, users= other_user, is_group= False).first()
        if chat is None:
            chat = Chat.objects.create(is_group = False)
            chat.users.add(request.user, other_user)
        return JsonResponse({
            "success": True,
            "chat_id": chat.id,
            "username": other_user.last_name
        })
    
class MessageHistoryView(
        LoginRequiredMixin,
        View
    ):
    def get(self, request, chat_id):
        if not Chat.objects.filter(id= chat_id, users= request.user).exists():
            return JsonResponse({'success': False}, status= 403)
        
        query = Message.objects.filter(chat_id= chat_id).select_related("sender").order_by("-created_at", '-id')
        page_object = Paginator(query, 10).get_page(request.GET.get('page', 1))
        messages = list(page_object.object_list)[::-1]
        
        return JsonResponse({
            'messages': [{'id': message.id, 'text': message.text, 'sender': message.sender.username} for message in messages],
            'has_next': page_object.has_next()
        })