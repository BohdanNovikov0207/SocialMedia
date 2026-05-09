from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, TemplateView, CreateView

from .forms import PostForm, HashtagForm
from .models import Post, Tag

class PostView(TemplateView):
    template_name = "post_app/post.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context["form_post"] = PostForm()
        return context

class PostCreateView(LoginRequiredMixin, FormView):
    form_class = PostForm
    success_url = reverse_lazy("posts")
    login_url = reverse_lazy("user/auth")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if self.request.method == "POST":
            kwargs["links"] = self.request.POST.getlist("links")
            self.kwargs["photos"] = self.request.FILES.getlist("photos")

        return kwargs
    
    def form_valid(self, form):
        
        post = form.save(author=self.request.user)
        return JsonResponse(
            {
                "success": True,
                "message": "Публікацію створено успішно",
                "redirect_url": str(self.success_url),
                "post_id": post.id,
            
            }
        )
    
    def form_invalid(self, form):
        
        return JsonResponse(
            {
                "success": False,
                "errors": form.errors.get_json_data(),
            },
            status=400,
        )
        
class HashtagCreateView(CreateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'hashtag_form' not in context:
            context['hashtag_form'] = HashtagForm()
        return context
    
    def from_valid(self, form):
        response = super().from_valid(form)
        hashtag = HashtagForm(self.request.POST)
        if hashtag.is_valid():
            tag = hashtag.cleaned_data.get('hashtag')
            if tag:
                tag = tag.strip()
                if not tag.startswith("#"):
                    tag = f'#{tag}'
                
                Tag.objects.get_or_create(name=tag)
        return response