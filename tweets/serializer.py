from rest_framework import serializers
from users.models import User


class TweetSerializer(serializers.Serializer):
    payload = serializers.CharField(max_length=180, required=True)
    user = serializers.CharField()
    # user = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all(), required=True
    # )
    created_at = serializers.DateTimeField()
