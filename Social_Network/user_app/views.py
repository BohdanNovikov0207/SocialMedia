from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, ListView
from django.http import JsonResponse, HttpRequest
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils.friend_queries import get_users_by_section
from django.core.paginator import Paginator
from django.template.loader import render_to_string

from .forms import EmailUserCreationForm, EmailAuthenticatedForm, EmailConfirmForm
from django.core.mail import send_mail
from random import randint
from django.conf import settings
from django.urls import reverse, reverse_lazy
from .models import User
from post_app.models import Post
from .utils.friend_action import accept_friend_request, add_friend_request, delete_friendship, dismiss_recommendation

# Create your views here.

class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = "user_app/settings.html"
    login_url = reverse_lazy("AuthPage")

class LogoutView(TemplateView):
    template_name = "user_app/logout.html"
    
class AuthView(TemplateView):
    template_name = "user_app/auth.html"
     
    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)    
        context["form_register"] = EmailUserCreationForm()
        context["form_login"] = EmailAuthenticatedForm()
        context["form_confirm"] = EmailConfirmForm()
        return context
    
class RegisterView(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            confirm_code = str(randint(100000, 999999))

            request.session["confirm_user_id"] = user.id
            request.session["confirm_code"] = confirm_code

            send_mail(
                subject= "Код пiдтверждення SocialMedia",
                message= f"Ваш код пiдтвердження: {confirm_code}",
                from_email= settings.EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
            return JsonResponse({
                'success': True,
                'message': 'Користувача успішно зареєстровано'
            })
        
        return JsonResponse({
            'success': False,
            'errors': form.errors.get_json_data()
        }, status= 400)


class LoginView(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        form = EmailAuthenticatedForm(request= request, data= request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request= request, user= user)

            return JsonResponse({
                "success": True,
                "redirect_url": reverse("MainPage")
            })
            
        return JsonResponse({
            "success": False,
            "errors": form.errors.get_json_data()
        }, status=400)

class ConfirmView(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        form = EmailConfirmForm(request.POST)
        
        if form.is_valid():
            code = form.cleaned_data["code"]
            
            session_code = request.session.get("confirm_code")
            user_id = request.session.get("confirm_user_id")

            if session_code == code and user_id:
                user = User.objects.get(id=user_id)
                user.is_active = True
                user.save()

                del request.session["confirm_code"]
                del request.session["confirm_user_id"]

                return JsonResponse({
                    "success": True
                })
            
        return JsonResponse({
            "success": False,
            "errors": form.errors.get_json_data()
        }, status=400)

class LogoutView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        logout(request)
        return redirect('AuthPage')

class FriendsView(LoginRequiredMixin, TemplateView):
    template_name = "user_app/friends.html"
    login_url = reverse_lazy("AuthPage")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = {
            'requests': {'title': 'Запити', 'users': get_users_by_section(user = self.request.user, section= 'requests')[:3]},
            'recommendations': {'title': 'Рекомендації', 'users': get_users_by_section(user = self.request.user, section= 'recommendations')[:6]},
            'friends': {'title': 'Всі друзі', 'users': get_users_by_section(user = self.request.user, section= 'friends')[:6]},
        }
        return context  

class FriendsSectionView(FriendsView):
    def get(self, request, section, *args, **kwargs):
        # Отримуємо потрібний список за назвою вкладки.
        users = get_users_by_section(request.user, section)
        # Розбиваємо людей на порції по 6 карток.
        page_obj = Paginator(users, 6).get_page(request.GET.get("page", 1))
        # Рендеримо тільки поточну порцію карток вибраної вкладки.
        htm= render_to_string("user_app/particles/friends/friends_card.html", 
                                {"users": page_obj.object_list, "section": section}, 
                                request=request
                                )
        # Повертаємо HTML поточної порції і ознаку наступної сторінки.
        return JsonResponse({"html": html, "has_next": page_obj.has_next()})
#  
class FriendActionView(LoginRequiredMixin, View):
    login_url = reverse_lazy('auth')
    
    def post(self, request, user_id, action, *args, **kwargs):
        other_user = User.objects.get(id= user_id)
        
        if action == 'redirect':
            # (Используем f-строку, чтобы не зависеть от названий в urls.py)
            target_url = f'/user/profile/{user_id}/'
            
            # Возвращаем JSON с адресом для JavaScript
            return JsonResponse({'status': 'redirect', 'redirect_url': target_url})

        if action == 'add':
            add_friend_request(request.user, other_user)
            return JsonResponse({'status': 'success'})
        if action == 'dismiss':
            return JsonResponse(dismiss_recommendation(request.user, other_user))
        if action == 'accept':
            action_result = accept_friend_request(request.user, other_user)
            action_result['friend_html'] = render_to_string(
                'user_app/particles/friends/friends_card.html',
                {'users': [action_result['friend']], 'section': 'friends'},
                request= request
            )
            del action_result['friend']
            
            return JsonResponse(action_result)
        # 
        return JsonResponse(delete_friendship(request.user, other_user))

class ProfileView(ListView):
    template_name = "user_app/profile_page.html"
    paginate_by = 5
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context["user_id"] = self.kwargs.get('user_id')
        context["user_profile"] = User.objects.get(id= self.kwargs.get('user_id'))
        return context
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Post.objects.filter(author_id = user_id).order_by("-created_at")
    
    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # із моделі Post отримуємо всі пости у змінну queryset
            queryset = self.get_queryset()
            paginator = Paginator(queryset, self.paginate_by)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            if int(page_number) > paginator.num_pages:
                return JsonResponse({'success': False})
            return JsonResponse({
                'success': True,
                'html': render_to_string("post_app/particles/show_post.html", {
                    'posts': page_obj.object_list
                },
                request= request
                )
            })
        
        return super().get(request, *args, **kwargs)