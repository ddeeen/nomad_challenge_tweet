from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("<int:user_id>", views.UserDetail.as_view()),
    path("<int:user_id>/tweets", views.UserTweets.as_view()),
    path("password", views.UserPasswordChange.as_view()),
    path("login", views.UserLogin.as_view()),
    path("logout", views.UserLogout.as_view()),
]
