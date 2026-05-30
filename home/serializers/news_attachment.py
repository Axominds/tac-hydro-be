from rest_framework import serializers

from home.models import News, NewsAttachment


class NewsAttachmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsAttachment
        fields = ["id", "news_id", "file", "title"]


class NewsAttachmentDetailSerializer(NewsAttachmentListSerializer):
    class Meta(NewsAttachmentListSerializer.Meta):
        fields = ["id", "news_id", "file", "title"]


class NewsAttachmentCreateSerializer(serializers.ModelSerializer):
    news_id = serializers.PrimaryKeyRelatedField(
        queryset=News.objects.all(),
        source="news",
    )
    file = serializers.FileField()

    class Meta:
        model = NewsAttachment
        fields = ["id", "news_id", "file", "title"]


class NewsAttachmentUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)

    class Meta:
        model = NewsAttachment
        fields = ["title"]
