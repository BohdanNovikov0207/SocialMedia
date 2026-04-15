from django.urls import path
from .views import PostView

app_name = 'PostPage'

urlpatterns = [
    path('', PostView.as_view(), name='post_app')
]