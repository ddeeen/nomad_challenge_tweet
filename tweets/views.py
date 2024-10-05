from .models import Tweet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import TweetSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT


class Tweets(APIView):

    def get(self, request):
        tweets = Tweet.objects.all()
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TweetSerializer(data=request.data)
        if serializer.is_valid():
            new_tweet = serializer.save()
            return Response(TweetSerializer(new_tweet).data)
        else:
            return Response(serializer.errors)


class TweetDetail(APIView):

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
        serializer = TweetSerializer(tweet, data=request.data)
        if serializer.is_valid():
            updated_tweet = serializer.save()
            return Response(TweetSerializer(updated_tweet).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, tweet_id):
        tweet = self.get_object(tweet_id)
        tweet.delete()
        return Response(HTTP_204_NO_CONTENT)
