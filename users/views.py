from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from tweets.serializer import TweetSerializer
from .models import User


@api_view(["GET"])
def see_user_tweets(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise NotFound

    serializer = TweetSerializer(user.tweets.all(), many=True)
    return Response(serializer.data)
