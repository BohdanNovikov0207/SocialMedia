from django.urls import path
from .views import FriendsView

app_name = 'FriendsPage'

urlpatterns = [
    path('', FriendsView.as_view(), name='friends_app')
]