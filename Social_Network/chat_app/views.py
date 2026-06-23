from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView , FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpRequest
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Subquery, OuterRef, Count, Q
from django.utils.timezone import localtime
from datetime import timedelta
from .models import Chat, Message, MessageImage

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone
# Create your views here.
from .models import Chat, Message
from .consumers import PresenceConsumer
from .forms import MessageForm
from user_app.utils.friend_queries import get_users_by_section
import json

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
        last_personal_message_subquery = Message.objects.filter(chat= OuterRef('id')).order_by('-id')
        context['personal_chats'] = Chat.objects.filter(users= self.request.user, is_group= False).order_by('id').annotate(
            last_message_text = Subquery(last_personal_message_subquery.values('text')[:1]),
            last_message_time = Subquery(last_personal_message_subquery.values('created_at')[:1])
        ).order_by('id')

        last_group_message_subquery = Message.objects.filter(chat= OuterRef('id')).order_by('-id')

        context["group_chats"] = Chat.objects.filter(users=self.request.user, is_group=True).order_by("id").annotate(
            last_message_text=Subquery(last_group_message_subquery.values("text")[:1]),
            last_message_time=Subquery(last_group_message_subquery.values("created_at")[:1]),
            total_members = Count('users')
        ).order_by("id")

        context['unread_count'] = Message.objects.filter(chat__users=self.request.user).exclude(sender=self.request.user).exclude(readers=self.request.user).distinct().count()
        
        
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
            "username": other_user.last_name,
        })
    
class MessageHistoryView(LoginRequiredMixin, View):
    def get(self, request, chat_id):
        if not Chat.objects.filter(id=chat_id, users=request.user).exists():
            return JsonResponse({'success': False}, status=403)
        
        query = Message.objects.filter(chat_id=chat_id).select_related("sender").order_by("-created_at", '-id')
        page_object = Paginator(query, 10).get_page(request.GET.get('page', 1))
        messages = list(page_object.object_list)[::-1]

        unread_in_this_chat = Message.objects.filter(chat_id=chat_id).exclude(sender=request.user).exclude(readers=request.user)
        for msg in unread_in_this_chat:
            msg.readers.add(request.user)

        new_unread_total = Message.objects.filter(
            chat__users=request.user
        ).exclude(
            sender=request.user
        ).exclude(
            readers=request.user
        ).distinct().count()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_notes_{request.user.id}",
            {
                "type": "unread_update",
                "unread_count": new_unread_total
            }
        )

        chat = Chat.objects.get(id=chat_id)
        is_group = chat.is_group
        total_members = 0
        group_users_ids = []
        user_status = "offline"
        other_user_id = ""
        
        if is_group:
            total_members = chat.users.count()
            group_users_ids = [str(user.id) for user in chat.users.all()]
        else:
            other_user = chat.users.exclude(id=request.user.id).first()
            if other_user:
                other_user_id = str(other_user.id)
                online_user = getattr(PresenceConsumer, 'online_users_count', set())
                if str(other_user.id) in online_user:
                    user_status = "online"
        
        return JsonResponse({
            'messages': [{
                'id': message.id,
                'text': message.text, 
                'sender': message.sender.username, 
                "images": [image.image.url for image in message.images.all()], 
                'created_at': (message.created_at + timedelta(hours=3)).strftime('%H:%M') if message.created_at else ''
                } for message in messages],
            'has_next': page_object.has_next(),
            'current_user': request.user.username,
            'is_group': is_group,
            'total_members': total_members,
            'group_users_ids': group_users_ids,
            'user_status': user_status,
            'other_user_id': other_user_id
        })

class CreateGroupView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
            
            action = data.get('action')
            group_id = data.get('group_id')
            
            if action == 'update_group_settings' and group_id:
                chat = get_object_or_404(Chat, id=group_id, is_group=True)
                
                new_name = data.get('new_name', '').strip()
                if new_name:
                    chat.name = new_name
                    chat.save()
                
                removed_users = data.get('removed_users', [])
                if removed_users:
                    chat.users.remove(*User.objects.filter(id__in=removed_users))
                
                added_users = data.get('added_users', [])
                if added_users:
                    friends_list_id = get_users_by_section(user=request.user, section='friends').filter(id__in=added_users).values_list('id', flat=True)
                    chat.users.add(*User.objects.filter(id__in=friends_list_id))
                
                return JsonResponse({
                    'success': True,
                    'chat_id': chat.id,
                    'name': chat.name
                })

        group_name = request.POST.get('name', '').strip()
        friends_id = request.POST.getlist('users')
        
        if not group_name:
            return JsonResponse({'success': False, 'error': 'name required'}, status=400)
            
        friends_list_id = get_users_by_section(user=request.user, section='friends').filter(id__in=friends_id).values_list('id', flat=True)
        
        chat = Chat.objects.create(name=group_name, is_group=True, admin=request.user)
        chat.users.add(request.user)
        chat.users.add(*User.objects.filter(id__in=friends_list_id))
        
        return JsonResponse({
            'success': True,
            'chat_id': chat.id,
            'name': chat.name
})

class MessageUploadView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, chat_id: int, *args, **kwargs):

        if not Chat.objects.filter(id = chat_id, users = request.user).exists():
            return JsonResponse({'success': False}, status= 403)
        
        text = request.POST.get("text", "").strip()
        images = request.FILES.getlist("images")
        
        if not images and not text:
            return JsonResponse({'success': False, "error": "required message"}, status= 400)
        
        message = Message.objects.create(chat_id= chat_id, sender= request.user, text= text)
        message.readers.add(request.user)
        
        for image in images:
            MessageImage.objects.create(message= message, image= image)
        
        image_urls= [image.image.url for image in message.images.all()] 
        
        channel_layer= get_channel_layer()

        
        async_to_sync(channel_layer.group_send)(
            f"chat_{chat_id}",
            {
                "type": "send_message",
                "id": message.id,
                "text": message.text,
                "sender": message.sender.username,
                "created_at": timezone.localtime(message.created_at).isoformat(),
                "images": image_urls
            }
        )
        chat = Chat.objects.get(id=chat_id)
        other_users = chat.users.exclude(id=request.user.id)
        
        for user in other_users:
            new_unread_count = Message.objects.filter(
                chat__users=user
            ).exclude(
                sender=user
            ).exclude(
                readers=user
            ).distinct().count()

            async_to_sync(channel_layer.group_send)(
                f"user_notes_{user.id}",
                {
                    "type":"unread_update",
                    "unread_count": new_unread_count
                }
            )
        return JsonResponse({"success": True })
