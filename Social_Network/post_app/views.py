from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, TemplateView, CreateView
from django.core.paginator import Paginator
from django.template.loader import render_to_string

from .forms import PostForm, HashtagForm
from .models import Post, Tag

class PostView(LoginRequiredMixin, ListView):
    template_name = "post_app/post.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context["form_post"] = PostForm()
        context["hashtag_form"] = HashtagForm()
        context["posts"] = Post.objects.filter(author_id = self.request.user)[:self.paginate_by]
        return context

    def get_queryset(self):
        return Post.objects.filter(author_id = self.request.user)
    
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
    
class PostCreateView(LoginRequiredMixin, FormView):
    form_class = PostForm
    success_url = reverse_lazy("PostPage")
    login_url = reverse_lazy("AuthPage")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if self.request.method == "POST":
            kwargs["links"] = self.request.POST.getlist("links")
            kwargs["images"] = self.request.FILES.getlist("images")

        return kwargs
    
    def form_valid(self, form: PostForm):
        
        post = form.save(author=self.request.user)
        return JsonResponse(
            {
                "success": True,
                "message": "Публікацію створено успішно",
                "redirect_url": str(self.success_url),
                "post_id": post.id,
            
            }
        )
    
    def form_invalid(self, form: PostForm):
        
        return JsonResponse(
            {
                "success": False,
                "errors": form.errors.get_json_data(),
            },
            status=400,
        )
        
class HashtagCreateView(FormView):
    form_class = HashtagForm
    template_name = "post_app/add_hashtag.html"

    def form_valid(self, form):
        tag_obj = form.save() 
        return JsonResponse({
            "status": "success", 
            "tag_name": tag_obj.name
        }, status=200)

    def form_invalid(self, form):
        return JsonResponse({
            "status": "error", 
            "errors": form.errors
        }, status=400)
