from django.urls import path
from .views import SettingsView, LogoutView, AuthView

urlpatterns = [
    path(route='settings', view=SettingsView.as_view(), name="SettingsPage"),
    path(route= 'logout', view=LogoutView.as_view(), name="LogoutPage"),
    path(route= 'auth', view=AuthView.as_view(), name="AuthPage"),
]   