from django.urls import path
from .views import FriendsView

urlpatterns = [
    path(route='friends', view=FriendsView.as_view(), name="FriendsPage")
]