from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.

class UserView(TemplateView):
    template_name = "user_app/user.html"