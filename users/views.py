from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.views import APIView
from .models import User
from tweets.serializer import TweetSerializer
from . import serializers


class Users(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = serializers.TinyUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError("Input password")
        serializer = serializers.PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class UserDetail(APIView):

    def get_object(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, user_id):
        user = self.get_object(user_id)
        serializer = serializers.PublicUserSerializer(user)
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
