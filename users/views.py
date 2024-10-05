from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from .models import User
from tweets.serializer import TweetSerializer
from .serializers import TinyUserSerializer


class Users(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = TinyUserSerializer(users, many=True)
        return Response(serializer.data)


class UserTweets(APIView):

    def get_objects(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user.tweets.all()
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, user_id):
        tweets = self.get_objects(user_id)
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data)
