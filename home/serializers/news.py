from rest_framework import serializers

from home.models import News, NewsCategory
from home.serializers.news_attachment import NewsAttachmentDetailSerializer


class NewsListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ["id", "title", "news_date", "image", "summary", "news_category_id", "is_published"]

    def get_image(self, obj):
        if not obj.image:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class NewsRetrieveSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    attachments = NewsAttachmentDetailSerializer(many=True, read_only=True)

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
            "attachments",
        ]

    def get_image(self, obj):
        if not obj.image:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class NewsCreateSerializer(serializers.ModelSerializer):
    news_category_id = serializers.PrimaryKeyRelatedField(queryset=NewsCategory.objects.all(), source="news_category")
    image = serializers.FileField(required=False)
    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "news_category_id",
            "news_date",
            "image",
            "summary",
            "content_html",
            "is_published",
        ]


class NewsUpdateSerializer(NewsCreateSerializer):
    class Meta(NewsCreateSerializer.Meta):
        pass
