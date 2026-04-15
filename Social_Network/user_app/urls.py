from django.urls import path
from .views import UserView

app_name = 'user_app'

urlpatterns = [
    path('settings/', UserView.as_view(), name='settings_app')
]
