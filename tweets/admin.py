from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Tweet, Like


class ElonFilter(admin.SimpleListFilter):

    title = "Filter by word - Elon Musk"
    parameter_name = "elon"

    def lookups(self, request, model_admin):
        return [
            ("elon_musk", "Elon Musk"),
            ("not_elon_musk", "Not Elon Musk"),
        ]

    def queryset(self, request, tweets):
        elon_musk = "Elon Musk"
        elon = self.value()
        if elon:
            if elon == "elon_musk":
                return tweets.filter(payload__contains=elon_musk)
            else:
                return tweets.exclude(payload__contains=elon_musk)
        else:
            return tweets


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "payload",
        "likes",
        "created_at",
        "updated_at",
    )

    list_filter = (
        ElonFilter,
        "created_at",
    )

    search_fields = (
        "payload",
        "user__username",
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "tweet",
        "created_at",
        "updated_at",
    )

    list_filter = ("created_at",)

    search_fields = ("user__username",)
