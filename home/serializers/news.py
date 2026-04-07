from load_env import env
from rest_framework import serializers

from home.models import News


class NewsListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ["id", "title", "news_date", "image", "summary"]

    def get_image(self, obj):
        if not obj.image:
            return None
        return f"{env.BACKEND_API_BASE_URL}/{obj._meta.app_label}/{obj._meta.model_name}/{obj.pk}/image/"


class NewsRetrieveSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "news_category_id",
            "news_date",
            "image",
            "published_at",
            "summary",
            "content_html",
            "is_published",
            "created_at",
            "updated_at",
        ]

    def get_image(self, obj):
        if not obj.image:
            return None
        return f"{env.BACKEND_API_BASE_URL}/{obj._meta.app_label}/{obj._meta.model_name}/{obj.pk}/image/"


class NewsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            "title",
            "news_category_id",
            "news_date",
            "published_at",
            "summary",
            "content_html",
            "is_published",
        ]


class NewsUpdateSerializer(NewsCreateSerializer):
    class Meta(NewsCreateSerializer.Meta):
        pass
