from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.

class FriendsView(TemplateView):
    template_name = "friends_app/friends.html"