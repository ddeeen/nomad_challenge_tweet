from django.urls import path
from . import views

urlpatterns = [
    path("<int:user_id>/tweets", views.UserTweets.as_view()),
]
