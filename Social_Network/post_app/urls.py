from django.urls import path
from .views import PostCreateView, PostView, HashtagCreateView

urlpatterns = [
    path(route='', view=PostView.as_view(), name="PostPage"),
    path(route='create', view=PostCreateView.as_view(), name="PostCreateForm"),
    path(route='create_hashtag', view=HashtagCreateView.as_view(), name="HashtagCreateForm")
]