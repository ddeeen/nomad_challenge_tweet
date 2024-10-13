from rest_framework import serializers
from tweets.serializer import TweetSerializer
from .models import User


class TinyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
        ]


class PublicUserSerializer(serializers.ModelSerializer):
    tweets = TweetSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "tweets",
        ]


class PrivateUserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()

    class Meta:
        model = User
        exclude = [
            "password",
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        ]
        # fields = "__all__"
        # fields = ["name", "username", "email"]
