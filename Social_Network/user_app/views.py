from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, View
from django.http import JsonResponse, HttpRequest
from django.contrib.auth import login, logout

from .forms import EmailUserCreationForm, EmailAuthenticatedForm, EmailConfirmForm
from django.core.mail import send_mail
from random import randint
from django.conf import settings
from django.urls import reverse
from .models import User
# Create your views here.

class SettingsView(TemplateView):
    template_name = "user_app/settings.html"


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