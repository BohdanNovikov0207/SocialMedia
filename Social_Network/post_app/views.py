from django.shortcuts import render
from django.views.generic.base import TemplateView, View
# from .forms import PostForm
from django.http import HttpRequest
# Create your views here.

class PostView(TemplateView):
    template_name = "post_app/post.html"

# class PostCreateView(View):
#     template_name = 'post.html'
#     def post(self, request: HttpRequest, *args, **kwargs):
#         form = PostForm(request.POST)