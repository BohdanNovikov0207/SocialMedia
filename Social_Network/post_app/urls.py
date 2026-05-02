from django.urls import path
from .views import PostView

urlpatterns = [
    path(route='posts', view=PostView.as_view(), name="PostPage"),
#    path(route='', view=PostCreateView.as_view(), name="PostForm")
]