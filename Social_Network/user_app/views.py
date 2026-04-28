from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, View
from django.http import JsonResponse, HttpRequest
from django.contrib.auth import login

from .forms import EmailUserCreationForm, EmailAuthenticatedForm
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
        context["form_confirm"] = ''
        return context
    
class RegisterView(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
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
            return redirect('MainPage')
        return JsonResponse({
            "success": True,
            'errors': form.errors.get_json_data()
        })