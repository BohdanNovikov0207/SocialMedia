from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.

class PostView(TemplateView):
    template_name = "post_app/post.html"