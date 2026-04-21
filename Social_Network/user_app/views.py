from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.

class SettingsView(TemplateView):
    template_name = "user_app/settings.html"


class LogoutView(TemplateView):
    template_name = "user_app/logout.html"