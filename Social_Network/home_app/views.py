from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from .forms import FirstLoginForm
from post_app.forms import PostForm
from django.views import View
from django.http import JsonResponse, HttpRequest


# Create your views here.

class HomeView(TemplateView):
    template_name = "home_app/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["firstlogin_form"] = FirstLoginForm()
        context["form_post"] = PostForm()

        user = self.request.user
        
        if not user.username and user.is_authenticated:
            context["firstlogin_form"] = FirstLoginForm()
            context["show_firstlogin"] = True

        return context
            

class FirstLoginView(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        form = FirstLoginForm(request.POST)

        print(request.user)
        print(request.user.username)
        
        if form.is_valid():
            user = request.user
            user.last_name = form.cleaned_data.get('displayname')
            user.username = form.cleaned_data.get('username')
            user.save()

            return JsonResponse({
                'success': True
            })
        
        return JsonResponse({
            "success": False,
            "errors": form.errors.get_json_data()
        }, status=400)