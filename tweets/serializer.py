from rest_framework import serializers
from .models import Tweet


# class TweetSerializer(serializers.Serializer):
#     payload = serializers.CharField(max_length=180, required=True)
#     user = serializers.CharField()
#     # user = serializers.PrimaryKeyRelatedField(
#     #     queryset=User.objects.all(), required=True
#     # )
#     created_at = serializers.DateTimeField()


class TweetSerializer(serializers.ModelSerializer):
    # user = serializers.CharField()

    class Meta:
        model = Tweet
        fields = ["payload", "user", "likes", "created_at"]
        read_only_fields = ["user", "likes", "created_at"]
