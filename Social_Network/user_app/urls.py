from django.urls import path
from .views import SettingsView, LogoutView, AuthView, LoginView, RegisterView

urlpatterns = [
    path(route='settings', view=SettingsView.as_view(), name="SettingsPage"),
    path(route= 'logout', view=LogoutView.as_view(), name="LogoutPage"),
    path(route= 'auth', view=AuthView.as_view(), name="AuthPage"),
    path(route= 'login', view=LoginView.as_view(), name="LoginForm"),
    path(route= 'register', view=RegisterView.as_view(), name="RegisterForm"),
    
]   