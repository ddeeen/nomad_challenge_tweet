from .models import Tweet
from rest_framework.response import Response
from .serializer import TweetSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class Tweets(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        tweets = Tweet.objects.all()
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TweetSerializer(data=request.data)
        if serializer.is_valid():
            new_tweet = serializer.save(user=request.user)
            return Response(TweetSerializer(new_tweet).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class TweetDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, tweet_id):
        try:
            return Tweet.objects.get(pk=tweet_id)
        except Tweet.DoesNotExist:
            raise NotFound

    def get(self, request, tweet_id):
        tweet = self.get_object(tweet_id)
        serializer = TweetSerializer(tweet)
        return Response(serializer.data)

    def put(self, request, tweet_id):
        tweet = self.get_object(tweet_id)
        if tweet.user != request.user:
            raise PermissionDenied
        serializer = TweetSerializer(tweet, data=request.data)
        if serializer.is_valid():
            updated_tweet = serializer.save()
            return Response(TweetSerializer(updated_tweet).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, tweet_id):
        tweet = self.get_object(tweet_id)
        if tweet.user != request.user:
            raise PermissionDenied
        tweet.delete()
        return Response(status=HTTP_204_NO_CONTENT)
