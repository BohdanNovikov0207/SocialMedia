from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from .forms import FirstLoginForm
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from post_app.forms import PostForm
from django.views import View
from django.http import JsonResponse, HttpRequest
from post_app.models import Post
from django.core.paginator import Paginator
from django.template.loader import render_to_string

# Create your views here.

class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home_app/main.html'
    context_object_name = 'posts'
    paginate_by = 5
    # 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_post"] = PostForm()

        user = self.request.user
        
        if not user.username and user.is_authenticated:
            context["firstlogin_form"] = FirstLoginForm()
            context["show_firstlogin"] = True

        return context
    # 
    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # із моделі Post отримуємо всі пости у змінну queryset
            queryset = self.get_queryset()        
            paginator = Paginator(queryset, self.paginate_by)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            if int(page_number) > paginator.num_pages:
                return JsonResponse({'success': False})
            return JsonResponse({
                'success': True,
                'html': render_to_string(self.template_name, {'posts': page_obj.object_list})
            })
        
        return super().get(request, *args, **kwargs)

        
            

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

    