from django.urls import path
from .views import SettingsView, LogoutView, AuthView, LoginView, RegisterView, ConfirmView, LogoutView, FriendsView, FriendActionView, FriendsSectionView, ProfileView 

urlpatterns = [
    path(route='settings', view=SettingsView.as_view(), name="SettingsPage"),
    path(route= 'logout', view=LogoutView.as_view(), name="LogoutPage"),
    path(route= 'auth', view=AuthView.as_view(), name="AuthPage"),
    path(route= 'login', view=LoginView.as_view(), name="LoginForm"),
    path(route= 'register', view=RegisterView.as_view(), name="RegisterForm"),
    path(route= 'confirm', view= ConfirmView.as_view(), name="ConfirmForm"),
    path(route= 'logout', view= LogoutView.as_view(), name="Logout"),
    path(route= 'friends', view=FriendsView.as_view(), name="FriendsPage"),
    path("friends/<str:section>/", FriendsSectionView.as_view(), name="friends_section"),  
    path("friends/action/<int:user_id>/<str:action>/", FriendActionView.as_view(), name="friends_action"),
    path("profile/<int:user_id>/", view=ProfileView.as_view(), name="ProfilePage"),
] 