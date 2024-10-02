from django.shortcuts import render
from django.http import HttpResponse
from .models import Tweet


# Create your views here.
def see_all_tweets(request):
    tweets = Tweet.objects.all()
    return render(request, "all_tweets.html", {"tweets": tweets})
