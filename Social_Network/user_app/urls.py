from django.urls import path
from .views import UserView

urlpatterns = [
    path(route='user/settings', view=UserView.as_view(), name="UserPage")
]